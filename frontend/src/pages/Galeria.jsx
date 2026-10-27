import {useState,useEffect} from "react";
import buscarLeiloes from "../services/api.js";
import CardLeilao from "../components/LeilaoCard.jsx";
import "./Galeria.css"


function Galeria_leilao(){
    const[leiloes,setLeiloes]=useState([])
    const[erro,setErro]=useState(null)
    const[carregando,setCarregando]=useState(true)
    const[filtro,setFiltro]=useState("todos")
    useEffect(()=>{
        async function carregar_leiloes(){
            try {
               const dados=await buscarLeiloes();
                setLeiloes(dados)
            }catch (error){
                setErro(error)
            }finally {
                setCarregando(false)
            }
        }

        carregar_leiloes()


    },[])
    const leiloes_filtrado=leiloes.filter(item=> {
        if(item.status ==="cancelado"){
            return false
        }
        if (filtro === "todos") {
            return true;
        }
        return item.status == filtro;
    })
    if(carregando){
       return <p>Carregando.....</p>
    }
    if(erro){
        return <p>Erro :{erro.message}</p>
    }


    return(
        <>
            <div className="filtros">
                <button className={filtro ==="todos"?"ativo":""} onClick={()=>{setFiltro("todos")}}>Todos</button>
                <button className={filtro === "agendado"?"ativo":""} onClick={()=>{setFiltro("agendado")}}>Agendado</button>
                <button className={filtro === "ativo"?"ativo":""} onClick={()=>{setFiltro("ativo")}}>Ativos</button>
                <button className={filtro==="encerrado"?"ativo":""} onClick={()=>{setFiltro("encerrado")}}>Encerrados</button>
            </div>
            <section className="galeria-grid">
                {leiloes_filtrado.length===0 && <p>Nenhum leilão encontrado</p>}
                {leiloes_filtrado.map(item=>(
                    <CardLeilao key={item.id} leilao={item}/>
                ))}

            </section>
        </>
    )

}

export default Galeria_leilao