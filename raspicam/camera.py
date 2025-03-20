import cv2
import time

def open_camera(image_name):
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

    if not cap.isOpened():
        print("Error: Cannot access camera")
        return False
    
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)

    for _ in range(5):
        ret, frame = cap.read()
        if not ret:
            cap.release()
            return None
        time.sleep(0.5)
    
    ret, frame = cap.read()
    cap.release()
    if ret:
        cv2.imwrite(f"/home/monlemon/project/photo/{image_name}", frame)
        print(f"Photo saved: {image_name}")
        return image_name
    return None