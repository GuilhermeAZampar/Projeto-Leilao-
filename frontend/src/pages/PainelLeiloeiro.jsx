import {useEffect, useState} from "react";
import  buscarLeiloes, {buscarObras,criarLeilao,buscarUsuario,cancelarLeilao,buscarLances} from "../services/api.js";


export default function BuscarObra({token}){
    const[obra,setObra]=useState([])
    const[termo,setTermo]=useState('')
    const[carregando,setCarregando]=useState(false)
    const[erro,setErro]=useState(null)
    const[obraSelecionada,setObraSelecionada]=useState('')

    const [descricao,setDescricao]=useState('')
    const[valorInicial,setValorInicial]=useState('')
    const [incrementoMinimo,setIncrementoMinimo]=useState('')
    const[inicio,setInicio]=useState('')
    const[fim,setFim]=useState('')
    const[criando,setCriando]=useState(false)
    const[erroCriacao,setErroCriacao]=useState(null)

    const[usuario,setUsuario]=useState(null)
    const[meus_leiloes,setmeusLeiloes]=useState([])
    const [erroLeiloes,setErroLeiloes]=useState(null)

    useEffect(()=>{
        async function carregar_meusleiloes(){
            if(!token)return;
            setErroLeiloes(null)
            try{
                const[dadosUsuario,leiloes]=await Promise.all([
                    buscarUsuario(token),
                    buscarLeiloes()
                ])
                setUsuario(dadosUsuario)
                const leiloes_filtrados=leiloes.filter(leilao=>leilao.leiloeiro_id === dadosUsuario.id)
                const leiloes_com_resultado = await Promise.all(
                    leiloes_filtrados.map(async (item)=>{
                        if(item.status !="encerrado"){
                            return item
                        }
                        const lances=await buscarLances(item.id)
                        return {...item,lance_vencedor:lances[0]??null
                        }
                    })
                )
                setmeusLeiloes(leiloes_com_resultado)

            }catch (error){
                setErroLeiloes(error.message)

            }

        }
        carregar_meusleiloes()
    },[token])

   async function handleObra(e){
        e.preventDefault()
        setCarregando(true)
        setErro(null)
        try{
            const dados= await buscarObras(termo)
            setObra(dados.data)
        }catch (error){
            setErro(error.message)
        }finally {
            setCarregando(false)
        }
    }
    async function handleCancelar(id){
        setErroLeiloes(null)
        try{
            await cancelarLeilao(id,token)
            setmeusLeiloes(lista=>lista.map((leilao=>leilao.id===id?{...leilao,status:"cancelado"}:leilao)))
        }catch (error){
            setErroLeiloes(error.message)
        }
    }
    async function handleCriarLeilao(e){
        e.preventDefault()
        setCriando(true)
        setErroCriacao(null)
        try{
            const dados={
                titulo:obraSelecionada.title,
                descricao:descricao,
                imagem_url:obraSelecionada.images?.web?.url ?? "",
                item_externo_id:String(obraSelecionada.id),
                valor_inicial:valorInicial,
                incremento_minimo:incrementoMinimo,
                inicio_em:new Date(inicio).toISOString(),
                fim_em:new Date(fim).toISOString()

            }
            const novo_leilao= await criarLeilao(token,dados)
            setmeusLeiloes(anterioes=>[...anterioes,novo_leilao])
            alert("Leilao Criado com Sucesso")
        }catch (error){
            setErroCriacao(error.message)

        }finally {
            setCriando(false)
        }
    }
    const total_recebido=meus_leiloes.reduce((total,item)=>{
        if(item.status === "encerrado" && item.lance_vencedor){
            return total + Number(item.lance_vencedor.valor)
        }
        return total
    },0)
    return(
        <>
            <form onSubmit={handleObra}>
                <input type={"text"} value={termo} onChange={(e)=>{setTermo(e.target.value)}} required/>
                <button type={"submit"} disabled={carregando}>{carregando?"Carregando...":"Pesquisar"}</button>
            </form>
            {erro &&(<p>{erro}</p>)}
            <h2>Meus Leilões</h2>
            <p>Total Recebido: {total_recebido.toLocaleString("pt-br",{style:"currency",currency:"BRL"})}</p>
            {erroLeiloes && (<p>Erro: {erroLeiloes}</p>)}
            {meus_leiloes.length===0?(<p>Nao ha leiloes</p>):(
                <ul>
                    {meus_leiloes.map(item=>(
                        <li key={item.id}>{item.titulo} - {item.status}
                            {item.status != "cancelado" && item.status != "encerrado" &&(
                                <button type={"button"} onClick={()=>handleCancelar(item.id)}>Cancelar Leilão</button>
                            )}
                            {item.status === "encerrado"&&(
                                <p>
                                    {item.lance_vencedor ? `Arrematado por ${Number(item.lance_vencedor.valor).toLocaleString("pt-br",{"style":"currency","currency":"BRL"})}`:"Encerrrado sem lances" }

                                </p>
                            )}
                        </li>

                    ))}
                </ul>
                )}
            <ul>
                {obra.map(item=>(
                    <li key={item.id}>
                        {item.title}
                        <button type={"button"} onClick={()=>{setObraSelecionada(item)}}>Selecionar</button>
                    </li>

                ))}
            </ul>
            {obraSelecionada &&(
                <form onSubmit={handleCriarLeilao}>
                    <h2>Criar Leilão {obraSelecionada.title}</h2>
                    <label>Descricao: <input type={"text"} value={descricao} onChange={(e)=>setDescricao(e.target.value)} required/></label>
                    <label>Valor Inicial: <input type={"number"} step={"0.01"} min={"0.01"}value={valorInicial} onChange={(e)=>setValorInicial(e.target.value)} required/></label>
                    <label>Incremento Minímo: <input type={"number"} step={"0.01"} min={"0.01"}value={incrementoMinimo} onChange={(e)=>setIncrementoMinimo(e.target.value)} required/></label>
                    <label>Incio em: <input type={"datetime-local"} value={inicio} onChange={(e)=>setInicio(e.target.value)} required/></label>
                    <label>Fim em: <input type={"datetime-local"} value={fim} onChange={(e)=>setFim(e.target.value)} required/></label>
                <button type={"submit"} disabled={criando}>{criando?"Criando..":"Criar Leilão"}</button>
                    {erroCriacao && (<p>{erroCriacao}</p>)}

                </form>
            )}
        </>
    )

}