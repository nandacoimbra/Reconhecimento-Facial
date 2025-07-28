import serial

def configurar_serial(porta):
    return serial.Serial(porta, 115200, timeout=1)

def ler_comando_serial(ser):
    if ser.in_waiting:
        msg = ser.readline().decode().strip()
        if msg:
            print(f"Comando recebido: {msg}")
        return msg
    return None

def enviar_mensagem(ser, mensagem):
     if ser and ser.is_open:
        ser.write((mensagem+ '\n').encode('utf-8'))
