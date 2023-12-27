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

def processar_mensagem(message):
    
    if message == "1":
        # print("O usuário acertou")
        
        if detected_emotion == 'angry':
            ser.write('2'.encode())
             
    
    elif message == "0":
        # print("O roboldo errou")
        
        if detected_emotion == 'sad':
            ser.write('1'.encode())
        
    
    elif message == "2":
        # print("O roboldo acertou")
        
        if detected_emotion == 'happy':
            ser.write('0'.encode())
    
    elif message == "3":
        # print("O jogador venceu")
        
        if detected_emotion == 'sad':
            ser.write('1'.encode())
    
    elif message == "4":
         # print("O Roboldo venceu")
        
        if detected_emotion == 'happy':
            ser.write('0'.encode())
    
    elif message == "5":
         # print("EMPATE")
        
        if detected_emotion == 'surprise':
            ser.write('5'.encode())
    
    elif message == 'inicio':
        ser.write('6'.encode())
        
    
    else:
        print("Mensagem não reconhecida")

    # if message in ["0", "1", "2", "3", "4", "5", "inicio"]:
    #     sound = pygame.mixer.Sound(audio_file)
    #     sound.play()
    #     pygame.time.wait(int(sound.get_length() * 1000))
    # else:
    #     print("Mensagem não reconhecida")


def detectar_emocoes():
    # Inicializar o detector de emoções
    detector = FER(mtcnn=True)

    # Inicializar a webcam
    cap = cv2.VideoCapture(0)

    # Encontrar o próximo número de arquivo disponível
    file_number = 1
    while os.path.exists(f"emotions_output_{file_number}.txt"):
        file_number += 1

    # Abrir o arquivo de texto para salvar as taxas de emoções
    output_file_path = f"emotions_output_{file_number}.txt"
    output_file = open(output_file_path, "w")

    detected_emotions = {'happy': 0, 'sad': 0, 'angry': 0, 'surprise': 0, 'neutral': 0, 'fear': 0, 'disgust': 0}
    total_frames = 0

    emotion_detected = None

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
                emotion_detected = emotion
            return emotion_detected
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

HOST = 'localhost'
PORT = 3005

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print('Aguardando conexões...')

    while True:
        conn, addr = server_socket.accept()
        print('Conectado por', addr)
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                message = data.decode('utf-8')
                print('Recebido:', message)
                processar_mensagem(message)
                detected_emotion = detectar_emocoes()

                