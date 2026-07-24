from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from src.cloudidesandbox.logging_ import AppLogger
from src.cloudidesandbox.api_v1.services.workspaces import initialize_user_workspace
from src.cloudidesandbox.api_v1.services.terminal import TerminalService

logger = AppLogger(__name__, to_file=True).get_logger()
router = APIRouter()


@router.websocket("ws/terminal/{container_id}")
async def terminal_session(websocket: WebSocket, container_id: str) -> None:
    await websocket.accept()
    initialize_user_workspace()
    ts = TerminalService(websocket, container_id)
    await ts.run()
    await websocket.close()
