from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from cloudidesandbox.core.logging import AppLogger
from src.cloudidesandbox.services.workspaces import initialize_user_workspace
from src.cloudidesandbox.services.terminal import TerminalService

logger = AppLogger(__name__, to_file=True).get_logger()
router = APIRouter()


@router.websocket("/ws/terminal/{container_id}")
async def terminal_session(websocket: WebSocket, container_id: str) -> None:
    await websocket.accept()
    initialize_user_workspace()
    ts = TerminalService(websocket, container_id)
    await ts.run()
    await websocket.close()
