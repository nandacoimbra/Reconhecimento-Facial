# Importações dos módulos

#funções de comunicação serial
from src.serial_comm import configurar_serial, ler_comando_serial, enviar_mensagem 
#função para capturar rosto via webcam
from src.camera import detectar_rosto_continuo 
#funções para manipular encodings (carregar, salvar, remover)
from src.encoding import carregar_encodings, salvar_encoding, remover_encoding_por_id 
#funções de reconhecimento facial e desenho na imagem
from src.recognition import comparar_com_base, desenha_retangulo_e_nome
#configurações do sistema (portas, diretórios, índices)
from config.settings import SERIAL_PORT, ENCODINGS_DIR, CAMERA_INDEX, ACCESS_DIR
#opencv2 para manipulação de imagens
import cv2 # type: ignore
#os para manipulação de diretórios e arquivos
import os
#datetime para timestamp na gravação de imagens
from datetime import datetime

# Função principal que controla o fluxo do sistema de reconhecimento facial
def fluxo_principal():
        # Garante que o diretório de acesso exista
    os.makedirs(ACCESS_DIR, exist_ok=True)

    # Configura a comunicação serial na porta definida em SERIAL_PORT
    ser = configurar_serial(SERIAL_PORT)
    print("Sistema de reconhecimento iniciado. Aguardando comandos...")

    # Loop infinito que mantém o sistema rodando e aguardando comandos
    while True:
        # Lê o comando recebido via porta serial
        comando = ler_comando_serial(ser)

        # Caso o comando seja para tirar foto e cadastrar um novo usuário
        # Formato esperado: "tirar_foto|id_usuario|nome_usuario"
        if comando and comando.startswith("tirar_foto|"):
            partes = comando.split("|")
            if len(partes) == 3:
                id_usuario, nome_usuario = partes[1], partes[2]
                print(f"Iniciando cadastro de {nome_usuario} (ID: {id_usuario})...")
                
                # Informa ao ESP32 que o cadastro começou
                enviar_mensagem(ser, "cadastro_iniciado")
                
                # Captura a foto, gera encoding e salva no diretório
                sucesso = salvar_encoding(id_usuario, nome_usuario, ENCODINGS_DIR)
                
                # Se deu certo, confirma para o ESP32, senão informa erro
                enviar_mensagem(ser, "cadastro_finalizado" if sucesso else "erro_foto")

        # Caso o comando seja para iniciar o reconhecimento facial
        elif comando and comando == "iniciar_reconhecimento_facial":
            print("Reconhecimento facial solicitado pelo ESP32.")
            
            # Mantém a câmera ligada e espera que um rosto fique visível por pelo menos 2 segundos
            frame = detectar_rosto_continuo(duracao_minima=2.0, mostrar_camera=False)
            
            if frame is not None:
                # Carrega todos os encodings salvos (rostos cadastrados)
                encodings, nomes, ids = carregar_encodings(ENCODINGS_DIR)
                # Compara o rosto capturado com os encodings da base
                nome, id_usuario, localizacao = comparar_com_base(frame, encodings, nomes, ids)
                # Se reconheceu, envia ID do usuário para o ESP32
                if nome != "Desconhecido":
                    enviar_mensagem(ser, f"face_detectada:{id_usuario}")
                    print(f"Face detectada: {nome} (ID: {id_usuario})...")
                    # Salva recorte do rosto (se tiver localização), com timestamp
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    safe_name = nome.replace(" ", "_")
                    filename = f"{id_usuario}_{safe_name}_{timestamp}.jpg"
                    caminho = os.path.join(ACCESS_DIR, filename)
                    if localizacao:
                        top, right, bottom, left = map(int, localizacao)
                        # Protege índices fora do frame
                        top = max(0, top); left = max(0, left)
                        bottom = min(frame.shape[0], bottom); right = min(frame.shape[1], right)
                        desenha_retangulo_e_nome(frame, top, right, bottom, left, nome, id_usuario)
                        cv2.imwrite(caminho, frame)
                    else:
                        cv2.imwrite(caminho, frame)
                    print(f"Frame salvo em: {caminho}")
                else:
                    enviar_mensagem(ser, "face_nao_reconhecida")
                    print("Nenhuma correspondência na base.")
            else:
                # Se não conseguiu capturar nenhum rosto, também informa falha
                enviar_mensagem(ser, "face_nao_reconhecida")
                print("Nenhum rosto detectado.")

        # Caso o comando seja para remover um usuário já cadastrado
        # Formato esperado: "remover_usuario|id_usuario"
        elif comando and comando.startswith("remover_usuario|"):
            partes = comando.split("|")
            if len(partes) == 2:
                id_usuario = partes[1]
                print(f"Removendo usuário ID: {id_usuario}...")
                
                # Remove o encoding do diretório
                sucesso = remover_encoding_por_id(id_usuario, ENCODINGS_DIR)
                
                if sucesso:
                    enviar_mensagem(ser, "usuario_removido")
                    print("Usuário removido com sucesso.")
                else:
                    enviar_mensagem(ser, "erro_remover_usuario")
                    print("Erro ao remover usuário.")

        # else:
        #     # Caso não haja comando ou seja um comando inválido, não faz nada
        #     # Mantém o loop aguardando novos comandos


# Ponto de entrada do programa
if __name__ == "__main__":
    fluxo_principal()
