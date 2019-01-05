# Import Libraries

import requests
from bs4 import BeautifulSoup
import codecs
import html2text

import os
import sys
import pyttsx3

from gtts import gTTS


#---------------------------------------------------------
# To extract html page content
#--------------------------------
def extractPageContent(pageURL):
    page = requests.get(pageURL)
    #print("page = ", page.content)

    soup = BeautifulSoup(page.content, 'html.parser')

    #print(soup.prettify())

    return soup

#------------------------------------------------------
#To get the header
#-------------------
def getHeader():
    header = pageSoup.findAll("header")
    #print(header)

#-------------------------------------------------------
#To remove unwanted content from html page
#------------------------------------------
def removeNotContent():

    # Remove NAV (Breadcum)
    # ---------------------
    for x in pageSoup.findAll('ol', class_="breadcrumb"):
        x.decompose()


    # Remove Modal ( Top Menu)
    # ------------------------
    for x in pageSoup.findAll('div', class_="modal-content"):
        x.decompose()


    # Remove Navbar Modal ( Top Menu)
    # -------------------------------
    for x in pageSoup.findAll('nav', class_="navbar"):
        x.decompose()

    # Remove any button
    # -----------------
    for x in pageSoup.findAll('button', class_="btn"):
        x.decompose()

    # Remove any Image
    # -----------------
    for x in pageSoup.findAll('img', class_=""):
        x.decompose()

    # To remove all script Tags
    # -----------------------------
    for x in pageSoup.findAll('script'):
        x.decompose()

    # To remove # tags
    #----------------------------------
    for x in pageSoup.findAll('#'):
        x.decompose()

    # To remove hidden tags
    # ----------------------------------
    for x in pageSoup.findAll('li', class_="hide"):
        x.decompose()

    # To remove all href tags
    for a in pageSoup.findAll('a'):
        a.replaceWithChildren()


#------------------------------------------------
# To get the footer
# -----------------------
def getFooter():
    bottom = pageSoup.findAll("footer")
    #print("bottom = ", bottom)



#--------------------------------------------
# To Remove footer
#-------------------
def removeFooter():
    for x in pageSoup.findAll("footer"):
        x.decompose()



#---------------------------------------------
#To get final clean text
#-----------------------

def getCleanText():
    f = codecs.open("C:/MachineLearning/RD/Demo/TextToAudio/abc1.html", mode="w", encoding="utf-8")
    # soup.footer.decompose()
    f.write(pageSoup.prettify())
    f.close()

    # To convert html to txt
    # ---------------------------

    html = open("C:/MachineLearning/RD/Demo/TextToAudio/abc1.html").read()
    txt = html2text.html2text(html)

    # print(txt)

    # To write output file--------------
    file1 = open("C:/MachineLearning/RD/Demo/TextToAudio/output.txt", "w")  # write mode
    file1.write(txt)
    file1.close()

def getCleanText1():

    txt = html2text.html2text(pageSoup.prettify())
    txt = txt.replace("#", "")
    txt = txt.replace("*", "")
    return txt

#------------------------------------------------------------------------------
# Save Google Audio
#--------------------
def SaveAudio():
    tts = gTTS(text=txtAudio, lang='en')
    tts.save("webAudio.mp3")
    print("Audio Saved-----")
    PlayAudio()


def PlayAudio():
    os.system("webAudio.mp3")
#-------------------------------------------------------------------------------
# To play teh Audio
# ---------------------
def getAudioEngine():

    #engine = pyttsx3.init("sapi5", debug=True)
    engine = pyttsx3.init()
    print("engine = ", engine)
    # To change the rate of audio
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 10)

    # To change the voice to female
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # changing index changes voices but ony 0 and 1 are working here

    return engine


#--------------------------------------
# To play the clean text
#------------------------
def startAudio():
    audioEngine.say(txtAudio)
    audioEngine.runAndWait()
    #audioEngine.startLoop()

    print("Audio playing.....")

#----------------------------------------
# To stop the audio
#--------------------
def endAudio():
    audioEngine.endLoop()








#--------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
#Function Calls
#----------------

pageSoup = extractPageContent("https://www.calibehr.com/insight/#pills-process")

getHeader()

removeNotContent()

removeFooter()

#getCleanText()

txtAudio = getCleanText1()

print("-----------------------------")
print("txtAudio = ", txtAudio)

audioEngine = getAudioEngine()

#startAudio()

#SaveAudio()  # To store the Audio file as mp3, to be uncommented