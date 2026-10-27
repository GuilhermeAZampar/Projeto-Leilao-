from collections import defaultdict
from starlette.websockets import WebSocket, WebSocketDisconnect



class ConnectionManager:
    def __init__(self):
        self.conexoes=defaultdict(list)

    async def conectar(self,leilao_id:int,websocket:WebSocket):
        await websocket.accept()
        self.conexoes[leilao_id].append(websocket)

    def desconectar(self,leilao_id:int,websocket:WebSocket):
        if websocket in self.conexoes[leilao_id]:
            self.conexoes[leilao_id].remove(websocket)

    async def enviar_para_leilao(self,leilao_id:int,mensagem:dict):
        for websocket in list(self.conexoes[leilao_id]):
            try:
                await websocket.send_json(mensagem)
            except (WebSocketDisconnect, RuntimeError):
                self.desconectar(leilao_id,websocket)



manager = ConnectionManager()