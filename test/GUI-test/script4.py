import cv2
import mediapipe as mp
import numpy as np
import pyautogui

THR = 0.1
WRIST_THR = 0.2

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

def get_last_k_valid_reading(prev_results, k):
    valid_readings = []
    for i in range(1, len(prev_results)):
        prev_landmarks = get_hand_landmarks(prev_results[-i])
        if prev_landmarks is not None:
            valid_readings.append(prev_landmarks)
            if len(valid_readings) == k:
                return valid_readings
    return valid_readings

def left_click():
    pyautogui.click(button='left')
    print('left clicked')

def right_click():
    pyautogui.click(button='right')
    print('right clicked')

def mouse_move(results, prev_results, image_height, image_width):
    curr_landmarks = get_hand_landmarks(results)
    prev_landmarks = get_last_k_valid_reading(prev_results, 5)[0]
    second_prev_landmarks = get_last_k_valid_reading(prev_results, 5)[-1]

    if curr_landmarks is None or prev_landmarks is None:
        return

    curr_x_coords = np.array([curr_landmarks.landmark[i].x for i in range(len(curr_landmarks.landmark))])[8]
    curr_y_coords = np.array([curr_landmarks.landmark[i].y for i in range(len(curr_landmarks.landmark))])[8]
    prev_x_coords = np.array([prev_landmarks.landmark[i].x for i in range(len(prev_landmarks.landmark))])[8]
    prev_y_coords = np.array([prev_landmarks.landmark[i].y for i in range(len(prev_landmarks.landmark))])[8]
    diff = (curr_x_coords - prev_x_coords, curr_y_coords - prev_y_coords)

    sec_prev_x_coords = np.array([second_prev_landmarks.landmark[i].x for i in range(len(second_prev_landmarks.landmark))])[8]
    sec_prev_y_coords = np.array([second_prev_landmarks.landmark[i].y for i in range(len(second_prev_landmarks.landmark))])[8]
    control_diff = (curr_x_coords - sec_prev_x_coords, curr_y_coords - sec_prev_y_coords)

    if np.absolute(control_diff[0]) >= 0.003 or np.absolute(control_diff[1]) >= 0.003:
        pyautogui.moveRel(int(diff[0] * image_width * 3), int(diff[1] * image_height * 3), duration=0.1)
        print('mouse moved')

def scroll(results, prev_results):
    curr_landmarks = get_hand_landmarks(results)
    prev_landmarks = get_hand_landmarks(prev_results)

    if curr_landmarks is None or prev_landmarks is None:
        return

    curr_y_coords = np.array([curr_landmarks.landmark[i].y for i in range(len(curr_landmarks.landmark))])[8]
    prev_y_coords = np.array([prev_landmarks.landmark[i].y for i in range(len(prev_landmarks.landmark))])[8]
    diff = curr_y_coords - prev_y_coords

    if np.absolute(diff) >= 0.01:
        pyautogui.scroll(100 * diff)
        print('scrolled')

def compute_distance_matrix(hand_landmarks):
    x_coords = np.array([hand_landmarks.landmark[i].x for i in range(len(hand_landmarks.landmark))])
    y_coords = np.array([hand_landmarks.landmark[i].y for i in range(len(hand_landmarks.landmark))])
    z_coords = np.array([hand_landmarks.landmark[i].z for i in range(len(hand_landmarks.landmark))])
    dm = np.zeros(shape=(len(z_coords), len(z_coords)))
    for i in range(len(z_coords)):
        for j in range(len(z_coords)):
            dm[i, j] = np.sqrt(np.square(x_coords[i] - x_coords[j])
                               + np.square(y_coords[i] - y_coords[j])
                               + np.square(z_coords[i] - z_coords[j]))
    return dm

