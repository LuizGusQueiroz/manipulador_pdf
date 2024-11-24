import importlib.metadata
import subprocess
import requests
import socket
import sys


def update():
    print('Verificando atualizações...')

    pacote = "manipulador_pdf"

    if tem_conexao():
        try:
            # Obtém a versão da biblioteca instalada
            versao_instalada = importlib.metadata.version(pacote)
            print(f"Versão atual do pacote: {versao_instalada}")

            # Obtém a versão mais recente disponível no PyPI
            versao_mais_recente = obter_versao_mais_recente(pacote)
            if versao_mais_recente:
                print(f"Versão mais recente disponível: {versao_mais_recente}")

                # Compara as versões
                if versao_instalada != versao_mais_recente:
                    print("Atualizando biblioteca...")
                    subprocess.check_call([subprocess.sys.executable, "-m", "pip", "install", "--upgrade", pacote])

                    # Reinicia o script para refletir a versão mais recente
                    print("Reiniciando o script para usar a versão mais recente...")
                    subprocess.run([sys.executable, __file__])  # Reinicia o script
                    sys.exit()  # Encerra o processo atual para evitar que o código continue a rodar

            else:
                print("Não foi possível verificar a versão mais recente.")

        except importlib.metadata.PackageNotFoundError:
            print("Biblioteca não encontrada. Instalando recursos...")
            subprocess.check_call([subprocess.sys.executable, "-m", "pip", "install", pacote])


def tem_conexao() -> bool:
    try:
        socket.create_connection(('8.8.8.8', 53), timeout=5)
        return True
    except Exception:
        return False


def obter_versao_mais_recente(pacote):
    """
    Obtém a versão mais recente do pacote disponível no PyPI usando a API JSON do PyPI.
    """
    try:
        # Faz uma requisição GET à API do PyPI
        response = requests.get(f"https://pypi.org/pypi/{pacote}/json")
        response.raise_for_status()  # Levanta um erro se a requisição falhar
        data = response.json()
        return data["info"]["version"]
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar a versão mais recente: {e}")
        return None
