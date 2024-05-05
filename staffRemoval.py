import denoise as dn
import cv2

def removeStaff(img):
    img1 = dn.threshold(img)

    height, width = img1.shape
    # histogram = np.zeros(img.shape, np.uint8)
    staves =[]

    for row in range(1, height):
        pixels = 0
        for col in range(width):
            # pixels += (img1[row][col] == 255)
            pixels += (img1[row][col] == 0)
        # for pixel in range(pixels):
        #     histogram[row][pixel] = 255
        if pixels > width * 0.5:
            if(len(staves)== 0 or abs(staves[-1][0] + staves[-1][1] - row) >= 1):
                staves.append([row, 1])
            else:
                staves[-1][1] += 1
            # for col in range(width):
            #     img[row][col] = 0;
    for staff in staves :
        top_pixel = staff[0]
        bot_pixel = staff[0] + staff[1] - 1

        for col in range(1, width):
            # if(img1[top_pixel-1][col]==0 and img1[bot_pixel+1][col] == 0):
            if(img1[top_pixel-1][col]==255 and img1[bot_pixel-1][col] == 255):
                for row in range(top_pixel, bot_pixel+1):
                    # img1[row][col] = 0
                    img1[row][col] = 255
    
    return img1, staves