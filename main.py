import logging
from pymongo import MongoClient
from telegram import Update
from telegram.ext import Updater, MessageHandler, CallbackContext

TOKEN = "5058249365:AAE7RbZy5yn28LYjmfFlFt9WxalJrDny8zk"
MONGO_URI = "mongodb+srv://abc:abcd@cluster0.nkcgfam.mongodb.net/?retryWrites=true&w=majority"  # Update with your MongoDB connection URI
DATABASE_NAME = "telegram_chat_analysis"
COLLECTION_NAME = "chat_data"

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a MongoDB client and connect to the database
mongo_client = MongoClient(MONGO_URI)
db = mongo_client[DATABASE_NAME]
collection = db[COLLECTION_NAME]


def store_chat_data(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    message = update.message.text

    # Check if the message is a reply to a previous message
    if update.message.reply_to_message:
        # Retrieve the ID of the message being replied to
        replied_message_id = update.message.reply_to_message.message_id

        # Retrieve the text of the replied message
        replied_message = update.message.reply_to_message.text

        # Store the question, reply, and user information in the MongoDB collection
        data = {
            "chat_id": chat_id,
            "user_id": user_id,
            "question": replied_message,
            "reply": message
        }
        collection.insert_one(data)


def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Register the message handler to analyze and store chat data
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), store_chat_data))

    updater.start_polling()
    logger.info("Bot started polling...")
    updater.idle()


if __name__ == '__main__':
    main()
