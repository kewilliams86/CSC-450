import warnings
warnings.filterwarnings("ignore")
from pandas import DataFrame
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.metrics import classification_report

def getData():
    line = ""
    corpus = {
        "abstract_and_title" : [],
        "disease" : []
        }
    with open("all_file_terms.txt") as file:
        for i in range(100000):
            line = file.readline()
            line = line.split("\t")
            #print(line[2])
            abstract_title = line[0]+" "+line[1]
            disease = line[2]
            corpus["abstract_and_title"].append(abstract_title.strip())
            corpus["disease"].append(disease.strip())
    print("Processing %d abstract-disease pairs." % len(corpus["abstract_and_title"]))
    return corpus

def formatData(dataFrame):
    cv = CountVectorizer(strip_accents="ascii", token_pattern=u"(?ui)\\b\\w*[a-z]+\\w*\\b", lowercase=True, stop_words="english")

    abstracts = cv.fit_transform(dataFrame['abstract_and_title'])

    x_train, x_test, y_train, y_test = train_test_split(dataFrame["abstract_and_title"], dataFrame["disease"], train_size=0.8, random_state = 1)


    x_train_cv = cv.fit_transform(x_train)
    x_test_cv = cv.transform(x_test)
 

    return x_train_cv, x_test_cv, y_train, y_test, x_train


def printTransform(ab) :
    ab = [ab]
    abstract_cv = cv.fit_transform(ab)
    print(abstract_cv)



def results(predictions, y_test):
    print("Accuracy score:", accuracy_score(y_test, predictions))
    #Total correct(TP+TN) / total
    print("Precision score:", precision_score(y_test, predictions, average="weighted"))
    #(TP) / (TP/FP) [Preportion of predicted positives that are correct]
    print("Recall score: ", recall_score(y_test, predictions, average="weighted"))
    #(TP) / (TP+FN) [Preportion of positives that are correctly preficted)

def predict(abstract, NB, x_train):
    cv = CountVectorizer(strip_accents="ascii", token_pattern=u"(?ui)\\b\\w*[a-z]+\\w*\\b", lowercase=True, stop_words="english")

    cv.fit(x_train)
    featureNames = cv.get_feature_names()
    train_dtm = cv.transform(x_train)
    
    test_dtm = cv.transform(abstract)

    dd = DataFrame(test_dtm.toarray(), columns = featureNames)
    #print(dd)
    #return dd

    prediction = NB.predict(test_dtm)
    return prediction



#cv = CountVectorizer(strip_accents="ascii", token_pattern=u"(?ui)\\b\\w*[a-z]+\\w*\\b", lowercase=True, stop_words="english")

#abstract = 'Lung cancer is a disease of the lung'    
#abstract_cv = cv.fit_transform(abstract)
#abstract_cv.reshape(1,-1)
#prediction = NB.predict(abstract_cv)
    



def main():
    corpus = getData()
    dataFrame = DataFrame(data=corpus)
    x_train_cv, x_test_cv, y_train, y_test, x_train = formatData(dataFrame)

    naive_bayes = MultinomialNB(fit_prior = False)
    fitData = naive_bayes.fit(x_train_cv, y_train)
    predictions = naive_bayes.predict(x_test_cv)
    results(predictions, y_test)


    from collections import Counter
    c = Counter(y_train)
    from operator import itemgetter
    l = [ (key,value) for key,value in c.items()]
    c = sorted(l, key = itemgetter(1), reverse = True)


    #vals = list(c.keys())
    ##counts = list(c.values())
    #d = {'disease':, 'frequency':counts}

    c= DataFrame(c)
    #print(c)
    #print(x_test_cv)


    #print(classification_report(predictions, y_test))

    #dd = predict(["We are studying lung diseases but not lung cancer"], naive_bayes, x_train)
    #print(dd)

main()
input("<Enter to close>")

#Questions:
#Recall and precision score averages
#Balanced Accuracy
#Macro (But remove small classes)
#KFold
