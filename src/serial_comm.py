import serial
# Funções para comunicação serial com o ESP32
def configurar_serial(porta):
    return serial.Serial(porta, 115200, timeout=1)
# Função para ler comandos da porta serial
def ler_comando_serial(ser):
    if ser.in_waiting:
        msg = ser.readline().decode().strip()
        if msg:
            print(f"Comando recebido: {msg}")
        return msg
    return None
# Função para enviar mensagens via porta serial
def enviar_mensagem(ser, mensagem):
     if ser and ser.is_open:
        ser.write((mensagem+ '\n').encode('utf-8'))
 