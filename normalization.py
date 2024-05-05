import cv2

def normalization(img, staves):
    avg_distance = 0
    standard = 10

    lines = int(len(staves)/5)
    for line in range(lines):
        for staff in range(4):
            staff_above = staves[line * 5 + staff][0]
            staff_below = staves[line *5 + staff + 1][0]
            avg_distance += abs(staff_above - staff_below)
    avg_distance /= len(staves) - lines

    height, width = img.shape
    weight = standard/avg_distance

    new_width = int(width * weight)
    new_height = int(height * weight)

    img = cv2.resize(img, (new_width, new_height))

    ret, img = cv2.threshold(img, 1227, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    staves = [x[0] * weight for x in staves]
    return img, staves