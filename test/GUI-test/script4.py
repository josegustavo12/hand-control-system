import cv2
import mediapipe as mp
import numpy as np
import pyautogui

THR = 0.1
WRIST_THR = 0.2

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

def get_last_k_valid_readings(prev_results, k):
    valid_readings = []

    for result in reversed(prev_results):
        # pega os pontos de referencia das mãos (landmarks)
        hand_landmarks = get_hand_landmarks(result)
        # se os pontos forem validos, add na lista
        if hand_landmarks:
            valid_readings.append(hand_landmarks)
        #para dps de k leituras
        if len(valid_readings) == k:
            break

    return valid_readings

def perform_click(action):
    if action == 'left_click':
        button = 'left'
    else:
        button = 'right'
        
    pyautogui.click(button=button)
    print("{} clicked".format(button))

def move_mouse(curr_landmarks, prev_landmarks, image_height, image_width):
    # coordenadas atuais
    curr_x, curr_y = get_coords(curr_landmarks, 8)
    # coordenadas anteriores
    prev_x, prev_y = get_coords(prev_landmarks, 8) 

    diff_x = curr_x - prev_x # calculo da diferença em x
    diff_y = curr_y - prev_y # calculo da diferença em y
    
    sensitivity_factor = 0.5 # sensibilidade do mouse
    # calcula o movimento no eixo x/y do mouse, multiplicando as coordenadas pela largura da imagem e pela sensibilidade
    move_x = int(diff_x * image_width * sensitivity_factor) 
    move_y = int(diff_y * image_height * sensitivity_factor)
    # função do pyautogui que move o mouse
    pyautogui.moveRel(move_x, move_y, duration=0.2)
   
    print('Mouse moved')

def scroll_mouse(curr_landmarks, prev_landmarks):
    # obtem as coordenadas atuais e anteriores do eixo y
    curr_y = get_coords(curr_landmarks, 8)[1] 
    prev_y = get_coords(prev_landmarks, 8)[1]

    # calcula a diferença da atual e da anterior
    diff = curr_y - prev_y
    sensitivity_factor = 0.01 # sensibilidade do scroll

    if abs(diff) >= sensitivity_factor:
        pyautogui.scroll(100 * diff) # movimento do scroll
        print('scrolled')

def get_coords(landmarks, idx):
    x = landmarks.landmark[idx].x # objeto (landmarks), atributo (landmark) e indice da coordenada x
    y = landmarks.landmark[idx].y
    return x, y # retorna uma tupla com as coordenadas

def compute_distance_matrix(hand_landmarks):

    coords = []

    for lm in hand_landmarks.landmark: # itera sobre cada landmark

        coords.append((lm.x, lm.y, lm.z)) # add esses pontos no coords

    coords = np.array(coords) 

    diff_vectors = coords[:, np.newaxis] - coords # calcula o vetor diferença de todos os pontos 

    # a np.linalg.norm é usada para calcular a norma euclidiana da matriz (dois pontos em um espaço tridimensional)
    distance_matrix = np.linalg.norm(diff_vectors, axis=2)

    # cada pontos (i,j) da matriz representa a distancia entre o ponto i e o ponto j
    return distance_matrix

def get_hand_landmarks(results):

    if not results.multi_handedness: # verifica se tem +1 mão
        return None
    
    for hand in results.multi_handedness: # itera sobre as lateralidades

        if hand.classification[0].label == 'Right': # verifica se é direita

            return results.multi_hand_landmarks[results.multi_handedness.index(hand)] # retorna os pontos de referencia da mão direita
        elif hand.classification[0].label == 'Left':
            return results.multi_hand_landmarks[results.multi_handedness.index(hand)]
    
    
    return None # retorna nada caso não veja mão

def recognize_gesture(hand_landmarks):
    dist_m = compute_distance_matrix(hand_landmarks)
    
    # calcula a distancia entre pontos especificos 
    thumb_idx_dist = dist_m[4, 8]
    mid_idx_dist = dist_m[8, 12]
    wrist_ring_dist = dist_m[0, 16]
    wrist_mid_dist = dist_m[0, 12]
    wrist_pinky_dist = dist_m[0, 20]
    base_idx_thumb_dist = dist_m[4, 5]
    
    # Coordenadas y dos pontos de referência da mão
    y_coords = []
    for lm in hand_landmarks.landmark:
        y_coords.append(lm.y)
    y_coords = np.array(y_coords)


    # mover o mouse
    if (y_coords[12] - y_coords[6] > THR and y_coords[16] - y_coords[6] > THR and 
        y_coords[20] - y_coords[6] > THR and base_idx_thumb_dist <= THR and 
        y_coords[8] - y_coords[6] < THR):
        return 'mouse_move'
    
    # clicar com o botão esquerdi
    elif thumb_idx_dist <= THR and mid_idx_dist > THR and wrist_ring_dist > WRIST_THR and wrist_mid_dist > WRIST_THR and wrist_pinky_dist > WRIST_THR:
        return 'left_click'
    
    # clicar com o botão direito
    elif (y_coords[15] - y_coords[6] < THR and dist_m[4, 12] < THR and y_coords[15] - y_coords[12] < THR and 
          y_coords[18] - y_coords[12] < THR and y_coords[19] - y_coords[6] < THR and y_coords[15] - y_coords[6] < THR and 
          y_coords[12] - y_coords[14] > THR and y_coords[12] - y_coords[19] > THR):
        return 'right_click'
    
    # scroll
    elif (y_coords[12] - y_coords[14] < THR and y_coords[16] - y_coords[6] > THR and 
          y_coords[20] - y_coords[6] > THR and base_idx_thumb_dist <= THR and 
          y_coords[8] - y_coords[6] < THR and y_coords[12] - y_coords[6] < THR):
        return 'scroll'
    
    return None # caso nenhum gesto seja reconhecido

prev_res = [] # resultados anteriores 
cap = cv2.VideoCapture(0)

while cap.isOpened():

    ret, frame = cap.read()
    
    if not ret:
        print("Ignoring empty camera frame.")
        continue

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    image_height, image_width, _ = frame.shape

    results = hands.process(frame_rgb) # processa os resultados da detecção da mão
    
    if results.multi_handedness:

        curr_landmarks = get_hand_landmarks(results) # pontos de referencia atuais
        
        if curr_landmarks:
            # cria a ação/gesto com base nos pontos de referencia
            action = recognize_gesture(curr_landmarks)
            
            if action and len(prev_res) >= 5:

                prev_landmarks = get_last_k_valid_readings(prev_res, 5)[0] # referencia das ultimas 5 detecções válidas (aplicação do filtro)
                
                if action == 'left_click':
                    perform_click(action)
                elif action == 'right_click':
                    perform_click(action)
                elif action == 'mouse_move':
                    move_mouse(curr_landmarks, prev_landmarks, image_height, image_width)
                elif action == 'scroll':
                    scroll_mouse(curr_landmarks, prev_landmarks)
            
            prev_res.append(results) # add os resultados anteriores
            if len(prev_res) > 10: # limite de tamanho para 10
                prev_res = prev_res[-10:]
            # para evitar de crescer infinito e deixar o codigo mais lento
    
    frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
    
    if results.multi_hand_landmarks: # desenha os landmarks
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame_bgr, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Hand Control System", frame_bgr)

    if cv2.waitKey(10) & 0xFF == ord('q'): # sair = q
        break

cap.release()
cv2.destroyAllWindows()
hands.close()