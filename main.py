import cv2
import os
import numpy as np
import fitz
import denoise as dn
import staffRemoval as sr
import normalization as nor
import objectDetection as od
import stemCheck as sc
import function as fc
import recognition_modules as rm
import predict as pd
import scoreToMidi as stm
import mido
from mido import MidiFile, MidiTrack, Message, MetaMessage

# pdf to png
file_name = "testScore"
page_path = "./Input"

doc = fitz.open(f"{page_path}/{file_name}.pdf") # 업로드 된 파일
if not os.path.exists(f"{page_path}/{file_name}"):
    os.mkdir(f"{page_path}/{file_name}") # 파일의 각 페이지를 저장하기 위한 폴더
resource_path = f"{page_path}/{file_name}"
page_cnt = 0

for i, page in enumerate(doc):
    img = page.get_pixmap()
    img.save(f"{resource_path}/{i}.png") # 각 페이지 png 파일으로 저장
    page_cnt += 1

if not os.path.exists(f"{page_path}/{file_name}/crop"):
    os.mkdir(f"{page_path}/{file_name}/crop")

resource_path = f"{page_path}/{file_name}"
for i in range(page_cnt):
    img = cv2. imread(f"{resource_path}/{i}.png")
    dn.dnImg(img, f"{resource_path}/crop") # 페이지 내 악보 개수

# 파트별 악보 분리
box_cnt = len(os.listdir(f"{resource_path}/crop"))
if not os.path.exists(f"{page_path}/{file_name}/part"):
    os.mkdir(f"{page_path}/{file_name}/part")

for i in range(box_cnt):
    img = cv2. imread(f"{resource_path}/crop/{i}.png")
    dn.split_part(img, f"{resource_path}/part", i)

# 악보 데이터 인식
resource_path = f"{resource_path}/part"
part_num = len(os.listdir(resource_path))

for i in range (part_num):
    mid = MidiFile() # 새 MIDI 파일 생성
    mid.ticks_per_beat = 480

    track = MidiTrack()
    mid.tracks.append(track)

    bpm = 128 # BPM
    microseconds_per_beat = int(60000000 / bpm)

    track.append(MetaMessage('set_tempo', tempo=microseconds_per_beat))

    for j in range(box_cnt):
        words = pd.decode_score(f'{resource_path}/{i}/{j}.png', 
                        'C:/Users/SSAFY/Desktop/soyi/scoreRecognition/Models/semantic_model/semantic_model.meta', 
                        'C:/Users/SSAFY/Desktop/soyi/scoreRecognition/Data/vocabulary_semantic.txt')
        stm.word2midi(mid, track, words)
    
    if not os.path.exists(f"Output/midi"):
        os.mkdir(f"Output/midi")

    # MIDI 파일 저장
    mid.save(f'Output/midi/{file_name}_part{i}.mid')

# 악보 정규화
# img, staves = nor.normalization(img, staves)

# 객체 검출
# img, objects = od.objectDetection(img, staves)

# 음표 기둥 인식
# img, objects = sc.stem_check(img, objects)

# 정보 확인
# for i in range(len(objects)):
#     obj = objects[i]
#     line = obj[0]
#     stats = obj[1]
#     stems = obj[2]
#     direction = obj[3]
#     staff = staves[line*5: (line + 1) * 5]
#     print(line, stats, stems, direction)

# 음자리표 인식


# 조표 인식
# def recognition(img, staves, objects):
#     key = 0
#     time_signature = False
#     beats =[]
#     pitches = []

#     for i in range(1, len(objects)):
#         obj = objects[i]
#         line = obj[0]
#         stats = obj[1]
#         stems = obj[2]
#         direction = obj[3]
#         (x,y,w,h,area) = stats
#         staff = staves[line*5: (line+1)*5]
#         if not time_signature:
#             ts, temp_key = rm.recognize_key(img, staff, stats)
#             time_signature = ts
#             key += temp_key
#             if time_signature:
#                 fc.put_text(img, key, (x, y+h+fc.weighted(20)))
#         else:
#             pass

#         cv2.rectangle(img, (x,y,w,h), (255, 0, 0), 1)
#         # fc.put_text(img, i, (x,y-fc.weighted(30)))

#     return img, key, beats, pitches

# img, key, beats, pitches = recognition(img, staves, objects)

# 박자표 인식


# 출력
# cv2.imshow('image', img)
# k = cv2.waitKey(0)
# if(k==27):
#     cv2.destroyAllWindows()

