import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)
from t_for_bot import predict____  # prediction function

# Token
BOT_TOKEN = "tg_token"

# Global variables
video_count = 0   # Counter for processed videos
user_state = {}   # Dictionary for storing user states


# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome = f"<b>Hello {update.effective_user.first_name}!!! We are glad you joined our project!</b>"
    await update.message.reply_text(welcome)
    await update.message.reply_text("Please send a video for analysis.")
    user_state[update.effective_chat.id] = "ready"


# /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "<b>Help menu:</b>\n"
        "/start - Start working with the bot\n"
        "/help - Show this message\n"
        "/stats - Show statistics\n"
        "/cancel - Cancel the current action\n"
        "Simply send a video file for analysis.\n"
    )
    await update.message.reply_text(help_text)


# /cancel command
async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_state[update.effective_chat.id] = "ready"
    await update.message.reply_text(
        "❌Current action canceled. You can send a new video."
    )


# /stats command
async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global video_count
    markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Send new video", callback_data="new_video")]]
    )
    await update.message.reply_text(
        f"Total processed videos: {video_count}",
        reply_markup=markup
    )


# Handle received video
async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global video_count
    try:
        chat_id = update.effective_chat.id

        # Get video file
        video = update.message.video
        file = await context.bot.get_file(video.file_id)

        # Create folder if not exists
        if not os.path.exists("videos"):
            os.makedirs("videos")

        # Save 
        video_path = f"videos/{video.file_id}.mp4"
        await file.download_to_drive(video_path)

        video_count += 1
        await update.message.reply_text("✅Video received. Analyzing...")

        # Call prediction function
        pred_class, conf = predict____(video_path)

        await update.message.reply_text(
            f"Prediction: {pred_class}\n"
            f"Confidence: {conf}%\n"
            f"Total videos: {video_count}"
        )

        # Two buttons
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("New video", callback_data="new_video"),
             InlineKeyboardButton("Statistics", callback_data="show_stats")]
        ])

        await update.message.reply_text("Choose an action:", reply_markup=markup)
        user_state[chat_id] = "ready"

    except Exception as e:
        await update.message.reply_text("⚠️ Error while processing the video.")
        user_state[update.effective_chat.id] = "error"


# Handle button callbacks
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global video_count
    query = update.callback_query
    await query.answer()

    try:
        if query.data == "new_video":
            await query.message.reply_text("Send a new video for analysis.")
            user_state[query.message.chat.id] = "ready"

        elif query.data == "show_stats":
            last_video = (
                os.listdir("videos")[-1]
                if os.path.exists("videos") and len(os.listdir("videos")) > 0
                else "no data"
            )
            markup = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🎥 Send new video", callback_data="new_video")]]
            )
            await query.message.reply_text(
                f"Statistics:\n"
                f"Processed videos: {video_count}\n"
                f"Last video: {last_video}",
                reply_markup=markup
            )

        # Remove old buttons
        await query.edit_message_reply_markup(reply_markup=None)

    except Exception as e:
        print(f"Error in callback: {e}")


def main():
    print("Running...")
    app = Application.builder().token(BOT_TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("cancel", cancel_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(MessageHandler(filters.VIDEO, handle_video))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_polling()


if __name__ == "__main__":
    main()
