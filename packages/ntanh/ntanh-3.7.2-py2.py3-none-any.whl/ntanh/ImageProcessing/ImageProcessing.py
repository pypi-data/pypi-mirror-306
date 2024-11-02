import cv2
import numpy as np 

def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result
 

def ImageInfomation(img):
    # Calculate the focus measure using Laplacian operator
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    focus_measure = cv2.Laplacian(gray, cv2.CV_64F).var()

    # Calculate the brightness using mean of pixel values
    brightness = cv2.mean(img)[0]

    # Calculate the contrast using standard deviation of pixel values
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    contrast = cv2.meanStdDev(gray)[1][0][0]

    # Calculate the sharpness using Laplacian of Gaussian operator
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    sharpness = cv2.Laplacian(blur, cv2.CV_64F).var()

    # Print the calculated parameters
    # print('Focus:', focus_measure)
    # print('Brightness:', brightness)
    # print('Contrast:', contrast)
    # print('Sharpness:', sharpness)
    return f"Focus:{round(focus_measure, 1)}, brightness:{round(brightness)}, contrast:{round(contrast)}, sharpness:{round(sharpness)}"

