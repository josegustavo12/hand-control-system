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

## Função "calculate_distance":
```python
def calculate_distance(point1, point2):
    return math.sqrt((point2.x - point1.x) ** 2 + (point2.y - point1.y) ** 2)
```
Essa função calcula a distância euclidiana entre dois pontos no espaço 2D.

## Função "normalized_to_pixel_coordinates":
Essa função facilita a transição entre as coordenadas normalizadas, que variam de 0 a 1 e são usadas pelo MediaPipe Holistic para representar posições na imagem, e as coordenadas em pixels, que são usadas para desenhar os landmarks na imagem e realizar cálculos de distância, como visto no restante do código.

```python
def normalized_to_pixel_coordinates(normalized_landmark, image_width, image_height):
    return int(normalized_landmark.x * image_width), int(normalized_landmark.y * image_height)
```
1. **Entrada de Parâmetros:**
   - A função recebe três parâmetros:
     - `normalized_landmark`: as coordenadas normalizadas do landmark (ponto) que queremos converter.
     - `image_width`: a largura da imagem em pixels.
     - `image_height`: a altura da imagem em pixels.

2. **Cálculo das Coordenadas em Pixels:**
   - Para converter as coordenadas normalizadas para pixels, multiplicamos as coordenadas normalizadas pelas dimensões correspondentes da imagem.
   - Isso é feito multiplicando o valor normalizado de x pela largura da imagem e o valor normalizado de y pela altura da imagem.
   - Essa multiplicação nos dá as coordenadas do landmark em pixels na imagem.

3. **Conversão para Inteiros:**
   - Uma vez que as coordenadas em pixels podem ser números de ponto flutuante, arredondamos esses valores para o número inteiro mais próximo.
   - Isso é importante, pois as coordenadas de pixels devem ser números inteiros para serem utilizadas corretamente ao desenhar ou realizar outras operações na imagem.

4. **Saída:**
   - A função retorna as coordenadas do landmark convertidas para pixels na imagem como uma tupla de inteiros, onde o primeiro elemento representa a coordenada x e o segundo elemento representa a coordenada y.

6. **Captura de vídeo da webcam:**
   - Iniciamos a captura de vídeo da webcam para obter os frames em tempo real.

7. ## Obter a resolução do monitor e o tamanho físico do dispositivo:
```python
monitors = get_monitors()
monitor = monitors[0]  
screen_width = monitor.width
screen_height = monitor.height
screen_width_mm = monitor.width_mm
screen_height_mm = monitor.height_mm
```
   - Utilizamos a biblioteca `screeninfo` para obter a resolução e o tamanho físico do monitor. Isso é usado para calcular a proporção de pixels por centímetro.

## Desenho das Landmarks e Cálculo da Distância:
   - Para cada mão detectada no frame, desenhamos as landmarks usando o módulo `mp_drawing`.
   - Calculamos a distância entre o polegar e o indicador para cada mão e exibimos essa distância na tela usando `cv2.putText`.
   - A distância é calculada em centímetros usando a proporção de pixels por centímetro obtida anteriormente.

Esse código é uma implementação funcional de rastreamento de mãos em tempo real com cálculo de distância entre dois dedos usando o MediaPipe Holistic.    
Ainda há um erro no cálculo da distância, mas esse cálculo foi feito apenas para fins demonstrativos. Ao final do projeto, irei utilizar apenas o cálculo em pixels, já que usarei isso para controlar o volume do computador.

# Volume Control Test
O código fornecido utiliza a biblioteca `pulsectl` para controlar o volume de dispositivos de saída de áudio no PulseAudio. Abaixo está uma explicação detalhada de cada parte do código:

```python
import pulsectl
```
A biblioteca `pulsectl` é importada. Essa biblioteca permite interação com o servidor PulseAudio para gerenciar dispositivos de áudio.

```python
pulse = pulsectl.Pulse('volume-control')
```
Aqui, um objeto `Pulse` é criado com o nome 'volume-control'. Esse objeto será usado para se comunicar com o servidor PulseAudio.

```python
sinks = pulse.sink_list()
```
A lista de dispositivos de saída de áudio (sinks) disponíveis é obtida chamando o método `sink_list` do objeto `pulse`.

