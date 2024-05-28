import cv2
import mediapipe as mp
import math
from screeninfo import get_monitors

mp_holistic = mp.solutions.holistic
holistic = mp_holistic.Holistic(static_image_mode=False)
mp_drawing = mp.solutions.drawing_utils

def calculate_distance(point1, point2):
    return math.sqrt((point2.x - point1.x) ** 2 + (point2.y - point1.y) ** 2)

def normalized_to_pixel_coordinates(normalized_landmark, image_width, image_height):
    return int(normalized_landmark.x * image_width), int(normalized_landmark.y * image_height)

cap = cv2.VideoCapture(0)

monitors = get_monitors()
monitor = monitors[0]  
screen_width = monitor.width
screen_height = monitor.height
screen_width_mm = monitor.width_mm
screen_height_mm = monitor.height_mm

pixels_per_cm_horizontal = screen_width / screen_width_mm
pixels_per_cm_vertical = screen_height / screen_height_mm
pixels_to_cm_ratio = (pixels_per_cm_horizontal + pixels_per_cm_vertical) / 2

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
        distance_cm = (distance_pixels / pixels_to_cm_ratio) * 100
        
        cv2.putText(frame, f'Direita: {distance_cm:.2f} cm', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        cv2.line(frame, thumb_tip_coords, index_finger_tip_coords, (0, 255, 0), 2)

    if results.left_hand_landmarks:
        mp_drawing.draw_landmarks(frame, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        thumb_tip = results.left_hand_landmarks.landmark[mp_holistic.HandLandmark.THUMB_TIP]
        index_finger_tip = results.left_hand_landmarks.landmark[mp_holistic.HandLandmark.INDEX_FINGER_TIP]
        
        thumb_tip_coords = normalized_to_pixel_coordinates(thumb_tip, image_width, image_height)
        index_finger_tip_coords = normalized_to_pixel_coordinates(index_finger_tip, image_width, image_height)
        
        distance_pixels = calculate_distance(thumb_tip, index_finger_tip)
        distance_cm = (distance_pixels / pixels_to_cm_ratio) * 100
        
        cv2.putText(frame, f'Esquerda: {distance_cm:.2f} cm', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        cv2.line(frame, thumb_tip_coords, index_finger_tip_coords, (0, 255, 0), 2)

    cv2.imshow("Hand Tracking", frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
holistic.close()
