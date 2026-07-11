import docker
import time
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(filename)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
    ],
)


def run_interactive_sandbox():
    client = (
        docker.from_env()
    )  # данный метод ищет сам сокет (var/run/docker.sock) и возвращает объект клиента
    container = client.containers.run(
        image="python:3.12-slim",  # Образ который мы берем для контейнера
        command="sleep infinity",  # ЧТобы контейнер не сразу потух
        detach=True,  # Запуск в фоновом режиме, чтобы Python скрипт шел дальше
        tty=True,  # Поддержка терминала внутри контейнера
    )
    print("Добро пожаловать в CloudIdeSandbox! Чтобы завершить сессию, введите exit")
    logger.info("Пользователь успешно вошел в контейнер")
    try:
        while True:
            command = input("CloudeIdeSandbox > ").strip()
            if command.lower() == "exit":
                print("Выход осуществлен успешно")
                break
            if not command:
                continue
            exit_code, output = container.exec_run(command)
            if not output:
                print(f"Выполнено с кодом {exit_code}")
            else:
                print(output.decode("utf-8").strip())
    finally:
        try:
            container.stop()
            print("Работа контейнера успешно остановлена")
            container.remove()
            print("Контейнер успешно удален")
        except Exception as ex:
            print("Возникла ошибка, запускаем принудительное удаление контейнера")


if __name__ == "__main__":
    run_interactive_sandbox()
