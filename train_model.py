import cv2
import os
import numpy as np
import pickle

DATASET_DIR = "dataset/authorized"
TRAINER_DIR = "trainer"

def train_model():
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    face_samples = []
    ids = []
    label_ids = {}
    current_id = 0

    # Map each person name to a numeric ID
    for person_name in os.listdir(DATASET_DIR):
        person_folder = os.path.join(DATASET_DIR, person_name)
        if not os.path.isdir(person_folder):
            continue

        if person_name not in label_ids:
            label_ids[person_name] = current_id
            current_id += 1

        person_id = label_ids[person_name]

        for img_name in os.listdir(person_folder):
            if not img_name.lower().endswith((".png", ".jpg", ".jpeg")):
                continue

            img_path = os.path.join(person_folder, img_name)
            img = cv2.imread(img_path)
            if img is None:
                continue

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                roi = gray[y:y+h, x:x+w]
                face_samples.append(roi)
                ids.append(person_id)

    if len(face_samples) == 0:
        print("[ERROR] No faces found in dataset. Check your images.")
        return

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(face_samples, np.array(ids))

    os.makedirs(TRAINER_DIR, exist_ok=True)
    recognizer.save(os.path.join(TRAINER_DIR, "lbph_model.yml"))

    with open(os.path.join(TRAINER_DIR, "labels.pickle"), "wb") as f:
        pickle.dump(label_ids, f)

    print("[INFO] Training completed.")
    print("[INFO] Saved model in trainer/lbph_model.yml")
    print("[INFO] Saved labels in trainer/labels.pickle")


if __name__ == "__main__":
    train_model()
