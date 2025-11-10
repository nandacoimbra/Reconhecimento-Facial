import face_recognition # type: ignore
import cv2 # type: ignore
import os
import pickle
import time
from config.settings import CAMERA_INDEX


# Carrega todos os encodings salvos em uma pasta
def carregar_encodings(pasta):
    encs, nomes, ids = [], [], []
    for arquivo in os.listdir(pasta):  # Percorre todos os arquivos na pasta
        if arquivo.endswith(".pkl"):  # Cada encoding está salvo em um arquivo pickle
            with open(os.path.join(pasta, arquivo), "rb") as f:
                dados = pickle.load(f)  # Carrega o dicionário com id, nome e encoding
                encs.append(dados["encoding"])
                nomes.append(dados["nome"])
                ids.append(dados["id"])
    return encs, nomes, ids


# Captura um rosto via webcam, gera encoding e salva em arquivo .pkl
def salvar_encoding(id_usuario, nome_usuario, pasta_encodings):

    cap = cv2.VideoCapture(CAMERA_INDEX)  # Abre a câmera padrão (id=0)
    if not cap.isOpened():
        print("Erro ao acessar a câmera.")
        return False

    print("Aguardando rosto para captura automática...")
    encoding_salvo = False
    inicio_contagem = None  # Para controlar os 5s de rosto visível

    while True:
        ret, frame = cap.read()  # Lê frame da câmera
        if not ret:
            continue  # Se não conseguiu capturar, tenta de novo

        # Reduz o tamanho do frame (1/4 da imagem → mais rápido)
        # Converte para RGB (padrão usado pela lib face_recognition)
        pequena = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb = cv2.cvtColor(pequena, cv2.COLOR_BGR2RGB)

        # Detecta rostos no frame
        localizacoes = face_recognition.face_locations(rgb)

        if localizacoes:
            # Se achou rosto, inicia a contagem de tempo
            if inicio_contagem is None:
                inicio_contagem = time.time()
            # Se o rosto ficou 5 segundos visível → captura encoding
            elif time.time() - inicio_contagem >= 5.0:
                encodings = face_recognition.face_encodings(rgb, localizacoes)
                if encodings:
                    # Usa o primeiro rosto encontrado
                    encoding = encodings[0]

                    # Monta dicionário com dados do usuário
                    dados = {"id": id_usuario, "nome": nome_usuario, "encoding": encoding}

                    # Salva em arquivo pickle
                    nome_arquivo = f"{id_usuario}_{nome_usuario}.pkl"
                    caminho_completo = os.path.join(pasta_encodings, nome_arquivo)
                    with open(caminho_completo, "wb") as f:
                        pickle.dump(dados, f)

                    print(f"Encoding salvo com sucesso: {caminho_completo}")
                    encoding_salvo = True
                    break
                else:
                    print("Rosto não pôde ser codificado. Tente novamente.")
                    inicio_contagem = None  # Reinicia contagem
        else:
            # Se rosto some da tela → reinicia contagem
            inicio_contagem = None

        # Mostra janela com o vídeo ao vivo para dar feedback visual
        cv2.imshow("Cadastro Facial", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break  # Permite sair manualmente com a tecla "q"

    # Libera câmera e fecha janela ao fim
    cap.release()
    cv2.destroyAllWindows()
    return encoding_salvo


# Remove encoding salvo com base no ID do usuário
def remover_encoding_por_id(id_usuario, pasta_encodings):
    """Remove o arquivo de encoding do usuário pelo ID."""
    for arquivo in os.listdir(pasta_encodings):
        if arquivo.endswith(".pkl"):  # Procura apenas nos arquivos pickle
            caminho = os.path.join(pasta_encodings, arquivo)
            with open(caminho, "rb") as f:
                dados = pickle.load(f)
            if str(dados["id"]) == str(id_usuario):  # Confere se ID bate
                os.remove(caminho)  # Deleta o arquivo
                return True
    return False
