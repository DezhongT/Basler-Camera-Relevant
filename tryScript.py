import cv2
import numpy as np

video_path = "playVideo.mp4"

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Couldn't open the video file")

def mouse_callback(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        col_idx = x // 120
        row_idx = y // 80
        print(f"row idx is {row_idx}, col idx is {col_idx}")
        if (row_idx, col_idx) in Zoom_idx:
            Zoom_idx.remove((row_idx, col_idx))
        else:
            Zoom_idx.append((row_idx, col_idx))

# create a 8 x 12 grid
frames = []
Zoom_idx = []
clean_frames = []

count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    big_frame = np.zeros((960, 1920, 3), dtype = np.uint8)
    # arrange all frames
    count = count % 96
    # 1920 x 960, 80 x 120
    resized_frame = cv2.resize(frame, (120, 80), interpolation=cv2.INTER_AREA)
    frames.append(resized_frame)
    clean_frames.append(frame)
    if len(frames) > 96:
        del frames[0]
        del clean_frames[0]
    # add color to the zoomed-in boundary
    # for row_idx, col_idx in Zoom_idx:
    #     idx = row_idx * 8 + col_idx
    #     if frames[idx] is not None:

    for n, frame in enumerate(frames):
        row_idx = n//8
        col_idx = n%8
        frame = frame.copy()
        if (row_idx, col_idx) in Zoom_idx:
            height, width, _ = frame.shape
            color = (0, 255, 0)  # Green color
            frame = cv2.rectangle(frame, (0, 0), (width-1, height-1), color, thickness=2)
        if frame is not None:
            big_frame[row_idx*80:(row_idx+1)* 80, col_idx * 120:(col_idx+ 1) * 120] = frame

    # add zoomed-in image (960, 960)
    num_img = len(Zoom_idx)
    # define the grid (960, 640)
    if num_img == 1:
        for row_idx, col_idx in Zoom_idx:
            idx = row_idx * 8 + col_idx
            frame = clean_frames[idx]
            resized_frame = cv2.resize(frame, (960, 640), interpolation=cv2.INTER_AREA)
            height, width, _ = resized_frame.shape
            color = (0, 255, 0)  # Green color
            resized_frame = cv2.rectangle(resized_frame, (0, 0), (width-1, height-1), color, thickness=2)
            big_frame[160:160+640, 960:] = resized_frame

    if num_img == 2:
        # (480, 960)
        for n, idx in enumerate(Zoom_idx):
            row_idx = idx[0]
            col_idx = idx[1]
            idx = row_idx * 8 + col_idx
            frame = clean_frames[idx]
            resized_frame = cv2.resize(frame, (720, 480), interpolation=cv2.INTER_AREA)
            height, width, _ = resized_frame.shape
            color = (0, 255, 0)  # Green color
            resized_frame = cv2.rectangle(resized_frame, (0, 0), (width-1, height-1), color, thickness=2)
            big_frame[n*480:(n+1)*480, 960+120:960+120+720] = resized_frame




    count += 1
    cv2.imshow("Video", big_frame)
    cv2.setMouseCallback("Video", mouse_callback)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
