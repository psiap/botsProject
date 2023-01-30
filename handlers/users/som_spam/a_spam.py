import asyncio
import csv
import datetime
import glob
import os
import random
import re
import shutil
import sys
import time
from queue import Queue

import socks
import telethon
from telethon import TelegramClient
from telethon.tl import functions

from data.loader_path import path_user_proxy, path_user_save, path_spam_bd, path_text_spam


class Spammer_in_tg_asyncio(object):
    def __init__(self, msg):
        self.__send_max = 1000
        self.__msg = msg

    def create_array_users_in_path(self):
        with open(path_user_proxy, 'r+', encoding='utf-8') as file:
            proxy_file = [pr.rstrip() for pr in file.readlines()]

        sessions_len = [f"{path_user_save}{s}" for s in os.listdir(path_user_save) if
                        not '.session-journal' in s and '.session' in s ]

        with open(path_spam_bd, newline='', encoding='utf-8') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';')
            usernames = [user[0].replace('@', '') for user in spamreader if user[0]]

        with open(path_text_spam, 'r+', encoding='utf-8') as file:
            # text_spam = [pr.rstrip() for pr in file.readlines()]
            text_spam_s = file.read()

        return proxy_file, sessions_len, usernames, text_spam_s

    def create_array_queue(self, proxy_file, usernames,sessions_len):
        que_array_proxy,que_array_users, que_sessions_len = Queue(), Queue(), Queue()
        for i_proxy in proxy_file:
            que_array_proxy.put(i_proxy)


        for __user in usernames:
            que_array_users.put(__user)

        for __ss in sessions_len:
            que_sessions_len.put(__ss)

        return que_array_proxy, que_array_users, que_sessions_len

    async def a_create_task_in_account(self,sessions_len,que_sessions_len,que_array_proxy):
        tasks = []
        for _ in sessions_len:
            task = asyncio.create_task(self.create_session(que_sessions_len=que_sessions_len,
                                                           que_array_proxy=que_array_proxy
                                                           ))
            tasks.append(task)

        temp_array = await asyncio.gather(*tasks)
        new_array = [x for x in temp_array if x is not None]

        return new_array

    async def __start__(self):
        start_time = time.time()

        self.error_mess = 0
        self.comp_mess = 0

        proxy_file, sessions_len, usernames, text_spam_s = self.create_array_users_in_path()

        que_array_proxy, que_array_users, que_sessions_len = self.create_array_queue(
            proxy_file=proxy_file,
            usernames=usernames,
            sessions_len=sessions_len
        )
        array_clien_session = await self.a_create_task_in_account(sessions_len,que_sessions_len,que_array_proxy)

        await self.__msg.edit_text(f"Аккаунтов: {len(array_clien_session)}")
        tasks_send_mess = []
        for __name_client in array_clien_session:
            tasks_send_mess.append(
                asyncio.create_task(
                    self.send_messag_session(
                        client=__name_client,
                        q_user=que_array_users,
                        text_spam=text_spam_s
                    )))

        await asyncio.gather(*tasks_send_mess)
        await self.__msg.edit_text(f"Время работы: {time.time() - start_time}\n"
                                   f"Пользователей для спама: {len(usernames)}\n"
                                   f"Попыток отправить сообщения: {self.comp_mess + self.error_mess}\n"
                                   f"Сообщений отправлено: {self.comp_mess}\n"
                                   f"Сообщений не отправлено: {self.error_mess}")
    async def create_session(self, que_sessions_len, que_array_proxy):
        if que_sessions_len.empty() or que_array_proxy.empty():
            return
        __proxy = que_array_proxy.get()
        __account = que_sessions_len.get()
        proxy_temp = __proxy.split(':')

        ip, port, login, password = proxy_temp[0], proxy_temp[1], proxy_temp[2], proxy_temp[3]
        proxy = (socks.SOCKS5, ip, int(port), True, login, password)
        api_hash = f'844{random.randint(0, 9)}5e{random.randint(0, 9)}61eb1cc1cafba945{random.randint(0, 9)}50b98e3d'
        client_spam = TelegramClient(__account, 2192239,api_hash,proxy=proxy)

        await client_spam.connect()
        auth = await client_spam.is_user_authorized()
        if not auth:
            await client_spam.disconnect()
            try:
                shutil.move(__account, f"deleteaccount/{__account.replace('telegramusers/', '')}")
            except:
                pass
        else:
            return [__account, client_spam]

    async def send_messag_session(self, client, q_user, text_spam):
        temp_count = 0
        name_session, client_s = client[0], client[1]
        text_spam_t = text_spam
        while True:
            user_id = q_user.get()
            try:
                try:
                    if '[name]' in text_spam:
                        result = await client_s(functions.users.GetFullUserRequest(user_id))
                        first_name = result.to_dict()['users'][0]['first_name']
                        text_spam_t = text_spam.replace('[name]',first_name)
                    else:
                        text_spam_t = text_spam.replace('[name]', '')
                except Exception as E:
                    pass
                try:
                    if user_id.isdigit():
                        pass
                        #await client_s.send_message(entity=int(user_id), message=text_spam,link_preview=False)

                        #await client_s.send_message(entity=int(user_id), message=text_spam)
                    else:
                        #await client_s.send_message(entity=user_id, message=text_spam,link_preview=False)
                        if 'photo' in text_spam_t:

                            await client_s.send_message(entity=user_id, message=text_spam_t.replace('~photo',''),file=rf'data/avatar/1.png', parse_mode='html')
                        else:
                            await client_s.send_message(entity=user_id, message=text_spam_t.replace('~text',''), parse_mode='html')
                    temp_count += 1
                    self.comp_mess += 1
                except telethon.errors.rpcerrorlist.FloodWaitError as E:
                    e_sleep = int(re.findall(r'\b\d+\b', f"{E}")[0])
                    if e_sleep > 400:
                        await client_s.disconnect()

                        return
                    else:
                        await asyncio.sleep(e_sleep)
                except telethon.errors.rpcerrorlist.PeerFloodError as E:
                    await client_s.disconnect()
                    return
                except Exception as E:
                    self.error_mess += 1
                    q_user.put(user_id)
                delay = random.randint(15, 45)
                await asyncio.sleep(delay)
            except Exception as E:
                pass
            q_user.empty()

            if temp_count > 10:
                await self.__msg.edit_text(f"Попыток отправить сообщения: {self.comp_mess + self.error_mess}\n"
                                           f"Сообщений отправлено: {self.comp_mess}\n"
                                           f"Сообщений не отправлено: {self.error_mess}")
                await client_s.disconnect()
                return
            elif q_user.empty() and self.comp_mess > self.__send_max:
                await self.__msg.edit_text(f"Попыток отправить сообщения: {self.comp_mess + self.error_mess}\n"
                                           f"Сообщений отправлено: {self.comp_mess}\n"
                                           f"Сообщений не отправлено: {self.error_mess}")
                await client_s.disconnect()
                return