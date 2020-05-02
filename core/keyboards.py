from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton

def post_keyboard():
    button_publish = InlineKeyboardButton(text='🗒️ Опубликовать', callback_data='publish')
    button_delete = InlineKeyboardButton(text='❌ Удалить', callback_data='delete')
    store_button = InlineKeyboardButton(text='📦 Отложить', callback_data='store')
    keyboard = InlineKeyboardMarkup([[button_delete, button_publish],
                                        [store_button]])
    return keyboard

def rating_keyboard(rating=(0, 0), btype: int=1, message_id: str=None):
    btypes = [['⬆️', '⬇️'], ['👍', '👎']]
    c_up_data = f'rating_up:{message_id}'
    c_down_data = f'rating_down:{message_id}'
    button_up = InlineKeyboardButton(text=f'{btypes[btype][0]} {rating[0]}', callback_data=c_up_data)
    button_down = InlineKeyboardButton(text=f'{btypes[btype][1]} {rating[1]}', callback_data=c_down_data)
    keyboard = InlineKeyboardMarkup([[button_up, button_down]])
    return keyboard