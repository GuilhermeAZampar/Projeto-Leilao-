import {useState,useEffect} from "react";
import {buscar_meusArremates} from "../services/api.js";
import {Link} from "react-router-dom";


export default function BuscarArremates ({token}){
    const [arremates,setArremates]=useState([])
    const[carregando,setCarregando]=useState(true)
    const [erro,setErro]=useState(null)
    useEffect(()=>{
          async function buscar(){

            setCarregando(true)
            setErro(null)
             try{
                const dados= await buscar_meusArremates(token)
                setArremates(dados)
            }catch (error){
                 setErro(error.message)
             }finally {
                setCarregando(false)
        }


    }
    buscar()
    },[token])


    if(carregando){
        return <p>Carregando...</p>
    }
    if(erro){
        return <p>Erro: {erro}</p>
    }
    return(
        <>
            <section>
                <h2>Meus Arremates</h2>
                {arremates.length === 0 ?(
                    <p>Voce ainda nao participou de leilões</p>
                ):(
                    <ul>
                        {arremates.map(item=>(
                            <li key={item.id}>{item.titulo} - {item.status} {item.venceu && <div><p>Voce venceu</p><Link to={`/comprovante/${item.id}`}>Ver comprovante</Link></div>}</li>
                        ))}
                    </ul>
                )}

            </section>
        </>
    )
}