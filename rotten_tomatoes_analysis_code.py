# -*- coding: utf-8 -*-
"""Rotten Tomatoes Analysis Code

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/161x06f9_v0N3CtQfVieBKiHpXwFY67r8
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

from google.colab import files
uploaded = files.upload()
import io

data = pd.read_csv(io.BytesIO(uploaded['movies.csv']))

data.head()

data.tail()

data.describe()

print(data.isnull().sum()) #to check count of missing values

filtered_data = data.drop(['rating','writer',
                           'release_date_(theaters)','box_office_(gross_usa)',
                           'sound_mix','aspect_ratio','view_the_collection'], axis=1)
filtered_data = filtered_data.dropna(axis=0, how='all')
filtered_data.shape
filtered_data.isnull().all(axis=0)

filtered_data.shape

filtered_data
filtered_data.describe()

import matplotlib.pyplot as plt
states = filtered_data['critic_score']
ax = filtered_data['critic_score'].value_counts()[:20].plot(kind='barh', title="Prominence of high critic scores")
#plot(kind='bar',figsize=(10,5),
ax.set_xlabel("Number of movies")
ax.set_ylabel("Critic Score")

ax3 = plt.hist(x=filtered_data['critic_score'], bins='auto', color='green',
                            alpha=0.7, rwidth=0.85)
plt.grid(axis='y', alpha=0.75)
plt.xlabel('Critic scores')
plt.ylabel('Number of movies')
plt.title('Prominence of high critic scores')

ax4 = plt.hist(x=filtered_data['people_score'], bins='auto', color='red',
                            alpha=0.7, rwidth=0.85)
plt.grid(axis='y', alpha=0.75)
plt.xlabel('People scores')
plt.ylabel('Number of movies')
plt.title('Prominence of high people scores')

import matplotlib.pyplot as plt
states = filtered_data['director']
ax1 = filtered_data['director'].value_counts()[:5].plot(kind='barh', title="Directors with the highest rated movies")
#plot(kind='bar',figsize=(10,5),
ax1.set_xlabel("Number of highly rated movies")
ax1.set_ylabel("Directors")

import matplotlib.pyplot as plt
states = filtered_data['producer']
ax1 = filtered_data['producer'].value_counts()[:5].plot(kind='barh', color = 'pink', title="Producers with the highest rated movies")
#plot(kind='bar',figsize=(10,5),
ax1.set_xlabel("Number of highly rated movies")
ax1.set_ylabel("Producers")

filtered_data['type'].unique()

pie = filtered_data['type'].value_counts()[:5].plot.pie(
                                     autopct=(lambda p : '{:.2f}%'.format(p)),
                                     fontsize=10
                                     , pctdistance=0.5,
                                     figsize=(8, 8))
plt.ylabel("")

#filtered_data['categories'].unique()
filtered_data['reviews.rating'].unique()

ax3 = plt.hist(x=filtered_data['reviews.rating'], bins='auto', color='#0504aa',
                            alpha=0.7, rwidth=0.85)
plt.grid(axis='y', alpha=0.75)
plt.xlabel('Ratings')
plt.ylabel('Frequency')
plt.title('Rating Frequencies')

from wordcloud import WordCloud, STOPWORDS

comment_words = ''
stopwords = set(STOPWORDS)
for val in filtered_data['consensus']:
     
    # typecaste each val to string
    val = str(val)
 
    # split the value
    tokens = val.split()
     
    # Converts each token into lowercase
    for i in range(len(tokens)):
        tokens[i] = tokens[i].lower()
     
    comment_words += " ".join(tokens)+" "
 
wordcloud = WordCloud(width = 800, height = 800,
                background_color ='white',
                stopwords = stopwords,
                min_font_size = 10).generate(comment_words)
 
# plot the WordCloud image                      
plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)
 
plt.show()

filtered_data['reviews.rating'].unique()

from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import classification_report
naive_data = filtered_data1
naive_data = naive_data.dropna(axis=0, how='any')
from sklearn.model_selection import train_test_split

def create_nb_classifier(df, test_size=0.2):
    pipeline = Pipeline([
        ('vectorizer', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('classifier', MultinomialNB())
    ])

    X = df['reviews.text']
    y = df['reviews.rating']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
    # Grid Search for Optimal Hyperparameters
    param_grid = {
    'classifier__alpha': [0.1, 1.0, 10.0]
    }
    grid_search = GridSearchCV(pipeline, param_grid, cv=5)
    grid_search.fit(X_train, y_train)
    classifier = grid_search.best_estimator_
    return classifier, X_test, y_test

vals = create_nb_classifier(naive_data)
classifier = vals[0]
new_reviews = vals[1]
testval = vals[2]
predictions = classifier.predict(new_reviews)
accuracy = accuracy_score(testval, predictions)
print(f'Accuracy: {accuracy:.2f}')
print(classification_report(testval, predictions))

# Select the predictors and the target variable
'''
X = naive_data.drop('reviews.rating', axis=1)
y = naive_data['reviews.rating']

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Create the sv classifier
model = make_pipeline(TfidfVectorizer(), MultinomialNB())
# Train the model using the training data
model.fit(X_train, y_train)
# Predict the categories of the test data
predicted_categories = model.predict(X_test)
'''

#naive_data = filtered_data
#naive_data = naive_data.dropna(axis=0, how='any')
predictor_data = filtered_data
predictor_data = predictor_data.dropna(axis=0, how='any')
def label_review(row):
    if row['critic_score'] >= 95:
        return 'positive'
    else:
        return 'negative'
    

# Add the label column to the DataFrame
predictor_data['review_class'] = predictor_data.apply(label_review, axis=1)
predictor_data.head()

from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import classification_report


def create_nb_classifier(df, test_size=0.2):
    pipeline = Pipeline([
        ('vectorizer', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('classifier', MultinomialNB())
    ])

    X = df['consensus']
    y = df['review_class']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
    # Grid Search for Optimal Hyperparameters
    param_grid = {
    'classifier__alpha': [0.1, 1.0, 10.0]
    }
    grid_search = GridSearchCV(pipeline, param_grid, cv=5)
    grid_search.fit(X_train, y_train)
    classifier = grid_search.best_estimator_
    return classifier, X_test, y_test

keep_columns = ['consensus', 'review_class']
nbdata = predictor_data

# Get a list of all columns that are not in the list of columns to keep
drop_columns = [col for col in nbdata.columns if col not in keep_columns]

# Drop the columns
nbdata = nbdata.drop(columns=drop_columns)

nbdata.head()
vals = create_nb_classifier(nbdata)
classifier = vals[0]
new_reviews = vals[1]
testval = vals[2]
predictions = classifier.predict(new_reviews)
accuracy = accuracy_score(testval, predictions)
print(f'Accuracy: {accuracy:.2f}')
print(classification_report(testval, predictions))

import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score
from sklearn.preprocessing import LabelEncoder

# Encode the target variable as a binary numerical label
le = LabelEncoder()
y_test_enc = le.fit_transform(testval)
y_pred_enc = le.fit_transform(predictions)

fpr, tpr, thresholds = roc_curve(y_test_enc, y_pred_enc)
plt.fill_between(fpr, tpr, alpha=0.2)
# Calculate the area under the curve
auc = roc_auc_score(y_test_enc, y_pred_enc)

# Plot the ROC curve
plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % auc)
plt.plot([0, 1], [0, 1], 'k--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend(loc="lower right")
plt.show()

predictor_data = naive_data
predictor_data = predictor_data.dropna(axis=0, how='any')
def label_review(row):
    if row['reviews.rating'] >= 3:
        return 'positive'
    else:
        return 'negative'

# Add the label column to the DataFrame
predictor_data['review_class'] = predictor_data.apply(label_review, axis=1)
dropped = predictor_data
dropped.drop(labels='reviews.rating', axis=1, inplace=True)
dropped.head()

from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import classification_report
naive_data = filtered_data1
naive_data = naive_data.dropna(axis=0, how='any')
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score
from sklearn.multiclass import OneVsRestClassifier

predictor_data = naive_data
predictor_data = predictor_data.dropna(axis=0, how='any')
def label_review(row):
    if row['reviews.rating'] >= 3:
        return 'positive'
    else:
        return 'negative'

# Add the label column to the DataFrame
predictor_data['review_class'] = predictor_data.apply(label_review, axis=1)
dropped = predictor_data
dropped.drop(labels='reviews.rating', axis=1, inplace=True)
dropped.head()

def create_nb_classifier(df, test_size=0.2):
    pipeline = Pipeline([
        ('vectorizer', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('classifier', MultinomialNB())
    ])

    X = df['reviews.text']
    y = df['review_class']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
    # Grid Search for Optimal Hyperparameters
    param_grid = {
    'classifier__alpha': [0.1, 1.0, 10.0]
    }
    grid_search = GridSearchCV(pipeline, param_grid, cv=5)
    grid_search.fit(X_train, y_train)
    classifier = grid_search.best_estimator_
    return classifier, X_test, y_test

vals = create_nb_classifier(dropped)
classifier = vals[0]
new_reviews = vals[1]
testval = vals[2]
predictions = classifier.predict(new_reviews)
accuracy = accuracy_score(testval, predictions)
print(f'Accuracy: {accuracy:.2f}')
print(classification_report(testval, predictions))