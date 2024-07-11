import cv2
import numpy as np
from mtcnn import MTCNN
from tensorflow.keras.models import load_model
from efficientnet.tfkeras import preprocess_input

# Load the trained model
model_path = 'best_model.h5'
loaded_model = load_model(model_path)

# Set the input size
input_size = 128  # Adjust as needed

def preprocess_image(img):
    img = cv2.resize(img, (input_size, input_size))
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    return img

def predict_face(image):
    img = preprocess_image(image)
    prediction = loaded_model.predict(img)
    class_label = "Real" if prediction > 0.75 else "Fake"
    confidence = prediction[0, 0] if class_label == "Fake" else 1 - prediction[0, 0]
    return class_label, confidence

def process_video(video_path, output_path='output.avi'):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    detector = MTCNN()
    fourcc = cv2.VideoWriter_fourcc(*'H264')
    out = cv2.VideoWriter(output_path, fourcc, 20.0, (640, 480))  # Adjust frame size if needed

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Detect faces
        faces = detector.detect_faces(frame)

        # Loop through each detected face
        for face in faces:
            bounding_box = face['box']
            confidence = face['confidence']

            if confidence > 0.95:  # Adjust confidence threshold if needed
                x, y, w, h = bounding_box
                face_image = frame[y:y+h, x:x+w]

                # Predict using the trained model
                class_label, confidence = predict_face(face_image)

                # Display result on the frame
                label = f"{class_label} ({confidence:.2%})"
                cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Write the frame to the output video
        out.write(frame)

        # Display the frame with predictions
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
