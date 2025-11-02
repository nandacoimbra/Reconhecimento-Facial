import cv2
import face_recognition

# Função que compara um frame da câmera com a base de encodings já cadastrados
def comparar_com_base(frame, encodings_conhecidos, nomes_conhecidos, ids_conhecidos):
    # Reduz a imagem para 1/4 do tamanho original (acelera o processamento)
    pequena = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    
    # Converte de BGR (padrão OpenCV) para RGB (padrão da biblioteca face_recognition)
    rgb = cv2.cvtColor(pequena, cv2.COLOR_BGR2RGB)
    
    # Localiza os rostos presentes na imagem (mesmo que tenha mais de um)
    localizacoes = face_recognition.face_locations(rgb)
    
    # Gera os encodings (representação matemática única de cada rosto detectado)
    encodings = face_recognition.face_encodings(rgb, localizacoes)

    # Para cada rosto detectado, compara com os encodings conhecidos
    for encoding in encodings:
        # Compara o encoding atual com todos os encodings já cadastrados
        matches = face_recognition.compare_faces(encodings_conhecidos, encoding)
        
        # Se encontrar pelo menos uma correspondência (match True)
        if True in matches:
            # Pega o índice do primeiro match encontrado
            idx = matches.index(True)
            
            # Retorna o nome e ID do usuário correspondente
            return nomes_conhecidos[idx], ids_conhecidos[idx]
    
    # Se nenhum rosto foi reconhecido, retorna valores padrão
    return "Desconhecido", "?"
