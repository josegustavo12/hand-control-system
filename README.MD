# Hand Control System

## Descrição

Este projeto utiliza a biblioteca MediaPipe e a OpenCV para reconhecer gestos das mãos e realizar ações no computador, como mover o mouse, clicar e rolar. Ele também inclui uma interface gráfica feita com Tkinter para executar diferentes scripts.
O Projeto possui codigos exemplos de como cada funcionalidade foi construida e arquivos MD explicando passo a passo os códigos.

## Funcionalidades

- Reconhecimento de gestos para controle do mouse.
- Interface gráfica com Tkinter para executar diferentes scripts.
- Contagem de dedos usando MediaPipe.
- Controle do Volume.

## Estrutura do Projeto

```
hand-control-system/
├── test/
│   └── GUI-test/
│       ├── app.py           # Script principal com a interface gráfica
│       ├── script1.py       # Exemplo de script 1
│       ├── script2.py       # Exemplo de script 2
│       ├── script3.py       # Exemplo de script 3
│       ├── script4.py       # Exemplo de script 4
│       └── script5.py       # Exemplo de script 5
```

## Como Baixar

1. Clone o repositório:
   ```bash
   git clone https://github.com/josegustavo12/hand-control-system
   cd hand-control-system
   ```

2. Navegue até o diretório `GUI-test`:
   ```bash
   cd test/GUI-test
   ```

## Instalação das Bibliotecas

Certifique-se de ter o Python 3 instalado. Você pode instalar as bibliotecas necessárias usando `pip`:

```bash
pip install opencv-python-headless mediapipe numpy pyautogui
```

## Como Executar

1. **Certifique-se de que a estrutura do diretório esteja correta conforme descrito.**
2. **Execute o script principal:**
   ```bash
   python3 app.py
   ```

## Código

### `app.py`

```python
import tkinter as tk
from tkinter import messagebox
import subprocess
import os

# pega o diretorio atual da pasta e add o caminho restante (caminho padrão para quem clonar o repositorio)
scripts_dir = os.getcwd() + "/test/GUI-test"

# funções que executam o script
def script1():
    try:
        subprocess.run(["python3", os.path.join(scripts_dir, "script1.py")], check=True)
        messagebox.showinfo("Script 1", "Script 1 executado com sucesso!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erro", f"Erro ao executar Script 1: {e}")

def script2():
    try:
        subprocess.run(["python3", os.path.join(scripts_dir, "script2.py")], check=True)
        messagebox.showinfo("Script 2", "Script 2 executado com sucesso!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erro", f"Erro ao executar Script 2: {e}")

def script3():
    try:
        subprocess.run(["python3", os.path.join(scripts_dir, "script3.py")], check=True)
        messagebox.showinfo("Script 3", "Script 3 executado com sucesso!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erro", f"Erro ao executar Script 3: {e}")

def script4():
    try:
        subprocess.run(["python3", os.path.join(scripts_dir, "script4.py")], check=True)
        messagebox.showinfo("Script 4", "Script 4 executado com sucesso!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erro", f"Erro ao executar Script 4: {e}")

def script5():
    try:
        subprocess.run(["python3", os.path.join(scripts_dir, "script5.py")], check=True)
        messagebox.showinfo("Script 5", "Script 5 executado com sucesso!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erro", f"Erro ao executar Script 5: {e}")


# cria a janela principal
root = tk.Tk()
root.title("Controle de Scripts")
root.geometry("400x300")
root.configure(bg="#2C3E50")

# estilização dos botoes
button_style = {
    "font": ("Helvetica", 12, "bold"),
    "bg": "#3498DB",
    "fg": "white",
    "relief": tk.RAISED,
    "bd": 3,
    "width": 20,
    "height": 2,
}

# add os botoes a janela e coloca o que eles tem que fazer (command)
button1 = tk.Button(root, text="Count Fingers", command=script1, **button_style)
button1.pack(pady=10)

button2 = tk.Button(root, text="Pyautogui Mouse", command=script2, **button_style)
button2.pack(pady=10)

button3 = tk.Button(root, text="Volume Hand Control", command=script3, **button_style)
button3.pack(pady=10)

button4 = tk.Button(root, text="Projeto final", command=script4, **button_style)
button4.pack(pady=10)

root.mainloop()

```
## Funcionamento 
### GUI:
![Count Fingers](fotos/Captura%20de%20tela%20de%202024-05-28%2020-18-29.png)

