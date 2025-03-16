#huggingface на этом сайте найдешь создашь айпи токен для ии
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


def generate_image_with_huggingface(description):
    
    url = "токен для генер."

   
    headers = {
        "Authorization": "Bearer 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"  
    }

   
    payload = {
        "inputs": description, 
        "options": {"wait_for_model": True}
    }

   
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()  
       
        with open("generated_image.png", "wb") as f:
            f.write(response.content)
        return "generated_image.png"
    except requests.exceptions.RequestException as e:
        raise Exception(f"Ошибка при выполнении запроса: {e}")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Напиши /generate <описание>, чтобы сгенерировать изображение.")

async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Пожалуйста, напишите описание после команды /generate.")
        return

    description = ' '.join(context.args)
    try:
        image_path = generate_image_with_huggingface(description)  
        with open(image_path, "rb") as img:
            await update.message.reply_photo(photo=img)
    except Exception as e:
        await update.message.reply_text(f"Ошибка при генерации изображения: {e}")



if __name__ == '__main__':
    app = ApplicationBuilder().token("бот токен").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("generate", generate))



    print("Бот запущен!")
    app.run_polling()
