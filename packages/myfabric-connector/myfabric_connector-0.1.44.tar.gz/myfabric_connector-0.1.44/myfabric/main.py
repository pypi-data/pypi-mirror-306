# myfabric/main.py

import sys
import asyncio
import websockets
import logging
from logging.handlers import RotatingFileHandler
import requests
from pysher import Pusher
import argparse
from .__version__ import __version__

REVERB_ENDPOINT = "app.myfabric.ru"
APP_KEY = "3ujtmboqehae8ubemo5n"


# Точка входа в программу
def main():
    parser = argparse.ArgumentParser(description='MyFabric Connector')
    parser.add_argument('--version', action='version', version=f'MyFabric Connector {__version__}')
    parser.add_argument('--log-file', default='/var/log/myfabric/myfabric.log', help='Путь к файлу логов')
    parser.add_argument('--log-level', default='INFO',
                        help='Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)')
    parser.add_argument('moonraker_url', help='URL Moonraker WebSocket (например, localhost:7125)')
    parser.add_argument('moonraker_login', help='Логин от moonraker')
    parser.add_argument('moonraker_password', help='Пароль от moonraker')
    parser.add_argument('printer_key', help='Ключ принтера в MyFabric (хэш-строка)')
    parser.add_argument('myfabric_login', help='E-mail от учетной записи MyFabric')
    parser.add_argument('myfabric_password', help='Пароль от учётной записи MyFabric')
    args = parser.parse_args()

    # Настройка логирования
    log_level = getattr(logging, args.log_level.upper(), logging.INFO)
    logger = logging.getLogger('myfabric')
    logger.setLevel(log_level)

    # Создаем обработчик логов с ротацией
    handler = RotatingFileHandler(
        args.log_file, maxBytes=10 * 1024 * 1024, backupCount=5)
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Запуск основного цикла
    try:
        asyncio.run(start_proxy(args.moonraker_url, args.printer_key, args.myfabric_login, args.myfabric_password, args.moonraker_login,
                                args.moonraker_password))
    except KeyboardInterrupt:
        logger.info("Остановка программы по запросу пользователя")
    except Exception as e:
        logger.exception(f"Произошла ошибка: {e}")
        sys.exit(1)


# Функция для запуска прокси
async def start_proxy(moonraker_url, printer_key, login, password, moonraker_login, moonraker_password):
    channel_name = f'private-printers.{printer_key}'
    bearer = login_fabric(login, password)

    moonraker_api_key = get_moonraker_token(moonraker_url, moonraker_login, moonraker_password)
    moonraker_ws = f"ws://{moonraker_url}/websocket?token={moonraker_api_key}"

    await proxy_moonraker_reverb(moonraker_ws, channel_name, bearer)
    # Запуск задач
    # await asyncio.gather(
    #    moonraker_to_reverb(moonraker_ws, channel_name, bearer),
    #    reverb_to_moonraker(moonraker_ws, channel_name, bearer)
    # )


# todo: deprecated Пересылка сообщений из Moonraker в Reverb
async def moonraker_to_reverb(moonraker_url, channel_name, bearer):
    logger = logging.getLogger('myfabric')
    try:
        async with websockets.connect(moonraker_url) as moonraker_ws:
            logger.info(f"Подключено к Moonraker на {moonraker_url}")
            # Инициализируем Pusher-клиент
            reverb_pusher = Pusher(
                custom_host=REVERB_ENDPOINT,
                key=APP_KEY,
                secure=True,
                daemon=True,
                reconnect_interval=5
            )

            # Функция обратного вызова при установлении соединения
            def connect_handler(data):
                logger.info("Соединение с Reverb установлено (Moonraker to Reverb)")
                # Аутентифицируемся и подписываемся на приватный канал
                ws_auth_token = auth_reverb(bearer, channel_name, reverb_pusher.connection.socket_id)
                channel = reverb_pusher.subscribe(channel_name, ws_auth_token)
                # Сохраняем объект канала для отправки сообщений
                reverb_pusher.channel = channel

            reverb_pusher.connection.bind('pusher:connection_established', connect_handler)
            reverb_pusher.connect()

            # Ждем установления соединения и подписки на канал
            while reverb_pusher.connection.state != "connected" or channel_name not in reverb_pusher.channels:
                await asyncio.sleep(0.1)

            while True:
                try:
                    message = await moonraker_ws.recv()
                    logger.debug(f"Получено сообщение от Moonraker: {message}")
                    # Отправляем сообщение в приватный канал Reverb
                    reverb_pusher.channel.trigger('client-event', message)
                except websockets.ConnectionClosed:
                    logger.warning("Соединение с Moonraker закрыто")
                    break
                except Exception as e:
                    logger.error(f"Ошибка при пересылке сообщения в Reverb: {e}")
    except Exception as e:
        logger.exception(f"Ошибка в moonraker_to_reverb: {e}")


