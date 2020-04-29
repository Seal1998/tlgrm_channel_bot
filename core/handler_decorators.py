from core import database as db

def check_user_flags(handler_function):
    def wrapper(update, context):
        ud = context.user_data
        if 'addchannel_query' in ud.keys() and ud['addchannel_query']:
            try:
                #проверить, что бот администратор в канале
                if db.add_channel(update.message.forward_from_chat.id):
                    update.message.reply_text('Ок. Канал запомнил')
                else:
                    update.message.reply_text('Канал уже добавлен')
                del context.user_data['addchannel_query']
            except:
                handler_function(update, context)
        else:
            handler_function(update, context)
    return wrapper

def callback(func=None, *, alert:str=None):
    def alert_wrapper(callback_function):
        def wrapper(update, context):
            callback_function(update, context)
            update.callback_query.answer(text=alert)
        return wrapper
    if func:
        return alert_wrapper(func)
    else:
        return alert_wrapper

def delete(handler_function):
    def wrapper(update, context):
        handler_function(update, context)
        if update.callback_query:
            message = update.callback_query.message
        else:
            message = update.message
        message.delete()
    return wrapper