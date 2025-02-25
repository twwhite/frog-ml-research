import os

from ultralytics import YOLO
import cv2


VIDEOS_DIR = os.path.join('.', 'videos')

video_path = os.path.join(VIDEOS_DIR, "out2.mp4")
video_path_out = os.path.join(VIDEOS_DIR, "out2_out.mp4")
print(video_path)
cap = cv2.VideoCapture(video_path)
ret, frame = cap.read()
print(frame)
height, width, _ = frame.shape
out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc(*'mp4v'), 30, (width, height))

model_path = "./runs/detect/train/weights/best.pt"

model = YOLO(model_path)

threshold = 0.1


quadrant_coordinates_1 = (0, 0, width//2, height//2)
quadrant_coordinates_2 = (width//2, 0, width, height//2)
quadrant_coordinates_3 = (0, height//2, width//2, height)
quadrant_coordinates_4 = (width//2, height//2, width, height)

# Total frames in video:
count = 1
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
cotton_frames = 0
substrate_frames = 0
water_frames = 0
on_hide_frames = 0
in_hide_frames = 0


while ret:

    results = model(frame)[0]

    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        if score > threshold:

            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
            cv2.putText(frame, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

            # If the object is in the first quadrant
            if x1 < width//2 and y1 < height//2:
                cv2.putText(frame, "Cotton", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
                cotton_frames += 1
                

            # If the object is in the second quadrant
            if x1 > width//2 and y1 < height//2:
                cv2.putText(frame, "Substrate", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
                substrate_frames += 1

            # If the object is in the third quadrant
            if x1 < width//2 and y1 > height//2:
                cv2.putText(frame, "Water", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
                water_frames += 1

            # If the object is in the fourth quadrant
            if x1 > width//2 and y1 > height//2:
                cv2.putText(frame, "On_Hide", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
                on_hide_frames += 1

        else:
            cv2.putText(frame, "In_Hide", (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
        

        # Append summary percent of video in each quadrant in a single row at bottom of frame in smaller
        msg1 = f"C: {cotton_frames/count*100:.1f}% | S: {substrate_frames/count*100:.1f}% | W: {water_frames/count*100:.1f}%"
        msg2 = f"OH: {on_hide_frames/count*100:.1f}% | IH: {in_hide_frames/count*100:.1f}%"
        cv2.putText(frame, msg1, (10, height - 50),
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, msg2, (10, height - 20),
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Print progress
    print(f"Frame {count} / {length} ({count/length*100:.2f}%)")
    count += 1
    out.write(frame)
    ret, frame = cap.read()

cap.release()
out.release()
cv2.destroyAllWindows()