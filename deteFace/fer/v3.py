from fer import FER
import cv2
import tensorflow as tf
import datetime
import os

# Inicializar o detector de emoções
detector = FER(mtcnn=False)

# Inicializar a webcam
cap = cv2.VideoCapture(0)

# Encontrar o próximo número de arquivo disponível
file_number = 1
while os.path.exists(f"emotions_output_{file_number}.txt"):
    file_number += 1

# Abrir o arquivo de texto para salvar as taxas de emoções
output_file_path = f"emotions_output_{file_number}.txt"
output_file = open(output_file_path, "w")

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

            # Salvar a taxa de emoção no arquivo de texto
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            output_line = f"{timestamp}: {emotion} - {face['emotions'][emotion]}\n"
            output_file.write(output_line)

    # Exibir o frame com a detecção de emoção
    cv2.imshow('Webcam', frame)

    # Parar a execução se a tecla 'q' for pressionada
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Fechar o arquivo de texto
output_file.close()

# Liberar a webcam e fechar a janela
cap.release()
cv2.destroyAllWindows()

print(f"As taxas de emoções foram salvas em {output_file_path}")
