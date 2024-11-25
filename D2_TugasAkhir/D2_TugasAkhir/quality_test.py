import cv2
import numpy as np

def nothing(x):
    pass

# Membaca gambar
img = cv2.imread('Data_latih/busuk3.jpg')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Membuat jendela untuk trackbars
cv2.namedWindow('Trackbars')

# Membuat trackbars untuk mengatur batas bawah dan atas
cv2.createTrackbar('Lower H', 'Trackbars', 0, 179, nothing)
cv2.createTrackbar('Lower S', 'Trackbars', 0, 255, nothing)
cv2.createTrackbar('Lower V', 'Trackbars', 0, 255, nothing)
cv2.createTrackbar('Upper H', 'Trackbars', 179, 179, nothing)
cv2.createTrackbar('Upper S', 'Trackbars', 255, 255, nothing)
cv2.createTrackbar('Upper V', 'Trackbars', 255, 255, nothing)

while True:
    # Mendapatkan posisi trackbars
    lower_h = cv2.getTrackbarPos('Lower H', 'Trackbars')
    lower_s = cv2.getTrackbarPos('Lower S', 'Trackbars')
    lower_v = cv2.getTrackbarPos('Lower V', 'Trackbars')
    upper_h = cv2.getTrackbarPos('Upper H', 'Trackbars')
    upper_s = cv2.getTrackbarPos('Upper S', 'Trackbars')
    upper_v = cv2.getTrackbarPos('Upper V', 'Trackbars')

    # Mendefinisikan batas bawah dan atas
    lower_bound = np.array([lower_h, lower_s, lower_v])
    upper_bound = np.array([upper_h, upper_s, upper_v])

    # Membuat mask dan hasil
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    result = cv2.bitwise_and(img, img, mask=mask)

    # Menampilkan gambar asli, mask, dan hasil
    cv2.imshow('Original', img)
    cv2.imshow('Mask', mask)
    cv2.imshow('Result', result)

    # Break loop dengan menekan 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
