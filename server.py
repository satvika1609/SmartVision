from flask import Flask, jsonify, send_from_directory, request, session
import os
import csv
import subprocess
import json

app = Flask(__name__, static_folder="frontend", static_url_path="")
app.secret_key = "super_secret_key"


# =========================
# PATH CONFIG
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOG_FILE = os.path.join(BASE_DIR, "logs", "log.csv")
IMG_DIR = os.path.join(BASE_DIR, "logs", "intruder_images")
DATASET_DIR = os.path.join(BASE_DIR, "dataset", "authorized")
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

ADMIN_FILE = os.path.join(BASE_DIR, "admin.json")


# =========================
# ADMIN FILE HELPERS
# =========================

def load_admin():
    if not os.path.exists(ADMIN_FILE):
        return {"username": "admin", "password": "1234"}

    with open(ADMIN_FILE, "r") as f:
        return json.load(f)


def save_admin(data):
    with open(ADMIN_FILE, "w") as f:
        json.dump(data, f)


# =========================
# SERVE FRONTEND
# =========================

@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


# =========================
# LOGIN
# =========================

@app.route("/api/login", methods=["POST"])
def login():

    data = request.json

    username = data.get("username")
    password = data.get("password")

    admin = load_admin()

    if username == admin["username"] and password == admin["password"]:

        session["logged_in"] = True

        return jsonify({"status": "ok"})

    return jsonify({"status": "error"})


# =========================
# CHECK SESSION
# =========================

@app.route("/api/check_auth")
def check_auth():

    if session.get("logged_in"):
        return jsonify({"status": "ok"})

    return jsonify({"status": "no"})


# =========================
# LOGOUT
# =========================

@app.route("/api/logout")
def logout():

    session.clear()
    return jsonify({"status": "ok"})


# =========================
# FORGOT PASSWORD / CHANGE
# =========================

@app.route("/api/change_password", methods=["POST"])
def change_password():

    data = request.json

    username = data.get("username")
    new_password = data.get("new_password")

    admin = load_admin()

    if username != admin["username"]:
        return jsonify({"status": "error", "msg": "Invalid username"})

    admin["password"] = new_password
    save_admin(admin)

    return jsonify({"status": "ok"})


# =========================
# GET LOGS
# =========================

@app.route("/api/logs")
def get_logs():

    logs = []

    if not os.path.exists(LOG_FILE):
        return jsonify([])

    with open(LOG_FILE, newline="") as f:

        reader = csv.DictReader(f)

        for row in reader:

            timestamp = row.get("timestamp")
            filename = row.get("filename")

            if not timestamp or not filename:
                continue

            logs.append({
                "timestamp": timestamp.strip(),
                "filename": filename.strip()
            })

    logs.reverse()
    return jsonify(logs)


# =========================
# LATEST INTRUSION
# =========================

@app.route("/api/latest_intrusion")
def latest_intrusion():

    if not os.path.exists(LOG_FILE):
        return jsonify({"status": "empty"})

    with open(LOG_FILE, newline="") as f:
        rows = list(csv.DictReader(f))

    if len(rows) == 0:
        return jsonify({"status": "empty"})

    latest = rows[-1]

    filename = latest.get("filename", "").strip()

    image_path = os.path.join(IMG_DIR, filename)

    if not os.path.exists(image_path):
        return jsonify({"status": "missing"})

    return jsonify({
        "status": "ok",
        "timestamp": latest.get("timestamp"),
        "filename": filename,
        "image_url": f"/intruder_images/{filename}"
    })


# =========================
# SERVE IMAGES
# =========================

@app.route("/intruder_images/<filename>")
def serve_intruder_image(filename):
    return send_from_directory(IMG_DIR, filename)


# =========================
# STAFF
# =========================

@app.route("/api/staff")
def get_staff():

    if not os.path.exists(DATASET_DIR):
        return jsonify([])

    return jsonify(os.listdir(DATASET_DIR))


@app.route("/api/add_staff", methods=["POST"])
def add_staff():

    name = request.form.get("name")
    files = request.files.getlist("images")

    person_path = os.path.join(DATASET_DIR, name)
    os.makedirs(person_path, exist_ok=True)

    for file in files:
        file.save(os.path.join(person_path, file.filename))

    return "ok"


@app.route("/api/delete_staff", methods=["POST"])
def delete_staff():

    data = request.json
    name = data.get("name")

    path = os.path.join(DATASET_DIR, name)

    if os.path.exists(path):
        import shutil
        shutil.rmtree(path)

    return "ok"


@app.route("/api/regenerate", methods=["POST"])
def regenerate():

    subprocess.run(["python", "generate_embeddings.py"])
    return "ok"


# =========================
# RUN
# =========================

if __name__ == "__main__":
    app.run(debug=True)