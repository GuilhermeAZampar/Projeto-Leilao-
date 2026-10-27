from fastapi import APIRouter,Depends,HTTPException,status,BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import select,desc
from database import get_db
from dependencies import get_usuario
from models.usuario import Usuario,PapelUsuario
from models.leilao import Leilao,StatusLeilao
from models.lance import Lance
from testdb import resultado
from.carteira import Carteira
from schemas.leilao import LeilaoCriacao,LeilaoResposta
from datetime import datetime, timezone, timedelta
from services.api_obras import buscar_obras,pesquisar_obras
from schemas.lance import LanceCriacao,LanceResposta
from services.auditoria import verificar_auditoria,registrar_evento
from services.websocket_manager import manager
from services.auditoria import verificar_auditoria
import httpx

router = APIRouter(prefix="/leiloes",tags=["leilao"])


@router.post("/",response_model=LeilaoResposta,status_code=status.HTTP_201_CREATED)
def leilao(dados:LeilaoCriacao,usuario_atual:Usuario=Depends(get_usuario),db:Session=Depends(get_db),):
    if usuario_atual.papel != PapelUsuario.LEILOEIRO:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Erro apenas leiloeiros podem criar leilões")

    if dados.inicio_em.utcoffset() is None or dados.fim_em.utcoffset() is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="As Datas precisam informar o fuso")
    if dados.fim_em <= dados.inicio_em:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Erro a data de fim nao pode ser meno que a de inicio")
    if dados.inicio_em <= datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Erro a data de encerramento deve ser maior")

    try:
        obras_resposta = buscar_obras(int(dados.item_externo_id))
        obra = obras_resposta["data"]
        titulo_obra = obra["title"]
        imagem_obra = (obra.get("images") or {}).get("web") or {}
        imagem_url = imagem_obra.get("url")
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Erro a obra deve ser um numero inteiro")
    except httpx.HTTPStatusError as erro:
        if erro.response.status_code== 404:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Erro ao encontrar a obra na API")
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="A API retornou um erro")
    except httpx.RequestError:
        raise HTTPException(status_code=503,detail="API indisponivel")



    novo_leilao=Leilao(
        leiloeiro_id=usuario_atual.id,
        titulo=titulo_obra,
        descricao=dados.descricao,
        imagem_url=imagem_url,
        item_externo_id=dados.item_externo_id,
        valor_inicial=dados.valor_inicial,
        incremento_minimo=dados.incremento_minimo,
        status=StatusLeilao.AGENDADO,
        inicio_em=dados.inicio_em,
        fim_em=dados.fim_em,
    )

    db.add(novo_leilao)
    db.commit()
    db.refresh(novo_leilao)
    return novo_leilao


@router.get("/",response_model=list[LeilaoResposta])
def listagem_leilao(db:Session=Depends(get_db)):
    leiloes=db.scalars(select(Leilao)).all()
    return leiloes


@router.post("/{leilao_id}/lances",response_model=LanceResposta,status_code=status.HTTP_201_CREATED)
def lance(leilao_id:int,dados:LanceCriacao,background_task:BackgroundTasks,usuario_atual:Usuario=Depends(get_usuario),db:Session=Depends(get_db)):
    try:
        if usuario_atual.papel != PapelUsuario.LICITANTE:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Erro apenas Licitantes podem dar lances")

        consulta = db.scalar(select(Leilao).where(Leilao.id == leilao_id).with_for_update())
        if not consulta:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Erro ao encontrar a leilao")

        agora = datetime.now(timezone.utc)
        if agora < consulta.inicio_em or agora >= consulta.fim_em:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Erro o leilao esta fora do periodo de lances")

        if consulta.status in(StatusLeilao.CANCELADO,StatusLeilao.ENCERRADO):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Leilao nao encontrado ou cancelado")

        if consulta.status == StatusLeilao.AGENDADO:
            consulta.status = StatusLeilao.ATIVO

        maior_lance = db.scalar(select(Lance).where(Lance.leilao_id == leilao_id).order_by(desc(Lance.valor)).limit(1))
        mesmo_licitante = (maior_lance is not None and maior_lance.licitante_id == usuario_atual.id)
        if mesmo_licitante:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Voce ja fez um lance")

        valor_reservado=dados.valor

        if maior_lance is None:
            valor_minimo = consulta.valor_inicial
        else:
            valor_minimo = maior_lance.valor + consulta.incremento_minimo

        if dados.valor < valor_minimo:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Erro o valor do lance deve ser maior que o minimo")

        ids_usuarios = [usuario_atual.id]

        if maior_lance is not None and not mesmo_licitante:
            ids_usuarios.append(maior_lance.licitante_id)

        carteiras = db.scalars(
            select(Carteira)
            .where(Carteira.usuario_id.in_(ids_usuarios))
            .order_by(Carteira.usuario_id)
            .with_for_update()
        ).all()

        carteiras_por_usuario = {
            c.usuario_id: c for c in carteiras
        }

        carteira = carteiras_por_usuario.get(usuario_atual.id)

        if carteira is None:
            raise HTTPException(
                status_code=404,
                detail="Carteira não encontrada"
            )

        saldo_disponivel = carteira.saldo - carteira.saldo_reservado

        if saldo_disponivel < valor_reservado:
            raise HTTPException(
                status_code=400,
                detail="Saldo insuficiente para realizar o lance"
            )

        if maior_lance is not None and not mesmo_licitante:
            carteira_antiga = carteiras_por_usuario.get(
                maior_lance.licitante_id
            )

            if carteira_antiga is None:
                raise HTTPException(
                    status_code=404,
                    detail="Carteira anterior não encontrada"
                )

            carteira_antiga.saldo_reservado -= maior_lance.valor

        carteira.saldo_reservado += valor_reservado
        if consulta.fim_em - agora <= timedelta(minutes=2):
            consulta.fim_em = agora + timedelta(minutes=2)



        novo_lance=Lance(
          leilao_id=leilao_id,
          licitante_id=usuario_atual.id,
          valor=dados.valor
         )

        db.add(novo_lance)
        db.flush()
        dados_auditoria={"lance_id":novo_lance.id,"licitante_id":usuario_atual.id,"valor":str(dados.valor)}
        registrar_evento(db,leilao_id,"LANCE_REGISTRADO",dados_auditoria)
        db.commit()
        db.refresh(novo_lance)
        dados_background={"tipo":"NOVO_LANCE","valor":str(dados.valor)}
        background_task.add_task(manager.enviar_para_leilao,leilao_id,dados_background)
        return novo_lance
    except Exception:
        db.rollback()
        raise



