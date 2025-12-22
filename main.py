from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8538748627:AAGaOYs-V17YITSPENRWWPTJSvVY4ZssCos"

# DADOS REAIS DO SOFASCORE - 22/12/2025
JOGOS = {
    "fulham x nottingham forest": {
        "liga": "Premier League", "data": "22/12 - 20h00",
        "casa": "Fulham", "fora": "Nottingham Forest",
        "forca_casa": 70, "forca_fora": 72,
        "gols_casa": 1.4, "gols_fora": 1.3,
        "gols_sofr_casa": 1.3, "gols_sofr_fora": 1.1,
        "cantos_casa": 5.0, "cantos_fora": 4.8,
        "cartoes_casa": 1.6, "cartoes_fora": 1.8,
        "forma_casa": "VDVDV", "forma_fora": "VVLLV",
        "posicao_casa": 9, "posicao_fora": 15,
        "h2h_gols": 2.5,
        "odds_casa": 2.50, "odds_empate": 3.30, "odds_fora": 2.88,
        "contexto": "Jogo equilibrado. Fulham leve favorito em casa. Forest com forma irregular."
    },
    "athletic club x espanyol": {
        "liga": "LaLiga", "data": "22/12 - 20h00",
        "casa": "Athletic Club", "fora": "Espanyol",
        "forca_casa": 78, "forca_fora": 58,
        "gols_casa": 1.6, "gols_fora": 1.0,
        "gols_sofr_casa": 0.8, "gols_sofr_fora": 1.6,
        "cantos_casa": 5.5, "cantos_fora": 4.0,
        "cartoes_casa": 2.0, "cartoes_fora": 2.2,
        "forma_casa": "LWWWW", "forma_fora": "DLDLD",
        "posicao_casa": 5, "posicao_fora": 18,
        "h2h_gols": 2.2,
        "odds_casa": 1.85, "odds_empate": 3.30, "odds_fora": 4.75,
        "contexto": "Athletic FAVORITO! 4 vitorias seguidas. Espanyol luta contra rebaixamento."
    },
    "napoli x bologna": {
        "liga": "Supercoppa Italiana", "data": "22/12 - 19h00",
        "casa": "Napoli", "fora": "Bologna",
        "forca_casa": 82, "forca_fora": 72,
        "gols_casa": 2.0, "gols_fora": 1.5,
        "gols_sofr_casa": 0.8, "gols_sofr_fora": 1.2,
        "cantos_casa": 5.8, "cantos_fora": 5.0,
        "cartoes_casa": 1.8, "cartoes_fora": 2.0,
        "forma_casa": "VVVDV", "forma_fora": "VDVDV",
        "posicao_casa": 1, "posicao_fora": 7,
        "h2h_gols": 2.5,
        "odds_casa": 2.15, "odds_empate": 3.10, "odds_fora": 3.70,
        "contexto": "Napoli favorito. Lider da Serie A contra Bologna."
    },
}

def calcular_prob_resultado(jogo):
    odds_casa = jogo["odds_casa"]
    odds_empate = jogo["odds_empate"]
    odds_fora = jogo["odds_fora"]
    prob_casa = round((1 / odds_casa) * 100 * 0.9)
    prob_empate = round((1 / odds_empate) * 100 * 0.9)
    prob_fora = round((1 / odds_fora) * 100 * 0.9)
    total = prob_casa + prob_empate + prob_fora
    prob_casa = round((prob_casa / total) * 100)
    prob_empate = round((prob_empate / total) * 100)
    prob_fora = 100 - prob_casa - prob_empate
    return prob_casa, prob_empate, prob_fora

def calcular_prob_gols(jogo):
    media_gols = jogo["gols_casa"] + jogo["gols_fora"]
    h2h = jogo.get("h2h_gols", media_gols)
    media_ajustada = (media_gols + h2h) / 2
    prob_over05 = min(95, 50 + (media_ajustada - 1.0) * 25)
    prob_over15 = min(92, 40 + (media_ajustada - 1.5) * 22)
    prob_over25 = min(85, 25 + (media_ajustada - 2.0) * 18)
    prob_over35 = min(75, 15 + (media_ajustada - 2.5) * 14)
    prob_btts_casa = min(1, jogo["gols_casa"] / 2)
    prob_btts_fora = min(1, jogo["gols_fora"] / 2)
    prob_btts = round(prob_btts_casa * prob_btts_fora * 100)
    return {
        "over05": round(max(30, prob_over05)),
        "over15": round(max(25, prob_over15)),
        "over25": round(max(20, prob_over25)),
        "over35": round(max(15, prob_over35)),
        "btts": max(25, min(80, prob_btts))
    }

