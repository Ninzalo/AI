import datetime
import os
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

best_score = {
        'title': '',
        'best_score': 0
        }
dataset_dir = f'{os.getcwd()}\\Dataset'
datasets = []
for dataset_name in os.listdir(dataset_dir):
    if not 'names' in dataset_name:
        dataset = []
        with open(f'{dataset_dir}\\{dataset_name}', 'r') as f:
            dataset_file = json.load(f)
        for title in dataset_file:
            dataset.append([title['title'], title['fine']])
        datasets.append(dataset)
with open(f'{dataset_dir}\\names.txt', 'r') as names:
    texts = [row.strip() for row in names if ':' not in row]
# texts = ['алиса умница @bratishkinoff', 'Вовчик и его чат закибербулили цириллу @cirilla04', 'Спалил айпишники @bratishkinoff', 'ХАХАХХАХА. Смех 6 кадров @bratishkinoff', 'Hesus pomogi @bratishkinoff', 'ben-prediction @jesusavgn', 'про хеса @bratishkinoff', 'Алексей открой методичку напиши в гугле Андрей Луганский методичка там все пруфы @jesusavgn', 'плачет @mazellovvv']

# texts = [f'{input()}']

for iteration, text in enumerate(texts[:]):
    print('==========')
    print(iteration + 1, text)
    print('==========')
    start_time = datetime.datetime.now()
    for num, dataset in enumerate(datasets):
        corpus = [example for example, intent in dataset]
        y = [intent for example, intent in dataset]

        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform(corpus)
        # print(X)
        # print(vectorizer.get_feature_names_out())

        clf = LogisticRegression(random_state=0, max_iter=300000)
        clf.fit(X, y)

        z = clf.predict(vectorizer.transform([text]))
        # print(z)
        # print(vectorizer.transform([text]).toarray())

        f = clf.predict_proba(vectorizer.transform([text]))
        f = f[0][0]

        f = round(f, 8)
        f = f * 100
        if f > best_score['best_score']:
            best_score['best_score'] = f
            best_score['title'] = text
            best_score['dataset'] = num + 1
        print(f'Интересно на {f}%')

    print(datetime.datetime.now() - start_time)

print(best_score)



