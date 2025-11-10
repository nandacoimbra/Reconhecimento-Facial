import cv2 # type: ignore
import face_recognition # type: ignore

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
    for idx_enc, encoding in enumerate(encodings):
        # Compara o encoding atual com todos os encodings já cadastrados
        matches = face_recognition.compare_faces(encodings_conhecidos, encoding)
        # Se encontrar pelo menos uma correspondência (match True)
        if True in matches:
            # Pega o índice do primeiro match encontrado
            idx = matches.index(True)
            # Recupera a localização correspondente (em coordenadas da imagem reduzida)
            top, right, bottom, left = localizacoes[idx_enc]
            # Converte para coordenadas do frame original (multiplica pelo fator de redução)
            scale = 4
            top_o, right_o, bottom_o, left_o = top * scale, right * scale, bottom * scale, left * scale
            # Retorna o nome, ID e localização no frame original
            return nomes_conhecidos[idx], ids_conhecidos[idx], (top_o, right_o, bottom_o, left_o)
    # Se nenhum rosto foi reconhecido, retorna valores padrão
    return "Desconhecido", "?", None

# Desenha um retângulo ao redor do rosto e adiciona o nome e ID abaixo para salvar a imagem de acesso
def desenha_retangulo_e_nome(frame, top, right, bottom, left, nome, id_usuario):
    # Desenha um retângulo ao redor do rosto
    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
    # Adiciona o nome e ID abaixo do retângulo
    cv2.putText(frame, f"{nome} (ID: {id_usuario})", (left, bottom + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)