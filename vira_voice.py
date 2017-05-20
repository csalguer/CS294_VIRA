from __future__ import print_function
from gtts import gTTS
import sys
import os
import wave
import pyaudio

class VIRAVoiceBox(object):
	"""docstring for VIRAVoiceBox"""
	def __init__(self):
		super(VIRAVoiceBox, self).__init__()
		self.chunk_size = 1024  

	def utterPhrase(self, text):
	    assert text is not None
	    path = self.__createSpokenWAV(text)
	    if path is None:
	        print("[Error]: Couldn't find file location for temp utterance")
	        return False
	    print("Attempting to play: ", path)
	    self.__playbackUtterance(path)
	    return True

	def __createSpokenWAV(self, text):
	    try:
	        winPath = os.path.join(os.getcwd(), 'resources\\temp\\output.wav')
	        relPath = 'resources/temp/output.wav'
	       	gTTS(text, lang='en', slow=True).save(relPath)
	        return relPath
	    except Error:
	        print("Error in voice_synth creation")
	        return None

	def __playbackUtterance(self, pathname): 
		f = wave.open(pathname,"rb")
		p = pyaudio.PyAudio() 
		stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
						channels = f.getnchannels(),
						rate = f.getframerate(),
						output = True)
		data = f.readframes(self.chunk_size)
		while data:  
			stream.write(data)
			data = f.readframes(self.chunk_size)
		stream.stop_stream()
		stream.close()
		p.terminate()




def main():
	vb = VIRAVoiceBox()
	vb.utterPhrase("Choices are, One: Mobius Final Fantasy, Two: Tilt brush, Three: Bio shock")

if __name__ == '__main__':
	main()
		