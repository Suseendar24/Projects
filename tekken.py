import cv2
import mediapipe as mp
import pyvjoy  
import time
cap = cv2.VideoCapture(0)
mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils
pose = mp_pose.Pose()
j = pyvjoy.VJoyDevice(1)
def send_input(x_axis, y_axis, button1=False, button2=False): 
    j.set_axis(pyvjoy.HID_USAGE_X, x_axis)  
    j.set_axis(pyvjoy.HID_USAGE_Y, y_axis) 
    j.set_button(1, int(button1))
    j.set_button(2, int(button2))
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = pose.process(rgb)
    height, width = frame.shape[:2]
    punch = False
    defend = False
    if result.pose_landmarks:
        mp_draw.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        lm = result.pose_landmarks.landmark
        wrist_x = int(lm[16].x * width)
        wrist_y = int(lm[16].y * height)
        shoulder_x = int(lm[12].x * width)
        shoulder_y = int(lm[12].y * height)
        eye_y = int(lm[10].y * height)
        if abs(wrist_x - shoulder_x) > 90:
            punch = True
            cv2.putText(frame, 'Punch', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 2)
        if wrist_y < eye_y:
            defend = True
            cv2.putText(frame, 'Defend', (50, 90), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 2)
        joy_x = 16384 + (wrist_x - width // 2) * 50
        joy_y = 16384 + (wrist_y - height // 2) * 50
        joy_x = max(0, min(32768, joy_x))
        joy_y = max(0, min(32768, joy_y))
        send_input(joy_x, joy_y, button1=punch, button2=defend)
    else:
        send_input(16384, 16384, button1=False, button2=False)
    cv2.imshow("Motion Control", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()
send_input(16384, 16384, button1=False, button2=False)
