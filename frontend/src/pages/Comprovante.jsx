import {useEffect,useState} from "react";
import {comprovante} from "../services/api.js";
import {useParams} from "react-router-dom";

export default function Comprovante (){
    const {id}=useParams()
    const[dados,setDados]=useState(null)
    const [carregando,setCarregando]=useState(true)
    const[erro,setErro]=useState(null)
    useEffect(()=>{
       async function carregarComprovante(){
           setCarregando(true)
           setErro(null)
        try{
            const resposta =  await comprovante(id)
            setDados(resposta)
        }catch (error){
            setErro(error.message)
        }finally {
            setCarregando(false)
        }
       }

        carregarComprovante()
    },[id])
    if(carregando){
       return <p>Carregando...</p>
    }
    if(erro){
        return <p>Erro:{erro}</p>
    }
    return(
        <>
            <section>
                <h2>Comprovantes</h2>
                    <p>Leilao: {dados.leilao_id}</p>
                    <p>Obra: {dados.titulo}</p>
                    <p>Vencedor: {dados.vencedor}</p>
                    <p>Valor: {Number(dados.valor_arremate).toLocaleString("pt-br",{"style":"currency","currency":"BRL"})}</p>
                    <p>Encerramento {new Date(dados.fim_em).toLocaleString("pt-br")}</p>
            </section>
        </>
    )
}