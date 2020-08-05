from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton

def post_keyboard(channel_to_post):
    button_publish = InlineKeyboardButton(text='🗒️ Опубликовать', callback_data=f'publish:{channel_to_post.channel_id}')
    button_delete = InlineKeyboardButton(text='❌ Удалить', callback_data='delete')
    button_store = InlineKeyboardButton(text='📦 Отложить', callback_data='delay')
    button_switch_context = InlineKeyboardButton(text=f'📚 Контекст | @{channel_to_post.channel_username}', callback_data='context_keyboard:post')

    keyboard = InlineKeyboardMarkup([[button_delete, button_publish],
                                    [button_store, button_switch_context]])
    return keyboard

def rating_keyboard(rating=(0, 0), btype: int=1, message_id: str=None):
    btypes = [['⬆️', '⬇️'], ['👍', '👎']]
    c_up_data = f'rating_up:{message_id}'
    c_down_data = f'rating_down:{message_id}'
    button_up = InlineKeyboardButton(text=f'{btypes[btype][0]} {rating[0]}', callback_data=c_up_data)
    button_down = InlineKeyboardButton(text=f'{btypes[btype][1]} {rating[1]}', callback_data=c_down_data)
    keyboard = InlineKeyboardMarkup([[button_up, button_down]])
    return keyboard

def change_channel_context_keyboard(channels, back_to=''):
    switch_channel_keyboard = [
            InlineKeyboardButton(text=f'@{c.channel_username}', 
                                callback_data=f'switch_context:{c.channel_id}:{back_to}')
            for c in channels
        ]
    return InlineKeyboardMarkup([[btn] for btn in switch_channel_keyboard])

def default_settings_keyboard(user):
    button_contexts = InlineKeyboardButton(text=f'📚 Контекст | @{user.current_channel.channel_username}', callback_data='context_keyboard:defaults')
    button_close = InlineKeyboardButton(text='❌ Закрыть', callback_data='delete')
    keyboard = InlineKeyboardMarkup([[button_contexts],
                                    [button_close]])
    return keyboard