```python
if sinks:
    sink = sinks[0]
    print(f"Dispositivo de saída atual: {sink.description}")
```
Se a lista de dispositivos de saída não estiver vazia, o primeiro dispositivo (sink) é selecionado e sua descrição é exibida.

```python
    current_volume = sink.volume.values[0]
    print(f"Volume atual: {current_volume * 100:.0f}%")
```
O volume atual do dispositivo selecionado é obtido e exibido. `sink.volume.values[0]` acessa o volume do primeiro canal (os valores são geralmente os mesmos para todos os canais, então pegar o primeiro é suficiente). O volume é exibido em porcentagem.

```python
    new_volume = 0.5
    pulse.volume_set_all_chans(sink, new_volume)
    print(f"Volume definido para {new_volume * 100:.0f}%")
```
O volume é definido para 50% (0.5 em uma escala de 0 a 1) para todos os canais do dispositivo de saída usando o método `volume_set_all_chans`. A nova configuração de volume é então exibida.

```python
else:
    print("Nenhum dispositivo de saída de áudio encontrado.")
```
Se nenhum dispositivo de saída for encontrado, uma mensagem é exibida informando isso.

```python
pulse.close()
```
A conexão com o servidor é fechada com o `pulse.close()`

# Código Final:
```python
import cv2
import mediapipe as mp
import math
import pulsectl


mp_holistic = mp.solutions.holistic
holistic = mp_holistic.Holistic(static_image_mode=False)
mp_drawing = mp.solutions.drawing_utils

def volume_control(new_volume):
    
    pulse = pulsectl.Pulse('volume-control')
    sinks = pulse.sink_list()

    if sinks:
        sink = sinks[0]
        current_volume = sink.volume.values[0]
        pulse.volume_set_all_chans(sink, new_volume)
        cv2.putText(frame, f'Volume: {distance_pixels*100:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    else:
        return print("Nenhum dispositivo de saída de áudio encontrado.")

    pulse.close()


def calculate_distance(point1, point2):
    return math.sqrt((point2.x - point1.x) ** 2 + (point2.y - point1.y) ** 2)

def normalized_to_pixel_coordinates(normalized_landmark, image_width, image_height):
    return int(normalized_landmark.x * image_width), int(normalized_landmark.y * image_height)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = holistic.process(frame_rgb)

    image_height, image_width, _ = frame.shape

    if results.right_hand_landmarks:
        mp_drawing.draw_landmarks(frame, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        thumb_tip = results.right_hand_landmarks.landmark[mp_holistic.HandLandmark.THUMB_TIP]
        index_finger_tip = results.right_hand_landmarks.landmark[mp_holistic.HandLandmark.INDEX_FINGER_TIP]
        
        thumb_tip_coords = normalized_to_pixel_coordinates(thumb_tip, image_width, image_height)
        index_finger_tip_coords = normalized_to_pixel_coordinates(index_finger_tip, image_width, image_height)
        
        distance_pixels = calculate_distance(thumb_tip, index_finger_tip)
        volume_control(distance_pixels)
        cv2.line(frame, thumb_tip_coords, index_finger_tip_coords, (0, 255, 0), 2)

    if results.left_hand_landmarks:
        mp_drawing.draw_landmarks(frame, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        thumb_tip = results.left_hand_landmarks.landmark[mp_holistic.HandLandmark.THUMB_TIP]
        index_finger_tip = results.left_hand_landmarks.landmark[mp_holistic.HandLandmark.INDEX_FINGER_TIP]
        
        thumb_tip_coords = normalized_to_pixel_coordinates(thumb_tip, image_width, image_height)
        index_finger_tip_coords = normalized_to_pixel_coordinates(index_finger_tip, image_width, image_height)
        
        distance_pixels = calculate_distance(thumb_tip, index_finger_tip)
        volume_control(distance_pixels)

        cv2.line(frame, thumb_tip_coords, index_finger_tip_coords, (0, 255, 0), 2)

    cv2.imshow("Hand Tracking", frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
holistic.close()
```

No codigo final eu só juntei a ideia principal do dois projetos inicais, ao invez de ter um valor constante no `new_volume` o valor é modificado conforme a distancia em pixels do valor já normalizado
Vale falar também que eu adicionei uma lógica de que, caso o dedo mindinho esteja abaixado ele executa a ação de mudar o volume. a explicação é simples e se inspira no count-fingers
