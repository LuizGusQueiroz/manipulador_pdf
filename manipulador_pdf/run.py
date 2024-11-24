from .configs.main_hub import main_hub
from .update import update
import socket


def run():
    update()
    main_hub()


def tem_conexao() -> bool:
    try:
        # Estabelece uma conexão com o servidor DNS do Google
        socket.create_connection(('8.8.8.8', 53), timeout=5)
        return True
    except Exception:
        return False
