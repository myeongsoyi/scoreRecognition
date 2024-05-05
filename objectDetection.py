import cv2
import function as fc

def objectDetection(img, staves):

    closing_img = fc.closing(img)

    lines = int(len(staves)/5)
    object = []

    cnt, labels, stats, centroids = cv2.connectedComponentsWithStats(closing_img)

    for i in range(1, cnt):
        (x, y, w, h, area) = stats[i]
        if w>= fc.weighted(5) and h>= fc.weighted(5):
            center = fc.get_center(y, h)
            # cv2.rectangle(img, (x, y, w, h), (255, 0, 0), 1)
            # put_text(img, w, (x, y + h + 30))
            # put_text(img, h, (x, y + h + 60))
            # 
            # cv2.rectangle(img,(x,y,w,h),(255,0,0),1)
            for line in range(lines):
                area_top = staves[line*5] - fc.weighted(20)
                area_bot = staves[(line+1)*5-1] + fc.weighted(20)
                if area_top <= center <= area_bot:
                    object.append([line, (x, y, w, h, area)])

    object.sort()

    return img, object