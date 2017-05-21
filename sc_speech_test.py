from spell_corrector import SpellCorrector
from steam_utility import SteamUtility
import speech_recognition as sr

def main():
	app_data_dir =  '/Users/Ikechi/Library/Application Support/Steam/SteamApps/common'
	stmUtil = SteamUtility(app_data_dir)
	appNames = stmUtil.getAllApps()
	sc = SpellCorrector(appNames)
	rec = sr.Recognizer()
	with sr.Microphone() as source:
		print "What would you like to play?"
		audio = rec.listen(source)
		print "Done! Sending..."


	try:
		print rec.recognize_google(audio)
		appName = sc.getClosestName(rec.recognize_google(audio))
		if appName:
			print("Okay, opening " + appName)
		else:
			print "Sorry, I could not understand what you said."
	except sr.UnknownValueError:
		print("Sorry, I didn't recognize what you said")
	except sr.RequestError as e:
		print("Could not request results from Google Speech Recognition service; {0}".format(e))



if __name__ == "__main__":
	main()