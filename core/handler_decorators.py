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

def add_user(handler_function):
    def wrapper(update, context):
        if update.callback_query:
            message = update.callback_query.message
            user = update.callback_query.from_user
            chat = message.chat
            if not db.check_user_exist(user.id) and \
                    db.get_current_channel():
                db.add_user(update.callback_query.from_user.id,
                            update.callback_query.from_user.username,
                            db.get_channel(message.chat.id).id)
        handler_function(update, context)
    return wrapper