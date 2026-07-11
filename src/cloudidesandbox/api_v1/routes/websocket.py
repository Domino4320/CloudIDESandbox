from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from fastapi.responses import FileResponse
from src.cloudidesandbox.logging_ import AppLogger
import docker

logger = AppLogger(__name__, to_file=True).get_logger()
router = APIRouter(prefix="/ws")


@router.websocket("/terminal")
async def terminal_route(websocket: WebSocket):
    await websocket.accept()
    logger.info("WebSocket подключение установлено")
    container = None
    try:
        client = docker.from_env()
        container = client.containers.run(
            image="python:3.12-slim",
            command=["sleep", "infinity"],
            tty=True,
            detach=True,
        )
        while True:
            command = await websocket.receive_text()
            command = command.strip()
            if not command:
                continue
            logger.info(f"Выполнение команды {command}")
            exit_code, output = container.exec_run(command)
            response_text = ""
            if output:
                response_text = output.decode("utf-8")
            else:
                response_text = f"Выполнено с кодом {exit_code}"
            await websocket.send_text(response_text)
    except WebSocketDisconnect as ex:
        logger.warning(f"Пользователь оборвал WebSocket подключение - {ex}")
    except Exception as ex:
        logger.error(f"Ошибка во время WebSocket подключения {ex}")
    finally:
        try:
            if container:
                container.stop()
                logger.info("Контейнер остановил свою работу")
                container.remove()
                logger.info("Контейнер мягко удален")
        except Exception as ex:
            logger.error(f"Возникла ошибка при удалении контейнера: {ex}")
            container.remove(force=True)
            logger.warning("Контейнер блы удален принудительно")


@router.get("/")
async def index():
    return FileResponse("src/cloudidesandbox/templates/index.html")
