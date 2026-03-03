import random
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

# Единая подпись для всех картинок
PHOTO_CAPTION = "✨котик для настроения✨"

# Загружаем текстовые предсказания
def load_predictions():
    with open("predictions.txt", "r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]

# Загружаем картинки из папки images
def load_images():
    image_folder = "images"
    files = os.listdir(image_folder)
    return [
        os.path.join(image_folder, f)
        for f in files
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

PREDICTIONS = load_predictions()
IMAGES = load_images()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Напиши /KindFuture 🔮")

async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = random.choice(["text", "photo"])

    if choice == "text" and PREDICTIONS:
        prediction = random.choice(PREDICTIONS)
        await update.message.reply_text(prediction)

    elif choice == "photo" and IMAGES:
        image_path = random.choice(IMAGES)
        with open(image_path, "rb") as photo:
            await update.message.reply_photo(
                photo=photo,
                caption=PHOTO_CAPTION
            )

    else:
        await update.message.reply_text("Пока нет контента 😢")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("KindFuture", predict))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
