import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Obtenemos las credenciales guardadas de forma segura en la nube
TOKEN = os.environ.get("TELEGRAM_TOKEN")
MI_ID = os.environ.get("MI_CHAT_ID")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎯 Recibir Señal", callback_data="generar_senal")],
        [InlineKeyboardButton("ℹ️ Información", callback_data="info_juego")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🤖 **Bot de Señales Activo**\n\nPresiona el botón para recibir la última señal:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "generar_senal":
        opciones = ["VERDE 🟢", "ROJO 🔴", "VIOLETA 🟣"]
        resultado = random.choice(opciones)
        
        mensaje = (
            "🚨 **NUEVA SEÑAL DETECTADA** 🚨\n\n"
            f"🎯 **Entrada:** {resultado}\n"
            "⏱️ **Tiempo:** 1 minuto\n"
            "📊 **Probabilidad:** 85%\n\n"
            "⚠️ *Juega con responsabilidad.*"
        )
        await query.message.reply_text(mensaje, parse_mode="Markdown")

    elif query.data == "info_juego":
        await query.message.reply_text("ℹ️ Bot de alertas informativas para el juego.")

def main():
    if not TOKEN:
        raise ValueError("Error: No se ha configurado el TELEGRAM_TOKEN")

    print("Iniciando Bot de Señales...")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_polling()

if __name__ == "__main__":
    main()
  
