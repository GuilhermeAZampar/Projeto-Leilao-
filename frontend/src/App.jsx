import './App.css'
import {BrowserRouter, Route, Routes, Links, Link} from "react-router-dom";
import Galeria_leilao from "./pages/Galeria.jsx";
import Detalhes from "./pages/DetalhesLeilao.jsx";
import {useState} from "react";
import Login from "./pages/Login.jsx";
import Carteira from "./pages/Carteira.jsx";
import BuscarObra from "./pages/PainelLeiloeiro.jsx";
import Comprovante from "./pages/Comprovante.jsx";
import BuscarArremates from "./pages/MeusArremates.jsx";
import ConsultarAuditoira from "./pages/Auditoria.jsx";


function App() {
    const[token,setToken]=useState(()=>{ return sessionStorage.getItem("token")})
    function aoLogar(access_token){
        sessionStorage.setItem("token",access_token)
        setToken(access_token)
    }

    function sair(){
        sessionStorage.removeItem("token")
        setToken(null)
    }

  return (

    <>
      <main>
          <h1>Leilão da Verzel</h1>
          {token && <button onClick={sair} className="botao-sair">Sair</button> }
            {!token &&<Login aoLogar={aoLogar}></Login>}
              <BrowserRouter>
                  <nav className="menu-navegacao">
                      <Link to="/">Galeria</Link>
                      {token &&(<Link to="/painel">Painel Leiloeiro</Link>)}
                      {token &&(<Link to={"/meus-arremates"}>Meus Arremates</Link>)}

                      {token &&(
                          <Link to="/carteira">Minha Carteira</Link>

                      )}
                  </nav>
          <Routes>
              <Route path="/" element={<Galeria_leilao/>}></Route>
              <Route path="/leiloes/:id" element={<Detalhes token={token}/>}></Route>
              <Route path="/carteira" element={<Carteira token={token}/>}></Route>
              <Route path="/painel" element={<BuscarObra token={token}/>}></Route>
              <Route path="/comprovante/:id" element={<Comprovante/>}></Route>
              <Route path="/meus-arremates" element={<BuscarArremates token={token}/>}></Route>
              <Route path="/auditoria/:id" element={<ConsultarAuditoira/>}></Route>
          </Routes>
      </BrowserRouter>


        </main>

    </>
  )
}

export default App
