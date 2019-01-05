#--------------------------------------------------------------
# py_translator
#----------------
import googletrans
from googletrans import Translator
translator = Translator()
translator = Translator(service_urls=[
      'translate.google.com',
      'translate.google.co.kr',
    ])
print("translator = ", translator)
#txt = translator.translate('मेरा नाम आकाश है.', dest='en')
print(translator.translate('My name is', dest='es'))

#print("txt = ", txt)



#unicode('मेरा नाम आकाश है', "utf-8")
#--------------------------------------------------------------
# py_translator
#----------------
#from py_translator import Translator
#s = Translator().translate(text='मेरा नाम आकाश है', dest='en').text
#print("s = ", s)

#--------------------------------------------------------------

#----------------------------------------------------------------

#from mstranslate import MSTranslate

#kk = MSTranslate('client_id', 'client_secret')
#print(kk.translate('मेरा पीएफ नहीं आया है', 'en'))


# Data Cleaning------------
print()
