const API_URL = "https://projeto-leilao.onrender.com";

export default async function buscarLeiloes (){
    const resposta=await fetch(`${API_URL}/leiloes/`)
    if(!resposta.ok){
        throw new Error("Errp ao conectar")
    }
    return await resposta.json()

}


export  async function buscarLeiloesPorId(id){
    const leiloes = await buscarLeiloes()
    return leiloes.find(leilao=>leilao.id === Number(id))??null;
}


export async function buscarLances(leilao_id){
    const resposta = await fetch(`${API_URL}/leiloes/${leilao_id}/lances`)
    if(!resposta.ok){
        throw new Error("Erro ao conectar")
    }
    return await resposta.json()
}


export async function enviar_lances(leilao_id,token,valor){
    const resposta = await fetch(`${API_URL}/leiloes/${leilao_id}/lances`,{
        method:"POST",
        headers:{
            "Content-type":"application/json",
            "Authorization":`Bearer ${token}`
        },
        body:JSON.stringify({
            valor:valor
        })
    })
    const dados = await resposta.json()
    if(!resposta.ok){
        throw new Error(dados.detail ||"Erro ao enviar lances")
    }
    return dados
}


export async function fazer_login(email,senha){
    const resposta = await fetch(`${API_URL}/auth/login`,{
        method:"POST",
        headers:{
            "Content-type":"application/json"
        },body:JSON.stringify({
            email:email,
            senha:senha
        })



    })
    const dados=await resposta.json()
    if (!resposta.ok){
        throw new Error(dados.detail ||"Erro ao login")
    }
    return dados
}


export  async function buscarCarteira(token){
    const resposta=await fetch(`${API_URL}/carteira/`,{
        headers:{
            "Authorization":`Bearer ${token}`
        }
    })
    const dados = await resposta.json()
    if(!resposta.ok){
        throw new Error(dados.detail || "Erro ao buscar carteira")
    }

    return dados
}

export  async function fazer_deposito(token,valor) {
    const resposta = await fetch(`${API_URL}/carteira/depositar`,{
        method:"POST",
        headers:{
            "Content-type":"application/json",
            "Authorization":`Bearer ${token}`
        },
        body:JSON.stringify({
            "valor":valor
        })
    })
    const dados=await resposta.json()
    if(!resposta.ok){
        throw new Error(dados.detail || "Erro ao fazer deposito")
    }
    return dados
}

export async function buscarObras(termo){
    const resposta=await fetch(`${API_URL}/obras/pesquisar?termo=${encodeURIComponent(termo)}`)
    if(!resposta.ok){
        throw new Error("Erro ao buscar obras")
    }

    return await resposta.json()
}

export async function criarLeilao(token,dados){
    const resposta = await fetch(`${API_URL}/leiloes/`,{
        method:"POST",
        headers:{
            "Content-type":"application/json",
            "Authorization":`Bearer ${token}`
        },
        body:JSON.stringify(dados)

    })
    const dados_reposta=await resposta.json()
    if(!resposta.ok){
        throw new Error(dados_reposta.detail || "Erro ao criar leilão")
    }

    return dados_reposta
}

export async function buscarUsuario(token){
    const resposta=await fetch(`${API_URL}/auth/me`,{
        method:"POST",
        headers:{
            "Authorization":`Bearer ${token}`
        }
    })
    const dados=await resposta.json()
    if(!resposta.ok){
        throw new Error(dados.detail ||  "Erro ao buscar usuario")
    }
    return  dados
}


export async function cancelarLeilao(id,token){
    const resposta=await fetch(`${API_URL}/leiloes/${id}/cancelar`,{
        method:"PATCH",
        headers:{"Authorization":`Bearer ${token}`}
    })

    const data_reposta=await resposta.json()
    if(!resposta.ok){
        throw new Error(data_reposta.detail || "Erro ao cancelar leilao")
    }
    return data_reposta
}

export async function comprovante(id){
    const reposta = await fetch(`${API_URL}/leiloes/${id}/comprovante`)
    const dados=await reposta.json()
    if(!reposta.ok){
        throw new Error(dados.detail || "erro ao pegar comprovante")
    }
    return dados
}

export async function buscar_meusArremates(token){
    const resposta = await fetch(`${API_URL}/leiloes/meus-arremates`,{
        headers:{
            "Authorization":`Bearer ${token}`
        }
    })
    const dados = await resposta.json()
    if(!resposta.ok){
        throw new Error(dados.detail || "Erro ao buscar arremantes")
    }

    return dados

}


export async function buscar_auditoria(id){
    const resposta=await fetch(`${API_URL}/leiloes/${id}/auditoria`)
    const dados= await resposta.json()
    if(!resposta.ok){
        throw new Error(dados.detail || "Erro ao buscar auditoria")
    }

    return dados

}