@router.get("/{leilao_id}/lances",response_model=list[LanceResposta])
def historico_lance(leilao_id: int,db:Session = Depends(get_db)):
    leilao=db.get(Leilao,leilao_id)
    if leilao is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Lance nao encontrado")

    resposta=db.scalars(select(Lance).where(Lance.leilao_id==leilao_id).order_by(desc(Lance.valor))).all()

    resultado=[]

    for lance in resposta:
        resultado.append(LanceResposta(
            id=lance.id,
            leilao_id=lance.leilao_id,
            licitante_id=lance.licitante_id,
            licitante_nome=f"Licitante #{lance.licitante_id}",
            valor=lance.valor,
            criado_em=lance.criado_em
        ))

    return resultado

@router.patch("/{leilao_id}/cancelar")
def cancelar_leilao(leilao_id: int,usuario_atual:Usuario=Depends(get_usuario),db:Session = Depends(get_db)):
    leilao=db.scalar(select(Leilao).where(Leilao.id==leilao_id).with_for_update())
    if not leilao:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Voce nao pode cancelar o leilao de outro usuario")
    if leilao.leiloeiro_id != usuario_atual.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Voce nao pode cancelar o leilao de outro usuario")

    lance_existe=db.scalar(select(Lance).where(Lance.leilao_id==leilao_id).limit(1))

    if lance_existe:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Nao é possivel cancelar um leilao que ja possui lances")

    if leilao.status in(StatusLeilao.ENCERRADO , StatusLeilao.CANCELADO):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Voce nao pode cancelar um leilao encerrado ou cancelado")

    leilao.status = StatusLeilao.CANCELADO
    db.commit()
    return {"mensagem":"Leilao cancelado"}


@router.get("/{leilao_id}/comprovante")
def comprovante(leilao_id: int,db:Session=Depends(get_db)):
    leilao=db.get(Leilao,leilao_id)
    if leilao is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Erro ao procurar leilao")

    if leilao.status != StatusLeilao.ENCERRADO:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Erro o leilao ainda nao foi encerrado")

    lance_vencedor=db.scalar(select(Lance).where(Lance.leilao_id==leilao_id).order_by(desc(Lance.valor),desc(Lance.id)).limit(1))
    if lance_vencedor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Esse leilao acabou sem vencedor")
    return {
        "leilao_id": leilao.id,
        "titulo": leilao.titulo,
        "valor_arremate":lance_vencedor.valor,
        "vencedor": f"Licitante #{lance_vencedor.licitante_id}",
        "fim_em":leilao.fim_em

    }


@router.get("/meus-arremates")
def arremates(db:Session=Depends(get_db),usuario_atual:Usuario=Depends(get_usuario)):
    arremate=db.scalars(select(Lance.leilao_id).where(Lance.licitante_id == usuario_atual.id).distinct()).all()
    leiloes=db.scalars(select(Leilao).where(Leilao.id.in_(arremate))).all()
    resultado=[]
    for leilao in leiloes:
        maior_lance=db.scalar(select(Lance).where(Lance.leilao_id==leilao.id).order_by(desc(Lance.valor),desc(Lance.id)).limit(1))
        venceu=(leilao.status == StatusLeilao.ENCERRADO and maior_lance is not None and maior_lance.licitante_id == usuario_atual.id )
        resultado.append({
            "id": leilao.id,
            "titulo": leilao.titulo,
            "status": leilao.status.value,
            "maior_lance":maior_lance.valor if maior_lance else None,
            "venceu":venceu

        })
    return resultado


@router.get("/{leilao_id}/auditoria")
def auditoria(leilao_id:int,db:Session=Depends(get_db)):
    leilao=db.get(Leilao,leilao_id)
    if leilao is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Leilao nao encontrado")
    return verificar_auditoria(db, leilao_id)
