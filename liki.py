import cv2
import mediapipe as mp
import pyautogui

x1 = y1 = x2 = y2 = 0

# Initialize the webcam
webcam = cv2.VideoCapture(0)

# Initialize MediaPipe Hands solution
my_hands = mp.solutions.hands.Hands()

# Initialize the drawing utility from MediaPipe
drawing_utils = mp.solutions.drawing_utils

while True:
    # Capture frame from the webcam
    ret, image = webcam.read()
    
    # If the frame was not captured successfully, exit the loop
    if not ret:
        break
    
    # Flip the image for a mirror effect
    image = cv2.flip(image, 1)
    
    frame_height, frame_width, _ = image.shape
    
    # Convert the image from BGR (default OpenCV format) to RGB
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Process the RGB image to detect hands
    output = my_hands.process(rgb_image)
    
    # Extract the hand landmarks
    hands = output.multi_hand_landmarks
    
    # If hand landmarks are detected
    if hands:
        for hand in hands:
            # Draw the hand landmarks on the original image
            drawing_utils.draw_landmarks(image, hand, mp.solutions.hands.HAND_CONNECTIONS)
            landmarks = hand.landmark
            
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                
                # Draw a circle on the thumb tip (id == 4)
                if id == 4:
                    cv2.circle(img=image, center=(x, y), radius=8, color=(0, 255, 0), thickness=3)
                    x2 = x
                    y2 = y
                
                # Draw a circle on the index finger tip (id == 8)
                if id == 8:
                    cv2.circle(img=image, center=(x, y), radius=8, color=(0, 0, 255), thickness=3)
                    x1 = x
                    y1 = y

        # Calculate the distance between the thumb and index finger tips
        dist = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
        print(f"Distance: {dist}")  # Debug statement to check distance

        # Draw a line between the thumb and index finger tips
        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 5)
        
        # Adjust volume based on the distance
        if dist > 50:
            pyautogui.press("volumeup")
            print("Volume Up")  # Debug statement
        else:
            pyautogui.press("volumedown")
            print("Volume Down")  # Debug statement
                
    # Display the image with hand landmarks in a window
    cv2.imshow("Hand volume control using python", image)
    
    # Wait for a key press for 10ms
    key = cv2.waitKey(10)
    
    # If 'q' key is pressed, break the loop
    if key & 0xFF == ord('q'):
        break

# Release the webcam and destroy all OpenCV windows
webcam.release()
cv2.destroyAllWindows()
