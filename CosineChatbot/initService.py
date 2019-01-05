import json

from flask import Flask, jsonify, request
app = Flask(__name__)
#app.config['SERVER_NAME'] = "http://mitra.calibehr.com/Webservices12/:5000"

import createModel    # To Initialize the Model class, so that only one instance is created

# Global Variables to store -----------------------
INITIALIZED = False
MODEL = ''
CHATBOT = " "
PAST_QUESTIONS = []
PAST_QUESTIONS_VECTORS = []
PAST_ANSWERS = []
#------------------------------------------------------
@app.route('/MitraChatService', methods=['GET','POST'])       #Default page
def chatMitraApp():

    mChatBot = createModel.CreateModel()


    # Need to commented ************
    quesText = "Wrong information in my esic card"

    queryType = 0

    #*****************************************

    # To send the response to Mitra ----------------------


    if request.method == 'POST':

        quesText = request.form['question']
        defaultAnswer = 0

        quesText = str(quesText)
        quesText = quesText.strip()
        quesText = ' '.join(quesText.split())


    # To check for a valid question -------------------------
    if quesText == '':
        print("Iffffff")
        strMessage = "Please enter a valid question."
        strSucess = 0
        staticAnswer = ''

    else:
        print("Elseeeee")
        strMessage = "Got answer to user question"
        strSucess = 1

        # To get the response of Question --------------------
        staticAnswer = mChatBot.getRelevantAnswer(quesText)

        if staticAnswer == "Default Answer":
            staticAnswer = "We have sent your request to concerned team, you will hear from us in 2 business days."
            defaultAnswer = 1
        else:
            defaultAnswer = 0

        print("staticAnswer = ", staticAnswer)

    data = {'type': strSucess, 'message': strMessage, 'staticAnswer': staticAnswer, 'defaultAnswer': defaultAnswer}

    print("data = ", data)

    return json.dumps(data)


#----------------------------------------------------------
#App Call
#----------
if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host='0.0.0.0', debug=True)   #So that the changes are reflected directly on server

#------------------------------------------------------------
