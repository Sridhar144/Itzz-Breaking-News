from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from sklearn.model_selection import train_test_split
from joblib import load
import re
import string
# from sklearn.feature_extraction.text import TfidfVectorizer
data='C:/Users/Admin/Desktop/Web_Develop/NewsOrion/Notebooks/data.csv'
df = pd.read_csv(data)

# Extract the 'text' column as a pandas Series
x = df.loc[:, 'text']
y = df.loc[:, 'class']

# Convert the pandas Series to a list
x = x.tolist()
y = y.tolist()
vectorization = TfidfVectorizer()
# x = data["text"]
# y = data["class"]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.124582201)
xv_train = vectorization.fit_transform(x_train)

random_forest = load('C:/Users/Admin/Desktop/Web_Develop/NewsOrion/Notebooks/News-predictor.joblib')
LR = load('C:/Users/Admin/Desktop/Web_Develop/NewsOrion/Notebooks/News-predictor_LR.joblib')
DT = load('C:/Users/Admin/Desktop/Web_Develop/NewsOrion/Notebooks/News-predictor_DT.joblib')
gb = load('C:/Users/Admin/Desktop/Web_Develop/NewsOrion/Notebooks/News-predictor_GB.joblib')
def manual_testing(news):#ml tokenization vectorization work
    # vector = load('C:/Users/Admin/Desktop/Web_Develop/NewsOrion/Notebooks/vectorization.joblib')

    vector = load('C:/Users/Admin/Desktop/Web_Develop/NewsOrion/Notebooks/vectorization_temp.joblib')

    testing_news = {"text":[news]}
    new_def_test = pd.DataFrame(testing_news)
    new_def_test["text"] = new_def_test["text"].apply(wordopt)
    new_x_test = new_def_test["text"]
    new_xv_test = vector.transform(new_x_test)
    pred_LR = LR.predict(new_xv_test)
    pred_DT = DT.predict(new_xv_test)
    pred_GBC = gb.predict(new_xv_test)
    pred_RFC = random_forest.predict(new_xv_test)
    return pred_GBC, pred_LR, pred_DT, pred_RFC
    
    # return pred_LR, pred_DT, pred_GBC, pred_RFC


def wordopt(text):#word processing portion
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub("\\W"," ",text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    return text



# ml func