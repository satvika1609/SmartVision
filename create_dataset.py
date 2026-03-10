import cv2
import os
import time


# =========================
# CONFIG
# =========================
DATASET_DIR = "dataset/authorized"
IMAGE_SIZE = 160      # FaceNet recommended size
MAX_IMAGES = 60       # Images per person
CAPTURE_DELAY = 0.25  # Seconds between captures


# =========================
# DATASET FUNCTION
# =========================
def create_dataset_from_webcam(person_name):

    person_path = os.path.join(DATASET_DIR, person_name)
    os.makedirs(person_path, exist_ok=True)

    cap = cv2.VideoCapture(0)

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    count = 0
    last_save_time = time.time()

    print("\n[INFO] Starting webcam...")
    print("[INFO] Move your head slowly (left/right/up/down)")
    print("[INFO] Press Q to stop early\n")

    while True:

        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5,
            minSize=(80, 80)
        )

        for (x, y, w, h) in faces:

            # Capture every few milliseconds
            if time.time() - last_save_time >= CAPTURE_DELAY:

                face = frame[y:y+h, x:x+w]  # RGB (color)

                if face.size == 0:
                    continue

                # Resize for FaceNet
                face = cv2.resize(face, (IMAGE_SIZE, IMAGE_SIZE))

                count += 1

                img_path = os.path.join(person_path, f"{count}.jpg")
                cv2.imwrite(img_path, face)

                last_save_time = time.time()

                print(f"[INFO] Captured image {count}/{MAX_IMAGES}")

            # Draw rectangle
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.putText(
            frame,
            f"Images: {count}/{MAX_IMAGES}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            2
        )

        cv2.imshow("Dataset Capture - Press Q to Stop", frame)

        if cv2.waitKey(1) & 0xFF == ord('q') or count >= MAX_IMAGES:
            break

    cap.release()
    cv2.destroyAllWindows()

    print(f"\n[SUCCESS] Dataset completed for {person_name}")
    print(f"[INFO] Total images saved: {count}\n")


# =========================
# MAIN
# =========================
if __name__ == "__main__":

    name = input("Enter authorized person name: ").strip()

    if name == "":
        print("Name cannot be empty")
    else:
        create_dataset_from_webcam(name)