# todo: deprecated Пересылка сообщений из Reverb в Moonraker
async def reverb_to_moonraker(moonraker_url, channel_name, bearer):
    logger = logging.getLogger('myfabric')
    while True:
        try:
            async with websockets.connect(moonraker_url) as moonraker_ws:
                logger.info(f"Подключено к Moonraker на {moonraker_url}")

                # Инициализируем Pusher-клиент
                reverb_pusher = Pusher(
                    custom_host=REVERB_ENDPOINT,
                    key=APP_KEY,
                    secure=True,
                    daemon=True,
                    reconnect_interval=5,
                )

                # Функция обратного вызова при установлении соединения
                def connect_handler(data):
                    logger.info("Соединение с Reverb установлено (Reverb to Moonraker)")
                    # Подписываемся на приватный канал
                    ws_auth_token = auth_reverb(bearer, channel_name, reverb_pusher.connection.socket_id)
                    channel = reverb_pusher.subscribe(channel_name, ws_auth_token)
                    channel.bind('moonraker-request', reverb_message_handler)

                # Обработчик сообщений из Reverb
                def reverb_message_handler(message):
                    logger.debug(f"Получено сообщение от Reverb: {message}")
                    # Отправляем сообщение в Moonraker и ожидаем ответ
                    asyncio.create_task(send_message_and_wait_response(moonraker_ws, message))

                reverb_pusher.connection.bind('pusher:connection_established', connect_handler)
                reverb_pusher.connect()

                # Ждем установления соединения
                while reverb_pusher.connection.state != "connected":
                    await asyncio.sleep(0.1)

                # Listen for responses from Moonraker
                async for message in moonraker_ws:
                    logger.debug(f"Получен ответ от Moonraker: {message}")
                    # Optionally, relay it back to Reverb or process it
        except websockets.exceptions.ConnectionClosed as e:
            logger.warning(f"Соединение с Moonraker закрыто: {e}. Переподключение...")
            await asyncio.sleep(5)  # Wait before reconnecting
        except Exception as e:
            logger.exception(f"Ошибка в reverb_to_moonraker: {e}")
            await asyncio.sleep(5)


# todo: deprecated
async def send_message_and_wait_response(moonraker_ws, message):
    logger = logging.getLogger('myfabric')
    try:
        logger.debug(f"Отправка сообщения в Moonraker: {message}")
        await moonraker_ws.send(message)
        logger.debug("Сообщение отправлено, ожидание ответа...")

        # Ожидание ответа с таймаутом
        try:
            response = await asyncio.wait_for(moonraker_ws.recv(), timeout=5)
            logger.debug(f"Получен ответ от Moonraker: {response}")
        except asyncio.TimeoutError:
            logger.error("Таймаут ожидания ответа от Moonraker")
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения в Moonraker: {e}")


def login_fabric(login, password):
    logger = logging.getLogger('myfabric')
    # Аутентификация
    res = requests.post(f'https://{REVERB_ENDPOINT}/api/auth/login', json={
        'email': login,
        'password': password,
    })
    if res.status_code != 200:
        logger.error(f'CANNOT SIGN IN ({res.status_code}): {res.text}')
        return
    data = res.json()
    logger.info(f'LOGGED IN ({res.status_code})')
    bearer = data['access_token']
    return bearer


