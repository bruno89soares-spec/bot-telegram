from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8538748627:AAGaOYs-V17YITSPENRWWPTJSvVY4ZssCos"

JOGOS = {
    "newcastle x chelsea": {
        "liga": "Premier League", "data": "20/12 - 09h30",
        "casa": "Newcastle", "fora": "Chelsea",
        "forca_casa": 72, "forca_fora": 78,
        "gols_casa": 1.8, "gols_fora": 2.2,
        "gols_sofr_casa": 1.4, "gols_sofr_fora": 1.0,
        "cantos_casa": 5.5, "cantos_fora": 5.8,
        "cartoes_casa": 1.6, "cartoes_fora": 1.9,
        "forma_casa": "VVDEV", "forma_fora": "VVVEV",
        "contexto": "Newcastle em casa forte, Chelsea em boa fase"
    },
    "manchester city x west ham": {
        "liga": "Premier League", "data": "20/12 - 12h00",
        "casa": "Man City", "fora": "West Ham",
        "forca_casa": 88, "forca_fora": 68,
        "gols_casa": 2.8, "gols_fora": 1.0,
        "gols_sofr_casa": 1.2, "gols_sofr_fora": 1.8,
        "cantos_casa": 7.2, "cantos_fora": 3.5,
        "cartoes_casa": 1.2, "cartoes_fora": 1.8,
        "forma_casa": "DEVDD", "forma_fora": "DVDVE",
        "contexto": "City em crise mas favorito em casa"
    },
    "tottenham x liverpool": {
        "liga": "Premier League", "data": "20/12 - 14h30",
        "casa": "Tottenham", "fora": "Liverpool",
        "forca_casa": 76, "forca_fora": 90,
        "gols_casa": 2.1, "gols_fora": 2.6,
        "gols_sofr_casa": 1.4, "gols_sofr_fora": 0.6,
        "cantos_casa": 5.5, "cantos_fora": 6.2,
        "cartoes_casa": 1.8, "cartoes_fora": 1.5,
        "forma_casa": "VDVEV", "forma_fora": "VVVVV",
        "contexto": "CLASSICO! Liverpool lider invicto"
    },
    "everton x arsenal": {
        "liga": "Premier League", "data": "20/12 - 17h00",
        "casa": "Everton", "fora": "Arsenal",
        "forca_casa": 62, "forca_fora": 85,
        "gols_casa": 1.2, "gols_fora": 2.4,
        "gols_sofr_casa": 1.8, "gols_sofr_fora": 0.8,
        "cantos_casa": 4.0, "cantos_fora": 6.5,
        "cartoes_casa": 2.2, "cartoes_fora": 1.6,
        "forma_casa": "DDDVE", "forma_fora": "VVVEV",
        "contexto": "Arsenal favorito, Everton em crise"
    },
    "wolves x brentford": {
        "liga": "Premier League", "data": "20/12 - 12h00",
        "casa": "Wolves", "fora": "Brentford",
        "forca_casa": 65, "forca_fora": 70,
        "gols_casa": 1.4, "gols_fora": 1.8,
        "gols_sofr_casa": 1.6, "gols_sofr_fora": 1.4,
        "cantos_casa": 4.8, "cantos_fora": 5.2,
        "cartoes_casa": 2.0, "cartoes_fora": 1.8,
        "forma_casa": "DDDVD", "forma_fora": "VEVVE",
        "contexto": "Wolves em ma fase, Brentford consistente"
    },
    "real madrid x sevilla": {
        "liga": "LaLiga", "data": "20/12 - 17h00",
        "casa": "Real Madrid", "fora": "Sevilla",
        "forca_casa": 92, "forca_fora": 72,
        "gols_casa": 2.5, "gols_fora": 1.0,
        "gols_sofr_casa": 0.8, "gols_sofr_fora": 1.6,
        "cantos_casa": 6.5, "cantos_fora": 4.0,
        "cartoes_casa": 2.0, "cartoes_fora": 2.5,
        "forma_casa": "VVVEV", "forma_fora": "DEVDD",
        "contexto": "Real Madrid em casa, Sevilla em ma fase"
    },
    "osasuna x alaves": {
        "liga": "LaLiga", "data": "20/12 - 14h30",
        "casa": "Osasuna", "fora": "Alaves",
        "forca_casa": 68, "forca_fora": 62,
        "gols_casa": 1.4, "gols_fora": 1.0,
        "gols_sofr_casa": 1.2, "gols_sofr_fora": 1.4,
        "cantos_casa": 5.0, "cantos_fora": 4.2,
        "cartoes_casa": 2.5, "cartoes_fora": 2.8,
        "forma_casa": "VEVDE", "forma_fora": "EDVDD",
        "contexto": "Jogo equilibrado"
    },
    "rb leipzig x bayer leverkusen": {
        "liga": "Bundesliga", "data": "20/12 - 14h30",
        "casa": "RB Leipzig", "fora": "Leverkusen",
        "forca_casa": 82, "forca_fora": 88,
        "gols_casa": 2.2, "gols_fora": 2.4,
        "gols_sofr_casa": 1.0, "gols_sofr_fora": 0.8,
        "cantos_casa": 5.8, "cantos_fora": 5.5,
        "cartoes_casa": 1.8, "cartoes_fora": 1.6,
        "forma_casa": "VVDEV", "forma_fora": "VVVVV",
        "contexto": "CLASSICO! Leverkusen invicto"
    },
    "stuttgart x hoffenheim": {
        "liga": "Bundesliga", "data": "20/12 - 11h30",
        "casa": "Stuttgart", "fora": "Hoffenheim",
        "forca_casa": 78, "forca_fora": 70,
        "gols_casa": 2.0, "gols_fora": 1.5,
        "gols_sofr_casa": 1.2, "gols_sofr_fora": 1.6,
        "cantos_casa": 5.5, "cantos_fora": 4.8,
        "cartoes_casa": 1.8, "cartoes_fora": 2.2,
        "forma_casa": "VVVDE", "forma_fora": "DEVDE",
        "contexto": "Stuttgart favorito em casa"
    },
    "juventus x roma": {
        "liga": "Serie A", "data": "20/12 - 16h45",
        "casa": "Juventus", "fora": "Roma",
        "forca_casa": 82, "forca_fora": 75,
        "gols_casa": 1.8, "gols_fora": 1.4,
        "gols_sofr_casa": 0.6, "gols_sofr_fora": 1.2,
        "cantos_casa": 5.5, "cantos_fora": 5.0,
        "cartoes_casa": 2.2, "cartoes_fora": 2.5,
        "forma_casa": "EEVVE", "forma_fora": "VDVED",
        "contexto": "CLASSICO! Juve solida defensivamente"
    },
    "lazio x cremonese": {
        "liga": "Serie A", "data": "20/12 - 14h00",
        "casa": "Lazio", "fora": "Cremonese",
        "forca_casa": 78, "forca_fora": 55,
        "gols_casa": 2.2, "gols_fora": 0.8,
        "gols_sofr_casa": 1.0, "gols_sofr_fora": 2.0,
        "cantos_casa": 6.0, "cantos_fora": 3.5,
        "cartoes_casa": 1.8, "cartoes_fora": 2.0,
        "forma_casa": "VVVEV", "forma_fora": "DDDVD",
        "contexto": "Lazio grande favorito"
    },
    "fontenay x psg": {
        "liga": "Copa da Franca", "data": "20/12 - 17h00",
        "casa": "Fontenay", "fora": "PSG",
        "forca_casa": 35, "forca_fora": 90,
        "gols_casa": 0.5, "gols_fora": 3.5,
        "gols_sofr_casa": 2.5, "gols_sofr_fora": 0.5,
        "cantos_casa": 2.5, "cantos_fora": 8.0,
        "cartoes_casa": 2.0, "cartoes_fora": 1.2,
        "forma_casa": "VDVDD", "forma_fora": "VVVVV",
        "contexto": "PSG grande favorito"
    },
}
def calcular_prob_resultado(forca_casa, forca_fora, gols_casa, gols_fora, gols_sofr_casa, gols_sofr_fora):
    diff_forca = forca_casa - forca_fora
    vantagem_casa = 5
    ataque_casa = gols_casa * 10
    defesa_casa = (2 - gols_sofr_casa) * 10
    ataque_fora = gols_fora * 10
    defesa_fora = (2 - gols_sofr_fora) * 10
    score_casa = forca_casa + ataque_casa + defesa_casa + vantagem_casa
    score_fora = forca_fora + ataque_fora + defesa_fora
    total = score_casa + score_fora + 30
    prob_casa = min(85, max(10, (score_casa / total) * 100 + diff_forca * 0.3))
    prob_fora = min(85, max(10, (score_fora / total) * 100 - diff_forca * 0.3))
    prob_empate = max(10, 100 - prob_casa - prob_fora)
    total_prob = prob_casa + prob_empate + prob_fora
    prob_casa = round((prob_casa / total_prob) * 100)
    prob_empate = round((prob_empate / total_prob) * 100)
    prob_fora = 100 - prob_casa - prob_empate
    return prob_casa, prob_empate, prob_fora

