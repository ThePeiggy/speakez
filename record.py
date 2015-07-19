import __future__
import pyaudio
import wave


CHUNK = 14700 
FORMAT = pyaudio.paInt16 #paInt8
CHANNELS = 2
RATE = 44100 #sample rate
RECORD_SECONDS = 2
THRESHOLD = 500
#WORD_LENGTH = 0
#WAVE_OUTPUT_FILENAME = "output"



def trim(snd_data):
    "Trim the blank spots at the start and end"
    def _trim(snd_data):
        snd_started = False
        r = array('h')

        for i in snd_data:
            if not snd_started and abs(i)>THRESHOLD:
                snd_started = True
                r.append(i)

            elif snd_started:
                r.append(i)
        return r

    # Trim to the left
    snd_data = _trim(snd_data)

    # Trim to the right
    snd_data.reverse()
    snd_data = _trim(snd_data)
    snd_data.reverse()
    return snd_data

def is_silent(snd_data):
  return max(snd_data) < THRESHOLD

p = pyaudio.PyAudio()

wordsdict = {'tomorrow': ['to','mo','rrow'] , 
      'she': ['she'],
      'knee': ['knee'],
      'home':['ho','me'] }

word = str(raw_input('Enter word to consider: '))
word_arr = wordsdict[word]
WORD_LENGTH = len(word_arr)
#print WORD_LENGTH
print ("The word is " + word)
rec = raw_input("Speak the highlighted portion of the word when prompted.")

if (rec == ''):
  stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK) #buffer

frames = []

for section in range(0,WORD_LENGTH):
  for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    #print i
    if (i == 0):
      left = ''
      for j in range(0,WORD_LENGTH):
        if (j == section):
          left += word_arr[j].upper() + " "
        else:
          left += word_arr[j] + " "
      print left
    frames.append(data) # 2 bytes(16 bits) per CHANNELS
  frames = trim(frames)
  wf = wave.open(word_arr[section]+".wav",'wb')
  wf.setnchannels(CHANNELS)
  wf.setsampwidth(p.get_sample_size(FORMAT))
  wf.setframerate(RATE)
  wf.writeframes(b''.join(frames))

  wf.close()
  frames = []



"""for i in range(0, int(RATE / CHUNK * WORD_LENGTH * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    #print i
    if (i % 3 == 0):
      #print int(RATE / CHUNK * WORD_LENGTH * RECORD_SECONDS)
      #print i/3
      left = ''
      for j in range(i/3,len(word_arr)):
        left += word_arr[j]
      print(left)
    frames.append(data) # 2 bytes(16 bits) per channel"""


stream.stop_stream()
stream.close()
p.terminate()

#wf = wave.open(WAVE_OUTPUT_FILENAME+"-"+word+".wav", 'wb')
wf = wave.open(word+".wav",'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()