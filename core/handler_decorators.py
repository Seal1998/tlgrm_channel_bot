from core import database as db

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
            if not db.check_user_exist(user.id, chat.id):
                db.add_user(update.callback_query.from_user.id,
                            update.callback_query.from_user.username,
                            chat.id)
        handler_function(update, context)
    return wrapper