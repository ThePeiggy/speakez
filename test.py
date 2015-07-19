def create_wordmap():
	wordmap = {"mo":"japsounds/mo.wav", "shi" : "japsounds/shi.wav"};
	return wordmap;

def create_speech(wordmap, sentence):
	speech_array = [];
	while len(sentence) > 0:
		found = False;
		for key, value in wordmap.iteritems():
			index = sentence.find(key);
			if index == 0:
				print key;
				found = True;
				seg = AudioSegment.from_wav(value);
				speech_array.append(seg);
				sentence = sentence[len(key):];
				break;

		if not found:
			print("Input Error");
			break;
	if len(speech_array) > 0:
		return sum(speech_array[1:], speech_array[0]);

	return None;



from pydub import AudioSegment
from pydub.playback import play

sentence = "moshimoshi";
wordmap = create_wordmap();
speech = create_speech(wordmap, sentence);
if speech != None:
	speech.export("speech.wav", format="wav");
else:
	print "Invalid Input";
