import cv2

detector_face = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')

capturar = cv2.VideoCapture('http://192.168.1.80:81/stream') #id da minha camera
# videoSaida = cv2.VideoWriter('videoFinal.avi', cv2.VideoWriter_fourcc(*'XVID'), 20, (640, 480))

capturar.set(cv2.CAP_PROP_FRAME_WIDTH, 640) #tam da captura (lembrar de verificar se minha camera aceita)
capturar.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
capturar.set(cv2.CAP_PROP_FPS, 24)

while True:
    #Ler a imagem
    ret, imagem = capturar.read()
    if(ret != None):

        #Converter para cinza
        cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        

        #Detectar faces
        faces = detector_face.detectMultiScale(cinza, scaleFactor=1.1, minNeighbors=10)

        #Desenhar o retangulo nas faces
        for (x, y, l, a) in faces:
            cv2.rectangle(imagem, (x, y), (x + l, y + a), (0, 0, 255), 2)

        #Mostrar a imagem
        cv2.imshow('Camera ESP32cam', imagem)

        # videoSaida.write(imagem)

        #Parar o programa quando apertar a tecla 'q'
        if cv2.waitKey(1) == ord('q'):
            break