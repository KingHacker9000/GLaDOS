from os import path
from pydub import AudioSegment

# files                                                                         
src = "a2.mp3"
dst = "a2.wav"

# convert wav to mp3                                                            


def convert_to_wav(src, dst):
    sound = AudioSegment.from_mp3(src)
    sound.export(dst, format="wav")