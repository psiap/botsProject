import os
import emojis
from data.loader_path import path_user_proxy, path_user_save


def create_array_account_proxy():
    with open(path_user_proxy, 'r+', encoding='utf-8') as file:
        proxy_file = [pr.rstrip() for pr in file.readlines()]

    sessions_len = [f"{path_user_save}{s}" for s in os.listdir(path_user_save) if
                    not '.session-journal' in s and '.session' in s]

    return proxy_file, sessions_len




async def replaceter_text_in_aiogram(new_text, array_caption):
    array_replace, array_emoji = [], []

    for i_emojis in list(emojis.get(new_text)):
        num_emojis = new_text.find(i_emojis) + 1
        array_emoji.append([i_emojis, num_emojis])

    count = 1
    if array_caption:
        for __link in array_caption:
            offset, length = __link['offset'], __link['length']
            for i in array_emoji:
                if i[1] <= __link['offset']:
                    array_emoji.remove(i)
                    count += 1

            if __link['type'] == 'text_link':
                replace_slovo = new_text[offset - count: offset + length - count + 1]
                array_replace.append([replace_slovo, f'<a href="{__link["url"]}">{replace_slovo}</a>'])
            if __link['type'] == 'bold':
                replace_slovo = new_text[offset - count: offset + length - count + 1]
                array_replace.append([replace_slovo, f'<b>{replace_slovo}</b>'])
            if __link['type'] == 'italic':
                replace_slovo = new_text[offset - count: offset + length - count + 1]
                array_replace.append([replace_slovo, f'<i>{replace_slovo}</i>'])

    for i in array_replace:
        if i[0] == '':
            continue
        new_text = new_text.replace(i[0], i[1])
    return new_text
