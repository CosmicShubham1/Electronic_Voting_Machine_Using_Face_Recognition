import face_recognition
import cv2
import os
import serial
import time

# 🔌 Setup serial (update COM port as needed)
ser = serial.Serial('COM3', 9600)
time.sleep(2)  # Give time to establish connection

# 📸 Get image name
image_folder = "./reference_photos"
image_name = input("Enter your image name (without extension): ")

# 🔍 Find the reference image
image_path = None
for ext in [".jpg", ".png", ".jpeg"]:
    potential_path = os.path.join(image_folder, image_name + ext)
    if os.path.exists(potential_path):
        image_path = potential_path
        break

if not image_path:
    print(f"Error: Image '{image_name}' not found in folder '{image_folder}'.")
    exit()

reference_image = face_recognition.load_image_file(image_path)
reference_encodings = face_recognition.face_encodings(reference_image)

if not reference_encodings:
    print("No face detected in the reference image.")
    exit()

reference_encoding = reference_encodings[0]

# 🟢 Start camera
video_capture = cv2.VideoCapture(0)
MATCH_DURATION = 5
match_start_time = None
not_match_start_time = None

cv2.namedWindow("Face Recognition", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Face Recognition", cv2.WND_PROP_TOPMOST, 1)

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for face_encoding, face_location in zip(face_encodings, face_locations):
        face_distance = face_recognition.face_distance([reference_encoding], face_encoding)
        match_percent = (1 - face_distance[0]) * 100

        top, right, bottom, left = [v * 4 for v in face_location]

        if match_percent >= 50:
            not_match_start_time = None
            if match_start_time is None:
                match_start_time = cv2.getTickCount() / cv2.getTickFrequency()

            elapsed = (cv2.getTickCount() / cv2.getTickFrequency()) - match_start_time

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, f"{match_percent:.2f}% Match", (left, top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            if elapsed >= MATCH_DURATION:
                print("Face verified.")
                video_capture.release()
                cv2.destroyAllWindows()

                # ✅ Check if already voted
                if os.path.exists("voted_users.txt"):
                    with open("voted_users.txt", "r") as f:
                        voted = f.read().splitlines()
                else:
                    voted = []

                if image_name in voted:
                    print("You have already voted.")
                    exit()

                # ✅ Send VERIFIED to Arduino to unlock voting
                ser.write(b'VERIFIED\n')
                print("Verification sent. Waiting for vote from Arduino...")

                while True:
                    if ser.in_waiting > 0:
                        vote = ser.readline().decode('utf-8').strip().upper()
                        if vote in ['A', 'B', 'C', 'D']:
                            print(f"Vote received: Candidate {vote} (including NOTA if D)")

                            # Save the vote
                            with open("votes.txt", "a") as file:
                                file.write(f"{image_name}: Candidate {vote}\n")

                            # Mark as voted
                            with open("voted_users.txt", "a") as f:
                                f.write(image_name + "\n")

                            print("Vote recorded successfully. Thank you for voting!")
                            exit()
                        else:
                            print(f"Invalid input received from Arduino: {vote}")

        else:
            match_start_time = None
            if not_match_start_time is None:
                not_match_start_time = cv2.getTickCount() / cv2.getTickFrequency()

            elapsed = (cv2.getTickCount() / cv2.getTickFrequency()) - not_match_start_time

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(frame, f"{match_percent:.2f}% No Match", (left, top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            if elapsed >= MATCH_DURATION:
                print("Face not recognized.")
                video_capture.release()
                cv2.destroyAllWindows()
                exit()

    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