### Script 1 (Count Fingers):
![Count Fingers](fotos/5dedoshandtracking.png)
![Count Fingers](fotos/5e3dedoshandtracking.png)


### Script 2 (Pyautogui Mouse):
- Digita um comando no terminal e o mouse irá executar
    - (move 540 879) ele irá mover para as coordenadas x = 540 e y = 879

### Script 3 (Volume Hand Control):
![Count Fingers](fotos/volume.png)

### Script 4 (Projeto final):
#### O projeto final possui os seguintes comandos:
- Todos os dedos abaixados e apenas o `indicador` levantado: Mover o mouse na direção do dedo
- Dedo indicador e do meio levantados: scroll do mouse (juntos = 0; separados aumenta)
- sinal de pinça (encostar o dedo indicador com o polegar): left click
- dedo mindinho levantado: right click

## Funcionamento do script 4:
### inicalização das bibliotecas:
```python
import cv2 # opencv 
import mediapipe as mp # landmarks
import numpy as np # operações numericas
import pyautogui # simular o mouse
```

### Constantes `THR` e `WRIST_THR`
- `THR`: Este é o limiar de tolerância usado para determinar certas condições de movimento das mãos. Por exemplo, se a diferença na coordenada y entre dois pontos específicos da mão for maior que THR, isso pode ser interpretado como um movimento significativo da mão na direção vertical. É uma forma de definir o quanto um movimento deve ser para ser considerado significativo.

- `WRIST_THR`: Este é um limiar específico usado para distinguir movimentos ou posições que envolvem o pulso (wrist). Por exemplo, pode ser usado para distinguir entre um gesto de clique e um gesto de rolagem, onde a posição do pulso é crucial para essa distinção.

### Função `get_last_k_valid_readings`
- Parametros: 
    - prev_results: lista com resultados anteriores
    - k: numero de leituras validas para obter

```python
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
```
- A função tem como papel impedir que as operações subsequentes a ela sejam baseadas em leituras das landmarks válidas, dessa forma a principal função dela é servir como um filtro

### Função `perform_click`
- Parametro:
    - action: ação do mouse
```python
def perform_click(action):
    if action == 'left_click':
        button = 'left'
    else:
        button = 'right'
        
    pyautogui.click(button=button)
    print("{} clicked".format(button))
```
### Função `move_mouse`
- Parametros
    - curr_landmarks: landmarks atuais (ponto de referencia da mão)
    - prev_landmarks: landmarks anteriores (ponto de referencia da mão)
    - image_height: altura da imagem
    - image_width: largura da imagem

```python
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
```

### Função `scroll_mouse`

- Parametros:
    - curr_landmarks: landmarks atuais
    - prev_landmarks: landmarks anteriores

```python
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
```

### Função `get_coords`
- Parametros:
    - landmarks: objeto que contem os pontos de referencia
    - idx: indice do ponto de referencia

```python
def get_coords(landmarks, idx):
    x = landmarks.landmark[idx].x # objeto (landmarks), atributo (landmark) e indice da coordenada x
    y = landmarks.landmark[idx].y
    return x, y # retorna uma tupla com as coordenadas
```

### Função `compute_distance_matrix`
- Parametros:
    - hand_landmarks: landmarks da mão

```python
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
```
- Essa função retorna a distancia entre todos os pontos de referencia na mão

### Função `get_hand_landmarks`
```python
def get_hand_landmarks(results):

    if not results.multi_handedness: # verifica se tem +1 mão
        return None
    
    for hand in results.multi_handedness: # itera sobre as lateralidades

        if hand.classification[0].label == 'Right': # verifica se é direita

            return results.multi_hand_landmarks[results.multi_handedness.index(hand)] # retorna os pontos de referencia da mão direita
        elif hand.classification[0].label == 'Left':
            return results.multi_hand_landmarks[results.multi_handedness.index(hand)]
    
    
    return None # retorna nada caso não veja mão
```

### Função `recognize_gesture`

```python
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
```

### Loop principal
```python
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
```

## Autor

José Gustavo Victor Pinheiro Alencar

