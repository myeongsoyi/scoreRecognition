import mido
from mido import MidiFile, MidiTrack, Message, MetaMessage
import Enums.note as note
import Enums.tick as tick

def word2midi(mid, track, words):

    # whole_note_ticks = mid.ticks_per_beat * 4 # 온 음표 틱 수
    # half_note_ticks = mid.ticks_per_beat * 2 # 2분 음표 틱 수
    # quater_note_ticks = mid.ticks_per_beat # 4분 음표 틱 수
    # eighth_note_ticks = mid.ticks_per_beat // 2  # 8분 음표 틱 수
    # sixteenth_note_ticks = mid.ticks_per_beat // 4  # 16분 음표 틱 수

    # for word in int2word:
    #     print(word, end='\n')

    time_since_last_event = 0
    velocity = 64

    for word in words:
        component_type = word.split('-')
        if component_type[0] == 'note':
            note_type = component_type[1].split('_')
            track.append(Message('note_on', note=getattr(note.notes,note_type[0]), velocity=velocity, time=float(time_since_last_event)))
            track.append(Message('note_off', note=getattr(note.notes,note_type[0]), velocity=velocity, time=float(mid.ticks_per_beat*getattr(tick.ticks, note_type[1]))))
            time_since_last_event = 0
        if component_type[0] == 'rest':
            time_since_last_event += float(getattr(tick.ticks,component_type[1]))

    # 패턴에 따라 메시지 추가
    # for i in range(len(pattern)):
    #     track.append(Message('note_on', note=notes[i], velocity=velocity, time=time_since_last_event[i]))
    #     track.append(Message('note_off', note=notes[i], velocity=velocity, time=(int)(pattern[i])))

    
