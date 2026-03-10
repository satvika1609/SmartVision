import cv2
import numpy as np
import pickle
import os
import time
import datetime
from deepface import DeepFace
import winsound
from twilio.rest import Client


# =========================
# TWILIO CONFIG
# =========================
ACCOUNT_SID = "YOUR_TWILIO_SID"
AUTH_TOKEN = "YOUR_TWILIO_TOKEN"
TWILIO_PHONE = "+18106432687"
YOUR_PHONE = "+918121355340"

client = Client(ACCOUNT_SID, AUTH_TOKEN)


# =========================
# CONFIG
# =========================
EMB_FILE = "trainer/embeddings.pickle"
LOG_DIR = "logs/intruder_images"
LOG_FILE = "logs/log.csv"

THRESHOLD = 0.6
COOLDOWN = 10

FRAME_SKIP = 3
RESIZE_WIDTH = 640


# =========================
# SETUP
# =========================
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs("logs", exist_ok=True)

if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f:
        f.write("timestamp,filename\n")

data = pickle.load(open(EMB_FILE, "rb"))

known_embeddings = np.array(data["embeddings"])
known_embeddings = known_embeddings / np.linalg.norm(
    known_embeddings, axis=1, keepdims=True
)

known_names = np.array(data["names"])

print(f"[INFO] Loaded {len(known_names)} faces")


last_alert_time = 0
frame_count = 0

last_faces = []
last_labels = []


# =========================
# ALERT FUNCTIONS
# =========================
def send_whatsapp_alert(timestamp):

    try:
        message = f"🚨 ALERT: Intruder Detected!\nTime: {timestamp}"

        client.messages.create(
            body=message,
            from_="whatsapp:+14155238886",
            to=f"whatsapp:{YOUR_PHONE}"
        )

        print("WhatsApp sent")

    except Exception as e:
        print("WhatsApp Error:", e)


def make_call_alert():

    try:
        client.calls.create(
            twiml='<Response><Say>Alert. Intruder detected.</Say></Response>',
            from_=TWILIO_PHONE,
            to=YOUR_PHONE
        )
        print("Call sent")

    except Exception as e:
        print("Call Error:", e)


# =========================
# LOG INTRUDER
# =========================
def log_intruder(frame):

    global last_alert_time

    timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    filename = f"intruder_{timestamp}.jpg"

    filepath = os.path.join(LOG_DIR, filename)

    cv2.imwrite(filepath, frame)

    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp},{filename}\n")

    print(f"[ALERT] Intruder logged {timestamp}")

    # Alarm sound
    for _ in range(3):
        winsound.Beep(1000, 250)

    # Send alerts
    send_whatsapp_alert(timestamp)
    make_call_alert()

    last_alert_time = time.time()


# =========================
# CAMERA
# =========================
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

print("[INFO] Camera started — press Q to exit")


while True:

    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    try:

        if frame_count % FRAME_SKIP == 0:

            h, w = frame.shape[:2]
            scale = RESIZE_WIDTH / w

            small = cv2.resize(frame, (RESIZE_WIDTH, int(h * scale)))

            detections = DeepFace.extract_faces(
                img_path=small,
                detector_backend="opencv",
                enforce_detection=False
            )

            detected_faces = []
            detected_labels = []

            for face in detections:

                area = face["facial_area"]

                x = int(area["x"] / scale)
                y = int(area["y"] / scale)
                fw = int(area["w"] / scale)
                fh = int(area["h"] / scale)

                face_img = frame[y:y+fh, x:x+fw]

                if face_img.size == 0:
                    continue

                # Embedding
                emb = DeepFace.represent(
                    img_path=face_img,
                    model_name="Facenet",
                    enforce_detection=False
                )[0]["embedding"]

                emb = np.array(emb)
                emb = emb / np.linalg.norm(emb)

                # Fast cosine similarity
                sims = np.dot(known_embeddings, emb)

                best_idx = np.argmax(sims)
                best_score = sims[best_idx]

                if best_score > THRESHOLD:

                    name = known_names[best_idx]
                    color = (0, 255, 0)

                else:

                    name = "INTRUDER"
                    color = (0, 0, 255)

                    current_time = time.time()

                    if current_time - last_alert_time > COOLDOWN:
                        log_intruder(face_img)

                detected_faces.append((x, y, fw, fh))
                detected_labels.append((name, color))

            if detected_faces:
                last_faces = detected_faces
                last_labels = detected_labels

    except Exception:
        pass


    # =========================
    # DRAW
    # =========================
    for (x, y, fw, fh), (name, color) in zip(last_faces, last_labels):

        cv2.rectangle(frame, (x, y), (x+fw, y+fh), color, 2)

        cv2.putText(
            frame,
            name,
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            color,
            2
        )

    cv2.imshow("AI Intrusion Detection", frame)

    key = cv2.waitKey(1) & 0xFF

    if key in [ord('q'), ord('Q'), 27]:
        break


cap.release()
cv2.destroyAllWindows()

print("[INFO] Stopped")