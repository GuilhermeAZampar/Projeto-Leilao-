import {useEffect,useState} from "react";
import {buscarCarteira} from "../services/api.js";
import {fazer_deposito} from "../services/api.js";

export default function Carteira ({token}){
    const[carteira,setCarteira]=useState(null)
    const[carregando,setCarregnado]=useState(true)
    const[erro,setErro]=useState(null)
    const[valorDeposito,setValoDeposito]=useState('')
    const[depositando,setDepositando]=useState(false)
    const[erroDeposito,setErroDeposito]=useState(null)
    useEffect(()=>{
        async function PegarCarteira(){
            setCarregnado(true)
            setErro(null)
            try{
                const dados = await buscarCarteira(token)
                setCarteira(dados)
            }catch (error){
                setErro(error.message)
            }finally {
                setCarregnado(false)
            }
        }
        PegarCarteira()
    },[token])
    async function handleDeposito(e){
        e.preventDefault()
        setDepositando(true)
        setErroDeposito(null)
        try{
            const dados = await fazer_deposito(token,valorDeposito)
            setCarteira(dados)
            setValoDeposito('')
        }catch (error){
            setErroDeposito(error.message)
        }
        finally {
            setDepositando(false)
        }

    }

    if(carregando){
        return <p>Carregando...</p>
    }
    if(erro){
        return <p>Erro: {erro}</p>
    }
    return(
        <>
            <section>
                <h1>Minha Carteira</h1>
                <p>Saldo: {Number(carteira.saldo).toLocaleString("pt-br",{"style":"currency","currency":"BRL"})}</p>
                <p>Saldo Disponível: {Number(carteira.saldo_disponivel).toLocaleString("pt-br",{"style":"currency","currency":"BRL"})}</p>
                <p>Saldo Comprometido: {Number(carteira.saldo_reservado).toLocaleString("pt-br",{"style":"currency","currency":"BRL"})}</p>
            </section>
            <form onSubmit={handleDeposito}>
                <input type={"number"} min={"0.01"} step={"0.01"} value={valorDeposito} placeholder={"Digite o valor do deposito"} onChange={(e)=>{setValoDeposito(e.target.value)}} required/>
                <button type={"submit"} disabled={depositando}>{depositando ? "Depositando...":"Fazer deposito"}</button>
            </form>
            {erroDeposito &&(<p>{erroDeposito}</p>)}
        </>
    )

}

