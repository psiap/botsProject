import asyncio
import csv
import datetime
import glob
import os
import random
import sys
import time
import socks
from telethon import TelegramClient
from telethon.tl import functions
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.channels import UpdateUsernameRequest, JoinChannelRequest, GetFullChannelRequest
from telethon.tl.functions.messages import GetHistoryRequest, ImportChatInviteRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from telethon.tl.types import ChannelParticipantsRecent



class Parser_chat(object):
    def __init__(self, msg):
        proxy = (socks.SOCKS5, '70.38.2.193', 12352, True, 'bbM762', '3nsMBb')
        api_hash = f'844{random.randint(0, 9)}5e{random.randint(0, 9)}61eb1cc1cafba945{random.randint(0, 9)}50b98e3d'
        self.client = TelegramClient(rf'data/start.session', 2192239, api_hash)

        self.__msg = msg



    async def save_user_in_bd_chat(self, all_members_parse, chat):
        _date_save = datetime.datetime.now()

        for _u in all_members_parse:
            print(_u)
        users_mass_s = [(_u.username, _u.id, _u.first_name, _u.last_name, _u.phone, _date_save) for _u in
                      all_members_parse if _u.username]
        try:
            with open(f'data/pars.csv', 'w',newline = '\n', encoding="utf-8", errors='ignore') as out:
                csv_out = csv.writer(out, delimiter=';')
                csv_out.writerow(['username', 'user_id', 'first_name', 'last_name', 'nomber', 'datepars'])
                csv_out.writerows(users_mass_s)
        except Exception as E:
            print(E)



    async def __start__(self, chat):
        await self.client.start()
        try:
            try:
                try:

                    self.__chat_id = chat
                    updates = await self.client(ImportChatInviteRequest(self.__chat_id.split('/')[-1].replace('+','')))
                    self.__chat_id = updates
                except Exception as E:
                    print(E)
                if 'join' in self.__chat_id:
                    await self.client(ImportChatInviteRequest(self.__chat_id))
                try:
                    await self.client(JoinChannelRequest(self.__chat_id))
                except Exception as E:
                    pass
            except Exception as E:
                pass
            try:
                full_info_chat = await self.client(GetFullChannelRequest(channel=self.__chat_id))
                all_members_count = full_info_chat.full_chat.participants_count
                online_count = full_info_chat.full_chat.online_count
                await self.__msg.edit_text(f"Всего пользователей: {all_members_count}\n"
                                           f"Онлайн пользователей: {online_count}")

                self.start_time = time.time()
            except Exception as E:
                pass
            all_members_parse = []
            members, members_w, members_m, members_y = {}, {}, {}, {}
        except Exception as E:
            print(E)

        try:
            ch = await self.client.get_entity(self.__chat_id)
        except Exception as E:
            pass

        data_today = datetime.datetime.now(datetime.timezone.utc)
        data_month = datetime.timedelta(days=31)
        data_week = datetime.timedelta(days=7)
        data_recently = datetime.timedelta(days=2)

        if all_members_count < 10200:
            offset = 0
            while True:
                try:
                    result = await self.client(functions.channels.GetParticipantsRequest(
                        channel=ch,
                        filter=ChannelParticipantsRecent(),
                        offset=offset,
                        limit=200,
                        hash=0
                    ))
                    for i in result.users:
                        try:

                            all_members_parse.append(i)
                        except Exception as E:
                            print(E)

                    if offset >= all_members_count * 2:
                        break
                    offset += 200
                except Exception as E:
                    pass

        else:
            try:
                member = self.client.iter_participants(ch, aggressive=True)
                async for i in member:
                    try:
                        all_members_parse.append(i)
                    except Exception as E:
                        print(E)
            except Exception as E:
                print(E)


        await self.save_user_in_bd_chat(all_members_parse, chat)

        await self.client.disconnect()
        await self.__msg.edit_text(f"Парсинг окончен: {time.time() - self.start_time}")
