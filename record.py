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



"""def trim(snd_data):
    "Trim the blank spots at the start and end"
    def _trim(snd_data):
        snd_started = False
        r = []

        for i in snd_data:
            if not snd_started and i>THRESHOLD:
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
    return snd_data"""

p = pyaudio.PyAudio()

# Dictionary of all words needed for the tonal dictonary
# Structure of the Dictionary(key = word containing tone(s) 
# value = array of tones for that word)
wordsdict = {'tomorrow': ['to','mo','rrow'] , 
      'she': ['she'],
      'knee': ['knee'],
      'home':['ho','me'] }

# Debugging input line to allow developer to test specific words in tonal dictionary
word = str(raw_input('Enter word to consider: ')).strip(" ")

# Array of tones within the word being considered
word_arr = wordsdict[word]

# Number of tones within tone array
WORD_LENGTH = len(word_arr)

#print WORD_LENGTH

# Inform user what word is to be shown for tonal recording
print ("The word is " + word)

# Instruction for user to only say the highlighted tone within the word
rec = raw_input("Speak the capitalized portion of the word when prompted.")

# Hitting "ENTER" begins the recording
if (rec == ''):
  stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK) #buffer

frames = []
#hframes = [h]

# For loop for each tone within the current word
for tone in range(0,WORD_LENGTH):
  # For loop for each recording segment of each tone
  for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    #hdata = [h,stream.read(CHUNK)]
    #print i

    if (i == 0):
      left = ''

      # For loop highlighting the specific tone being recorded currently
      # The tone in all caps is the tone being recorded
      for j in range(0,WORD_LENGTH):
        if (j == tone):
          left += word_arr[j].upper() + " "
        else:
          left += word_arr[j] + " "
      print left
    frames.append(data) # 2 bytes(16 bits) per CHANNELS
  #frames = trim(frames)

  # Save the tonal recording as the tone_name.wav
  wf = wave.open(word_arr[tone]+".wav",'wb')
  wf.setnchannels(CHANNELS)
  wf.setsampwidth(p.get_sample_size(FORMAT))
  wf.setframerate(RATE)
  wf.writeframes(b''.join(frames))
  wf.close()

  # Reset the recording in preparation for the next tone
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

"""#wf = wave.open(WAVE_OUTPUT_FILENAME+"-"+word+".wav", 'wb')
wf = wave.open(word+".wav",'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()"""