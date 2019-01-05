import json

from flask import Flask, jsonify, request
app = Flask(__name__)
#app.config['SERVER_NAME'] = "http://mitra.calibehr.com/Webservices12/:5000"

import initializeChatbot    # To Initialize the chatbot class, so that only one instance is created

# Global Variables to store -----------------------
INITIALIZED = False
CHATBOT = " "
PAST_QUESTIONS = []
#------------------------------------------------------
@app.route('/chat_mitraApp', methods=['GET','POST'])       #Default page
def chatMitraApp():

    mChatBot = initializeChatbot.MitraChatBot()


    # Need to commented ************
    quesText = "I need my PF number"

    queryType = 0

    #*****************************************

    # To send the response to Mitra ----------------------


    if request.method == 'POST':

        queryType = int(request.form['queryIndex'])
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
        arrResponse = mChatBot.getResponse(quesText, queryType)

        staticAnswer = arrResponse[0]
        defaultAnswer = arrResponse[1]
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
