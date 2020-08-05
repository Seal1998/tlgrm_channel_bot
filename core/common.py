from core.keyboards import rating_keyboard
import random

def publish_post(bot, chat_id, message=None, message_id=None, text=None, caption=None, photo=None, video=None, document=None):
    text = message.text if message else text
    photo = message.photo if message else photo
    video = message.video if message else video
    document = message.document if message else document
    caption = message.caption if message else caption
    message_id = message.message_id if message else message_id
    if text:
        bot.send_message(chat_id, text=text, reply_markup=rating_keyboard(message_id=message_id))
    elif photo:
        bot.send_photo(chat_id, photo=photo[0], reply_markup=rating_keyboard(message_id=message_id), caption=caption)
    elif video:
        bot.send_video(chat_id, video=video, reply_markup=rating_keyboard(message_id=message_id), caption=caption)
    elif document:
        bot.send_document(chat_id, document=document, reply_markup=rating_keyboard(message_id=message_id), caption=caption)