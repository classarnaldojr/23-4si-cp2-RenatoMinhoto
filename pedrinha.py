import cv2

import numpy as np

import matplotlib.pyplot as plt

#Pegando o vídeo
cap = cv2.VideoCapture('pedra-papel-tesoura.mp4')

pontos_jogador1 = 0
pontos_jogador2 = 0
previous_moves = []

res = ""

while True:

    #Lendo os frames do vídeo
    ret, frame = cap.read()

    foto = frame.copy() #Copio o frame para fazer outro retorno

    #Aplicando filtro de cinza
    img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #Aplicando suavização na imagem
    img = cv2.blur(img_hsv, (15, 15), 0)

    #Criando os ranges para as mascáras HSV
    hsv_low1 = np.array([0, 20, 10])
    hsv_up1 = np.array([18, 200, 200])
    hsv_low2 = np.array([0, 1, 1])
    hsv_up2 = np.array([255, 150, 250])

    #Criando as mascaras
    mask1 = cv2.inRange(img, hsv_low1, hsv_up1)
    mask2 = cv2.inRange(img, hsv_low2, hsv_up2)

    #Juntando as mascaras
    img_filtro = cv2.bitwise_or(mask1, mask2)

    #Encontrando os contornos da imagem
    contours, _ = cv2.findContours(img_filtro, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #Desenhando os contornos
    cv2.drawContours(foto, contours, -1, [0, 255, 0], 5)

    #Criando listas de contornos de acordo com a posição encontrada para identificar os Jogador 1 e 2
    c1 = contours[1]
    c2 = contours[0]

    #Pegando os momentos dos contornos para pegar a área
    m1 = cv2.moments(c1)
    m2 = cv2.moments(c2)
    

    #Pegando as áreas dos contornos (mãos dos jogadores)
    area1 = int(m1['m00'])
    area2 = int(m2['m00'])

    # Lógica para definir os tipos de objeto de acordo com sua área total (Jogador 1)
    if area1 < 58000:
        area1 = "Tesoura"

    elif area1 > 58000 and area1 < 70000:
        area1 = "Pedra"

    elif area1 > 70000:
        area1 = "Papel"

    # Lógica para definir os tipos de objeto de acordo com sua área total (Jogador 2)
    if area2 < 58000:
        area2 = "Tesoura"

    elif area2 > 58000 and area2 < 70000:
        area2 = "Pedra"

    elif area2 > 70000:
        area2 = "Papel"

    #Inversão para uma Das Detecções que foram processadas invertidas
    if area1 == "Pedra" and area2 == "Tesoura":
        area1 = "Tesoura"
        area2 = "Pedra"

    if len(previous_moves) == 0:
        if area1 == area2:
            res = "Draw!"
            previous_moves.append((area1, area2))
        elif (area1 == "Tesoura" and area2 == "Papel"):
                res = "Jogador 1 Ganhou!"
                pontos_jogador1 = pontos_jogador1 + 1
                previous_moves.append((area1, area2))
        elif (area1 == "Papel" and area2 == "Tesoura"):
            res = "Jogador 2 Ganhou!"
            pontos_jogador2 = pontos_jogador2 + 1
            previous_moves.append((area1, area2))
        elif (area1 == "Pedra" and area2 == "Tesoura"):
            res = "Jogador 1 Ganhou!"
            pontos_jogador1 = pontos_jogador1 + 1
            previous_moves.append((area1, area2))
        elif (area1 == "Tesoura" and area2 == "Pedra"):
            res = "Jogador 2 Ganhou!"
            pontos_jogador2 = pontos_jogador2 + 1
            previous_moves.append((area1, area2))
        elif (area1 == "Papel" and area2 == "Pedra"):
            res = "Jogador 1 Ganhou!"
            pontos_jogador1 = pontos_jogador1 + 1
            previous_moves.append((area1, area2))
        elif (area1 == "Pedra" and area2 == "Papel"):
            res = "Jogador 2 Ganhou!"
            pontos_jogador2 = pontos_jogador2 + 1
            previous_moves.append((area1, area2))
    else:
        if (area1, area2) != previous_moves[-1]:
            # atualizar as pontuações de acordo com a jogada atual
            if area1 == area2:
                res = "Empate!"
                previous_moves.append((area1, area2))
            elif (area1 == "Tesoura" and area2 == "Papel"):
                res = "Jogador 1 Ganhou!"
                pontos_jogador1 = pontos_jogador1 + 1
                previous_moves.append((area1, area2))
            elif (area1 == "Papel" and area2 == "Tesoura"):
                res = "Jogador 2 Ganhou!"
                pontos_jogador2 = pontos_jogador2 + 1
                previous_moves.append((area1, area2))
            elif (area1 == "Pedra" and area2 == "Tesoura"):
                res = "Jogador 1 Ganhou!"
                pontos_jogador1 = pontos_jogador1 + 1
                previous_moves.append((area1, area2))
            elif (area1 == "Tesoura" and area2 == "Pedra"):
                res = "Jogador 2 Ganhou!"
                pontos_jogador2 = pontos_jogador2 + 1
                previous_moves.append((area1, area2))
            elif (area1 == "Papel" and area2 == "Pedra"):
                res = "Jogador 1 Ganhou!"
                pontos_jogador1 = pontos_jogador1 + 1
                previous_moves.append((area1, area2))
            elif (area1 == "Pedra" and area2 == "Papel"):
                res = "Jogador 2 Ganhou!"
                pontos_jogador2 = pontos_jogador2 + 1
                previous_moves.append((area1, area2))

    #Título
    (cv2.putText(foto, "Prepare-se para o Pedra, Papel, Tesoura!",(265, 50), cv2.FONT_HERSHEY_DUPLEX,2, (0, 0, 0), 2, cv2.LINE_AA))

    #Jogada do Jogador 1
    (cv2.putText(foto, ("Jogador 1: " + str(area1)), (150, 850), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 0), 2, cv2.LINE_AA))
    
    #Jogada do Jogador 2
    (cv2.putText(foto, ("Jogador 2: " + str(area2)), (1150, 850), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 0), 2, cv2.LINE_AA))
    
    #Resultado da Rodada
    (cv2.putText(foto, str(res), (650, 1000), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 0), 2, cv2.LINE_AA))
    
    #Pontuação do Jogador 1
    (cv2.putText(foto, ("Pontos Jogador 1 = " + str(pontos_jogador1)), (150, 150), cv2.FONT_HERSHEY_DUPLEX, 2,(0, 0, 255), 2, cv2.LINE_AA))
    
    # Pontuação do Jogador 2
    (cv2.putText(foto,("Pontos Jogador 2 = " + str(pontos_jogador2)), (1050, 150), cv2.FONT_HERSHEY_DUPLEX, 2,(0, 0, 255), 2, cv2.LINE_AA))
    
    #Criando as janelas de output
    frame = cv2.resize(img_filtro, (640, 480))
    img_final = cv2.resize(foto, (640, 480))

    #Mostrando as janelas
    cv2.imshow("Detecção", frame)

    cv2.imshow("Jogo", img_final)

    #Finalizar o programa apertando a tecla Q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if not ret:
        break

#Printando os momentos dos contornos (ajudou a decidir como fazer a lógica para identificar os tipos dos objetos)
print(m1)
print(m2)    

cap.release()

cv2.destroyAllWindows()