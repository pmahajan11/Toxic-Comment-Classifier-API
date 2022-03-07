# Importing packages

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import contractions
#import nltk
import sklearn
#import scipy
#from nltk.corpus import stopwords
#nltk.download('stopwords')
#nltk.download('punkt')
#from nltk.tokenize import word_tokenize
#nltk.download('wordnet')
#from gensim.models import KeyedVectors
import pickle
#from gensim.models import KeyedVectors


# load the Stanford GloVe model dictionary
with open("app/ml/glove_dict.pkl", "rb") as file:
  glove_dict = pickle.load(file)

with open("app/ml/stopwords.pkl", "rb") as file:
  stopwords = pickle.load(file)

# Loading the ML model (Random Forest Classifier)
with open("app/ml/rfc_model.pkl", "rb") as file:
  rfc_model = pickle.load(file)


# Text preprocessing functions

def clean(comments):
  # Removing all non-alphabetical characters
  cleaned_comments = []
  for text in comments:
    #print(text)
    #print(type(text))
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\']', ' ', text)
    text = re.sub(r'^\s+|\s+$', '', text)
    cleaned_comments.append(text)
  #print(cleaned_comments)
  return cleaned_comments


def decontract(cleaned_comments):
  #Replacing contraction terms
  decontracted_comments = []
  for comment in cleaned_comments:
    decontracted_words = []
    for word in comment.split():
      decontracted_words.append(contractions.fix(word).lower())
    decontracted_comments.append(re.sub(r'\'', "", " ".join(decontracted_words).strip()))
  #print(decontracted_comments)
  return decontracted_comments


def remove_stopwords(decontracted_comments):
  preprocessed_comments = []
  for comment in decontracted_comments:
    comment_words = comment.split()
    filtered_words = [word for word in comment_words if word not in set(stopwords) and len(word) > 2]
    preprocessed_comments.append(" ".join(filtered_words).strip())
  #print(preprocessed_comments)
  return preprocessed_comments


def vectorize(preprocessed_comments, glove_model=glove_dict):
  vectorized_comments = np.empty((len(preprocessed_comments), 100))
  #glove_model = load_glove_vectors()
  for comment in preprocessed_comments:
    comment_vector = np.zeros(100)
    for word in comment.split():
      try:
        comment_vector = np.add(comment_vector, glove_model[word])
      except:
        pass
    vectorized_comments[list(preprocessed_comments).index(comment)] = comment_vector / (np.sqrt(comment_vector.dot(comment_vector)) + 0.0001)
  return vectorized_comments


def preprocess(comments_data, glove_model = glove_dict):
  
  # Checks if the input is either a string or a list of strings
  if type(comments_data) == str:
    cleaned_comments = clean([comments_data])
    decontracted_comments = decontract(cleaned_comments)
    preprocessed_comments = remove_stopwords(decontracted_comments)
    vectorized_comments = vectorize(preprocessed_comments, glove_model=glove_model)
    return vectorized_comments.reshape(1, -1)

  elif type(comments_data) == list and all(isinstance(item, str) for item in comments_data):
    cleaned_comments = clean(comments_data)
    decontracted_comments = decontract(cleaned_comments)
    preprocessed_comments = remove_stopwords(decontracted_comments, glove_model=glove_model)
    vectorized_comments = vectorize(preprocessed_comments)
    return vectorized_comments
  
  else:
    raise TypeError("Input must be a string or a list of strings!")


#print("toxic score:", rfc_model.predict_proba(preprocess("== wats this about me bein unable to edit kazakhstan?? == WHAT THE FUCK IS WRONG WITH YOU, BASTARD!!!! YOU SHOULD GO FUCKIN FALL IN A FUCKIN HOLE AND FUCKING DIE, WHORE!"))[0][1])