import asyncio
import csv
import datetime
import glob
import os
import random
import shutil
import sys
import time
from queue import Queue

import socks
from telethon import TelegramClient
from telethon.tl import functions
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.channels import UpdateUsernameRequest, JoinChannelRequest, GetFullChannelRequest, \
    InviteToChannelRequest
from telethon.tl.functions.contacts import ResolveUsernameRequest
from telethon.tl.functions.messages import GetHistoryRequest, ImportChatInviteRequest, CheckChatInviteRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from telethon.tl.types import ChannelParticipantsRecent, InputPeerChannel, InputUser

from data.loader_path import path_user_proxy, path_user_save, path_spam_bd


class get_user_invaiter_tg_asyncio(object):
    def __init__(self, chat_id, msg):
        self.__chat_id = chat_id
        self.__msg = msg


    def create_array_users_in_path(self):
        with open(path_user_proxy, 'r+', encoding='utf-8') as file:
            proxy_file = [pr.rstrip() for pr in file.readlines()]

        sessions_len = [f"{path_user_save}{s}" for s in os.listdir(path_user_save) if
                        not '.session-journal' in s and '.session' in s ]
        try:
            with open(path_spam_bd, newline='', encoding='utf-8') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=';')
                usernames = [user[0].replace('@', '') for user in spamreader if user[0]]

        except Exception as E:
            print(E)

        return proxy_file, sessions_len, usernames

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


        self.error_add = 0
        self.comp_add = 0

        proxy_file, sessions_len, usernames = self.create_array_users_in_path()

        que_array_proxy, que_array_users, que_sessions_len = self.create_array_queue(
            proxy_file=proxy_file,
            usernames=usernames,
            sessions_len=sessions_len
        )

        array_clien_session = await self.a_create_task_in_account(sessions_len, que_sessions_len, que_array_proxy)

        await self.__msg.edit_text(f"Аккаунтов: {len(array_clien_session)}")
        tasks_send_mess = []
        for __name_client in array_clien_session:
            tasks_send_mess.append(
                asyncio.create_task(
                    self.invite_users_session(
                        client=__name_client,
                        q_user=que_array_users
                    )))

        await asyncio.gather(*tasks_send_mess)
        await self.__msg.edit_text(f"Время работы: {time.time() - start_time}\n"
                                   f"Пользователей для инвайтинга: {len(usernames)}\n"
                                   f"Попыток добавить пользователя: {self.comp_add + self.error_add}\n"
                                   f"Пользователей добавлено: {self.comp_add}\n"
                                   f"Пользователей не получилось добавить: {self.error_add}")




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
            que_array_proxy.put(__proxy)

            await client_spam.disconnect()
            try:
                shutil.move(__account, f"deleteaccount/{__account.replace('telegramusers/', '')}")
            except:
                pass
        else:
            return [__account, client_spam]

    async def invite_users_session(self, client, q_user):
        temp_count = 0
        name_session, client_s = client[0], client[1]
        while True:
            user_id = q_user.get()
            try:
                try:
                    updates = await client_s(ImportChatInviteRequest(self.__chat_id.split('/')[-1].replace('+','')))
                    self.__chat_id = updates
                except Exception as E:
                    print(E)
                try:
                    await client_s(JoinChannelRequest(self.__chat_id))
                except Exception as E:
                    print(E)
                try:
                    group_info = await client_s.get_entity(self.__chat_id)
                    group_id = group_info.id
                    group_hash = group_info.access_hash
                    group = InputPeerChannel(group_id, group_hash)

                    user = await client_s(ResolveUsernameRequest(user_id))
                    user = InputUser(user.users[0].id, user.users[0].access_hash, )

                    await client_s(InviteToChannelRequest(group, [user]))
                    self.comp_add += 1
                    if self.comp_add % 10 == 0:
                        await self.__msg.edit_text(f"Пользователей добавленно: {self.comp_add}")
                except Exception as E:
                    self.error_add += 1
                #delay = random.randint(16, 35)
                delay = random.randint(5, 10)
                await asyncio.sleep(delay)
            except Exception as E:
                pass
            q_user.empty()
            temp_count += 1
            if temp_count > 10:
                await client_s.disconnect()
                return
            elif q_user.empty():
                await client_s.disconnect()
                return

