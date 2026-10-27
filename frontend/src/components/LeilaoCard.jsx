import "./LeilaoCard.css"
import{Link} from "react-router-dom";

export default function CardLeilao ({leilao}){
    return(
        <Link className="link-card" to={`/leiloes/${leilao.id}`}>
        <article className="card-leilao">
             {leilao.imagem_url ? (
                <img src={leilao.imagem_url} alt={leilao.titulo}/>

             ):(<div className="sem-imagem">Imagem Indisponivel</div>)}
            <div className="card-conteudo">
            <p>{leilao.titulo}</p>
            <p>{leilao.descricao}</p>
            <p>ID:#{leilao.id}</p>
            <p>Lance Inicial: {Number(leilao.valor_inicial).toLocaleString("pt-br",{
                "style":"currency",
                "currency":"BRL"
            })}</p>
            <p>{leilao.status}</p>

                </div>
        </article>
            </Link>

    )
}