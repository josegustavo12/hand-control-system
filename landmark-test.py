import mediapipe as mp
import numpy as np
import cv2 
import time
from cvzone.HandTrackingModule import HandDetector 


def calculate_distance(point1, point2): # calculando a distancia entre dois pontos
    point1 = np.array(point1)
    point2 = np.array(point2)
    return np.linalg.norm(point1 - point2)


# inicializando o modelo

mp_holistic = mp.solutions.holistic
holistic_model = mp_holistic.Holistic(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.7,
	model_complexity = 2
)
mp_drawing = mp.solutions.drawing_utils # desenhando o tracking 

# (0) in VideoCapture is used to connect to your computer's default camera
capture = cv2.VideoCapture(0)

# Initializing current time and precious time for calculating the FPS
previousTime = 0
currentTime = 0

while capture.isOpened(): # laço que abre a camera

	ret, frame = capture.read() # inicia a captura
	
	frame = cv2.resize(frame, (800, 600)) # redimensionando o quadro

	image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #convertendo o BGR para RGB (BGR é RGB ao contrário)

	# Making predictions using holistic model
	# To improve performance, optionally mark the image as not writeable to
	# pass by reference.
	image.flags.writeable = False
	results = holistic_model.process(image)
	image.flags.writeable = True

	# Converting back the RGB image to BGR
	image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

	# Landmarks da face
	mp_drawing.draw_landmarks(
	image,
	results.face_landmarks,
	mp_holistic.FACEMESH_CONTOURS,
	mp_drawing.DrawingSpec(
		color=(255,0,255),
		thickness=1,
		circle_radius=1
	),
	mp_drawing.DrawingSpec(
		color=(0,255,255),
		thickness=1,
		circle_radius=1
	)
	)

	# Landmarks das mãos
	# direita
	mp_drawing.draw_landmarks(
	image, 
	results.right_hand_landmarks, 
	mp_holistic.HAND_CONNECTIONS
	)
    # esquerda
	mp_drawing.draw_landmarks(
	image, 
	results.left_hand_landmarks, 
	mp_holistic.HAND_CONNECTIONS
	)
	
	# Calculating the FPS
	currentTime = time.time()
	fps = 1 / (currentTime-previousTime)
	previousTime = currentTime
	

    # Calculando a distancia entre dois pontos e mostrando 
	thump_tip = mp_holistic.HandLandmark.THUMB_TIP
	index_tip = mp_holistic.HandLandmark.INDEX_FINGER_TIP
	thump_tip = [thump_tip.x, thump_tip.y] # coordenadas do polegar
	index_tip = [index_tip.x, index_tip.y] # coordenadas do indicador
	distancia = calculate_distance(thump_tip, index_tip)
	cv2.putText(image, distancia, (10, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)

	# Displaying FPS on the image
	cv2.putText(image, str(int(fps))+" FPS", (10, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)

	# Display the resulting image
	cv2.imshow("Facial and Hand Landmarks", image)

	# Enter key 'q' to break the loop
	if cv2.waitKey(5) & 0xFF == ord('q'):
		break

capture.release()
cv2.destroyAllWindows()

