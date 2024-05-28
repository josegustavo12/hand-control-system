# Contagem de Dedos Usando MediaPipe Holistic

Este exemplo de código mostra como usar o MediaPipe Holistic para detectar e rastrear landmarks de pose, mãos e rosto em tempo real, utilizando a biblioteca OpenCV para captura e exibição de vídeo.

## Importações e Inicializações

```python
import cv2
import mediapipe as mp
```

## Inicialização do Módulo MediaPipe Holistic
```python
mp_holistic = mp.solutions.holistic
holistic = mp_holistic.Holistic(
    static_image_mode=False,         # Para vídeos em tempo real
    model_complexity=1,              # Complexidade média do modelo
    smooth_landmarks=True,           # Suavização temporal dos landmarks
    min_detection_confidence=0.5,    # Confiança mínima para a detecção inicial
    min_tracking_confidence=0.5      # Confiança mínima para o rastreamento
)
```
Os valores podem ser modificados a depender do problema
```python
mp_holistic = mp.solutions.holistic
holistic = mp_holistic.Holistic(
    static_image_mode=True,     # Para Imagens estáticass
    model_complexity=2,     # Aumenta a complexidade do modelo e melhora a precisão, mas aumenta muito o lag
)

```

## Inicialização do módulo MediaPipe Drawing
```python
mp_drawing = mp.solutions.drawing_utils
```
Será utilizado para desenhar as LandMarks

## Função "count_fingers"
```python
def count_fingers(hand_landmarks):

    # Lista com os pontos mais altos de cada dedo 
    fingers_tips = [
        mp_holistic.HandLandmark.INDEX_FINGER_TIP,
        mp_holistic.HandLandmark.MIDDLE_FINGER_TIP,
        mp_holistic.HandLandmark.RING_FINGER_TIP,
        mp_holistic.HandLandmark.PINKY_TIP
    ]
    
    fingers_folded = 0
    
    for tip_id in fingers_tips:
        finger_tip = hand_landmarks.landmark[tip_id]
        finger_dip = hand_landmarks.landmark[tip_id - 2] 

        # Se a coordenada y do tip estiver acima da do dip, o dedo está levantado
        if finger_tip.y < finger_dip.y:
            fingers_folded += 1
    
    # Verificação do polegar
    thumb_tip = hand_landmarks.landmark[mp_holistic.HandLandmark.THUMB_TIP]
    thumb_ip = hand_landmarks.landmark[mp_holistic.HandLandmark.THUMB_IP]

    # Se a coordenada x do tip estiver à esquerda (ou à direita, dependendo da mão) da do IP, o polegar está levantado
    if hand_landmarks.landmark[mp_holistic.HandLandmark.WRIST].x > thumb_tip.x > thumb_ip.x:
        fingers_folded += 1

    return fingers_folded
```
![Hand landmarks](./hand_landmarks.png)

A ideia do código é que quando a coordenada Y do TIP estiver maior que a coordenada Y do DIP o dedo está levantado

# Processamento com o modelo Holistic
```python
results = holistic.process(frame_rgb)
```

Guarda os valores dos frames na variavel results

# Desenho das Landmarks e Contagem dos dedos
```python
    if results.right_hand_landmarks:
        mp_drawing.draw_landmarks(frame, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        fingers_count = count_fingers(results.right_hand_landmarks)
        cv2.putText(frame, f'Fingers: {fingers_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    if results.left_hand_landmarks:
        mp_drawing.draw_landmarks(frame, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        fingers_count = count_fingers(results.left_hand_landmarks)
        cv2.putText(frame, f'Fingers: {fingers_count}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

```
- `if`:
    - serve para verificar se é a mão esquerda ou direita
- `mp_drawing.draw_landmarks(frame, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)`:
    - Desenha os Landmarks da mão direita
- `fingers_count = count_fingers(results.right_hand_landmarks)`: 
    - conta os dedos levantados da mão direita.
- `cv2.putText(frame, f'Fingers: {fingers_count}', (10, 30), cv2.FONT_HERSH EY_SIMPLEX, 1, (0, 255, 0), 2)`: 
    -  imprime o texto com o número de dedos levantados na imagem.

Funciona da mesma forma para a esquerda

## Explicação básica de como funciona o countfingers com o mediapipe 
### Objetivos futuros:
- Aplicar no projeto Geral de HANDCONTROL
- Melhorar a contagem com o uso das duas mão numa contagem maior (até 10 numeros)
- melhorar um pouco o código para que fique mais otimizado 