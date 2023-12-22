from fer import FER
import cv2
import tensorflow as tf
import datetime
import os
import socket
import pygame
import random
import serial
import time

pygame.mixer.init()

# Caminho absoluto para o diretório dos arquivos de áudio C2
audio_directory = r'C:\Users\caduc\Documents\meuTcc\deteFace\apython-speaks'


# Função para processar a mensagem e acionar o Arduino
def processar_mensagem(message):
    audio_file = None
    base_path = r'C:\Users\caduc\Documents\meuTcc\deteFace\apython-speaks'
    
    if message == 'happy':
        ser.write('0'.encode())
        audio_file = os.path.join(base_path, 'happy', 'happy1.mp3')   
    elif message == 'sad':
        ser.write('1'.encode())  
        audio_file = os.path.join(base_path, 'sad', 'sad1.mp3')  
    elif message == 'angry':
        ser.write('2'.encode())
        audio_file = os.path.join(base_path, 'angry', 'raiva1.mp3')  
    elif message == 'fear':
        ser.write('3'.encode())
        audio_file = os.path.join(base_path, 'fear', 'fear1.mp3')  
    elif message == 'disgust':
        ser.write('4'.encode())
        audio_file = os.path.join(base_path, 'disgust', 'disgust.mp3')  
    elif message == 'surprise':
        ser.write('5'.encode())
        audio_file = os.path.join(base_path, 'surprise', 'surprise1.mp3')  
    elif message == 'neutral':
        ser.write('6'.encode())
        #audio_file = os.path.join(r'C:\Users\caduc\Documents\meuTcc\deteFace\apython-\neutral', 'happy1.mp3')  
    else:
        print("Mensagem não reconhecida")

    if audio_file is not None and message in ["happy", "sad", "angry", "fear", "disgust", "surprise", "neutral"]:
        sound = pygame.mixer.Sound(audio_file)
        sound.play()
        pygame.time.wait(int(sound.get_length() * 1000))

        time.sleep(5)

# Inicializar o detector de emoções
detector = FER(mtcnn=True)

# Inicializar a webcam
cap = cv2.VideoCapture(0)

# Configurar a porta serial
ser = serial.Serial('COM5', 9600)

# Encontrar o próximo número de arquivo disponível
file_number = 1
while os.path.exists(f"emotions_output_{file_number}.txt"):
    file_number += 1

# Abrir o arquivo de texto para salvar as taxas de emoções
output_file_path = f"emotions_output_{file_number}.txt"
output_file = open(output_file_path, "w")

detected_emotions = {'happy': 0, 'sad': 0, 'angry': 0, 'surprise': 0, 'neutral': 0, 'fear': 0, 'disgust': 0}
total_frames = 0

while True:
    # Ler um frame da webcam
    ret, frame = cap.read()

    if not ret:
        break

    # Detectar emoções no frame
    emotions = detector.detect_emotions(frame)

    if emotions:
        total_frames += 1
        for face in emotions:
            x, y, w, h = face['box']
            emotion = max(face['emotions'], key=face['emotions'].get)
            detected_emotions[emotion] += face['emotions'][emotion]

            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

            # Salvar a taxa de emoção no arquivo de texto
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            output_line = f"{timestamp}: {emotion} - {face['emotions'][emotion]}\n"
            output_file.write(output_line)

            # Processar a mensagem e acionar o Arduino
            processar_mensagem(emotion)

    # Exibir o frame com a detecção de emoção
    cv2.imshow('Webcam', frame)

    # Parar a execução se a tecla 'q' for pressionada
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Calcular a média das taxas de emoção
average_emotions = {emotion: rate / total_frames for emotion, rate in detected_emotions.items()}

# Salvar a média das taxas de emoção no arquivo de texto
output_file.write("\n\nMedia das Taxas de Emocao:\n")
for emotion, average_rate in average_emotions.items():
    output_file.write(f"{emotion}: {average_rate}\n")

# Fechar o arquivo de texto
output_file.close()

# Liberar a webcam e fechar a janela
cap.release()
cv2.destroyAllWindows()

print(f"As taxas de emoções foram salvas em {output_file_path}")
