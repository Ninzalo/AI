# -*- coding: utf-8 -*-

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver.v2 as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

import time
import json
import random
import requests
import pickle
import os
import datetime
import emoji
import sys
import keyboard as kb
import win32api as win


class Twitch:
    def __init__(self):
        # self.google_username = google_login
        # self.google_password = google_password
        chrome_options = uc.ChromeOptions()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--profile-directory=Default")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--disable-plugins-discovery")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("user_agent=DN")
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument("--window-size=1032,720")

        self.driver = uc.Chrome(
            executable_path=r"X:\Programs\Python\tiktok\chromedriver\chromedriver.exe",
            version_main=98,
            options=chrome_options
        )


    def close_driver(self):
        self.driver.close()
        self.driver.quit()


    def google_auth(self, google_login):
        driver = self.driver
        driver.delete_all_cookies()
        driver.get("https://www.youtube.com")
        try:
            WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                           'Timed out waiting for PA creation ' +
                                           'confirmation popup to appear.')
            alert = driver.switch_to.alert
            alert.accept()
            driver.get("https://www.youtube.com")
        except TimeoutException:
            pass
        time.sleep(random.randrange(5, 10))
        for cookie in pickle.load(open(f"{os.getcwd()}\\cookies\\{google_login}_cookies", "rb")):
            driver.add_cookie(cookie)
        time.sleep(5)
        driver.refresh()
        time.sleep(10)

    def saver(self, my_ai, google_login):
        driver = self.driver
        # click on icon
        driver.find_element_by_xpath(
                '/html/body/ytd-app/div/div/ytd-masthead/div[3]/div[3]/div[2]/ytd-topbar-menu-button-renderer[3]/button'
                ).click()
        time.sleep(random.randrange(1, 2))
        # click on yt studio
        driver.find_element_by_xpath(
                '/html/body/ytd-app/ytd-popup-container/tp-yt-iron-dropdown/div/ytd-multi-page-menu-renderer/div[3]/div[1]/yt-multi-page-menu-section-renderer[1]/div[2]/ytd-compact-link-renderer[3]/a'
                ).click()
        time.sleep(random.randrange(5, 10))
        # click on content
        driver.find_element_by_xpath(
                '/html/body/ytcp-app/ytcp-entity-page/div/div/ytcp-navigation-drawer/nav/ytcp-animatable[2]/ul/li[2]/ytcp-ve/a/tp-yt-paper-icon-item/div[1]/tp-yt-iron-icon'
                ).click()
        time.sleep(random.randrange(3, 5))
        # click on 'lines on page'
        driver.find_element_by_xpath(
                '/html/body/ytcp-app/ytcp-entity-page/div/div/main/div/ytcp-animatable[3]/ytcp-content-section/ytcp-video-section/ytcp-video-section-content/div/div[2]/ytcp-table-footer/ytcp-select/ytcp-text-dropdown-trigger/ytcp-dropdown-trigger'
                ).click()
        time.sleep(random.randrange(1, 2))
        # click on 50
        driver.find_element_by_xpath(
                '/html/body/ytcp-text-menu/tp-yt-paper-dialog/tp-yt-paper-listbox/tp-yt-paper-item[3]'
                ).click()
        time.sleep(random.randrange(3, 5))
        data = []
        prev_pageSource = ''
        while True:
            try:
                pageSource = driver.page_source
                if pageSource == prev_pageSource:
                    break
                prev_pageSource = pageSource
                page_data = my_ai.parser(pageSource) 
                for item in page_data:
                    is_ok = my_ai.ok(name=item['title'])
                    if is_ok:
                        try:
                            data.append(item)
                        except:
                            pass
                with open(f'{os.getcwd()}\\Data\\{google_login}_data.json', 'w') as jf:
                    json.dump(data, jf, indent=4, ensure_ascii=False)
            except:
                pass
            try:
                driver.find_element_by_xpath('/html/body/ytcp-app/ytcp-entity-page/div/div/main/div/ytcp-animatable[3]/ytcp-content-section/ytcp-video-section/ytcp-video-section-content/div/div[2]/ytcp-table-footer/ytcp-icon-button[3]').click()
                time.sleep(random.randrange(4, 12))
            except:
                time.sleep(random.randrange(30, 60))
                if driver.find_element_by_xpath('/html/body/ytcp-app/ytcp-entity-page/div/div/main/div/ytcp-animatable[3]/ytcp-content-section/ytcp-video-section/ytcp-video-section-content/div/div[2]/ytcp-table-footer/ytcp-icon-button[3]'):
                    driver.find_element_by_xpath('/html/body/ytcp-app/ytcp-entity-page/div/div/main/div/ytcp-animatable[3]/ytcp-content-section/ytcp-video-section/ytcp-video-section-content/div/div[2]/ytcp-table-footer/ytcp-icon-button[3]').click()
                else:
                    break


    def parser(self, pageSource):
        soup = BeautifulSoup(pageSource, 'lxml')
        containers = soup.find_all('ytcp-video-row', class_='style-scope ytcp-video-section-content')
        print(len(containers))
        page_data = []
        for container in containers:
            title = container.find('h3', class_='video-title-wrapper style-scope ytcp-video-list-cell-video').find('a').text.strip().lower()
            print(f'Title: {title}')
            date = container.find('div', class_="cell-body tablecell-date sortable column-sorted style-scope ytcp-video-row").text.strip().lower().replace('публикация', '').strip()
            print(f'Date: {date}')
            views = container.find('div', class_='cell-body tablecell-views sortable right-align style-scope ytcp-video-row').text.strip()
            print(f'Views: {views}')
            try:
                likes_percentage = container.find('div', class_='percent-label style-scope ytcp-video-row').text.strip().replace(
                        '%', '').strip()
            except:
                likes_percentage = '-'
            try:
                likes_amount = container.find('div', class_='likes-label style-scope ytcp-video-row').text.strip().replace('%', '').strip().split(
                        'отм')[0].strip()
            except:
                likes_amount = '0'
            print(f'Likes percentage: {likes_percentage}')
            print(f'Likes: {likes_amount}')
            print('---------')
            video_data = {
                    'title': title,
                    'date': date,
                    'views': views,
                    'likes_percentage': likes_percentage,
                    'likes_amount': likes_amount
                    }
            page_data.append(video_data)
        return page_data

    def ok(self, name):

        words = [
            "!", "\\", "/", ":", "*", "?", '"', "<", ">", "|",
            "ブ", "ラ", "チ", "シ", "ュ", "キ", "ン", "の", "攻", "撃", "ャ", "丫",
            "嗨", "，", "我", "很", "酷", "肉", "乙",
            '嗨', '我', '很', '酷',
            '丫', '乂', '匚', '丫', '长', '闩', '匚', '囗', '匚', '从', 
            '乜', '匚', '人', '囗', '从',
            "Название отсутствует", "IRL", "стрим", "Стрим", "КАТАЕМСЯ",
            "хуй", "пизд", "дцп", "хохол", "пид", "gay", "геи", "гей", "nig", "негр",
            "еба", "секс", "бляд", "блят"
        ]

        is_ok = True

        for i in words:
            if i.lower() in name.lower():
                is_ok = False

        if ":" in emoji.demojize(name):
            is_ok = False

        return is_ok


    def main(self, my_ai):
        logins = ['bbvchatbot','freakclipspr']
        for login in logins:
            my_ai.google_auth(google_login=login)
            my_ai.saver(my_ai=my_ai, google_login=login)


if __name__ == '__main__':
    my_ai = Twitch()
    my_ai.main(my_ai=my_ai)