def calcular_prob_gols(gols_casa, gols_fora, gols_sofr_casa, gols_sofr_fora):
    media_gols = gols_casa + gols_fora
    prob_over05 = min(95, 50 + (media_gols - 1.0) * 30)
    prob_over15 = min(90, 40 + (media_gols - 1.5) * 25)
    prob_over25 = min(85, 30 + (media_gols - 2.0) * 20)
    prob_over35 = min(75, 20 + (media_gols - 2.5) * 15)
    prob_btts = min(80, (gols_casa * 20) + (gols_fora * 20) - 10)
    return {
        "over05": round(max(20, prob_over05)),
        "over15": round(max(15, prob_over15)),
        "over25": round(max(10, prob_over25)),
        "over35": round(max(5, prob_over35)),
        "btts": round(max(20, prob_btts))
    }

def calcular_prob_cantos(cantos_casa, cantos_fora):
    media = cantos_casa + cantos_fora
    return {
        "over85": round(max(20, min(90, 40 + (media - 8.5) * 15))),
        "over95": round(max(15, min(85, 35 + (media - 9.5) * 12))),
        "over105": round(max(10, min(75, 30 + (media - 10.5) * 10)))
    }

def calcular_prob_cartoes(cartoes_casa, cartoes_fora):
    media = cartoes_casa + cartoes_fora
    return {
        "over25": round(max(20, min(90, 40 + (media - 2.5) * 20))),
        "over35": round(max(15, min(80, 35 + (media - 3.5) * 15))),
        "over45": round(max(10, min(70, 25 + (media - 4.5) * 12)))
    }

