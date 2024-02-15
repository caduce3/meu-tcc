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

# Inicializar o detector de emoções
detector = FER(mtcnn=True)

# Inicializar a webcam
cap = cv2.VideoCapture(1)

# Configurar a porta serial
ser = serial.Serial('COM5', 9600)

# Encontrar o próximo número de arquivo disponível
file_number = 1

base_path = r'C:\Users\caduc\Documents\meuTcc\deteFace\apython-speaks\estudoParte2'
audio_inicial = os.path.join(base_path, 'entrada2.mp3')

pygame.mixer.init()
pygame.mixer.music.load(audio_inicial)
pygame.mixer.music.play()

# Função para processar a mensagem e acionar o Arduino
def processar_mensagem_arduino(message):
    if message == 'happy':
        ser.write('0'.encode())
    elif message == 'sad':
        ser.write('1'.encode())  
    elif message == 'angry':
        ser.write('2'.encode())
    elif message == 'fear':
        ser.write('3'.encode())
    elif message == 'disgust':
        ser.write('4'.encode())
    elif message == 'surprise':
        ser.write('5'.encode())
    elif message == 'neutral':
        ser.write('6'.encode())
    elif message == 'entrada':
        ser.write('9'.encode())
    else:
        print("Mensagem não reconhecida")

def reproduzir_piada(numero):
    audio_piada = os.path.join(base_path, f'emocoes_audios\\piadas\\piada{numero}.mp3')
    som_piada = pygame.mixer.Sound(audio_piada)
    som_piada.play()
    while pygame.mixer.get_busy():
        pygame.time.Clock().tick(10)

def processar_mensagem_audio(message):
    if message == 'happy' or message == 'surprise':
        audio = os.path.join(base_path, 'emocoes_audios', 'feliz', 'happyAudio.mp3')
        som = pygame.mixer.Sound(audio)
        som.play()
    elif message == 'sad':
        audio = os.path.join(base_path, 'emocoes_audios', 'sad', 'sadAudio.mp3')
        som = pygame.mixer.Sound(audio)
        som.play()
    elif message == 'angry' or message == 'disgust' or message == 'fear':
        audio = os.path.join(base_path, 'emocoes_audios', 'angry', 'angryAudio.mp3')
        som = pygame.mixer.Sound(audio)
        som.play()
    elif message == 'neutral':
        audio = os.path.join(base_path, 'emocoes_audios', 'neutral', 'neutralAudio.mp3')
        som = pygame.mixer.Sound(audio)
        som.play()
    else:
        print("Mensagem não reconhecida")

while os.path.exists(f"emotions_output_{file_number}.txt"):
    file_number += 1

# Abrir o arquivo de texto para salvar as taxas de emoções
output_file_path = f"emotions_output_{file_number}.txt"
output_file = open(output_file_path, "w")

detected_emotions = {'happy': 0, 'sad': 0, 'angry': 0, 'surprise': 0, 'neutral': 0, 'fear': 0, 'disgust': 0}
total_frames = 0

last_emotion1 = None
last_emotion2 = None
last_emotion3 = None
lista_de_emocoes = []

while True:
    # Ler um frame da webcam
    ret, frame = cap.read()

    if not ret:
        break

    # Detectar emoções no frame
    emotions = detector.detect_emotions(frame)
    print(emotions)

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

            
            processar_mensagem_arduino(emotion)
            
            if total_frames == 30:
                ser.write("9".encode())
                reproduzir_piada(1)
                ser.write("9".encode())
                
            if total_frames == 47:
                ser.write("9".encode())
                reproduzir_piada(2)
                ser.write("9".encode())
                
            elif total_frames == 65:  
                ser.write("9".encode())
                reproduzir_piada(3)
                ser.write("9".encode())
                

            # Após a reprodução da piada, usar a última emoção detectada
            if total_frames == 35:
                last_emotion1 = emotion
                lista_de_emocoes.append(last_emotion1)
                processar_mensagem_audio(last_emotion1)
            if total_frames == 52 :
                last_emotion2 = emotion
                processar_mensagem_audio(last_emotion2)
                lista_de_emocoes.append(last_emotion2)
            if total_frames == 73:
                last_emotion3 = emotion
                processar_mensagem_audio(last_emotion3)
                lista_de_emocoes.append(last_emotion3)

    # Exibir o frame com a detecção de emoção
    cv2.imshow('Webcam', frame)

    # Parar a execução se a tecla 'q' for pressionada
    if cv2.waitKey(1) & 0xFF == ord('w'):
        ser.write("9".encode())
        print(lista_de_emocoes)
        if lista_de_emocoes:
            most_common_emotion = max(set(lista_de_emocoes), key=lista_de_emocoes.count)
            print(f"Emoção mais frequente: {most_common_emotion}")

            # Play audio based on the most frequent emotion
            if most_common_emotion == 'happy' or most_common_emotion == 'surprise':
                audio = os.path.join(base_path, 'emocoes_audios', 'mais-happy.mp3')
                som = pygame.mixer.Sound(audio)
                som.play()
            elif most_common_emotion == 'sad':
                audio = os.path.join(base_path, 'emocoes_audios', 'mais-triste.mp3')
                som = pygame.mixer.Sound(audio)
                som.play()
            elif most_common_emotion == 'angry' or most_common_emotion == 'disgust' or most_common_emotion == 'fear':
                audio = os.path.join(base_path, 'emocoes_audios', 'mais-raiva.mp3')
                som = pygame.mixer.Sound(audio)
                som.play()
            elif most_common_emotion == 'neutral':
                audio = os.path.join(base_path, 'emocoes_audios', 'mais-neutro.mp3')
                som = pygame.mixer.Sound(audio)
                som.play()
            else:
                print("Emoção não reconhecida")
        else:
            print("Lista de emoções vazia.")
        time.sleep(8)
        break



# Fechar o arquivo de texto
output_file.close()

# Liberar a webcam e fechar a janela
cap.release()
cv2.destroyAllWindows()


print(f"As taxas de emoções foram salvas em {output_file_path}")
