from src.serial_comm import configurar_serial, ler_comando_serial, enviar_mensagem
from src.camera import detectar_rosto_continuo
from src.encoding import carregar_encodings, salvar_encoding
from src.recognition import comparar_com_base

from config.settings import SERIAL_PORT, ENCODINGS_DIR


def fluxo_principal():
    ser = configurar_serial(SERIAL_PORT)
    print("Sistema de reconhecimento iniciado. Aguardando comandos...")

    while True:
        comando = ler_comando_serial(ser)

        if comando and comando.startswith("tirar_foto|"):
            partes = comando.split("|")
            if len(partes) == 3:
                id_usuario, nome_usuario = partes[1], partes[2]
                print(f"Iniciando cadastro de {nome_usuario} (ID: {id_usuario})...")
                enviar_mensagem(ser, "cadastro_iniciado")
                sucesso = salvar_encoding(id_usuario, nome_usuario, ENCODINGS_DIR)
                enviar_mensagem(ser, "cadastro_finalizado" if sucesso else "erro_foto")

        elif comando and comando == "iniciar_reconhecimento_facial":
            print("Reconhecimento facial solicitado pelo ESP32.")
            frame = detectar_rosto_continuo(duracao_minima=2.0, mostrar_camera=False)
            if frame is not None:
                encodings, nomes, ids = carregar_encodings(ENCODINGS_DIR)
                nome, id_usuario = comparar_com_base(frame, encodings, nomes, ids)
                if nome != "Desconhecido":
                    enviar_mensagem(ser, f"face_detectada:{id_usuario}")
                    print(f"Face detectada: {nome} (ID: {id_usuario})...")
                else:
                    enviar_mensagem(ser, "face_nao_reconhecida")
                    print("Rosto não reconhecido.")
            else:
                enviar_mensagem(ser, "face_nao_reconhecida")
                print("Nenhum rosto detectado.")

        # else: 
        #     # Não faz nada, apenas aguarda comandos

if __name__ == "__main__":
    fluxo_principal()