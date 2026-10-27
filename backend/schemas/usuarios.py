from pydantic import BaseModel,EmailStr,Field
from models.usuario import PapelUsuario

class UsuarioCadastro(BaseModel):
    nome:str=Field(min_length=2,max_length=100)
    email:EmailStr
    senha:str=Field(min_length=8)
    papel:PapelUsuario


class UsuarioResposta(BaseModel):
    id:int
    nome:str
    email:EmailStr
    papel:PapelUsuario
    model_config = {"from_attributes":True}


class UsuarioLogin(BaseModel):
   email:EmailStr
   senha:str


class TokenResposta(BaseModel):
    access_token:str
    token_type:str="bearer"