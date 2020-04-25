from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton

def post_keyboard():
    button_publish = InlineKeyboardButton(text='🗒️ Опубликовать', callback_data='publish')
    button_delete = InlineKeyboardButton(text='❌ Удалить', callback_data='delete')
    store_button = InlineKeyboardButton(text='📦 Отложить', callback_data='store')
    keyboard = InlineKeyboardMarkup([[button_delete, button_publish],
                                        [store_button]])
    return keyboard

def rating_keyboard(up: int=0, down: int=0, btype: int=1):
    btypes = [['⬆️', '⬇️'], ['👍', '👎']]
    c_up_data = f'{up+1}:rating_up:{down}'
    c_down_data = f'{up}:rating_down:{down+1}'
    button_up = InlineKeyboardButton(text=f'{btypes[btype][0]} {up}', callback_data=c_up_data)
    button_down = InlineKeyboardButton(text=f'{btypes[btype][1]} {down}', callback_data=c_down_data)
    keyboard = InlineKeyboardMarkup([[button_up, button_down]])
    return keyboard