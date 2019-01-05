import chatbot_mitra
import Chatbot_Service


class MitraChatBot():
    chatbot = ""


    def __init__(self):

        if not Chatbot_Service.INITIALIZED:
            returnObj = chatbot_mitra.MitraChatbot()
            Chatbot_Service.CHATBOT = returnObj[0]  # To store the chatbot
            Chatbot_Service.PAST_QUESTIONS = returnObj[1]  # To store the past questions


            Chatbot_Service.INITIALIZED = True
            print("1111 self.chatbot initialized ----------------= ", self.chatbot)

        #self.chatbot = Chatbot_Service.CHATBOT
        #self.questions_data = Chatbot_Service.PAST_QUESTIONS

    def getResponse(self, txtUser, queryIndex):


        self.chatbot = Chatbot_Service.CHATBOT[queryIndex]
        self.questions_data = Chatbot_Service.PAST_QUESTIONS[queryIndex]

        print("self.chatbot = ", self.chatbot)

        #chatbot_mitra.setPastQuestions(self.questions_data)   #To set the past questions-----

        arrResponse = chatbot_mitra.getChatResponse(txtUser, self.chatbot)

        return arrResponse

        '''
        print("Type your question here...")
        while True:
            try:
                request = input('User: ')
                response = chatbot_mitra.getChatResponse(request, self.chatbot)
                print("Bot: ", response)
            # Press ctrl-c or ctrl-d to exit
            except (KeyboardInterrupt, EOFError, SystemExit):
                break
        '''

# -----------------------------------------------
# Initialize class
#--------------------

#mChatBot = MitraChatBot()
#print("mChatBot.chatbot = ", mChatBot.chatbot)


# -----------------------------------------------
# Get Response from class
#--------------------------
#txtUser = "Please share My pf account number"
#mChatBot.getResponse(txtUser)


#-----------------------------------------------








