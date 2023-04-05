import evaluate
import storage

from telegram import Update
from telegram.ext import Application, filters, MessageHandler, CommandHandler

db = storage.Storage()

def load_token(file_path):
    with open(file_path, 'r') as f:
        return f.read().rstrip()

async def on_message(update, context):
    message = update.message
    user = message.from_user
    user_name = user.name
    user_id = user.id

    db.set_name(user_id, user_name)

    text = message.text
    if text == None:
        return

    message_score = evaluate.evaluate(text)
    old_user_score = db.get_score(user_id)
    new_user_score = evaluate.compute_updated_user_score(old_user_score, message_score)
    print('User(id={}) old_score={:.2f} new_score={:.2f}'.format(user_id, old_user_score, new_user_score))

    db.set_score(user_id, new_user_score)
    db.save_to('state.pickle')

async def on_get_my_score(update, context):
    message = update.message
    user = message.from_user
    user_id = user.id
    user_score = db.get_score(user_id)

    await update.effective_message.reply_text('{:.2f}'.format(user_score))

async def on_score_table(update, context):
    user_id_score_pairs = db.list_everyone()

    result = []
    for user_id, score in user_id_score_pairs:
        user_name = db.get_name(user_id)
        result.append('{} {:.2f}'.format(user_name, score))

    result = '\n'.join(result)
    if result == '':
        result = 'Nothing to show'

    await update.effective_message.reply_text(result)

def main(token):
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler('get_my_score', on_get_my_score))
    application.add_handler(CommandHandler('score_table', on_score_table))
    application.add_handler(MessageHandler(filters.ALL, on_message))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    token = load_token('token.txt')
    db.load_from('state.pickle')
    main(token)
