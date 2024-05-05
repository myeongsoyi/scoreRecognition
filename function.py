import numpy as np
import cv2

def weighted(value):
    standard = 10
    return int(value*(standard/10))

def closing(img):
    kernel = np.ones((weighted(5), weighted(5)), np.uint8)
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    return img

def put_text(img, text, loc):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, str(text), loc, font, 0.5, (255, 0, 0), 2)

def get_line(img, axis, axis_value, start, end, length):
    if axis:
        points = [(i, axis_value) for i in range(start, end)]
    else:
        points = [(axis_value, i) for i in range(start, end)]
    pixels = 0
    for i in range(len(points)):
        (y, x) = points[i]
        pixels += (img[y][x] == 255)
        next_point = img[y+1][x] if axis else img[y][x+1]
        if next_point == 0 or i == len(points) -1:
            if pixels >= weighted(length):
                break
            else:
                pixels = 0
    return y if axis else x, pixels

def get_center(y,h):
        return (y+y+h)/2

def stem_detection(img, status, length):
    (x, y, w, h, area) = status
    stems = []
    for col in range(x, x+w):
        end, pixels = get_line(img, 'VERTICAL', col, y, y+h, length)
        if pixels:
            if len(stems) == 0 or abs(stems[-1][0] + stems[-1][2] - col) >= 1:
                (x, y, w, h) = col, end-pixels + 1, 1, pixels
                stems.append([x, y, w, h])
            else:
                stems[-1][2] += 1
    return stems