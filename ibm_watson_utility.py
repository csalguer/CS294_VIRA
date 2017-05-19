from __future__ import print_function
import sys
import os
import subprocess
import json
from watson_developer_cloud import TextToSpeechV1
import wave
import pyaudio


class IBMWatsonUtility(object):
    """docstring for IBMWatsonUtility"""
    def __init__(self):
        super(IBMWatsonUtility, self).__init__()
        self.TTS = TextToSpeechV1(
            username='6681dd9c-1d0d-42e9-bec4-d0cdbebe14d5',
            password='7A44PekScMqO',)


    def getVoices(self):
        jsonVoicesObj = self.TTS.voices()
        print(json.dumps(jsonVoicesObj, indent = 2))
        # return(json.load(jsonVoicesObj))


    def createSpokenWAV(self, text):
        try:
            winPath = os.path.join(os.getcwd(), 'resources\\temp\\output.wav')
            relPath = 'resources/temp/output.wav'
            with open(relPath, 'wb') as audio_file:
                audio_file.write(self.TTS.synthesize(text, accept='audio/wav',
                        voice="en-US_AllisonVoice"))
            print("Voice_synth: COMPLETE")
            return relPath
        except IOError:
            print("Error in voice_synth creation")
            return None


    def utter(self, text):
        assert text is not None
        path = self.createSpokenWAV(text)
        if path is None:
            print("[Error]: Couldn't find file location for temp utterance")
            return False
        print("Attempting to play: ", path)
        self.__playbackUtterance(path)
        return True




    #
    # NOTE:
    #   Private method, to be made public if creation of wav per utterance is
    #   Too expensive
    #
    def __playbackUtterance(self, pathname): 
        chunk_size = 1024  
        f = wave.open(pathname,"rb")
        p = pyaudio.PyAudio() 
        stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
                        channels = f.getnchannels(),
                        rate = f.getframerate(),
                        output = True)
        data = f.readframes(chunk_size)
        while data:  
            stream.write(data)
            data = f.readframes(chunk_size)
        stream.stop_stream()
        stream.close()
        p.terminate()


### EXAMPLE USAGE ###
def main():
    ibm = IBMWatsonUtility()
    ibm.getVoices()
    ibm.utter("Hello world")
    ibm.utter("MOBIUS FINAL FANTASY")
    ibm.utter("nosgoth")


if __name__ == "__main__":
    main()
