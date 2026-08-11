import asyncio
import os
from typing import Callable, Awaitable

OutputCallback = Callable[[str], Awaitable[None]]


class TerminalService:

    def __init__(self, container_id: str, output_callback: OutputCallback):
        self.output_callback = output_callback
        self.container_id = container_id
        self._master_fd = None
        self._proc = None

    async def start(self) -> None:
        self._master_fd, slave_fd = os.openpty()
        try:
            self._proc = await asyncio.create_subprocess_exec(
                "docker",
                "exec",
                "-it",
                self.container_id,
                "/bin/bash",
                stdin=self._slave_fd,
                stdout=self._slave_fd,
                stderr=slave_fd,
                preexec_fn=os.setsid,
            )
        finally:
            os.close(slave_fd)

    async def read_loop(self) -> None:
        while True:
            raw_response = await asyncio.to_thread(os.read, self._master_fd, 1024)
            response = raw_response.decode(errors="ignore")
            if not response:
                break
            await self.output_callback(response)

    async def write_input(self, data: str) -> None:
        if not data.endswith("\n"):
            data += "\n"
        await asyncio.to_thread(os.write, self._master_fd, data.encode("utf-8"))

    async def close(self):
        if self._master_fd:
            os.close(self._master_fd)
            self._master_fd = None

        if self._proc:
            if self._proc.returncode is None:
                self._proc.terminate()
                await self._proc.wait()
            self._proc = None
