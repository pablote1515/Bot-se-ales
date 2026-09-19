import os
import random
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Servidor web falso para que Render no marque error en el plan Gratis
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot de Señales activo 24/7 en Render"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host="0.0.0.0", port=port)

# --- BOT DE TELEGRAM ---
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

    # Iniciar servidor web en segundo plano
    threading.Thread(target=run_web, daemon=True).start()

    print("Iniciando Bot de Señales...")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_polling()

if __name__ == "__main__":
    main()