def encontrar_melhor_aposta(jogo, prob_casa, prob_empate, prob_fora, prob_gols, prob_cantos, prob_cartoes):
    apostas = []
    if prob_casa >= 70:
        apostas.append(("Vitoria " + jogo["casa"], prob_casa, "1.5u"))
    elif prob_casa >= 55:
        apostas.append(("Vitoria " + jogo["casa"], prob_casa, "1.0u"))
    if prob_fora >= 70:
        apostas.append(("Vitoria " + jogo["fora"], prob_fora, "1.5u"))
    elif prob_fora >= 55:
        apostas.append(("Vitoria " + jogo["fora"], prob_fora, "1.0u"))
    if prob_casa + prob_empate >= 75:
        apostas.append(("Dupla 1X (" + jogo["casa"] + "/Empate)", prob_casa + prob_empate, "1.0u"))
    if prob_fora + prob_empate >= 75:
        apostas.append(("Dupla X2 (Empate/" + jogo["fora"] + ")", prob_fora + prob_empate, "1.0u"))
    if prob_gols["over25"] >= 70:
        apostas.append(("Over 2.5 Gols", prob_gols["over25"], "1.5u"))
    elif prob_gols["over25"] >= 55:
        apostas.append(("Over 2.5 Gols", prob_gols["over25"], "1.0u"))
    if prob_gols["over15"] >= 80:
        apostas.append(("Over 1.5 Gols", prob_gols["over15"], "1.0u"))
    if prob_gols["over25"] <= 35:
        apostas.append(("Under 2.5 Gols", 100 - prob_gols["over25"], "1.0u"))
    if prob_gols["btts"] >= 65:
        apostas.append(("Ambas Marcam (BTTS)", prob_gols["btts"], "1.0u"))
    if prob_cantos["over95"] >= 65:
        apostas.append(("Over 9.5 Cantos", prob_cantos["over95"], "1.0u"))
    if prob_cartoes["over35"] >= 65:
        apostas.append(("Over 3.5 Cartoes", prob_cartoes["over35"], "1.0u"))
    apostas.sort(key=lambda x: x[1], reverse=True)
    return apostas[:3]
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
    prob_casa, prob_empate, prob_fora = calcular_prob_resultado(jogo["forca_casa"], jogo["forca_fora"], jogo["gols_casa"], jogo["gols_fora"], jogo["gols_sofr_casa"], jogo["gols_sofr_fora"])
    prob_gols = calcular_prob_gols(jogo["gols_casa"], jogo["gols_fora"], jogo["gols_sofr_casa"], jogo["gols_sofr_fora"])
    prob_cantos = calcular_prob_cantos(jogo["cantos_casa"], jogo["cantos_fora"])
    prob_cartoes = calcular_prob_cartoes(jogo["cartoes_casa"], jogo["cartoes_fora"])
    melhores = encontrar_melhor_aposta(jogo, prob_casa, prob_empate, prob_fora, prob_gols, prob_cantos, prob_cartoes)
    total_gols = jogo["gols_casa"] + jogo["gols_fora"]
    total_cantos = jogo["cantos_casa"] + jogo["cantos_fora"]
    total_cartoes = jogo["cartoes_casa"] + jogo["cartoes_fora"]
    analise = f"""
=============================
{jogo_key.upper()}
{jogo["liga"]} - {jogo["data"]}
=============================
CONTEXTO: {jogo["contexto"]}

FORMA: {jogo["casa"]} {jogo["forma_casa"]} | {jogo["fora"]} {jogo["forma_fora"]}

--- RESULTADO ---
{jogo["casa"]}: {prob_casa}%
Empate: {prob_empate}%
{jogo["fora"]}: {prob_fora}%

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
        conf = "ALTA" if prob >= 70 else "MEDIA"
        analise += f"{i}. {aposta}\n   {prob}% | {conf} | {unid}\n"
    return analise

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("BOT DE ANALISE ESPORTIVA\n\nComandos:\n/premier - Premier League\n/laliga - LaLiga\n/bundesliga - Bundesliga\n/seriea - Serie A\n/ligue1 - Ligue 1\n/jogos - Todos os jogos\n/melhores - Melhores apostas\n\nOu digite: Tottenham x Liverpool")

async def jogos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lista = "JOGOS DISPONIVEIS:\n\n"
    for jogo, dados in JOGOS.items():
        lista += f"- {jogo.title()} ({dados['liga']})\n"
    await update.message.reply_text(lista)

async def premier(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lista = "PREMIER LEAGUE:\n\n"
    for jogo, dados in JOGOS.items():
        if "Premier" in dados["liga"]:
            p1, pe, p2 = calcular_prob_resultado(dados["forca_casa"], dados["forca_fora"], dados["gols_casa"], dados["gols_fora"], dados["gols_sofr_casa"], dados["gols_sofr_fora"])
            fav = dados["casa"] if p1 > p2 else dados["fora"]
            lista += f"{jogo.title()}\n  Favorito: {fav} ({max(p1,p2)}%)\n\n"
    await update.message.reply_text(lista)

async def laliga(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lista = "LALIGA:\n\n"
    for jogo, dados in JOGOS.items():
        if "LaLiga" in dados["liga"]:
            p1, pe, p2 = calcular_prob_resultado(dados["forca_casa"], dados["forca_fora"], dados["gols_casa"], dados["gols_fora"], dados["gols_sofr_casa"], dados["gols_sofr_fora"])
            fav = dados["casa"] if p1 > p2 else dados["fora"]
            lista += f"{jogo.title()}\n  Favorito: {fav} ({max(p1,p2)}%)\n\n"
    await update.message.reply_text(lista)

async def bundesliga(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lista = "BUNDESLIGA:\n\n"
    for jogo, dados in JOGOS.items():
        if "Bundesliga" in dados["liga"]:
            p1, pe, p2 = calcular_prob_resultado(dados["forca_casa"], dados["forca_fora"], dados["gols_casa"], dados["gols_fora"], dados["gols_sofr_casa"], dados["gols_sofr_fora"])
            fav = dados["casa"] if p1 > p2 else dados["fora"]
            lista += f"{jogo.title()}\n  Favorito: {fav} ({max(p1,p2)}%)\n\n"
    await update.message.reply_text(lista)

async def seriea(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lista = "SERIE A:\n\n"
    for jogo, dados in JOGOS.items():
        if "Serie A" in dados["liga"]:
            p1, pe, p2 = calcular_prob_resultado(dados["forca_casa"], dados["forca_fora"], dados["gols_casa"], dados["gols_fora"], dados["gols_sofr_casa"], dados["gols_sofr_fora"])
            fav = dados["casa"] if p1 > p2 else dados["fora"]
            lista += f"{jogo.title()}\n  Favorito: {fav} ({max(p1,p2)}%)\n\n"
    await update.message.reply_text(lista)

async def ligue1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lista = "LIGUE 1 / COPA FRANCA:\n\n"
    for jogo, dados in JOGOS.items():
        if "Franca" in dados["liga"]:
            p1, pe, p2 = calcular_prob_resultado(dados["forca_casa"], dados["forca_fora"], dados["gols_casa"], dados["gols_fora"], dados["gols_sofr_casa"], dados["gols_sofr_fora"])
            fav = dados["casa"] if p1 > p2 else dados["fora"]
            lista += f"{jogo.title()}\n  Favorito: {fav} ({max(p1,p2)}%)\n\n"
    await update.message.reply_text(lista)

async def melhores(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lista = "MELHORES APOSTAS:\n\n"
    todas = []
    for jogo_key, jogo in JOGOS.items():
        p1, pe, p2 = calcular_prob_resultado(jogo["forca_casa"], jogo["forca_fora"], jogo["gols_casa"], jogo["gols_fora"], jogo["gols_sofr_casa"], jogo["gols_sofr_fora"])
        pg = calcular_prob_gols(jogo["gols_casa"], jogo["gols_fora"], jogo["gols_sofr_casa"], jogo["gols_sofr_fora"])
        pc = calcular_prob_cantos(jogo["cantos_casa"], jogo["cantos_fora"])
        pca = calcular_prob_cartoes(jogo["cartoes_casa"], jogo["cartoes_fora"])
        for ap, prob, un in encontrar_melhor_aposta(jogo, p1, pe, p2, pg, pc, pca):
            if prob >= 65:
                todas.append((jogo_key, ap, prob, un))
    todas.sort(key=lambda x: x[2], reverse=True)
    for i, (j, ap, prob, un) in enumerate(todas[:8], 1):
        lista += f"{i}. {j.title()}\n   {ap}\n   {prob}% | {un}\n\n"
    await update.message.reply_text(lista)

async def mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.lower().replace(" vs ", " x ").replace(" - ", " x ")
    analise = analisar_jogo(texto)
    if analise:
        await update.message.reply_text(analise)
    else:
        await update.message.reply_text("Jogo nao encontrado. Use /jogos")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("jogos", jogos))
    app.add_handler(CommandHandler("melhores", melhores))
    app.add_handler(CommandHandler("premier", premier))
    app.add_handler(CommandHandler("laliga", laliga))
    app.add_handler(CommandHandler("bundesliga", bundesliga))
    app.add_handler(CommandHandler("seriea", seriea))
    app.add_handler(CommandHandler("ligue1", ligue1))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mensagem))
    print("Bot iniciado!")
    app.run_polling()

if __name__ == "__main__":
    main()
