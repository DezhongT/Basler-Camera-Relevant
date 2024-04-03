from pypylon import pylon
import cv2


camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
converter = pylon.ImageFormatConverter()

# converting to opencv bgr format
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

# design a big img
# 1200 x 800 x 3, 1200 x 1920 x 3

def mouse_callback(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Left mouse button clicked at ({x}, {y})")

while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    if grabResult.GrabSucceeded():
        # Access the image data
        image = converter.Convert(grabResult)
        img = image.GetArray()
        # print(img.shape)
        cv2.namedWindow('title', cv2.WINDOW_NORMAL)
        cv2.imshow('title', img)
        cv2.setMouseCallback('title', mouse_callback)

        k = cv2.waitKey(1)
        if k == 27:
            break
    grabResult.Release()
    
# Releasing the resource    
camera.StopGrabbing()

cv2.destroyAllWindows()
# demonstrate some feature access
# new_width = camera.Width.Value - camera.Width.Inc
# if new_width >= camera.Width.Min:
#     camera.Width.Value = new_width
#
# numberOfImagesToGrab = 100
# camera.StartGrabbingMax(numberOfImagesToGrab)
#
# while camera.IsGrabbing():
#     grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
#
#     if grabResult.GrabSucceeded():
#         # Access the image data.
#         print("SizeX: ", grabResult.Width)
#         print("SizeY: ", grabResult.Height)
#         img = grabResult.Array
#         print("Gray value of first pixel: ", img[0, 0])
#
#     grabResult.Release()
# camera.Close()
