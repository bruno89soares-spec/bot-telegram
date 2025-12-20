from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8538748627:AAGaOYs-V17YITSPENRWWPTJSvVY4ZssCos"

JOGOS = {
    "tottenham x liverpool": {"liga": "Premier League", "gols_casa": 2.1, "gols_fora": 2.4, "cantos_casa": 5.2, "cantos_fora": 6.1, "cartoes_casa": 1.8, "cartoes_fora": 2.0, "contexto": "Clássico inglês, alta intensidade"},
    "arsenal x crystal palace": {"liga": "Premier League", "gols_casa": 2.3, "gols_fora": 1.1, "cantos_casa": 6.5, "cantos_fora": 4.2, "cartoes_casa": 1.5, "cartoes_fora": 2.1, "contexto": "Arsenal em casa forte"},
    "real madrid x barcelona": {"liga": "LaLiga", "gols_casa": 2.0, "gols_fora": 2.2, "cantos_casa": 5.5, "cantos_fora": 5.8, "cartoes_casa": 2.5, "cartoes_fora": 2.8, "contexto": "El Clásico, máxima intensidade"},
    "bayern x dortmund": {"liga": "Bundesliga", "gols_casa": 2.8, "gols_fora": 2.1, "cantos_casa": 6.2, "cantos_fora": 5.0, "cartoes_casa": 1.9, "cartoes_fora": 2.2, "contexto": "Der Klassiker"},
    "inter x milan": {"liga": "Serie A", "gols_casa": 1.9, "gols_fora": 1.7, "cantos_casa": 5.5, "cantos_fora": 5.0, "cartoes_casa": 2.3, "cartoes_fora": 2.5, "contexto": "Derby della Madonnina"},
    "psg x marseille": {"liga": "Ligue 1", "gols_casa": 2.5, "gols_fora": 1.3, "cantos_casa": 6.8, "cantos_fora": 4.5, "cartoes_casa": 2.0, "cartoes_fora": 2.8, "contexto": "Le Classique"},
}

def analisar_jogo(jogo_key):
    jogo = JOGOS.get(jogo_key.lower())
    if not jogo:
        return None
    total_gols = jogo["gols_casa"] + jogo["gols_fora"]
    total_cantos = jogo["cantos_casa"] + jogo["cantos_fora"]
    total_cartoes = jogo["cartoes_casa"] + jogo["cartoes_fora"]
    analise = f"""
⚽ *ANÁLISE: {jogo_key.upper()}*
🏆 {jogo["liga"]}

📋 *CONTEXTO:*
{jogo["contexto"]}

📊 *MÉDIAS ÚLTIMOS 5 JOGOS:*

*GOLS:*
• Casa: {jogo["gols_casa"]:.1f} | Fora: {jogo["gols_fora"]:.1f}
• Total esperado: {total_gols:.1f}
• Veredicto: {"Over 2.5 ✅" if total_gols > 2.5 else "Under 2.5 ✅"}

*CANTOS:*
• Casa: {jogo["cantos_casa"]:.1f} | Fora: {jogo["cantos_fora"]:.1f}
• Total esperado: {total_cantos:.1f}
• Veredicto: {"Over 9.5 ✅" if total_cantos > 9.5 else "Under 9.5 ✅"}

*CARTÕES:*
• Casa: {jogo["cartoes_casa"]:.1f} | Fora: {jogo["cartoes_fora"]:.1f}
• Total esperado: {total_cartoes:.1f}
• Veredicto: {"Over 4.5 ✅" if total_cartoes > 4.5 else "Under 4.5 ✅"}

💰 *RECOMENDAÇÃO:*
• Aposta: {"Over 2.5 Gols" if total_gols > 2.5 else "Under 2.5 Gols"}
• Unidades: 1.0u
• Confiança: Alta
"""
    return analise

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 *Bot de Análise Esportiva*\n\nComandos:\n/jogos - Ver jogos disponíveis\n/melhores - Melhores apostas\n\nOu digite o jogo: *Tottenham x Liverpool*", parse_mode="Markdown")

async def jogos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lista = "⚽ *JOGOS DISPONÍVEIS:*\n\n"
    for jogo in JOGOS.keys():
        lista += f"• {jogo.title()}\n"
    await update.message.reply_text(lista, parse_mode="Markdown")

async def melhores(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔥 *MELHORES APOSTAS:*\n\n1. Tottenham x Liverpool - Over 2.5 ✅\n2. Bayern x Dortmund - Over 2.5 ✅\n3. PSG x Marseille - Over 2.5 ✅", parse_mode="Markdown")

async def mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.lower()
    analise = analisar_jogo(texto)
    if analise:
        await update.message.reply_text(analise, parse_mode="Markdown")
    else:
        await update.message.reply_text("Jogo não encontrado. Use /jogos para ver disponíveis.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("jogos", jogos))
    app.add_handler(CommandHandler("melhores", melhores))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mensagem))
    print("Bot iniciado!")
    app.run_polling()

if __name__ == "__main__":
    main()
