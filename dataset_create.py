# -*- coding: utf-8 -*-
import os
import json
import datetime

data_dir = f'{os.getcwd()}\\Data'
dataset_dir = f'{os.getcwd()}\\Dataset'

def get_month(month):
    if month == 'мар.':
        month = '03'
    elif month == 'февр.':
        month = '02'
    elif month == 'янв.':
        month = '01'
    elif month == 'дек.':
        month = '12'
    elif month == 'нояб.':
        month = '11'
    elif month == 'окт.':
        month = '10'
    elif month == 'сент.':
        month = '09'
    elif month == 'авг.':
        month = '08'
    return month

today_date = datetime.date.today()
for dataset in os.listdir(data_dir):
    print(dataset)
    scores_amount = 0
    scores = []
    with open(f'{data_dir}\\{dataset}', 'r') as f:
        data = json.load(f)
    data_dict = []
    for video_data in data:
        try:
            title = video_data['title']
            if video_data['likes_amount'] == 'Нет':
                video_data['likes_amount'] = '0'
            likes_amount = ''
            views = ''
            for letter in str(video_data['views']):
                try:
                    letter = int(letter)
                    views += str(letter)
                except:
                    pass
            for letter in str(video_data['likes_amount']):
                try:
                    letter = int(letter)
                    likes_amount += str(letter)
                except:
                    pass
            video_data['likes_amount'] = likes_amount.strip()
            video_data['views'] = views.strip()
            if video_data['views'] == '':
                video_data['views'] = '0'
            if video_data['likes_amount'] == '':
                video_data['likes_amount'] = '0'

            dislikes = 0
            if '-' not in video_data['likes_percentage']:
                try:
                    dislikes = int(video_data['likes_amount'] * 100 / float(video_data['likes_percentage']))
                    print(dislikes)
                except:
                    dislikes = 0
            date = video_data['date'].split(' ')
            month = get_month(date[1])
            days = datetime.date(int(date[2]), int(month), int(date[0])) - today_date
            if str(days) == '0:00:00':
                days = '0'
            days = abs(int(str(days).split(' ')[0]))

            if days == 0:
                score = int(video_data['views']) + 5 * int(video_data['likes_amount']) - 5 * dislikes
            else:
                score = (int(video_data['views']) + 5 * int(video_data['likes_amount']) - 5 * dislikes) / days
            if score < 0:
                score = 0
            scores.append(score)
            data_dict.append({
                'title': title,
                'score': score
                })
        except Exception as ex:
            title = video_data['title']
            print(title,ex)
            # try:
                # print(days)
                # print(date)
            # except:
                # pass
    print(len(data_dict))
    scores_amount = len(scores)
    sum_of_scores = 0
    for score in scores:
        sum_of_scores += score
    average_score = sum_of_scores / scores_amount
    print(average_score)
    
    for item in data_dict:
        if item['score'] >= average_score:
            item['fine'] = 'Интересно'
        else:
            item['fine'] = 'НеИнтересно'
    with open(f'{dataset_dir}\\{dataset.split("_")[0]}_dataset.json', 'w') as fw:
        json.dump(data_dict, fw, indent=4, ensure_ascii=False)
