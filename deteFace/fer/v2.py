from fer import FER
import cv2
import pandas as pd
import os

# Inicializar o detector de emoções
detector = FER(mtcnn=False)

# Inicializar a webcam
cap = cv2.VideoCapture(0)

# Lista para armazenar as emoções detectadas
detected_emotions = []

while True:
    # Ler um frame da webcam
    ret, frame = cap.read()

    if not ret:
        break

    # Detectar emoções no frame
    emotions = detector.detect_emotions(frame)

    # Adicionar emoções detectadas à lista
    if emotions:
        detected_emotions.extend(emotions)

    # Exibir a emoção detectada na imagem
    if emotions:
        for face in emotions:
            x, y, w, h = face['box']
            emotion = max(face['emotions'], key=face['emotions'].get)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    # Exibir o frame com a detecção de emoção
    cv2.imshow('Cam ESP32', frame)

    # Parar a execução se a tecla 'q' for pressionada
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar a webcam e fechar a janela
cap.release()
cv2.destroyAllWindows()

# Calcular a emoção mais predominante durante o reconhecimento
if detected_emotions:
    emotions_df = pd.DataFrame(detected_emotions)
    most_common_emotion = emotions_df['emotions'].mode()

    if not most_common_emotion.empty:
        most_common_emotion_str = most_common_emotion.to_string(index=False)

        # Salvar a emoção mais predominante no arquivo de texto (usando um caminho absoluto)
        file_path = os.path.abspath("C:\\Users\\caduc\\Documents\\meu-tcc\\deteFace\\fer\\emotions.txt")
        with open(file_path, 'w') as f:
            f.write(most_common_emotion_str)
    else:
        print("Nenhuma emoção predominante detectada.")
else:
    print("Nenhuma emoção detectada.")
