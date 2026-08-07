from __future__ import annotations
import asyncio
from asyncio.subprocess import Process
import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi import WebSocket


class TerminalService:

    def __init__(self, websocket: WebSocket, container_id: str):
        self.websocket = websocket
        self.container_id = container_id

    async def _start_process(self) -> tuple[int, Process]:
        master_fd, slave_fd = os.openpty()
        try:
            proc = await asyncio.create_subprocess_exec(
                "docker",
                "exec",
                "-it",
                self.container_id,
                "/bin/bash",
                stdin=slave_fd,
                stdout=slave_fd,
                stderr=slave_fd,
                preexec_fn=os.setsid,
            )
        finally:
            os.close(slave_fd)
        return master_fd, proc

    async def _pty_to_web(self, master_fd: int) -> None:
        while True:
            raw_response = await asyncio.to_thread(os.read, master_fd, 1024)
            response = raw_response.decode(errors="ignore")
            if not response:
                return
            await self.websocket.send_text(response)

    async def _web_to_pty(self, master_fd: int) -> None:
        while True:
            request = await self.websocket.receive_text()
            if not request.endswith("\n"):
                request += "\n"
            await asyncio.to_thread(os.write, master_fd, request.encode("utf-8"))

    async def run(self) -> None:
        try:
            master_fd, proc = await self._start_process()
            task_read = asyncio.create_task(self._pty_to_web(master_fd))
            task_write = asyncio.create_task(self._web_to_pty(master_fd))
            _, pending = await asyncio.wait(
                [task_read, task_write],
                return_when=asyncio.FIRST_COMPLETED,
            )
        finally:
            for task in pending:
                task.cancel()
            os.close(master_fd)
            proc.terminate()
            await proc.wait()
