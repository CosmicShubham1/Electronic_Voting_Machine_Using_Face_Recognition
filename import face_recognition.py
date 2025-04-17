import face_recognition
import cv2
import os
import serial
import time

# 🔌 Connect to Arduino (Update COM port if needed)
ser = serial.Serial('COM3', 9600)
time.sleep(2)  # Wait for connection to stabilize

# 📂 Reference image input
image_folder = "./reference_photos"
image_name = input("Enter your image name (without extension): ")

# 📸 Search for valid image
image_path = None
for ext in [".jpg", ".jpeg", ".png"]:
    full_path = os.path.join(image_folder, image_name + ext)
    if os.path.exists(full_path):
        image_path = full_path
        break

if not image_path:
    print("❌ Image not found.")
    exit()

reference_img = face_recognition.load_image_file(image_path)
ref_encodings = face_recognition.face_encodings(reference_img)

if not ref_encodings:
    print("❌ No face found in reference image.")
    exit()

ref_encoding = ref_encodings[0]

# 🎥 Camera setup
video_capture = cv2.VideoCapture(0)
MATCH_DURATION = 5  # seconds of consistent match
match_start_time = None

print("📷 Show your face to the camera...")

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for face_encoding in face_encodings:
        distance = face_recognition.face_distance([ref_encoding], face_encoding)[0]
        match_percent = (1 - distance) * 100

        if match_percent >= 50:
            if match_start_time is None:
                match_start_time = time.time()
            elif time.time() - match_start_time >= MATCH_DURATION:
                print("✅ Face verified.")
                video_capture.release()
                cv2.destroyAllWindows()

                # ✅ Check if already voted
                voted_users = []
                if os.path.exists("voted_users.txt"):
                    with open("voted_users.txt", "r") as f:
                        voted_users = f.read().splitlines()

                if image_name in voted_users:
                    print("⚠️ You have already voted.")
                    exit()

                # Send "VERIFIED" to Arduino
                ser.write(b"VERIFIED\n")
                print("🕓 Waiting for vote from Arduino...")

                while True:
                    if ser.in_waiting > 0:
                        vote = ser.readline().decode().strip().upper()
                        if vote in ["A", "B", "C", "D"]:
                            print(f"🗳️ Vote received: Candidate {vote}")
                            with open("votes.txt", "a") as vf:
                                vf.write(f"{image_name}: Candidate {vote}\n")
                            with open("voted_users.txt", "a") as vf:
                                vf.write(image_name + "\n")
                            print("✅ Vote recorded. Thank you!")
                            exit()
                        else:
                            print(f"⚠️ Invalid vote received: {vote}")
        else:
            match_start_time = None  # Reset match timer if mismatch

    # Display camera feed
    cv2.imshow("Face Recognition", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
