# Chatbot using chatterBot class
#---------------------------------
from chatterbot import ChatBot

#creating a new ChatterBot instance
#The only required parameter for the ChatBot is a name. This can be anything you want.

#chatbot = ChatBot("Ron Obvious", read_only=True)


#----------------------------------------------------------------
# Using Logical Adapters
#-------------------------

chatbot = ChatBot("Training Example", read_only=False,
                  logic_adapters=[
                    {
                        'import_path': 'chatterbot.logic.BestMatch'
                    },
                    {
                        'import_path': 'chatterbot.logic.SpecificResponseAdapter',
                        'input_text': 'Help me!',
                        'output_text': 'Ok, here is a link: http://chatterbot.rtfd.org'
                    },
                    {
                        'import_path': 'adapter_mitra.MyLogicAdapter'
                    }

                ])

#_----------------------------------------------------------------------
# To change the Max words in statement
#----------------------------------------
from chatterbot import constants
#constants.STATEMENT_TEXT_MAX_LENGTH = 2000;

print("constants.STATEMENT_TEXT_MAX_LENGTH = ", constants.STATEMENT_TEXT_MAX_LENGTH)

#------------------------------------------------------------------------
# Global Variables
#--------------------

'''
{
        'import_path': 'chatterbot.logic.LowConfidenceAdapter',
        'threshold': 0.45,
        'default_response': 'I am sorry, but I do not understand.'
    },
'''

#------------------------------------------------------------------------
# Tarining chatbot with ListTrainer
#-------------------------------------------
from chatterbot.trainers import ListTrainer

chatbot.set_trainer(ListTrainer)

'''
#conversation = [
chatbot.train([
    "Hello",
    "Hello, how can I help you today!",
    "Hi Sir",
    "Hi there!, how can I help you today?",
    "Hi Mam",
    "Hi there!, how can I help you today?",
    "How are you doing?",
    "I'm doing great.",
    "That is good to hear, how can I help you today?",
    "Salary Slip",
    "You can download your salary slip from 2nd Tab in Mitra App.",
    "Thank you.",
    "You're welcome."
])
'''

#------------------------------------------------------------------------------
# Tain the model with notepad data
#----------------------------------
def trainChatModel():

    import re
    f = open('C:/MachineLearning/RD/chatterBOT/Shadab-Excel/PF-Question.txt', 'r')

    train_data = []

    print("f = ", f)

    for line in f:
        m = re.search('(Q:|A:)?(.+)', line)
        if m:
            train_data.append(m.groups()[1])

    print(len(train_data))
    #print(train_data[43])
    chatbot.train(train_data)

    # chatbot.train(conversation)




#--------------------------------------------------------------
# To save the Model and reuse later
#-----------------------------------
import pickle

# save the model to disk
filename = 'C:/MachineLearning/Project/ChatBot/chatterBOT/model_MitraChatterBOT.pickle'
#pickle.dump(chatbot, open(filename, 'wb'))

#------------------------------------------------------------
# To get response from Chatbot
#-------------------------------
def getChatResponse(txtUser):
    print("User: ", txtUser)

    response = chatbot.get_response(txtUser)
    #response = self.chatterbot.get_response(txtUser, conversation.id)
    response_data = response.serialize()
    print("Bot: ", response)
    print("response_data: ", response_data)





# ----------------------------------------------------------



















#---------------------------------------------------------------


'''
print("Type your question here...")
while True:
    try:
        request = input('User: ')
        response = chatbot.get_response(request)
        print("Bot: ", response)
    # Press ctrl-c or ctrl-d to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        break

'''








'''
#----------------------
# Get Chatbot Responses
#-----------------------------------------------

response = chatbot.get_response("Good morning!")
print("response.confidence = ", response.confidence)
print("response.in_response_to = ", response.in_response_to)
print("response = ", response)
print("---------------------------------")

#------------------------------------------------
response = chatbot.get_response("That is good to hear")
print("response = ", response)
print("---------------------------------")
#------------------------------------------------
#Specific statemnet output
#--------------------------------
response = chatbot.get_response("Help me!")
print(response.in_response_to)
print(response)
print("----------------------------------")
#Contains the output
#--------------------------------
response = chatbot.get_response("Hey Mike")
print(response)
print("----------------------------------")
'''


