import {useState} from "react";
import{fazer_login} from "../services/api.js";


export default function Login({aoLogar}){
    const[email,setEmail]=useState('')
    const[senha,setSenha]=useState('')
    const[erro,setErro]=useState(null)
    const[enviando,setEnviando]=useState(false)

   async function handlesubmit(event){
        event.preventDefault()
        setEnviando(true)
        setErro(null)
        try{
         const dados= await  fazer_login(email,senha)
            aoLogar(dados.access_token)
        }catch (error){
            setErro(error.message)
        }
        finally {
            setEnviando(false)
        }
    }

    return(
        <>
            <form onSubmit={handlesubmit}>
                <input type={"text"} value={email} placeholder={"Digite o email"} onChange={(e)=>{setEmail(e.target.value)}} required/>
                <input type={"password"} value={senha} placeholder={"Digite a senha"} onChange={(e)=>{setSenha(e.target.value)}} required/>
                <button type={"submit"} disabled={enviando}>{enviando ? "Enviando":"Fazer Login"}</button>
                {erro && <p>{erro}</p>}
            </form>
        </>
    )

}