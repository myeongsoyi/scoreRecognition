import function as fc

def recognize_key(img, staves, stats):
    (x, y, w, h, area) = stats
    ts_conditions = (
        staves[0] + fc.weighted(5) >= y >= staves[0] - fc.weighted(5) and
        staves[4] + fc.weighted(5) >= y + h >= staves[4] - fc.weighted(5) and
        staves[2] + fc.weighted(5) >= fc.get_center(y, h) >= staves[2] - fc.weighted(5) and
        fc.weighted(18) >= w >= fc.weighted(10) and
        fc.weighted(45) >= h >= fc.weighted(35) 
    )
    if ts_conditions:
        return True, 0
    else:
        stems = fc.stem_detection(img, stats, 20)
        if stems[0][0] - x >= fc.weighted(3):
            key = int(10*len(stems)/2)
        else:
            key = 100 * len(stems)
    return False, key