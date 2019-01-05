import numpy as np

from scipy import spatial

#-------------------------------------------------------------
# Average vector for all Questions
# --------------------------------------
def getCosine(txtQuest, model):


    index2word_set = set(model.wv.index2word)

    #print("index2word_set = ", index2word_set)

    sentence_1_avg_vector = []

    for sentence in txtQuest:
        avg_vector = avg_sentence_vector(sentence.split(), model)

        sentence_1_avg_vector.append(avg_vector)

    return sentence_1_avg_vector


def avg_sentence_vector(words, model):

    num_features = 100
    index2word_set = set(model.wv.index2word)

    #function to average all words vectors in a given paragraph
    featureVec = np.zeros((num_features,), dtype="float32")
    nwords = 0

    for word in words:
        if word in index2word_set:
            nwords = nwords+1
            featureVec = np.add(featureVec, model[word])

    if nwords>0:
        featureVec = np.divide(featureVec, nwords)


    return featureVec


# ---------------------------------------------------------------------------
# To get Cosine of all the sentences with new Question
# -------------------------------------------------------
def getHighestSimilarity(sentence_1_avg_vector, sentence_2_avg_vector):

    nHigestSim = 0
    nAnsIndex = float('nan')

    for x in range(0, len(sentence_1_avg_vector)):
        #print("---------------------------------", x)
        #print(sentence_1_avg_vector[x])

        sim = 1 - spatial.distance.cosine(sentence_1_avg_vector[x], sentence_2_avg_vector)
        #print("sim = ", sim)
        if sim > 0.50:

            #print("========", x)
            #print(sim)
            #print(txtQuestions[x])

            if sim > nHigestSim:
                nHigestSim = sim
                nAnsIndex = x
                print("nAnsIndex = ", nAnsIndex)


    return nAnsIndex
    # Note that spatial.distance.cosine computes the distance, and not the similarity.
    # So, you must subtract the value from 1 to get the similarity.


