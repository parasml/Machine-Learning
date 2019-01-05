from chatterbot.logic import LogicAdapter

#import mitraServices  #To get the various services of Mitra


class MyLogicAdapter(LogicAdapter):
    print("Inside function MyLogicAdapter -----------------")


    def __init__(self, **kwargs):
        super(MyLogicAdapter, self).__init__(**kwargs)


    #-------------------------------------------------------------------------
    # True for processing the request and False for not
    #----------------------------------------------------
    def can_process(self, statement):

        #SetQueryCategory(statement)

        print("statement.response_list = ", statement)

        #return True
        if statement.text.__contains__('Hey Mike'):
            print("statement.text = ", statement.text)
            #if statement.text.startswith('Hey Mike'):
            return True
        else:
            return False


    def process(self, statement):
        import random
        print("Inside function Process -----------")
        # Randomly select a confidence between 0 and 1
        confidence = random.uniform(0, 1)

        # For this example, we will just return the input as output
        selected_statement = statement
        selected_statement.confidence = confidence

        return selected_statement


