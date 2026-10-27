from fastapi.websockets import WebSocket,WebSocketDisconnect
from services.websocket_manager import manager
from fastapi import APIRouter


router = APIRouter()

@router.websocket("/leiloes/{leilao_id}/ws")
async def websocket_leilao(websocket: WebSocket,leilao_id: int):
    await manager.conectar(leilao_id,websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect :
        pass
    finally:
        manager.desconectar(leilao_id,websocket)
