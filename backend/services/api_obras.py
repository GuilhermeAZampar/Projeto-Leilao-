import httpx


BASE_URL="https://openaccess-api.clevelandart.org/api/artworks"

def buscar_obras(object_id:int):
    resposta=httpx.get(f"{BASE_URL}/{object_id}",timeout=10)
    resposta.raise_for_status()
    return resposta.json()

def pesquisar_obras(termo:str):
    resposta=httpx.get(BASE_URL,params={"q": termo,"hasImages":True,"limit":10 },timeout=10)
    resposta.raise_for_status()
    return resposta.json()