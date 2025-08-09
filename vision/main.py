import cv2
import numpy as np
import mediapipe as mp
from mediapipe.python.solutions.hands import HandLandmark
import serial
import time

def main():

    with serial.Serial('/dev/ttyACM0', baudrate=9600, bytesize=8, parity='N', stopbits=1) as port:
        port.write(b'0')
        time.sleep(1)
        port.write(b'45')

        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands()
        mp.draw = mp.solutions.drawing_utils
    
        stream = cv2.VideoCapture(0)

        # Get stream dimension once, assumes frame shape does not change
        if stream.isOpened():
            _, frame = stream.read()
            frameShape = frame.shape

        print('Starting tracking...\n')

        while stream.isOpened():
            ret, frame = stream.read()
            if not ret:
                break
        
            frame = cv2.flip(frame, 1)
            results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp.draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # check hand position
                hand_landmarks = results.multi_hand_landmarks[0]
                index_tip_position = hand_landmarks.landmark[HandLandmark.INDEX_FINGER_TIP]
                index_pip_position = hand_landmarks.landmark[HandLandmark.INDEX_FINGER_PIP]

                servo_position_1 = np.uint8(index_tip_position.y * 90)
                servo_position_2 = np.uint8(index_pip_position.y * 90)
                
                print(f'Position: {servo_position_1:3d}', end='\r')
                port.write(servo_position_1.tobytes())
                port.write(servo_position_2.tobytes())

            cv2.imshow('Hand Tracking', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        stream.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
