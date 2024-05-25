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
        cv2.putText(frame, f'Volume: {distance_pixels*100:.0f}%', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

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