def calcular_prob_cantos(jogo):
    total = jogo["cantos_casa"] + jogo["cantos_fora"]
    prob_over85 = min(85, 30 + (total - 8.5) * 15)
    prob_over95 = min(75, 25 + (total - 9.5) * 12)
    prob_over105 = min(65, 20 + (total - 10.5) * 10)
    return {"over85": round(max(20, prob_over85)), "over95": round(max(15, prob_over95)), "over105": round(max(10, prob_over105))}

def calcular_prob_cartoes(jogo):
    total = jogo["cartoes_casa"] + jogo["cartoes_fora"]
    prob_over25 = min(85, 30 + (total - 2.5) * 20)
    prob_over35 = min(75, 20 + (total - 3.5) * 15)
    prob_over45 = min(60, 15 + (total - 4.5) * 12)
    return {"over25": round(max(20, prob_over25)), "over35": round(max(15, prob_over35)), "over45": round(max(10, prob_over45))}

def encontrar_melhor_aposta(jogo, prob_casa, prob_empate, prob_fora, prob_gols, prob_cantos, prob_cartoes):
    apostas = []
    if prob_casa >= 60:
        apostas.append(("Vitoria " + jogo["casa"], prob_casa, "1.5u"))
    elif prob_casa >= 50:
        apostas.append(("Vitoria " + jogo["casa"], prob_casa, "1.0u"))
    if prob_fora >= 60:
        apostas.append(("Vitoria " + jogo["fora"], prob_fora, "1.5u"))
    elif prob_fora >= 50:
        apostas.append(("Vitoria " + jogo["fora"], prob_fora, "1.0u"))
    if prob_casa + prob_empate >= 70 and prob_casa < 55:
        apostas.append(("Dupla 1X (" + jogo["casa"] + " ou Empate)", prob_casa + prob_empate, "1.0u"))
    if prob_fora + prob_empate >= 70 and prob_fora < 55:
        apostas.append(("Dupla X2 (Empate ou " + jogo["fora"] + ")", prob_fora + prob_empate, "1.0u"))
    if prob_gols["over25"] >= 65:
        apostas.append(("Over 2.5 Gols", prob_gols["over25"], "1.5u" if prob_gols["over25"] >= 75 else "1.0u"))
    elif prob_gols["over15"] >= 75:
        apostas.append(("Over 1.5 Gols", prob_gols["over15"], "1.0u"))
    if prob_gols["over25"] <= 35:
        apostas.append(("Under 2.5 Gols", 100 - prob_gols["over25"], "1.0u"))
    if prob_gols["btts"] >= 60:
        apostas.append(("Ambas Marcam (BTTS)", prob_gols["btts"], "1.0u"))
    apostas.sort(key=lambda x: x[1], reverse=True)
    return apostas[:4]
def analisar_jogo(jogo_key):
    jogo = JOGOS.get(jogo_key.lower().strip())
    if not jogo:
        for key in JOGOS.keys():
            if jogo_key.lower() in key or key in jogo_key.lower():
                jogo = JOGOS[key]
                jogo_key = key
                break
    if not jogo:
        return None
    prob_casa, prob_empate, prob_fora = calcular_prob_resultado(jogo)
    prob_gols = calcular_prob_gols(jogo)
    prob_cantos = calcular_prob_cantos(jogo)
    prob_cartoes = calcular_prob_cartoes(jogo)
    melhores = encontrar_melhor_aposta(jogo, prob_casa, prob_empate, prob_fora, prob_gols, prob_cantos, prob_cartoes)
    total_gols = jogo["gols_casa"] + jogo["gols_fora"]
    total_cantos = jogo["cantos_casa"] + jogo["cantos_fora"]
    total_cartoes = jogo["cartoes_casa"] + jogo["cartoes_fora"]
    analise = f"""
=============================
{jogo_key.upper()}
{jogo["liga"]} - {jogo["data"]}
=============================
{jogo["contexto"]}

POSICOES: {jogo["casa"]} ({jogo["posicao_casa"]}o) vs {jogo["fora"]} ({jogo["posicao_fora"]}o)
FORMA: {jogo["casa"]} {jogo["forma_casa"]} | {jogo["fora"]} {jogo["forma_fora"]}

--- RESULTADO (Odds) ---
{jogo["casa"]}: {prob_casa}% (Odd {jogo["odds_casa"]})
Empate: {prob_empate}% (Odd {jogo["odds_empate"]})
{jogo["fora"]}: {prob_fora}% (Odd {jogo["odds_fora"]})

Dupla 1X: {prob_casa + prob_empate}%
Dupla X2: {prob_empate + prob_fora}%

--- GOLS (Media: {total_gols:.1f}) ---
Over 0.5: {prob_gols["over05"]}%
Over 1.5: {prob_gols["over15"]}%
Over 2.5: {prob_gols["over25"]}%
Over 3.5: {prob_gols["over35"]}%
BTTS: {prob_gols["btts"]}%

--- CANTOS (Media: {total_cantos:.1f}) ---
Over 8.5: {prob_cantos["over85"]}%
Over 9.5: {prob_cantos["over95"]}%
Over 10.5: {prob_cantos["over105"]}%

--- CARTOES (Media: {total_cartoes:.1f}) ---
Over 2.5: {prob_cartoes["over25"]}%
Over 3.5: {prob_cartoes["over35"]}%
Over 4.5: {prob_cartoes["over45"]}%

=============================
MELHORES APOSTAS:
=============================
"""
    for i, (aposta, prob, unid) in enumerate(melhores, 1):
        conf = "ALTA" if prob >= 65 else "MEDIA"
        analise += f"{i}. {aposta}\n   {prob}% | {conf} | {unid}\n"
    return analise

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("BOT DE ANALISE ESPORTIVA\nDados: Sofascore (22/12)\n\nComandos:\n/jogos - Todos os jogos\n/melhores - Melhores apostas\n/premier - Premier League\n/laliga - LaLiga\n\nOu digite: Athletic Club x Espanyol")