def get_hand_landmarks(results):
    if results.multi_handedness is None:
        return None
    multi_hand_landmarks = results.multi_hand_landmarks
    multi_handedness = results.multi_handedness

    hands_labels = [item.classification[0].label for item in multi_handedness if item.classification[0].label]

    if len(hands_labels) == 1:
        hands_index = 0
    else:
        if 'Right' in hands_labels and len(set(hands_labels)) == 2:
            hands_index = hands_labels.index('Right')
        else:
            return None
    hand_landmarks = multi_hand_landmarks[hands_index]
    return hand_landmarks

def recognize_gesture(results):
    hand_landmarks = get_hand_landmarks(results)
    if hand_landmarks is None:
        return None

    dist_m = compute_distance_matrix(hand_landmarks)
    action = None

    thumb_idx_dist = dist_m[4, 8]
    mid_thumb_dist = dist_m[4, 12]
    mid_idx_dist = dist_m[8, 12]
    base_idx_thumb_dist = dist_m[4, 5]
    wrist_idx_dist = dist_m[0, 8]
    wrist_mid_dist = dist_m[0, 12]
    wrist_ring_dist = dist_m[0, 16]
    wrist_pinky_dist = dist_m[0, 20]
    y_coords = np.array([hand_landmarks.landmark[i].y for i in range(len(hand_landmarks.landmark))])

    if check_pointing_action(hand_landmarks, dist_m):
        action = 'mouse_move'
    elif thumb_idx_dist <= THR and mid_idx_dist > THR and wrist_ring_dist > WRIST_THR and wrist_mid_dist > WRIST_THR and wrist_pinky_dist > WRIST_THR:
        action = 'left_click'
    elif check_right_click(hand_landmarks, dist_m):
        action = 'right_click'
    elif check_scrolling_action(hand_landmarks, dist_m):
        action = 'scroll'
    else:
        action = None

    return action

def check_right_click(hand_landmarks, dist_m):
    y_coords = np.array([hand_landmarks.landmark[i].y for i in range(len(hand_landmarks.landmark))])
    return y_coords[15] - y_coords[6] < THR and dist_m[4, 12] < THR \
           and y_coords[15] - y_coords[12] < THR and y_coords[18] - y_coords[12] < THR \
           and y_coords[19] - y_coords[6] < THR and y_coords[15] - y_coords[6] < THR \
           and y_coords[12] - y_coords[14] > THR and y_coords[12] - y_coords[19] > THR

def check_scrolling_action(hand_landmarks, dist_m):
    y_coords = np.array([hand_landmarks.landmark[i].y for i in range(len(hand_landmarks.landmark))])
    return y_coords[12] - y_coords[14] < THR and y_coords[16] - y_coords[6] > THR and y_coords[20] - y_coords[6] > THR \
           and dist_m[4, 5] <= THR and y_coords[8] - y_coords[6] < THR and y_coords[12] - y_coords[6] < THR

def check_pointing_action(hand_landmarks, dist_m):
    y_coords = np.array([hand_landmarks.landmark[i].y for i in range(len(hand_landmarks.landmark))])
    if y_coords[12] - y_coords[6] > THR and y_coords[16] - y_coords[6] > THR and y_coords[20] - y_coords[6] > THR \
            and dist_m[4, 5] <= THR and y_coords[8] - y_coords[6] < THR:
        return True
    return False

def compute_distance(x1, y1, x2, y2):
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

# Main loop for capturing and processing video input
prev_res = []

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Ignoring empty camera frame.")
        continue

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image_height, image_width, _ = frame.shape

    results = hands.process(frame_rgb)
    
    if results.multi_handedness:
        action = recognize_gesture(results)
        if action and len(prev_res) > 5:
            prev_action = recognize_gesture(prev_res[-1])
            prev_prev_action = recognize_gesture(prev_res[-2])
            if action == 'left_click' and prev_prev_action != 'left_click':
                left_click()
            elif action == 'right_click' and prev_action != 'right_click':
                right_click()
            elif action == 'mouse_move' and prev_action is not None:
                mouse_move(results, prev_res, image_height, image_width)
            elif action == 'scroll':
                scroll(results, prev_res[-5])
        prev_res.append(results)
    
    frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame_bgr, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Hand Control System", frame_bgr)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
hands.close()
