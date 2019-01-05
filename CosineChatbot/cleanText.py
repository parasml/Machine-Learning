from nltk.tokenize import word_tokenize

from nltk.corpus import words     #To get all english words

from autocorrect import spell    #To get the correct spelling word.

from nltk.stem import PorterStemmer

import re

#----------------------------------------------------------------------------
# Global Constant
#-------------------

STANDARD_WORDS = ['pf', 'uan', 'esic', 'kyc', '16', 'id', 'doj', 'd.o.j', 'f&f', 'tic', 'exp', 'mitra', 'sampark', 'app', "can't", "didn't", "haven't"]

ACRONYM_WORDS = {'provident fund': 'pf',
'employee provident fund': 'pf',
'Universal Account Number': 'uan',
'full and final': 'f&f',
'full & final':'f&f',
'need':'request',
'provide': 'request',
'want':'request',
'require':'request',
'download':'request',
'mob':'mobile',
'num': 'number',
'incorrect':'wrong',
'info': 'information',
'date of join': 'doj',
'date of joining': 'doj',
'date joining': 'doj',
'd.o.j': 'd.o.j',
'joining date': 'doj'
}

STOPWORDS =  ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll",
              "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's",
              'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
              'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was',
              'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'doing', 'a', 'an', 'the',
              'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against',
              'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out',
              'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all',
              'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'nor', 'only', 'own', 'same',
              'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll',
              'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'doesn', "doesn't", 'hadn',
              "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn',
              "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]


def cleanQuestions(arrQuestions):

    #print("arrQuestions = ", arrQuestions)
    txtQuest = []

    for strText in arrQuestions:
        # print("x = ", str(strText))

        strText = str(strText)


        strText = checkForPunctuation(strText)
        strTxt = checkForEnglishWords(strText)
        strText = checkForAcronym(strText)
        strText = removeStopWords(strText)
        #strText = StemmingSentences(strText)
        #print("strText = ", strText)
        txtQuest.append(strText)

    return txtQuest


#----------------------------------------------------------------------
# To replace the misspelled word
# ---------------------------------
def checkForEnglishWords(txtQuestion):

    # txtQuestion = "Where is my silary"

    txtWords = txtQuestion.split()

    # print("txtWords = ", txtWords)

    newText = []

    for x in txtWords:
        if x in words.words():
            # print("True")
            newText.append(x)
        elif x in STANDARD_WORDS:
            # print("True----------")
            newText.append(x)
        else:
            # print("False----------")
            newText.append(spell(x))

    # print("newText = ", newText)

    strText = ' '.join(newText)

    # print("strText *************************** = ", strText)

    return (strText)

# ------------------------------------------------------------------
# To check Acronym
# ---------------------
def checkForAcronym(strText):

    for txt in ACRONYM_WORDS.keys():
        find = r"\b" + re.escape(txt) + r"\b"

        # strText = strText.replace(txt, ACRONYM_WORDS.get(txt))  #This replaces substring also

        strText = re.sub(find, ACRONYM_WORDS.get(txt), strText)
        # print(re.sub(r"\bis\b", "je", x))

    return strText

# ----------------------------------------------------------------
# Check for Punctuation
# ------------------------
def checkForPunctuation(strText):

    # strText = "string. With. Punctuation?"
    strText = re.sub(r'[^\w\s]', '', strText)
    strText = strText.strip()
    strText = strText.lower()

    #print("Punctuation ----------------", strText)
    return strText

# ----------------------------------------------------------------
# To lemmitaize words
# ---------------------
def StemmingSentences(strText):
    # create an object of class PorterStemmer
    porter = PorterStemmer()

    strText = porter.stem(strText)

    return strText

# ----------------------------------------------------------------------
# To replace the misspelled word
# ---------------------------------
def checkForEnglishWords(txtQuestion):

    # txtQuestion = "Where is my silary"

    txtWords = txtQuestion.split()

    # print("txtWords = ", txtWords)

    newText = []

    for x in txtWords:
        if x in words.words():
            # print("True")
            newText.append(x)
        elif x in STANDARD_WORDS:
            # print("True----------")
            newText.append(x)
        else:
            # print("False----------")
            newText.append(spell(x))

    # print("newText = ", newText)

    strText = ' '.join(newText)

    # print("strText *************************** = ", strText)

    return (strText)

# ------------------------------------------------------------------
# To check Acronym
# ---------------------
def checkForAcronym(strText):

    for txt in ACRONYM_WORDS.keys():
        find = r"\b" + re.escape(txt) + r"\b"

        # strText = strText.replace(txt, ACRONYM_WORDS.get(txt))  #This replaces substring also

        strText = re.sub(find, ACRONYM_WORDS.get(txt), strText)
        # print(re.sub(r"\bis\b", "je", x))

    return strText

# ----------------------------------------------------------------
# Check for Punctuation
# ------------------------
def checkForPunctuation(strText):

    # strText = "string. With. Punctuation?"
    strText = re.sub(r'[^\w\s]', '', strText)
    strText = strText.strip()
    strText = strText.lower()

    #print("Punctuation ----------------", strText)
    return strText

# ----------------------------------------------------------------
# To lemmitaize words
# ---------------------
def StemmingSentences(strText):
    # create an object of class PorterStemmer
    porter = PorterStemmer()

    strText = porter.stem(strText)

    return strText

# ----------------------------------------------------------
# To clean the Questions and then Feed to model
# -------------------------------------------------
def removeStopWords(txtQuestion):

    # word_tokens = word_tokenize(txtQuestion)
    word_tokens = txtQuestion.split()

    filtered_sentence = [w for w in word_tokens if not w in STOPWORDS]

    strText = ' '.join(filtered_sentence)

    '''
    strText = strText.replace(" .", "")
    strText = strText.replace(" n't", "n't")
    strText = strText.replace(" ,", ",")
    strText = strText.replace(" '", "'")
    '''

    # print("Clean Question -----------------------------")
    # print(strText)

    # -----------------------------------------------------------------

    return strText

#----------------------------------------------------------------------
def getQuestionsArray(arrQuestions):
    # print("arrQuestions = ", arrQuestions)
    txtQuest = []

    for strText in arrQuestions:

        strText = str(strText)

        txtQuest.append(strText)

    return txtQuest


#------------------------------------------------------------------------
def removeExtraSpaces(strText):
    strText = strText.strip()

    strText = re.sub("\s\s+", " ", strText)

    return strText
#--------------------------------------------------------------------------
# Initialize class
#-------------------
'''
oCleanText = cleanText()

txtQuest = []
for strText in txtQuestions:
    # print("x = ", str(strText))

    strText = checkForPunctuation(str(strText))
    strText = cleanQuestions(str(strText))
    strTxt = checkForEnglishWords(str(strText))
    strText = checkForAcronym(strText)
    # strText = StemmingSentences(strText)
    print("strText = ", strText)
    txtQuest.append(strTxt)
'''
