# SmartVision – AI-Based Intrusion Detection System

SmartVision is an AI-based intrusion detection system designed to enhance security through real-time monitoring and face recognition. The system uses computer vision and machine learning techniques to detect human faces from a live camera feed and classify them as authorized or unauthorized users.

When an unknown individual is detected, the system identifies the intrusion and automatically sends alerts to the administrator. The system supports both WhatsApp notifications and phone call alerts using the Twilio API, ensuring immediate awareness of potential security breaches.

---

## Project Features

* Real-time face detection using OpenCV
* Face recognition for identifying authorized users
* Intrusion detection for unknown individuals
* Automated WhatsApp alert notifications when an intrusion is detected
* Automated phone call alerts using the Twilio API
* Dataset creation for authorized users
* Machine learning model training for face recognition
* Simple monitoring interface for real-time observation

---

## Technologies Used

* Python
* OpenCV
* Machine Learning
* Flask
* NumPy
* HTML, CSS, JavaScript
* Twilio API (for alerts)

---

## Project Structure

```
SmartVision
│
├── dataset/                # Face dataset for training
├── static/                 # CSS, JavaScript, images
├── templates/              # HTML templates for the interface
├── main.py                 # Main application file
├── train_model.py          # Script used to train the recognition model
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
```

---

## System Workflow

1. The system captures live video from the webcam.
2. OpenCV detects faces in the video frames.
3. The detected faces are compared with the trained dataset of authorized users.
4. If a match is found, the individual is recognized as an authorized user.
5. If the face does not match the dataset, the system marks it as an intrusion.
6. The system immediately triggers alerts through WhatsApp messages and phone calls to notify the administrator.

---

## Installation

Clone the repository

```
git clone https://github.com/satvika1609/SmartVision.git
```

Navigate to the project directory

```
cd SmartVision
```

Install the required dependencies

```
pip install -r requirements.txt
```

---

## Running the Project

Start the application using the following command:

```
python main.py
```

Once the application starts, the webcam activates and the system begins monitoring for authorized and unauthorized faces.

---

## Screenshots

### SmartVision Interface

<img width="1919" height="921" alt="Screenshot 2026-03-09 214453" src="https://github.com/user-attachments/assets/66ddae52-ac89-4158-abbf-e6f001976a39" />


### Real-Time Face Detection

<img width="795" height="640" alt="Screenshot 2026-03-09 214935" src="https://github.com/user-attachments/assets/2e7dbf16-b9ba-4109-a972-dba30a3d77a8" />


### Intrusion Detection Alert

![Screenshot_20260309_225302 jpg](https://github.com/user-attachments/assets/324b0026-5c06-4480-a26f-d82d700069f3)

---

## Future Improvements

* Integration with cloud-based monitoring systems
* Development of a mobile application for remote monitoring
* Support for multiple surveillance cameras
* Use of deep learning models for improved recognition accuracy
* Secure storage of intrusion logs and captured images

---

## Author

Satvika Chilakala
B.Tech Computer Science Student

GitHub: https://github.com/satvika1609

LinkedIn: https://linkedin.com/in/satvika-chilakala-284951256

---

## License

This project is licensed under the MIT License.
