import telebot
from bs4 import BeautifulSoup
import requests
import time


class TaskBot:
    def __init__(self, token, channel_name):
        self.CHANNEL_NAME = channel_name
        self.bot = telebot.TeleBot(token)


    def get_links(self, num_task):
        arr_links = []

        for num in range(num_task, num_task+1):
            url = 'https://euler.jakumo.org/problems/view/' + str(num) + '.html'
            arr_links.append(url)
 
        return arr_links


    def get_title(self, links):
        title = []

        for link in links:
            user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'

            html = requests.get(link, headers={'User-agent':user_agent}).content
            soup = BeautifulSoup(html, 'html.parser')
            titles = soup.find_all('div', class_='probTitle')
            
            for titl in titles:
                title.append(titl.text)

        return title


    def get_tasks(self, links):
        task = []

        for link in links:
            user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'

            html = requests.get(link, headers={'User-agent':user_agent}).content
            soup = BeautifulSoup(html, 'html.parser')
            tasks = soup.find_all('div', class_='problem_content')
            
            for taski in tasks:
                task.append(taski.text)

        return task
                

    def tasks_sender(self):
        num_task = 1

        while True:
            if num_task == 699:
                print("Tasks not found")
                self.bot.send_message(self.CHANNEL_NAME, '<b>Задачи закончились.</b>', parse_mode='html')
                break

            links = self.get_links(num_task)

            message_list = self.get_title(links) + self.get_tasks(links)
            message = f'<b>Номер задачи: {num_task}</b>\nhttps://euler.jakumo.org/problems/view/{num_task}.html\n<b>{message_list[0]}</b>\n{message_list[1]}'

            self.bot.send_message(self.CHANNEL_NAME, message, parse_mode='html')

            num_task = num_task + num_task

            time.sleep(43200)
        

task = TaskBot('token', 'channel')
task.tasks_sender()





        
