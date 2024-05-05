import function as fc

def stem_check(img, objects):
    for obj in objects:
        stats = obj[1]
        stems = fc.stem_detection(img, stats, 30)
        direction = None
        if len(stems) > 0:
            if stems[0][0] - stats[0] >= fc.weighted(5):
                direction = True
            else:
                direction = False
        obj.append(stems)
        obj.append(direction)

    for obj in objects:
        (x, y, w, h, area) = obj[1]
        if len(obj[2]):
            fc.put_text(img, len(obj[2]), (x, y+h+20))
    return img, objects