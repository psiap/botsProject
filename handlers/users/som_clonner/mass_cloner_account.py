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
from telethon.tl.functions.channels import UpdateUsernameRequest, JoinChannelRequest, GetFullChannelRequest
from telethon.tl.functions.messages import GetHistoryRequest, ImportChatInviteRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from telethon.tl.types import ChannelParticipantsRecent

from data.loader_path import path_user_proxy, path_user_save


class Update_photo_name_TG(object):
    def __init__(self,lang=None, static_img = None, static_first_name=None, static_last_name=None,static_about=None):
        self.__lang = lang
        self.__static_first_name = static_first_name
        self.__static_last_name = static_last_name
        self.__static_img = static_img
        self.__static_about = static_about



    def create_array_users_in_path(self):
        with open(path_user_proxy, 'r+', encoding='utf-8') as file:
            proxy_file = [pr.rstrip() for pr in file.readlines()]

        sessions_len = [f"{path_user_save}{s}" for s in os.listdir(path_user_save) if
                        not '.session-journal' in s and '.session' in s ]

        return proxy_file, sessions_len

    def create_array_queue(self, proxy_file,sessions_len):
        que_array_proxy,que_sessions_len = Queue(), Queue()
        for i_proxy in proxy_file:
            que_array_proxy.put(i_proxy)


        for __ss in sessions_len:
            que_sessions_len.put(__ss)

        return que_array_proxy, que_sessions_len

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
        proxy_file, sessions_len = self.create_array_users_in_path()

        que_array_proxy, que_sessions_len = self.create_array_queue(
            proxy_file=proxy_file,
            sessions_len=sessions_len
        )
        array_clien_session = await self.a_create_task_in_account(sessions_len, que_sessions_len, que_array_proxy)
        return True

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
            await client_spam(UpdateProfileRequest(
                first_name=self.__static_first_name,
                last_name=self.__static_last_name,
                about=self.__static_about
            ))

            await client_spam(UploadProfilePhotoRequest(
                await client_spam.upload_file(self.__static_img)
            ))

            await client_spam.disconnect()
            return __account
