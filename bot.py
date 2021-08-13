import telebot
from bs4 import BeautifulSoup
import requests
import time
import json
import threading
import apiai


class TaskBot:
    def __init__(self, token, channel_name=None, mode_chat_bot=False, user_id=None, num_task_bot=None, time_sleep=None):
        self.CHANNEL_NAME = channel_name
        self.bot = telebot.TeleBot(token)
        self.mode_chat_bot = mode_chat_bot
        self.user_id = user_id
        self.num_task_bot = num_task_bot
        self.time_sleep = time_sleep
        

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
            tasks = soup.find_all('div', class_='problemsItem')
            
            for taski in tasks:
                task.append(taski.text)

        return task


    def separation_list(self, arr):
        res = []
        count = len(arr) // 2
        
        for i in range(0, len(arr), count):
            res.append(arr[i:i+count])

        return res
                

    def tasks_sender(self): 
        num_task = 1
        status = ''

        if self.mode_chat_bot:
            num_task = self.num_task_bot

            if num_task <= 100:
                status = '😃'

            elif num_task <= 300:
                status = '😐'

            elif num_task <= 699:
                status = '😡'

            links = self.get_links(num_task)
            message_list = self.get_title(links) + self.get_tasks(links)
            
            try:
                title = message_list[0].replace('*', '×')
                task = message_list[1].replace('*', '×')
            except IndexError:
                self.bot.send_message(self.user_id, 'Ты дурачок? Я же сказал от 1 до 699')
                return
                
            if len(message_list[1]) > 4096:
                arr = self.separation_list(message_list[1])
                
                try:
                    message = f'*Номер задачи: {num_task}*\n*Уровень сложности: {status}*\nhttps://euler.jakumo.org/problems/view/{num_task}.html\nБот: @TaskMossBot\n*{title}*\n{arr[0]}\n*👇 подробнее о задаче*'
                    self.bot.send_message(self.user_id, message, parse_mode="Markdown")
                except telebot.apihelper.ApiException:
                    message = f'Номер задачи: {num_task}\nУровень сложности: {status}\nhttps://euler.jakumo.org/problems/view/{num_task}.html\nБот: @TaskMossBot\n{title}\n{arr[0]}\n👇 подробнее о задаче'
                    self.bot.send_message(self.user_id, message)

                message1 = f'{arr[1]}'
                self.bot.send_message(self.user_id, message1)

                num_task = num_task + 1
                return
            
            try:
                message = f'*Номер задачи: {num_task}*\n*Уровень сложности: {status}*\nhttps://euler.jakumo.org/problems/view/{num_task}.html\nБот: @TaskMossBot\n*{title}*\n{task}\n*👇 подробнее о задаче*'
                self.bot.send_message(self.user_id, message, parse_mode="Markdown")
            except telebot.apihelper.ApiException:
                message = f'Номер задачи: {num_task}\nСложность: {status}\nhttps://euler.jakumo.org/problems/view/{num_task}.html\nБот: @TaskMossBot\n{title}\n{task}\n👇 подробнее о задаче'
                self.bot.send_message(self.user_id, message)

            num_task = num_task + 1

        elif self.mode_chat_bot == False:
            while True:
                if num_task == 700:
                    print('Tasks not found')
                    self.bot.send_message(self.CHANNEL_NAME, '*Задачи закончились.*', parse_mode='Markdown')
                    break

                if num_task <= 100:
                    status = '😃'

                elif num_task <= 300:
                    status = '😐'

                elif num_task <= 699:
                    status = '😡'

                links = self.get_links(num_task)
                message_list = self.get_title(links) + self.get_tasks(links)
                title = message_list[0].replace('*', '×')

                task = message_list[1].replace('*', '×')

                if len(task) > 4096:
                    arr = self.separation_list(message_list[1])

                    try:
                        message = f'*Номер задачи: {num_task}*\n*Уровень сложности: {status}*\nhttps://euler.jakumo.org/problems/view/{num_task}.html\nБот: @TaskMossBot\n*{title}*\n{arr[0]}\n*👇 подробнее о задаче*'
                        self.bot.send_message(self.CHANNEL_NAME, message, parse_mode="Markdown")
                    except telebot.apihelper.ApiException:
                        message = f'Номер задачи: {num_task}\nУровень сложности: {status}\nhttps://euler.jakumo.org/problems/view/{num_task}.html\nБот: @TaskMossBot\n{title}\n{arr[0]}\n👇 подробнее о задаче'
                        self.bot.send_message(self.CHANNEL_NAME, message)
                    
                    message1 = f'{arr[1]}'
                    self.bot.send_message(self.CHANNEL_NAME, message1)

                    num_task = num_task + 1
                    time.sleep(self.time_sleep)
                    continue

                try:
                    message = f'*Номер задачи: {num_task}*\n*Уровень сложности: {status}*\nhttps://euler.jakumo.org/problems/view/{num_task}.html\nБот: @TaskMossBot\n*{title}*\n{task}\n*👇 подробнее о задаче*'
                    self.bot.send_message(self.CHANNEL_NAME, message, parse_mode="Markdown")
                except telebot.apihelper.ApiException:
                    message = f'Номер задачи: {num_task}\nУровень сложности: {status}\nhttps://euler.jakumo.org/problems/view/{num_task}.html\nБот: @TaskMossBot\n{title}\n{task}\n👇 подробнее о задаче'
                    self.bot.send_message(self.CHANNEL_NAME, message)

                num_task = num_task + 1
                time.sleep(self.time_sleep)


bot = telebot.TeleBot('1201089953:AAFfOtC2524F7btnS9Oppsfqur3xO6OgevU')

@bot.message_handler(commands=['start', 'help'])
def start_bot(message):
    first_name = message.from_user.first_name.replace('*', '×')
        
    mess = f'Привет *{first_name}.*\nУ меня 699 задач\n Напиши номер задачи от 1 до 699\n/easytask\n/normaltask\n/hardtask'
    bot.send_message(message.from_user.id, mess, parse_mode='Markdown')


@bot.message_handler(content_types=['text'])
def task_bot(message):
    num_task = message.text

    if message.text == '/easytask':
        res = ''

        for num in range(1, 101):
            res += f'{str(num)}\n'

        bot.send_message(message.from_user.id, res, parse_mode='Markdown')

    elif message.text == '/normaltask':
        res = ''

        for num in range(102, 301):
            res += f'{str(num)}\n'

        bot.send_message(message.from_user.id, res, parse_mode='Markdown')

    elif message.text == '/hardtask':
        res = ''

        for num in range(302, 699):
            res += f'{str(num)}\n'

        bot.send_message(message.from_user.id, res, parse_mode='Markdown')
        

    elif num_task.isdigit():
        num_task = int(num_task)
        user_id = message.from_user.id 

        task = TaskBot(token='', mode_chat_bot=True, user_id=user_id, num_task_bot=num_task)
        task.tasks_sender()

    else:
        request = apiai.ApiAI('09bafee7068548a89a5b8ef38cc1b0f3').text_request()
        request.lang = 'ru'
        request.session_id = 'session_1'
        request.query = message.text
        results = json.loads(request.getresponse().read().decode('utf-8'))

        mess = results['result']['fulfillment']['speech']
        bot.send_message(message.from_user.id, mess, parse_mode='Markdown')

        
thread = threading.Thread(target=bot.polling, daemon=True)
thread.start()

task = TaskBot('', '@eulermosstasks', time_sleep=60)
task.tasks_sender()

