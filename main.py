import cv2
import mediapipe as mp
import numpy as np
import pyautogui

# Inicializa o MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils


# Função para calcular a distância entre dois pontos
def calculate_distance(point1, point2):
    point1 = np.array(point1)
    point2 = np.array(point2)
    return np.linalg.norm(point1 - point2)


# Função para contar os dedos levantados
def count_fingers(hand_landmarks):
    fingers = []
    # IDs das pontas dos dedos: polegar, indicador, médio, anelar, mindinho
    finger_tips_ids = [
        mp_hands.HandLandmark.THUMB_TIP,
        mp_hands.HandLandmark.INDEX_FINGER_TIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP,
        mp_hands.HandLandmark.PINKY_TIP
    ]

    # Verifica se o polegar está levantado
    if hand_landmarks.landmark[finger_tips_ids[0]].x < hand_landmarks.landmark[finger_tips_ids[0] - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Verifica se os outros dedos estão levantados
    for id in range(1, 5):
        if hand_landmarks.landmark[finger_tips_ids[id]].y < hand_landmarks.landmark[finger_tips_ids[id] - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers


# Inicializa a captura de vídeo
cap = cv2.VideoCapture(0)

# Variáveis de controle de estado
controlling_mouse = False
clicking_left = False
clicking_right = False

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Converte a imagem para RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = hands.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Obtém as coordenadas das pontas do polegar e do indicador
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            thumb_tip_coords = [thumb_tip.x, thumb_tip.y]
            index_tip_coords = [index_tip.x, index_tip.y]

            # Calcula a distância entre o polegar e o indicador
            distance = calculate_distance(thumb_tip_coords, index_tip_coords)
            if distance < 0.05:  # Se a distância for menor que um limite, ativa o controle do mouse
                controlling_mouse = True
                clicking_left = False
                clicking_right = False
            else:
                controlling_mouse = False

            # Conta os dedos levantados
            fingers = count_fingers(hand_landmarks)

            if controlling_mouse:
                # Move o mouse conforme a posição do indicador
                screen_width, screen_height = pyautogui.size()
                x = int(index_tip.x * screen_width)
                y = int(index_tip.y * screen_height)
                pyautogui.moveTo(x, y)

            # Realiza um clique esquerdo se indicador e médio estiverem levantados (gesto "2")
            if fingers == [0, 1, 1, 0, 0]:
                clicking_left = True
                clicking_right = False
                controlling_mouse = False
            # Realiza um clique direito se todos os dedos, exceto o polegar, estiverem levantados (gesto "4")
            elif fingers == [0, 1, 1, 1, 1]:
                clicking_right = True
                clicking_left = False
                controlling_mouse = False

            # Executa o clique esquerdo
            if clicking_left:
                pyautogui.click(button='left')
            # Executa o clique direito
            elif clicking_right:
                pyautogui.click(button='right')

            # Desenha as landmarks da mão na imagem
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Mostra a imagem processada em uma janela
    cv2.imshow('Hand Mouse Control', image)

    # Encerra o programa se a tecla 'q' for pressionada
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Libera a captura de vídeo e fecha todas as janelas
cap.release()
cv2.destroyAllWindows()
