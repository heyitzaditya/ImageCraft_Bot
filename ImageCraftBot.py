import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes,
    MessageHandler, filters
)
from telegram.constants import ParseMode

BOT_TOKEN = "8305414697:AAEhSkZJZ7IroREzVN0j7K7irGwRfNmLjzc"
API_URL = "https://text-to-image.bjcoderx.workers.dev/?text="

ABOUT_USER = (
    "@ftd8s, a Python programmer, He develop and enhance python scripts.\n\n"
    "Dm @ftd8s for any query!"
)
ABOUT_BOT = (
    "This bot generates AI images based on your prompts.\n\n"
    "Use /generate <your prompt> to create an image.\n\n"
    "Example: `/generate A dragon flying over mountains`\n\n"
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    text = (
        f"👋 Hello {user_name}!\n\n"
        f"{ABOUT_BOT}\n\n"
        f"**About Developer:**\n{ABOUT_USER}"
    )
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "❗ Please provide a prompt. Example:\n`/generate A cat in space`",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    prompt = " ".join(context.args)
    waiting_message = await update.message.reply_text(
        "🎨 Generating image... Please wait for 10 to 20 seconds."
    )

    url = API_URL + requests.utils.quote(prompt)
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            await context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=waiting_message.message_id
            )
            await update.message.reply_photo(photo=response.content, caption=f"Prompt: {prompt}")
        else:
            await waiting_message.edit_text("❌ Failed to generate image. Try again.")
    except Exception as e:
        await waiting_message.edit_text(f"⚠️ Error: {e}")

async def invalid_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❌ Invalid command!\n\n"
        "Use /generate <prompt> to create an image.\n\n"
        "Example: `/generate A dragon flying over mountains`",
        parse_mode=ParseMode.MARKDOWN
    )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("generate", generate))
    # Catch all other commands and text
    app.add_handler(MessageHandler(filters.COMMAND | filters.TEXT, invalid_command))

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
