import docker
import time
from src.cloudidesandbox.logging_ import AppLogger

logger = AppLogger(__name__, to_file=True).get_logger()


def run_interactive_sandbox():
    client = (
        docker.from_env()
    )  # данный метод ищет сам сокет (var/run/docker.sock) и возвращает объект клиента
    logger.debug("Клиент докера создан")
    container = client.containers.run(
        image="python:3.12-slim",  # Образ который мы берем для контейнера
        command="sleep infinity",  # ЧТобы контейнер не сразу потух
        detach=True,  # Запуск в фоновом режиме, чтобы Python скрипт шел дальше
        tty=True,  # Поддержка терминала внутри контейнера
    )
    logger.debug("Контейнер инициализирован")
    print("Добро пожаловать в CloudIdeSandbox! Чтобы завершить сессию, введите exit")
    logger.info("Пользователь успешно вошел в контейнер")
    try:
        while True:
            command = input("CloudeIdeSandbox > ").strip()
            if command.lower() == "exit":
                print("Выход осуществлен успешно")
                logger.info("Пользователь вышел из контейнера")
                break
            if not command:
                logger.info("Пользователь ввел пустую команду")
                continue
            exit_code, output = container.exec_run(command)
            if not output:
                logger.info(
                    f"Команда пользователя успешно выполнена с кодом {exit_code} без дополнительного вывода"
                )
                print(f"Выполнено с кодом {exit_code}")
            else:
                result = output.decode("utf-8").strip()
                logger.info(f"Команда успешно выполнена. Лог комманды: {result}")
                print(result)
    finally:
        try:
            container.stop()
            logger.info("Работа контейнера завершена успешно")
            print("Работа контейнера успешно остановлена")
            container.remove()
            print("Контейнер успешно удален")
            logger.info("Контейнер успешно удален")

        except Exception as ex:
            print("Возникла ошибка, запускаем принудительное удаление контейнера")
            logger.warning(
                "Не удалось мягко удалить контейнер. Запустилось жесткое удаление"
            )


if __name__ == "__main__":
    run_interactive_sandbox()
