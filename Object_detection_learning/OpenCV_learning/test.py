import cv2
import matplotlib.pyplot as plt
import numpy as np

img=cv2.imread('guigui.jpeg')

cv2.imshow('image',img)
cv2.waitKey(1000)
cv2.destroyAllWindows()

def cv_show(name,img):
    cv2.imshow(name,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

print(img.shape)

img=cv2.imread('guigui.jpeg',cv2.IMREAD_GRAYSCALE)
print(img.shape)
cv_show('image2',img)