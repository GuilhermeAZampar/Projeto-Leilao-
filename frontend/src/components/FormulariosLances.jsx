import {useState} from "react";
import {enviar_lances} from "../services/api.js";

export default function FormulariosLance ({leilaoId,token,aoEnviar}){
    const[valor,setValor]=useState('')
    const[erro,setErro]=useState(null)
    const[enviando,setEnviando]=useState(false)
    async function handleSubmit(event){
        event.preventDefault()
        setErro(null)
        setEnviando(true)

        try {
            await enviar_lances(leilaoId,token,valor)
            setValor('')
            if(aoEnviar){
                await aoEnviar()
            }

        }catch (error){
            setErro(error.message)
        }finally {
            setEnviando(false)
        }
    }

    return(
        <>
            <form onSubmit={handleSubmit}>
                <label htmlFor="valor-lance">Valor Lance</label>
                <input id="valor-lance" step="0.01"  min="0.01" value={valor} onChange={(e)=>{setValor(e.target.value)}} required/>
                <button disabled={enviando} type={"submit"}>{enviando ? "Enviando" : "Dar Lance"}</button>
            </form>
            {erro && <p>{erro}</p>}

        </>
    )
}