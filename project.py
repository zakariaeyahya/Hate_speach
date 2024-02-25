import pandas as pd
train = pd.read_csv("train.csv", delimiter=',')
print("train set ;" % train.columns ,train.shape , len(train))
test = pd.read_csv("test.csv", delimiter=',')
print("test set ;" % test.columns ,test.shape , len(test))
import re
def clean_text(df , text_field):
    df[text_field]=df[text_field].str.lower()
    df[text_field] = df[text_field].apply(lambda x: re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", x))
    return df
test_clean =clean_text(test,"tweet")
train_clean =clean_text(train,"tweet")

from sklearn.utils import resample
train_majority = train_clean[train_clean.label==0]
train_minority= train_clean[train_clean.label==1]
train_minority_upsampled = resample(train_minority,replace= True ,
                                     n_samples= len(train_majority),random_state=123)
train_upsampled=pd.concat([train_minority_upsampled , train_majority])
print(train_upsampled['label'].value_counts())
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
pipeline_sgd = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('nb', SGDClassifier(max_iter=1000)),   
])
from sklearn.model_selection import train_test_split 
X_train, X_test, y_train, y_test = train_test_split(train_upsampled["tweet"],
                                                    train_upsampled["label"],test_size=0.2, random_state=42)
model = pipeline_sgd.fit(X_train ,y_train )
y_predict=model.predict(X_test)
from sklearn.metrics import f1_score
f1_score(y_test, y_predict)
print(f"F1 Score: {f1_score(y_test, y_predict)}")
import joblib
# Sauvegarde du modèle
joblib.dump(model, 'model.pkl')
