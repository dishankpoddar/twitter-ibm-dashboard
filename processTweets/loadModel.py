import pandas as pd
import numpy as np
from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
import pickle

# Load new csv
df=pd.read_csv('tweets_preprocessed_0.csv',index_col = None)
Input_column = df['tweet']
X = Input_column.values

# Load tokenizer
# with open('tokenizer.pickle', 'rb') as handle:
#     tokenizer = pickle.load(handle)
with open('tokenizer2.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

X= tokenizer.texts_to_sequences(X)
X = pad_sequences(X, padding='post', maxlen=57)

# Load model
# model = load_model('model.h5')
model = load_model('model2.h5')
predictions = model.predict(X)

# Convert predictions into binary values
threshold = 0.4
pred=predictions.copy()
pred[pred>=threshold]=1
pred[pred<threshold]=0
  
pred=pred.astype(int)

# Add labels into the dataframe and export it as a CSV
df = pd.concat([df, pd.DataFrame(pred)], axis=1)
df.columns = ['-','date','time','username','name','tweet','geo','Positive','Happy','Relief','Neutral','Anxious','Sad','Negative']
print(df)
df.to_csv('tweets.csv',index=False)


