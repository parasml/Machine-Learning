# Chatbot using chatterBot class
#---------------------------------
import createChatbotInstance

import os

questions_data = []
train_data = []

def MitraChatbot():

    #past_data = ["PF.txt", "Payroll.txt", "Onboarding.txt", "Insurance.txt", "Exit.txt"]
    #past_data = ["PF.txt", "Payroll.txt"]
    past_data = ["Onboarding.txt", "Insurance.txt", "Exit.txt"]

    nTotalChatBot = len(past_data)

    print("inside function MitraChatbot")


    # To clear previous chatter bot memory -----------------------

    arrChatBots = []
    arrQuestions = []

    for x in range(0, nTotalChatBot):

    # To remove past SQL lite past data files.
        try:
            strSQL_file = str("db.sqlite" + str(x+1))
            os.remove(strSQL_file)
        except:
            print("sqlite file is not present")


        chatBot = createChatbotInstance.getChatBot(x, past_data[x])

        arrChatBots.insert(x, chatBot[0])
        arrQuestions.insert(x, chatBot[1])
        #arrChatBots[x] = chatBot[0]
        #arrQuestions[x] = chatBot[1]

        #print("--------------------------------------------------------")
        #print(chatBot[1])

    return [arrChatBots, arrQuestions]




'''
#------------------------------------------------------------
# To get the past Questions
#---------------------------
def getPastQuestions():

    return questions_data

def setPastQuestions(questions_data):

    questions_data = questions_data

'''
#------------------------------------------------------------
# To get response from Chatbot
#-------------------------------
def getChatResponse(txtUser, chatbot):
    #print("User: ", txtUser)

    chatbot.read_only = True;

    txtUser = createChatbotInstance.cleanQuestions(txtUser)

    #txtUser = createChatbotInstance.checkForEnglishWords(txtUser)

    response = chatbot.get_response(txtUser)

    isDefaultAnswer = 0

    # To check for responses------------------------
    response = ToCheckIfAnsIsQues(str(response), questions_data)


    #-----------------------------------
    if str(response) == "Default Answer":
        response = "We have sent your request to concerned team, you will hear from us in 2 business days."
        isDefaultAnswer = 1

    elif str(response) == 'Did not got it':
        response = "Sorry I didn't get it. "
        isDefaultAnswer = 1


    arrResponse = [str(response), isDefaultAnswer]
    print("arrResponse = ", arrResponse)
    return arrResponse



    #response = self.chatterbot.get_response(txtUser, conversation.id)
    #response_data = response.serialize()
    #print("Bot: ", response)
    #print("response_data: ", response_data)


# ---------------------------------------------------------------------------
# To check if the got response is Question itself
#---------------------------------------------------
def ToCheckIfAnsIsQues(response, questions_data):

    #print("questions_data = ", questions_data)
    #print("response --------------  ", response)
    if str(response) in questions_data:
        print("iffffffffffffffffffffff")
        return "Default Answer"
    else:
        #print("Elseeeeeeeeeeeeeeeeeeee")
        return response












# -------------------------------------------------------------------------------------------
# *******************************************************************************************
# to be commented ( Function Calls )
#------------------
questions_data = []
returnObj = MitraChatbot()
chatbot = returnObj[0][1]
questions_data = returnObj[1][1]

print("chatbot = ", chatbot)
print("questions_data = ", questions_data)

#response = getChatResponse("ESIC/ Insurance card can be downloaded from 2nd tab on top of Mitra App.", chatbot)
#print("Bot: ", response)

chatbot.read_only = True;
#chatterbot.utils.remove_stopwords(tokens, language)
print("Type your question here...")
while True:
   try:
       request = input('User: ')

       request = createChatbotInstance.cleanQuestions(request)

       request = createChatbotInstance.checkForEnglishWords(request)

       #response = getChatResponse(request, chatbot)
       response = chatbot.get_response(request)

       # To check for responses------------------------

       response = ToCheckIfAnsIsQues(str(response), questions_data)

       print("Bot: ", response)

   # Press ctrl-c or ctrl-d to exit
   except (KeyboardInterrupt, EOFError, SystemExit):
       break


#---------------------------------------------------------------------
