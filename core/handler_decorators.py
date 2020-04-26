def check_user_flags(handler_function):
    def wrapper(update, context):
        ud = context.user_data
        if 'setchannel_query' in ud.keys() and ud['setchannel_query']:
            try:
                global_context['channel_id'] = update.message.forward_from_chat.id
                update.message.reply_text('Ок. Чат запомнил')
                del context.user_data['setchannel_query']
            except:
                handler_function(update, context)
        else:
            handler_function(update, context)
    return wrapper

def callback(handler_function):
    def wrapper(update, context):
        handler_function(update, context)
        update.callback_query.answer()
    return wrapper