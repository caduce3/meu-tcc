from fer import FER
import cv2
import tensorflow as tf

# Inicializar o detector de emoções
detector = FER(mtcnn=False)

#Inicializar a camera do esp32 cam
#cap = cv2.VideoCapture('http://172.16.0.42:81/stream')
cap = cv2.VideoCapture(0)

# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640) #tam da captura (lembrar de verificar se minha camera aceita)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
# cap.set(cv2.CAP_PROP_FPS, 10)
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
