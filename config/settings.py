import os

# SERIAL_PORT = '/dev/ttyUSB0'  # Linux
CAMERA_INDEX = 0  # Índice da câmera (0 para a primeira câmera conectada) windows
#CAMERA_INDEX = 1  # Índice da câmera (0 para a primeira câmera conectada) linux
SERIAL_PORT = 'COM7'  # ou 'COM3' no Windows
ENCODINGS_DIR = 'data\encodings'
# ENCODINGS_DIR = os.path.join('data', 'encodings') #diretorio linux

# Diretório onde serão salvos os frames de acesso (rostos reconhecidos)
ACCESS_DIR = os.path.join('data', 'access_frames')