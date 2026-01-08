import socket

import uvicorn

from kiosk.logger import logger


def get_lan_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        s.connect(('8.8.8.8', 80))
        lan_ip = s.getsockname()[0]
    except Exception as e:
        logger.error(f'get_lan_ip error: {e}')
        lan_ip = '127.0.0.1'
    finally:
        s.close()

    return lan_ip


if __name__ == '__main__':
    ip = get_lan_ip()
    port = 8080
    logger.info(f'Starting Kiosk server on {ip}:{port}')
    uvicorn.run(
        'app:app',
        host=ip,
        port=port,
        reload=True
    )
