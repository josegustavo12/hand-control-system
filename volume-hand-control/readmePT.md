O código foi elaborado para usar o MediaPipe Holistic, uma ferramenta poderosa para detectar e rastrear landmarks de pose, mãos e rosto em tempo real. Vamos analisar cada parte do código e seu papel no sistema:



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

## Desenho das Landmarks e Cálculo da Distância:**
   - Para cada mão detectada no frame, desenhamos as landmarks usando o módulo `mp_drawing`.
   - Calculamos a distância entre o polegar e o indicador para cada mão e exibimos essa distância na tela usando `cv2.putText`.
   - A distância é calculada em centímetros usando a proporção de pixels por centímetro obtida anteriormente.

Esse código é uma implementação funcional de rastreamento de mãos em tempo real com cálculo de distância entre dois dedos usando o MediaPipe Holistic.    
Ainda há um erro no cálculo da distância, mas esse cálculo foi feito apenas para fins demonstrativos. Ao final do projeto, irei utilizar apenas o cálculo em pixels, já que usarei isso para controlar o volume do computador.