import{useParams,Link} from "react-router-dom";
import {useState,useEffect} from "react";
import {buscarLeiloesPorId} from "../services/api.js";
import buscarLeiloes from "../services/api.js";
import {buscarLances,enviar_lances,buscarUsuario} from "../services/api.js";
import './DetalhesLeilao.css'



export default function Detalhes ({token}){
    const {id}=useParams()
    const[leilao,setLeilao]=useState(null)
    const[erro,setErro]=useState(null)
    const[carregando,setCarregando]=useState(true)
    const[lances,setLances]=useState([])
    const[valorlance,setValorLance]=useState('')
    const[enviandoLance,setEnviandoLance]=useState(false)
    const[erroLance,setErroLance]=useState(null)
    const[agora,setAgora]=useState(Date.now())
    const[usuario,setUsuario]=useState(null)
    useEffect(()=>{
        async function carregando_leilao(){
            setCarregando(true)
            setErro(null)
            try{
                const[dados_leilao,dados_Lance]=await Promise.all([
                    buscarLeiloesPorId(id),
                    buscarLances(id),

            ])
                setLeilao(dados_leilao);
                setLances(dados_Lance);
        }catch (error){
            setErro(error.message)
        }finally {
            setCarregando(false)
        }
        }

        carregando_leilao()

    },[id])
    useEffect(()=>{
        const conexao = new WebSocket(`ws://127.0.0.1:8000/leiloes/${id}/ws`)
        conexao.onmessage=async (evento)=>{
            const mensagem=JSON.parse(evento.data)
            if(mensagem.tipo==="NOVO_LANCE"){
                 const [lancesAtualizados, leilaoAtualizado] = await Promise.all([
                buscarLances(id),
                buscarLeiloesPorId(id)
            ])

                setLances(lancesAtualizados)
                setLeilao(leilaoAtualizado)
            }

        }
        return ()=>conexao.close()
    },[id])

    useEffect(()=>{
        const intervalo=setInterval(()=>{
            setAgora(Date.now())
        },1000)
        return ()=> clearInterval(intervalo)
    },[])

    async function HandleLances(e){
        e.preventDefault()
        setEnviandoLance(true)
        setErroLance(null)
        try{
          const dados=  await enviar_lances(id,token,valorlance)
            const  lanceAtualizados=await buscarLances(id)
            setLances(lanceAtualizados)
            setValorLance("")
        }catch (error){
            setErroLance(error.message)
        }finally {
            setEnviandoLance(false)
        }

    }
    useEffect(()=>{
        if(!token){
            setUsuario(null)
            return
        }
        async function carregarUsuario(){
            try{
                const dados = await buscarUsuario(token)
                setUsuario(dados)
            }catch (error){
                console.log("Erro: ",error)
                setUsuario(null)
            }
        }
        carregarUsuario()
    },[token])
    if(carregando){
        return <p>Carregando...</p>
    }
    if(erro){
        return <p>Erro:{erro}</p>
    }
    if(!leilao){
        return <p>Leilão não encontrado</p>
    }

    const segundos_restante=Math.max(0,
        Math.floor((new Date(leilao.fim_em).getTime()-agora)/1000)
    )
    const horas=Math.floor(segundos_restante/3600)
    const minutos=Math.floor((segundos_restante % 3600)/60)
    const segundos=segundos_restante % 60

    const maior_lance=lances[0]??null
    const Proximominimo=maior_lance ? Number(maior_lance.valor) + Number(leilao.incremento_minimo) : Number(leilao.valor_inicial)

    return(
        <>
            <main className="detalhes-leilao">
                <h2>Detalhes do leilao #{id}</h2>
                <h2>{leilao.titulo}</h2>
                {leilao.imagem_url ?(
                    <img className="detalhes-imagem" src={leilao.imagem_url} alt={leilao.titulo}/>

                ):(<p>Imagem indísponivel</p>)}
                <div className="detalhes-informacoes">
                    <div className="resumo-leilao">
                <p className="descricao-leilao">{leilao.descricao}</p>
                        <p><strong>Incremento mínimo :</strong> {Number(leilao.incremento_minimo).toLocaleString("pt-br",{"style":"currency","currency":"BRL"})}</p>
                        <p><strong>Lance inicial:</strong> {Number(leilao.valor_inicial).toLocaleString("pt-br",{"style":"currency","currency":"BRL"})}</p>
                        <p><strong>Inicia em:</strong> {new Date(leilao.inicio_em).toLocaleString("pt-br",{dateStyle:"short",timeStyle:"short"})}</p>
                        <p><strong>Encerra em:</strong> {new Date(leilao.fim_em).toLocaleString("pt-br",{dateStyle:"short",timeStyle:"short"})}</p>
                    <p className="tempo-leilao">Tempo para correr {horas}h  {minutos}min - {segundos}s</p>
                <p className="status-leilao">Status: {leilao.status}</p>
                    {leilao.status === "encerrado" && lances.length>0 &&(
                        <Link to={`/comprovante/${id}`}>Ver Comprovante</Link>
                    )}
                    <p className="proximo-lance">Próximo Lance mínimo : {Proximominimo.toLocaleString("pt-br",{"style":"currency","currency":"BRL"})}</p>
                    {usuario && maior_lance  &&  leilao.status !== "encerrado" && leilao.status !== "cancelado" && segundos_restante>0 &&(
                        <p className="aviso-lance">
                            {maior_lance.licitante_id===usuario.id ? "Voce esta ganhando":lances.some(lance=>lance.licitante_id===usuario.id)?"Voce foi superado":"Voce ainda nao deu lance"}
                        </p>
                    )}
                        </div>
                    <h3>Histórico</h3>
                    {leilao.status ==="encerrado" || leilao.status ==="cancelado"?(
                        <p>Esse leilao nao recebe mais lances</p>
                    ):token ? (
                         <form onSubmit={HandleLances}>
                        <input type={"number"} value={valorlance} min={Proximominimo} step={"0.01"} onChange={(e)=>setValorLance(e.target.value)} placeholder={"Digite o valor do lance"} required/>
                        <button type={"submit"} disabled={enviandoLance}>{enviandoLance ? "Enviando..." :"Dar lance"}</button>
                        {erroLance &&(<p role={"alert"}>{erroLance}</p>)}
                    </form>
                        ):(<p>Faça login para fazer lances</p>)}

                    {lances.length === 0 ?(
                        <p>Não ha histórico de lances</p>
                    ):(
                        <ul>
                            {lances.map(lance=>(
                                <li key={lance.id}>Licitante - {lance.licitante_nome ?? `Licitante #${lance.licitante_id}`}  {Number(lance.valor).toLocaleString("pt-br",{"style":"currency","currency":"BRL"})}</li>
                            ))}
                        </ul>
                    )}
                </div>
                <Link to={`/auditoria/${id}`}>Consultar Auditoria</Link>
            </main>
        </>
    )
}