async def jogos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lista = "JOGOS DE HOJE (22/12):\n\n"
    for jogo_key, dados in JOGOS.items():
        p1, pe, p2 = calcular_prob_resultado(dados)
        fav = dados["casa"] if p1 > p2 else dados["fora"]
        prob_fav = max(p1, p2)
        lista += f"{jogo_key.title()}\n  {dados['data']} | {dados['liga']}\n  Favorito: {fav} ({prob_fav}%)\n\n"
    await update.message.reply_text(lista)

async def melhores(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lista = "MELHORES APOSTAS (22/12):\n\n"
    todas = []
    for jogo_key, jogo in JOGOS.items():
        p1, pe, p2 = calcular_prob_resultado(jogo)
        pg = calcular_prob_gols(jogo)
        pc = calcular_prob_cantos(jogo)
        pca = calcular_prob_cartoes(jogo)
        melhores_jogo = encontrar_melhor_aposta(jogo, p1, pe, p2, pg, pc, pca)
        for ap, prob, un in melhores_jogo:
            if prob >= 55:
                todas.append((jogo_key, jogo["data"], ap, prob, un, jogo["liga"]))
    todas.sort(key=lambda x: x[3], reverse=True)
    for i, (j, data, ap, prob, un, liga) in enumerate(todas[:10], 1):
        conf = "ALTA" if prob >= 65 else "MEDIA"
        lista += f"{i}. {j.title()}\n   {liga} - {data}\n   {ap}\n   {prob}% | {conf} | {un}\n\n"
    await update.message.reply_text(lista)

async def premier(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lista = "PREMIER LEAGUE (22/12):\n\n"
    for jogo_key, dados in JOGOS.items():
        if dados["liga"] == "Premier League":
            p1, pe, p2 = calcular_prob_resultado(dados)
            lista += f"{jogo_key.title()}\n  {dados['data']}\n  {dados['casa']} {p1}% | Emp {pe}% | {dados['fora']} {p2}%\n  Forma: {dados['forma_casa']} vs {dados['forma_fora']}\n\n"
    await update.message.reply_text(lista)

async def laliga(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lista = "LALIGA (22/12):\n\n"
    for jogo_key, dados in JOGOS.items():
        if dados["liga"] == "LaLiga":
            p1, pe, p2 = calcular_prob_resultado(dados)
            lista += f"{jogo_key.title()}\n  {dados['data']}\n  {dados['casa']} {p1}% | Emp {pe}% | {dados['fora']} {p2}%\n  Forma: {dados['forma_casa']} vs {dados['forma_fora']}\n\n"
    await update.message.reply_text(lista)

async def mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.lower().replace(" vs ", " x ").replace(" - ", " x ")
    analise = analisar_jogo(texto)
    if analise:
        await update.message.reply_text(analise)
    else:
        await update.message.reply_text("Jogo nao encontrado. Use /jogos para ver disponiveis.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("jogos", jogos))
    app.add_handler(CommandHandler("melhores", melhores))
    app.add_handler(CommandHandler("premier", premier))
    app.add_handler(CommandHandler("laliga", laliga))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mensagem))
    print("Bot iniciado!")
    app.run_polling()

if __name__ == "__main__":
    main()
