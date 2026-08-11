from typing import Annotated
from fastapi import Depends, WebSocket
from src.cloudidesandbox.services.terminal import TerminalService


def get_terminal_service(websocket: WebSocket, container_id: str) -> TerminalService:
    async def send_text(data: str):
        await websocket.send_text(data)

    return TerminalService(container_id=container_id, output_callback=send_text)


TerminalServiceDep = Annotated[TerminalService, Depends(get_terminal_service)]
