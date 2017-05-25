import os
import sys
import wave

from gtts import gTTS
from playsound import playsound
import pyaudio


class VIRAVoiceBox(object):
	"""docstring for VIRAVoiceBox"""
	def __init__(self):
		super(VIRAVoiceBox, self).__init__()
		self.chunk_size = 1024  

	def utterPhrase(self, text):
	    assert text is not None
	    path = self.__createSpokenFile(text)
	    if path is None:
	        print("[Error]: Couldn't find file location for temp utterance")
	        return False
	    self.__playbackUtterance(path)
	    return True

	def __createSpokenFile(self, text, relPath='voice_files/output.mp3'):
		try:
			winRelPath = os.path.join(os.getcwd(), 'resources\\temp\\output.mp3')
			# relWavPath = 'voice_files/output.wav'
			gTTS(text, lang='en', slow=False).save(relPath)
			# rec = AudioSegment.from_mp3(relPath)
			# rec.export(relWavPath, format="wav")
			return relPath
		except:
			print("Error in voice_synth creation")
			return None

	def __playbackUtterance(self, pathname):
		print("Attempting to play: ", pathname)
		playsound(pathname)
		# buf = 3072
		# pygame.mixer.init()
		# fq, size, chn = pygame.mixer.get_init()
		# pygame.mixer.init(fq, size, chn, buf)
		# pygame.init()
		# pygame.mixer.init()
		# clock = pygame.time.Clock()
		# pygame.mixer.music.load(pathname)
		# pygame.mixer.music.play()
		# while True:
		# 	clock.tick(500)
		# 	print(clock)
		




def main():
	vb = VIRAVoiceBox()
	vb.utterPhrase("Choices are, One: Mobius Final Fantasy, Two: Tilt brush, Three: Bioshock, and finally Four: Faerie")

if __name__ == '__main__':
	main()
		