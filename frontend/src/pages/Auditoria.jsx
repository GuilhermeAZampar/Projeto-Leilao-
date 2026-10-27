import {useState,useEffect} from "react";
import {useParams} from "react-router-dom";
import {buscar_auditoria, buscarLances} from "../services/api.js";


export default function ConsultarAuditoira(){
    const{id}=useParams()
    const[auditoria,setAuditoria]=useState(null)
    const[lances,setLances]=useState([])
    const[carregando,setCarregando]=useState(true)
    const[erro,setErro]=useState(null)
    useEffect(()=>{
        async function buscar(){
            setCarregando(true)
            setErro(null)
            try {
                const [dadosAuditoria,dadosLances]=await Promise.all([buscar_auditoria(id),buscarLances(id)])
                setAuditoria(dadosAuditoria)
                setLances(dadosLances)
            }catch (error){
                setErro(error.message)
            }finally {
                setCarregando(false)
            }
        }
        buscar()
    },[id])
    if(carregando){
        return <p>Carrengado...</p>
    }
    if(erro){
        return <p>Erro: {erro}</p>
    }

    return(
        <>
            <section>
                <h2>Auditoria leilao #{id}</h2>
                <p>{auditoria.valido ? "Verifição Válida":"Foi encontrada uma incoerencia"}</p>
                {!auditoria.valido &&(<p>{auditoria.erro}</p>)}
                <h3>Histórico de lances</h3>
                {lances.length===0 ?(<p>Ainda não ha lances</p>):(
                    <ul>
                    {lances.map(lance=>(
                        <li key={lance.id}>
                            Licitante #{lance.licitante_id} - {""} {Number(lance.valor).toLocaleString("pt-br",{"style":"currency","currency":"BRL"})}
                        </li>

                        ))}
                        </ul>
                )}
            </section>
        </>
    )

}