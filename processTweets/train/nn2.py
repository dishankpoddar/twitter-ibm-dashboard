# !pip install scikit-multilearn

import pandas as pd
import numpy as np
from numpy import array
from numpy import asarray
from numpy import zeros
from keras.preprocessing.text import one_hot
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers.core import Activation, Dropout, Dense
from keras.layers import Flatten, LSTM
from keras.layers import GlobalMaxPooling1D
from keras.models import Model
from keras.layers.embeddings import Embedding
from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer
from keras.layers import Input
from keras.layers.merge import Concatenate
import pickle
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score,precision_score,recall_score

df=pd.read_csv('annotatedTweets.csv',index_col = None,usecols=[0,5,7,8,9,10,11,12,13])

df = df.fillna(0)
df[['Positive','Happy','Relief','Neutral','Anxious','Sad','Negative']]=df[['Positive','Happy','Relief','Neutral','Anxious','Sad','Negative']].astype(int)

Input_column = df['tweet']
Output_columns = df[['Positive','Happy','Relief','Neutral','Anxious','Sad','Negative']]
X = Input_column.values
y = Output_columns.values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

print("Check1")

tokenizer = Tokenizer(oov_token=True)
tokenizer.fit_on_texts(X_train)
X_train = tokenizer.texts_to_sequences(X_train)
X_test = tokenizer.texts_to_sequences(X_test)
X_train = pad_sequences(X_train, padding='post', maxlen=57)
X_test = pad_sequences(X_test, padding='post', maxlen=57)

embeddings_dictionary = dict()
vocab_size=len(tokenizer.word_index)+1
glove_file = open('glove.6B.300d.txt', encoding="utf8")
for line in glove_file:
    records = line.split()
    word = records[0]
    vector_dimensions = asarray(records[1:], dtype='float32')
    embeddings_dictionary[word] = vector_dimensions
glove_file.close()
embedding_matrix = zeros((vocab_size, 300))
for word, index in tokenizer.word_index.items():
    embedding_vector = embeddings_dictionary.get(word)
    if embedding_vector is not None:
        embedding_matrix[index] = embedding_vector

print("Check2")

model = Sequential()
model.add(Embedding(vocab_size, output_dim=300, input_length=57))
model.add(LSTM(128, return_sequences=True))  
model.add(LSTM(128))
model.add(Dense(7, activation='softmax'))
model.summary()

print("Check3")

model.compile(optimizer='adam', loss='binary_crossentropy',metrics=['acc'])
history = model.fit(X_train, y_train,
                    class_weight='balanced',
                    epochs=5,
                    batch_size=32,
                    validation_split=0.1,
                    callbacks=[])

score = model.evaluate(X_test, y_test, verbose=1)
print("Test Accuracy:", score)

with open('..\\tokenizer2.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

model.save("..\\model2.h5")
print("Saved model to disk")

# print(model.predict(X_test))

# X = tokenizer.texts_to_sequences(X)
# X = pad_sequences(X, padding='post', maxlen=57)
# print(model.predict(X))

# Test Score: 0.3665194511413574
# Test Accuracy: 0.5397082567214966
# Test Score: 1.0580517053604126
# Test Accuracy: 0.5356563925743103

# predictions=model.predict(X_test)
# thresholds=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
# for val in thresholds:
#     pred=predictions.copy()
  
#     pred[pred>=val]=1
#     pred[pred<val]=0
  
#     precision = precision_score(y_test, pred, average='micro')
#     recall = recall_score(y_test, pred, average='micro')
#     f1 = f1_score(y_test, pred, average='micro')
   
#     print("Micro-average quality numbers")
#     print("Precision: {:.4f}, Recall: {:.4f}, F1-measure: {:.4f}".format(precision, recall, f1))
