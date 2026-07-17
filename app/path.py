"""Caminhos usados pela aplicação em desenvolvimento e após compilação.

Os recursos incluídos pelo PyInstaller ficam dentro da pasta interna do pacote,
enquanto os dados modificáveis devem ficar junto ao executável. Esta separação
permite carregar imagens corretamente e guardar a base de dados sem escrever na
pasta interna do bundle.
"""

import sys
from pathlib import Path


IS_FROZEN = bool(getattr(sys, "frozen", False))

if IS_FROZEN:
    # Pasta visível ao utilizador, onde se encontra o LifePlanner.exe.
    BASE_DIR = Path(sys.executable).resolve().parent

    # Pasta interna criada pelo PyInstaller, onde ficam os assets empacotados.
    RESOURCE_DIR = Path(getattr(sys, "_MEIPASS", BASE_DIR)).resolve()
else:
    BASE_DIR = Path(__file__).resolve().parent.parent
    RESOURCE_DIR = BASE_DIR

ASSETS_DIR = RESOURCE_DIR / "assets"
ICONS_DIR = ASSETS_DIR / "icons"
IMAGES_DIR = ASSETS_DIR / "images"

# Dados e configurações alteráveis permanecem fora dos recursos empacotados.
DATA_DIR = BASE_DIR / "data"
CONFIG_DIR = BASE_DIR / "config"
ENV_FILE = BASE_DIR / ".env"
