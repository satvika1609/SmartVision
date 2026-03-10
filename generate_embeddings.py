import os
import pickle
import numpy as np
from deepface import DeepFace


DATASET_DIR = "dataset/authorized"
EMBEDDINGS_PATH = "trainer/embeddings.pickle"

MODEL = "Facenet"
DETECTOR = "retinaface"


def generate_embeddings():

    embeddings = []
    names = []

    total_images = 0

    for person_name in os.listdir(DATASET_DIR):

        person_folder = os.path.join(DATASET_DIR, person_name)

        if not os.path.isdir(person_folder):
            continue

        for img_name in os.listdir(person_folder):

            if not img_name.lower().endswith((".png", ".jpg", ".jpeg")):
                continue

            img_path = os.path.join(person_folder, img_name)

            try:

                result = DeepFace.represent(
                    img_path=img_path,
                    model_name=MODEL,
                    detector_backend=DETECTOR,
                    enforce_detection=True
                )

                embedding = result[0]["embedding"]

                embedding = np.array(embedding)

                # Normalize embedding
                embedding = embedding / np.linalg.norm(embedding)

                embeddings.append(embedding)
                names.append(person_name)

                total_images += 1

                print(f"[OK] {img_path}")

            except Exception as e:

                print(f"[SKIP] {img_path} -> {e}")


    data = {
        "embeddings": embeddings,
        "names": names
    }

    os.makedirs("trainer", exist_ok=True)

    with open(EMBEDDINGS_PATH, "wb") as f:
        pickle.dump(data, f)

    print("\n==============================")
    print(f"[SUCCESS] Saved {len(embeddings)} embeddings")
    print("==============================\n")


if __name__ == "__main__":
    generate_embeddings()
