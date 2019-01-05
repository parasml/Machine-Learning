#----------------------------------------------------------------------
# To create Model and save it
#------------------------------
import pandas as pd
import xlrd
from gensim.models import Word2Vec
import math

import initService
import cleanText
import getCosineDistance
import initService

#-----------------------------------------------------------------------
class CreateModel():

    questionsAvgVector = ''
    dtAnswers = ''
    model = ''

    def __init__(self):

        if not initService.INITIALIZED:

            print("Inside Inttttt function")

            #dtPastData = self.loadPastData()

            dtPastData = self.loadPastDataComplete()

            dtQuestions = dtPastData['Questions'].values.tolist()

            self.dtAnswers = dtPastData['Answers'].values.tolist()

            print("dtQuestions = ", dtQuestions)
            #print("dtAnswers = ", dtAnswers)

            arrCleanQuestions = cleanText.cleanQuestions(dtQuestions)

            print("arrCleanQuestions = ", arrCleanQuestions)

            self.model = self.textToVector(arrCleanQuestions)

            self.questionsAvgVector = getCosineDistance.getCosine(arrCleanQuestions, self.model)

            #arrQuest = cleanText.getQuestionsArray(dtQuestions)
            #self.questionsAvgVector = getCosineDistance.getCosine(arrQuest, self.model)

            #print("questionsAvgVector ====", questionsAvgVector)

            initService.MODEL = self.model
            initService.PAST_QUESTIONS_VECTORS = self.questionsAvgVector
            initService.PAST_ANSWERS = self.dtAnswers
            initService.INITIALIZED = True
        else:
            self.questionsAvgVector = initService.PAST_QUESTIONS_VECTORS
            self.dtAnswers = initService.PAST_ANSWERS
            self.model = initService.MODEL


    # Load Past Questions, single sheet------------------------------------------
    def loadPastData(self):

        data = pd.read_excel("C:/MachineLearning/Project/ChatBot/MitraChatbot/questions.xlsx")

        #print(data.head())

        return data

    # To Load all sheets of Past Questions------------------------------------------
    def loadPastDataComplete(self):

        xls = pd.ExcelFile("C:/MachineLearning/Project/ChatBot/MitraChatbot/questions.xlsx")
        xlsSheetName = xls.sheet_names

        frames = []
        data = pd.DataFrame()

        for i in range(0, len(xlsSheetName)):
            #print("i = ", i)
            sheet = xls.parse(i)
            frames.append(sheet)

        data = pd.concat(frames)
        #print(data.head())

        return data

    # Create Model -----------------------------------------------
    def textToVector(self, arrCleanQuestions):

        arrSentencesWords = []

        for txt in arrCleanQuestions:
            txtWords = txt.split()

            arrSentencesWords.append(txtWords)

        # train model
        model = Word2Vec(arrSentencesWords, min_count=1)

        # summarize the loaded model
        #print("model = ", model)

        # summarize vocabulary
        words = list(model.wv.vocab)
        #print("words = ", words)

        # access vector for one word ex: esic
        #print("model['esic'] = ", model['esic'])

        # save model
        model.save('model.bin')

        return model


    def getRelevantAnswer(self, txtUserQustion):

        strRelevantAnswer = ""

        arrQuestion = []

        arrQuestion.append(txtUserQustion)

        print("arrQuestion = ", arrQuestion)

        arrCleanQuestion = cleanText.cleanQuestions(arrQuestion)

        print("arrCleanQuestion = ", arrCleanQuestion)

        txtUserQuestion = arrCleanQuestion[0]   # Not cleaning up the User Question

        userQuestAvgVector = getCosineDistance.avg_sentence_vector(txtUserQustion.split(), self.model)

        #print("userQuestAvgVector = ", userQuestAvgVector)

        nIndex = getCosineDistance.getHighestSimilarity(self.questionsAvgVector, userQuestAvgVector)

        print("nIndex ------------------- = ", nIndex)
        #print(self.dtAnswers)
        #print(self.dtAnswers[int(nIndex)])

        if math.isnan(nIndex):
            strRelevantAnswer = "Default Answer"

        else:
            strRelevantAnswer = str(self.dtAnswers[int(nIndex)])

            strRelevantAnswer = cleanText.removeExtraSpaces(strRelevantAnswer)


        return strRelevantAnswer





'''
#-----------------------------------------------------------------
# Initialize class
#-------------------

oModel = CreateModel()
dtPastData = oModel.loadPastData()

dtQuestions = dtPastData[['Questions']].values.tolist()

dtAnswers = dtPastData[['Answers']].values.tolist()

#print("dtAnswers = ", dtAnswers)
'''


'''
mChatBot = CreateModel()


print("------------------------------------------")
txtUser = "Wrong information in my esic card"
mChatBot.getRelevantAnswer(txtUser)
'''