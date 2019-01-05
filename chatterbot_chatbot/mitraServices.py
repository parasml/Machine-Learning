import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

class TextPreprocessing():


    #-------------------------------------------------------
    # To remove Stop Words
    #-----------------------
    def removeStopWords(statement):

        stop_words = set(stopwords.words('english'))

        word_tokens = word_tokenize(statement)

        filtered_sentence = [w for w in word_tokens if not w in stop_words]


        print("statement.lower() = ", statement.lower())
        print("stop_words = ", stop_words)
        print("filtered_sentence = ", filtered_sentence)

        return filtered_sentence


    #-----------------------------------------------------------------------
    #To Select Query Category
    #----------------------------

    def SetQueryCategory(arrStatWords):

        strStatemnt = ' '.join(arrStatWords)
        strCategory = 'other'

        print("Function SetQueryCategory = ", strStatemnt)

        arrSalary = ['Salary', 'slip', 'pay', 'income', 'Deduction', 'incentive', 'sallary', 'Sal']
        arrPF = ['UAN', 'pf', 'provident', 'fund']
        arrInsurance = ['ESIC', 'insurance', 'medical']

        '''
        result = any(elem in arrStatWords for elem in arrSalary)

        if result:
            print("Yes, list1 contains any elements of list2 = ", result)
        else:
            print("No, list1 contains any elements of list2 = ", result)
        '''

        for word in arrSalary:
            if word in strStatemnt:
                print("Yes Present")
                strCategory = 'salary'
                break;




#-------------------------------------------------------------------------
# Function Calls
#-------------------
strStatWords = TextPreprocessing.removeStopWords('My Salary has not come')

TextPreprocessing.SetQueryCategory(strStatWords)
