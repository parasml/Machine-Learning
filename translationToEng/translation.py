#-----------------------------------------------------
#Importing Modules
#-------------------
from textblob import TextBlob
from profanity import profanity
import json


#-----------------------------------------------------------------
#Function: To convert text
#--------------------------
def getEnglishText(strRegionalTxt, from_lang, to_lang):

    strRegionalTxt = AvoidCommonWords(strRegionalTxt, from_lang)
    #print("strRegionalTxt1 = ", strRegionalTxt1)

    print("Inside function getEnglishText")
    txtUser = TextBlob(strRegionalTxt)
    print("Detect Lang = ", txtUser.detect_language())

    #GetProperNouns(txtUser)

    strfrom_lang = from_lang[0:2].lower()
    print("strfrom_lang = ", strfrom_lang)

    if strfrom_lang == str(txtUser.detect_language()):
        strSucess = "1"
        strMessage = "Successfully translated data"
        strEngText = txtUser.translate(from_lang=from_lang, to=to_lang)
    elif strfrom_lang == 'hi-IN':
        strSucess = "0"
        strMessage = "please ask your question in Hindi only."
        strEngText = ""
    elif strfrom_lang == 'ta-IN':
        strSucess = "0"
        strMessage = "please ask your question in Tamil only."
        strEngText = ""
    elif strfrom_lang == 'te-IN':
        strSucess = "0"
        strMessage = "please ask your question in Telugu only."
        strEngText = ""
    elif strfrom_lang == 'bn-IN':
        strSucess = "0"
        strMessage = "please ask your question in Bengali only."
        strEngText = ""
    else:
        strSucess = "0"
        strMessage = "Sorry! I didn't get it."
        strEngText = ""


    # check Profanity of the converted text ------------------------------
    checkProfanity = profanity.contains_profanity(str(strEngText))

    print("checkProfanity = ", checkProfanity)
    print("strEngText = ", strEngText)

    if checkProfanity == True:
        strSucess = "0"
        strMessage = "No profanity please."
        strEngText = ""



    returnObj = {"type": strSucess, "message": strMessage, "data": str(strEngText)}

    return returnObj

#---------------------------------------------------------------------------
# To avoid common words from getting translated
#------------------------------------------------
def AvoidCommonWords(strRegionalTxt, lang):

    arrHindi = ['संपर्क', 'सम्पर्क', 'मित्रा']
    arrTamil = ['தொடர்பு', 'தொடர்பு', 'மித்ரா']
    arrBengali = ['যোগাযোগ', 'যোগাযোগ', 'মিত্র']
    arrTelgu = ['సంప్రదించండి', 'సంప్రదించండి', 'మిత్రా']

    arrEnglish = ['Sampark', 'Sampark', 'Mitra']

    arrWordsToBeReplaced = []
    if lang == 'hi-IN':
        arrWordsToBeReplaced = arrHindi
    elif lang == 'ta-IN':
        arrWordsToBeReplaced = arrTamil
    elif lang == 'te-IN':
        arrWordsToBeReplaced = arrTelgu
    elif lang == 'bn-IN':
        arrWordsToBeReplaced = arrBengali

    for x in range(len(arrWordsToBeReplaced)):

        if str(arrWordsToBeReplaced[x]) in strRegionalTxt:
            print("Yessssssssssssss = ", arrWordsToBeReplaced[x], " = ", arrEnglish[x])

            strRegionalTxt = strRegionalTxt.replace(str(arrWordsToBeReplaced[x]), arrEnglish[x])


    return strRegionalTxt

#---------------------------------------------------------------------------
# To avoid common words from getting translated
#------------------------------------------------
def AvoidCommonWords1(strRegionalTxt, lang):

    restrictedWords = ['sampark', 'Mitra']

    convertedWords = []

    for word in restrictedWords:

        txtUser = TextBlob(word)
        strEngText = txtUser.translate(from_lang='en', to=lang)
        print("strEngText = ", strEngText)

        if str(strEngText) in strRegionalTxt:
            print("Yessssssssssssss = ", str(strEngText), " = ", word)

            strRegionalTxt = strRegionalTxt.replace(str(strEngText), word)

    print('************* strRegionalTxt = ', strRegionalTxt)

    return strRegionalTxt




#----------------------------------------------------------------------------
# To get Proper Nouns
#----------------------
def GetProperNouns(txtUser):

    import nltk
    #chunked = nltk.ne_chunk('मेरा नाम आकाश है')
    #print("chunked = ", chunked)

    my_sent = "WASHINGTON -- In the wake of a string of abuses by New York police officers in the 1990s, Loretta E. Lynch, the top federal prosecutor in Brooklyn, spoke forcefully about the pain of a broken trust that African-Americans felt and said the responsibility for repairing generations of miscommunication and mistrust fell to law enforcement."

    print(nltk.ne_chunk(my_sent, binary=True))


    '''
    print("inside function proper nouns for -------------------------")
    #print(txtUser.tags)
    #print(txtUser.noun_phrases)
    #print(txtUser.pos_tags)
    print(txtUser.parse())

    NPChunker = nltk.RegexpParser(pattern)
    result = NPChunker.parse(sentence)

    result.draw()

    print("-----------------------")
    for tag in txtUser.tags:
        #print("tag = ", tag[1])
        if tag[1] == 'NNP':
            print("Noun = ", tag[0])
    '''

#--------------------------------------------------------------------
# Function Calls
#------------------

#txtRegionalText = 'मेरा पीएफ नहीं आया है'
#txtRegionalText = 'मेरा नाम आकाश है'
#txtRegionalText = 'मैं आकाश हूं, सम्पर्क में लॉगिन करने में सक्षम नहीं हूं'
txtRegionalText = 'मैं आकाश हूं, मित्रा में लॉगिन करने में सक्षम नहीं हूं'
#txtRegionalText = 'मैं आकाश हूं, Mitra में लॉगिन करने में सक्षम नहीं हूं'
txtLang = "hi-IN"
resultObj = getEnglishText(txtRegionalText, txtLang, "en")

#print("resultObj = ", resultObj)

