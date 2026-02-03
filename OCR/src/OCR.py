import cv2
import easyocr
import numpy as np
from collections import deque

# --- Configuration ---
CAMERA_INDEX = 0
OCR_LANGUAGES = ['en']
DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 360
OCR_FRAME_INTERVAL = 5
CONFIDENCE_THRESHOLD = 0.5
ROI = (100, 260, 100, 540)  # (y1, y2, x1, x2) - adjust to fit text area
DEDUPLICATION_HISTORY = 10  # how many past texts to remember

# Initialize EasyOCR and webcam
reader = easyocr.Reader(OCR_LANGUAGES)
cap = cv2.VideoCapture(CAMERA_INDEX)
if not cap.isOpened():
    raise Exception("Could not open webcam")

print("Live OCR with ROI and de-duplication running. Press 'q' to quit.")

frame_count = 0
ocr_results = []
recent_texts = deque(maxlen=DEDUPLICATION_HISTORY)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame.")
        break

    # Resize and convert to grayscale
    frame_resized = cv2.resize(frame, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
    gray = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)

    # Extract ROI
    y1, y2, x1, x2 = ROI
    gray_roi = gray[y1:y2, x1:x2]

    frame_count += 1

    # Perform OCR at intervals
    if frame_count % OCR_FRAME_INTERVAL == 0:
        ocr_results = reader.readtext(gray_roi)

    # Draw ROI box
    cv2.rectangle(frame_resized, (x1, y1), (x2, y2), (255, 0, 0), 2)

    # Process and draw OCR results
    for (bbox, text, confidence) in ocr_results:
        if confidence > CONFIDENCE_THRESHOLD and text.strip():
            (tl, tr, br, bl) = bbox
            tl = (int(tl[0] + x1), int(tl[1] + y1))
            br = (int(br[0] + x1), int(br[1] + y1))

            if text not in recent_texts:
                print(f"Detected NEW: '{text}' (conf: {confidence:.2f})")
                recent_texts.append(text)

            cv2.rectangle(frame_resized, tl, br, (0, 255, 0), 2)
            cv2.putText(frame_resized, f"{text} ({confidence:.2f})", (tl[0], tl[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

    # Display output
    cv2.imshow("Train Car OCR - EasyOCR", frame_resized)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
