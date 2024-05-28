# Finger Counting Using MediaPipe Holistic

This example code demonstrates how to use MediaPipe Holistic to detect and track landmarks of the pose, hands, and face in real-time, utilizing the OpenCV library for video capture and display.

## Imports and Initializations

```python
import cv2
import mediapipe as mp
```

## Initialization of MediaPipe Holistic Module

```python
mp_holistic = mp.solutions.holistic
holistic = mp_holistic.Holistic(
    static_image_mode=False,         # For real-time videos
    model_complexity=1,              # Medium model complexity
    smooth_landmarks=True,           # Temporal smoothing of landmarks
    min_detection_confidence=0.5,    # Minimum confidence for initial detection
    min_tracking_confidence=0.5      # Minimum confidence for tracking
)
```

Values can be adjusted depending on the problem:

```python
mp_holistic = mp.solutions.holistic
holistic = mp_holistic.Holistic(
    static_image_mode=True,     # For static images
    model_complexity=2,         # Increases model complexity and accuracy, but significantly increases lag
)
```

## Initialization of MediaPipe Drawing Module

```python
mp_drawing = mp.solutions.drawing_utils
```

This will be used to draw the landmarks.

## "count_fingers" Function

```python
def count_fingers(hand_landmarks):

    # List of the highest points of each finger
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

        # If the y-coordinate of the tip is above the dip, the finger is raised
        if finger_tip.y < finger_dip.y:
            fingers_folded += 1
    
    # Thumb verification
    thumb_tip = hand_landmarks.landmark[mp_holistic.HandLandmark.THUMB_TIP]
    thumb_ip = hand_landmarks.landmark[mp_holistic.HandLandmark.THUMB_IP]

    # If the x-coordinate of the tip is to the left (or right, depending on the hand) of the IP, the thumb is raised
    if hand_landmarks.landmark[mp_holistic.HandLandmark.WRIST].x > thumb_tip.x > thumb_ip.x:
        fingers_folded += 1

    return fingers_folded
```

![Hand landmarks](./hand_landmarks.png)

The idea of the code is that when the Y coordinate of the TIP is greater than the Y coordinate of the DIP, the finger is raised.

# Processing with the Holistic Model

```python
results = holistic.process(frame_rgb)
```

Stores the frame values in the results variable.

# Drawing Landmarks and Finger Counting

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
    - Checks if it is the left or right hand.
- `mp_drawing.draw_landmarks(frame, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)`:
    - Draws the landmarks of the right hand.
- `fingers_count = count_fingers(results.right_hand_landmarks)`:
    - Counts the raised fingers of the right hand.
- `cv2.putText(frame, f'Fingers: {fingers_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)`:
    - Prints the text with the number of raised fingers on the image.

It works the same way for the left hand.

## Basic Explanation of How count_fingers Works with MediaPipe

### Future Goals:
- Apply in the overall HANDCONTROL project.
- Improve counting using both hands for a higher count (up to 10 numbers).
- Optimize the code for better performance.