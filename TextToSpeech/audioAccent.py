from gtts import gTTS

path = "C:/MachineLearning/RD/Demo/TextToSpeech/TestAudio/"
#---------------------------------------------------------------------------
# Generate English Audio
#-------------------------

file = open(path + "englishTxt.txt", "r", encoding="utf-8")
txtInput = file.read()

tts = gTTS(txtInput, lang='en')
tts.save('C:/MachineLearning/RD/Demo/TextToSpeech/TestAudio/englishAudio.mp3')


#---------------------------------------------------------------------------
# Genearate Hindi Audio
#-------------------------

#file = open(path + "hindiTxt.txt", "r", encoding="utf-8")
#txtInput = file.read()

#tts = gTTS(txtInput, lang='hi')
#tts.save('C:/MachineLearning/RD/Demo/TextToSpeech/TestAudio/hindiAudio.mp3')


#---------------------------------------------------------------------------
#Generate Tamil Audio
#---------------------

#file = open(path + "tamilTxt.txt", "r", encoding="utf-8")
#txtInput = file.read()

#tts = gTTS(txtInput, lang='en')
#tts.save('C:/MachineLearning/RD/Demo/TextToSpeech/TestAudio/tamilAudio.mp3')


#---------------------------------------------------------------------------


