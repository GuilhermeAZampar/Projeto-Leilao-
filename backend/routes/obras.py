from services.api_obras import buscar_obras,pesquisar_obras
from fastapi import APIRouter,HTTPException,Depends

router = APIRouter(prefix="/obras",tags=["obras"])


@router.get("/pesquisar")
def pesquisar(termo:str):
    return pesquisar_obras(termo)

@router.get("/{object_id}")
def obras(object_id:int):
    return buscar_obras(object_id)