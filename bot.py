from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from function_handle.fetch_puzzle_data import fetch_puzzle_data
from function_handle.searcher import search
from function_handle.event_check import get_event_data

# Function to handle the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! I am your bot.')

# Function to echo messages
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.text)

# Placeholder functions to be implemented
async def get_event_data_handle(event_name, event_level):
    result = get_event_data(event_name,event_level)
    return result

async def search_handle(search_query):
    result = search(search_query)
    return result

async def fetch_puzzle_data_handle(name, group_number, puzzle_number):
    result = fetch_puzzle_data(name,group_number,puzzle_number)
    return result

# Handler function for /get_event_data command
async def handle_get_event_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) < 2:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Usage: /get_event_data <event_name> <event_level>")
        return
    
    event_name = context.args[0]
    event_level = context.args[1]
    result = await get_event_data_handle(event_name, event_level)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Search Results: {result}")

# Handler function for /search command
async def handle_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Usage: /search <search_query>")
        return
    
    search_query = ' '.join(context.args)
    result = await search_handle(search_query)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Search Results: {result}")

# Handler function for /fetch_puzzle_data command
async def handle_fetch_puzzle_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) < 3:
        await update.message.reply_text("Usage: /fetch_puzzle_data <name> <group_number> <puzzle_number>")
        return
    
    name = context.args[0]
    group_number = context.args[1]
    puzzle_number = context.args[2]
    result = await fetch_puzzle_data_handle(name, group_number, puzzle_number)
    await update.message.reply_text(f"Puzzle Data: {result}")


def main():
    # Insert your bot token here
    application = ApplicationBuilder().token("TOKEN").build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("get_event_data", handle_get_event_data))
    application.add_handler(CommandHandler("search", handle_search))
    application.add_handler(CommandHandler("fetch_puzzle_data", handle_fetch_puzzle_data))


    # Start polling for updates
    application.run_polling()

if __name__ == '__main__':
    main()
