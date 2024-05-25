import cv2
import mediapipe as mp

mp_holistic = mp.solutions.holistic
holistic = mp_holistic.Holistic(static_image_mode=False)


mp_drawing = mp.solutions.drawing_utils

def count_fingers(hand_landmarks):
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

        if finger_tip.y < finger_dip.y:
            fingers_folded += 1
    
    thumb_tip = hand_landmarks.landmark[mp_holistic.HandLandmark.THUMB_TIP]
    thumb_ip = hand_landmarks.landmark[mp_holistic.HandLandmark.THUMB_IP]

    
    if hand_landmarks.landmark[mp_holistic.HandLandmark.WRIST].x > thumb_tip.x > thumb_ip.x:
        fingers_folded += 1

    return fingers_folded

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = holistic.process(frame_rgb)

    if results.right_hand_landmarks:
        mp_drawing.draw_landmarks(frame, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        fingers_count = count_fingers(results.right_hand_landmarks)
        cv2.putText(frame, f'Fingers: {fingers_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    if results.left_hand_landmarks:
        mp_drawing.draw_landmarks(frame, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        fingers_count = count_fingers(results.left_hand_landmarks)
        cv2.putText(frame, f'Fingers: {fingers_count}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Hand Tracking", frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
holistic.close()