def auth_reverb(bearer, channel_name, socket_id):
    logger = logging.getLogger('myfabric')
    request_data = {
        "channel_name": channel_name,
        "socket_id": socket_id
    }
    response = requests.post(
        f"https://{REVERB_ENDPOINT}/api/broadcasting/auth",
        json=request_data,
        headers={
            'Authorization': f'Bearer {bearer}'
        }
    )
    if response.status_code != 200:
        logger.error(f"Failed to get auth token from MyFabric ({response.status_code}): {response.text}")
        raise Exception("Authentication failed")
    auth_key = response.json().get("auth")
    if not auth_key:
        logger.error("Auth key not found in response")
        raise Exception("Authentication failed")
    return auth_key


def get_moonraker_token(moonraker_url, username, password):
    response = requests.post(f"http://{moonraker_url}/access/login", json={
        'username': username,
        'password': password,
        "source": "moonraker"
    })
    if response.status_code != 200:
        raise Exception(f"Failed to obtain Moonraker token: {response.status_code} {response.text}")
    data = response.json()
    bearer = data['result']['token']
    response = requests.get(f"http://{moonraker_url}/access/oneshot_token", headers={
        "Authorization": f'Bearer {bearer}'
    })
    data = response.json()
    return data.get("result")


async def proxy_moonraker_reverb(moonraker_url, channel_name, bearer):
    logger = logging.getLogger('myfabric')

    loop = asyncio.get_event_loop()  # Получаем ссылку на главный цикл событий

    # Initialize queues
    moonraker_to_reverb_queue = asyncio.Queue()
    reverb_to_moonraker_queue = asyncio.Queue()

    # Connect to Moonraker
    async with websockets.connect(moonraker_url) as moonraker_ws:
        logger.info(f"Connected to Moonraker at {moonraker_url}")

        # Initialize Pusher client
        reverb_pusher = Pusher(
            custom_host=REVERB_ENDPOINT,
            key=APP_KEY,
            secure=True,
            daemon=True,
            reconnect_interval=5
        )

        # Connection handlers
        async def moonraker_reader():
            async for message in moonraker_ws:
                logger.debug(f"Received from Moonraker: {message}")
                await moonraker_to_reverb_queue.put(message)

        async def moonraker_writer():
            logger.debug(f"moonraker_writer INIT")
            while True:
                message = await reverb_to_moonraker_queue.get()
                logger.debug(f"Trying to send to Moonraker: {message}")
                await moonraker_ws.send(message)
                logger.debug(f"Sent to Moonraker: {message}")

        def reverb_connect_handler(data):
            logger.info("Connected to Reverb")
            ws_auth_token = auth_reverb(bearer, channel_name, reverb_pusher.connection.socket_id)
            channel = reverb_pusher.subscribe(channel_name, ws_auth_token)
            channel.bind('moonraker-request', reverb_message_handler)
            reverb_pusher.channel = channel

        def reverb_message_handler(message):
            logger.debug(f"Received from Reverb: {message}")
            # asyncio.create_task(reverb_to_moonraker_queue.put(message))
            asyncio.run_coroutine_threadsafe(
                reverb_to_moonraker_queue.put(message),
                loop
            )

        # Bind handlers and connect
        reverb_pusher.connection.bind('pusher:connection_established', reverb_connect_handler)
        reverb_pusher.connect()

        # Start coroutines
        await asyncio.gather(
            moonraker_reader(),
            moonraker_writer(),
            handle_moonraker_to_reverb(moonraker_to_reverb_queue, reverb_pusher, channel_name)
        )


async def handle_moonraker_to_reverb(queue, reverb_pusher, channel_name):
    logger = logging.getLogger('myfabric')
    while True:
        message = await queue.get()
        if channel_name in reverb_pusher.channels:
            reverb_pusher.channels[channel_name].trigger('client-event', message)
            logger.debug(f"Sent to Reverb: {message}")
        else:
            logger.debug(f"No channel found for Reverb: {message}")


if __name__ == '__main__':
    main()
