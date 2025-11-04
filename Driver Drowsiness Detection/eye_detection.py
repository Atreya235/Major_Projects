import cv2
import time
import dlib
import imutils
from imutils import face_utils
from scipy.spatial import distance
from pygame import mixer

# Initialize mixer for alert sound
mixer.init()
mixer.music.load("music.wav")

def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

threshold = 0.25
frame_check = 20
flag = 0

(l_start, l_end) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(r_start, r_end) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

detect = dlib.get_frontal_face_detector()
predict = dlib.shape_predictor("shape_predictor_68_landmarks.dat")

cap = cv2.VideoCapture(0)

# ------------------- ⏱️ ADDED TIMER VARIABLES -------------------
countdown_started = False
countdown_start_time = None
countdown_duration = 6   # seconds
# ---------------------------------------------------------------

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    subjects = detect(gray, 0)

    for subject in subjects:
        shape = predict(gray, subject)
        shape = face_utils.shape_to_np(shape)

        leftEye = shape[l_start:l_end]
        rightEye = shape[r_start:r_end]

        left_ear = eye_aspect_ratio(leftEye)
        right_ear = eye_aspect_ratio(rightEye)
        ear = (left_ear + right_ear) / 2.0

        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

        if ear < threshold:
            flag += 1
            print(f"Frame count below threshold: {flag}")

            # ----------------- ⏱️ TIMER START -----------------
            if not countdown_started:
                countdown_started = True
                countdown_start_time = time.time()
            # Calculate remaining time
            elapsed = time.time() - countdown_start_time
            remaining = max(0, countdown_duration - int(elapsed))

            # Show timer on screen
            cv2.putText(frame, f"Eyes closed: {remaining}s", (400, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

            # When timer hits 0
            if remaining == 0:
                cv2.putText(frame, "******* ALERT *******", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.putText(frame, "******* ALERT *******", (10, 325),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                if not mixer.music.get_busy():
                    mixer.music.play()
            # -------------------------------------------------
        else:
            flag = 0
            mixer.music.stop()
            # Reset countdown if eyes open again
            countdown_started = False
            countdown_start_time = None

    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
