import json

from flask import Flask, jsonify, request
app = Flask(__name__)
#app.config['SERVER_NAME'] = "http://mitra.calibehr.com/Webservices12/:5000"

import translation     # Our PY file


#----------------------------------------------
@app.route('/text_translation', methods=['GET', 'POST'])       #Default page
def txtTranslation():

    # Need to commented ************
    #txtRegionalText = 'नमस्ते आप कैसे हैं, I am Prashan'
    txtRegionalText = "ஹலோ ஹொவ் ஆர் யு?"
    txtLang = "ta-IN"
    #*****************************************

    if request.method == 'POST':
        dataJSON = request.get_json(silent=True)
        txtRegionalText = dataJSON['text']
        txtLang = dataJSON['lang']



    resultObj = translation.getEnglishText(txtRegionalText, txtLang, "en")

    #strSucess = 1
    #strMessage = "Successfully translated data"

    #return jsonify(request.get_json())
    #return jsonify(dataJSON)
    #return jsonify({"text": "Hello World!!!"})


    #data = {'data': str(strEnglishTrans)}
    #print("resultObj = ", resultObj)
    data = {'type': resultObj['type'], 'message': resultObj['message'], 'data': resultObj['data']}
    #print("data = ", data)
    return json.dumps(resultObj)



#----------------------------------------------------------
#App Call
#----------
if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', debug=True)   #So that the changes are reflected directly on server
    #app.run(host=app.config['SERVER_NAME'], port=5000, debug=True)






#------------------------------------------------------------
#Proj Notes
#--------------
# Language Options
# 1) Hindi --> hi-IN
# 2) Tamil --> ta-IN
# 3) Telgu --> te-IN
# 4) Bengali --> bn-IN