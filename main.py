from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8538748627:AAGaOYs-V17YITSPENRWWPTJSvVY4ZssCos"

JOGOS = {
    "girona x atletico madrid": {
        "liga": "LaLiga", "data": "21/12 - 08h00",
        "casa": "Girona", "fora": "Atletico Madrid",
        "forca_casa": 72, "forca_fora": 85,
        "gols_casa": 1.6, "gols_fora": 1.8,
        "gols_sofr_casa": 1.2, "gols_sofr_fora": 0.8,
        "cantos_casa": 5.2, "cantos_fora": 5.0,
        "cartoes_casa": 1.8, "cartoes_fora": 2.2,
        "forma_casa": "VDVEV", "forma_fora": "VVVEV",
        "contexto": "Atletico favorito, Girona em casa forte"
    },
    "villarreal x barcelona": {
        "liga": "LaLiga", "data": "21/12 - 10h15",
        "casa": "Villarreal", "fora": "Barcelona",
        "forca_casa": 75, "forca_fora": 88,
        "gols_casa": 1.8, "gols_fora": 2.4,
        "gols_sofr_casa": 1.2, "gols_sofr_fora": 1.0,
        "cantos_casa": 5.5, "cantos_fora": 6.0,
        "cartoes_casa": 1.6, "cartoes_fora": 1.8,
        "forma_casa": "VVDEV", "forma_fora": "VVVDV",
        "contexto": "Barcelona favorito mas Villarreal joga bem em casa"
    },
    "elche x rayo vallecano": {
        "liga": "LaLiga", "data": "21/12 - 12h30",
        "casa": "Elche", "fora": "Rayo Vallecano",
        "forca_casa": 58, "forca_fora": 65,
        "gols_casa": 1.0, "gols_fora": 1.2,
        "gols_sofr_casa": 1.6, "gols_sofr_fora": 1.4,
        "cantos_casa": 4.2, "cantos_fora": 4.8,
        "cartoes_casa": 2.0, "cartoes_fora": 2.2,
        "forma_casa": "DDEVD", "forma_fora": "VDVED",
        "contexto": "Jogo equilibrado, times de meio/baixo tabela"
    },
    "real betis x getafe": {
        "liga": "LaLiga", "data": "21/12 - 15h00",
        "casa": "Real Betis", "fora": "Getafe",
        "forca_casa": 72, "forca_fora": 62,
        "gols_casa": 1.5, "gols_fora": 0.8,
        "gols_sofr_casa": 1.0, "gols_sofr_fora": 1.2,
        "cantos_casa": 5.5, "cantos_fora": 4.0,
        "cartoes_casa": 1.8, "cartoes_fora": 2.5,
        "forma_casa": "VVEVD", "forma_fora": "EDDVD",
        "contexto": "Betis favorito em casa, Getafe muito defensivo"
    },
    "aston villa x manchester united": {
        "liga": "Premier League", "data": "21/12 - 11h30",
        "casa": "Aston Villa", "fora": "Man United",
        "forca_casa": 78, "forca_fora": 75,
        "gols_casa": 1.8, "gols_fora": 1.4,
        "gols_sofr_casa": 1.0, "gols_sofr_fora": 1.6,
        "cantos_casa": 5.8, "cantos_fora": 5.0,
        "cartoes_casa": 1.6, "cartoes_fora": 2.0,
        "forma_casa": "VVVEV", "forma_fora": "DVDED",
        "contexto": "Villa em boa fase, United irregular"
    },
    "cagliari x pisa": {
        "liga": "Serie A", "data": "21/12 - 06h30",
        "casa": "Cagliari", "fora": "Pisa",
        "forca_casa": 62, "forca_fora": 58,
        "gols_casa": 1.2, "gols_fora": 1.0,
        "gols_sofr_casa": 1.4, "gols_sofr_fora": 1.2,
        "cantos_casa": 4.5, "cantos_fora": 4.2,
        "cartoes_casa": 2.0, "cartoes_fora": 1.8,
        "forma_casa": "DEVDE", "forma_fora": "VDVED",
        "contexto": "Jogo equilibrado"
    },
    "sassuolo x torino": {
        "liga": "Serie A", "data": "21/12 - 09h00",
        "casa": "Sassuolo", "fora": "Torino",
        "forca_casa": 60, "forca_fora": 68,
        "gols_casa": 1.2, "gols_fora": 1.4,
        "gols_sofr_casa": 1.6, "gols_sofr_fora": 1.2,
        "cantos_casa": 4.5, "cantos_fora": 5.0,
        "cartoes_casa": 1.8, "cartoes_fora": 2.0,
        "forma_casa": "DDDVE", "forma_fora": "VEVDE",
        "contexto": "Torino leve favorito"
    },
    "fiorentina x udinese": {
        "liga": "Serie A", "data": "21/12 - 12h00",
        "casa": "Fiorentina", "fora": "Udinese",
        "forca_casa": 75, "forca_fora": 65,
        "gols_casa": 1.8, "gols_fora": 1.2,
        "gols_sofr_casa": 0.8, "gols_sofr_fora": 1.4,
        "cantos_casa": 5.8, "cantos_fora": 4.5,
        "cartoes_casa": 1.6, "cartoes_fora": 2.0,
        "forma_casa": "VVVVE", "forma_fora": "DVDED",
        "contexto": "Fiorentina em otima fase, favorita"
    },
    "genoa x atalanta": {
        "liga": "Serie A", "data": "21/12 - 14h45",
        "casa": "Genoa", "fora": "Atalanta",
        "forca_casa": 62, "forca_fora": 85,
        "gols_casa": 1.2, "gols_fora": 2.6,
        "gols_sofr_casa": 1.8, "gols_sofr_fora": 0.8,
        "cantos_casa": 4.5, "cantos_fora": 6.5,
        "cartoes_casa": 2.2, "cartoes_fora": 1.6,
        "forma_casa": "DDEVD", "forma_fora": "VVVVV",
        "contexto": "Atalanta em fase espetacular"
    },
    "mainz x st pauli": {
        "liga": "Bundesliga", "data": "21/12 - 09h30",
        "casa": "Mainz", "fora": "St. Pauli",
        "forca_casa": 68, "forca_fora": 60,
        "gols_casa": 1.6, "gols_fora": 1.0,
        "gols_sofr_casa": 1.2, "gols_sofr_fora": 1.6,
        "cantos_casa": 5.0, "cantos_fora": 4.2,
        "cartoes_casa": 1.8, "cartoes_fora": 2.0,
        "forma_casa": "VVDEV", "forma_fora": "DDVED",
        "contexto": "Mainz favorito em casa"
    },
    "heidenheim x bayern": {
        "liga": "Bundesliga", "data": "21/12 - 11h30",
        "casa": "Heidenheim", "fora": "Bayern",
        "forca_casa": 62, "forca_fora": 92,
        "gols_casa": 1.2, "gols_fora": 3.0,
        "gols_sofr_casa": 1.8, "gols_sofr_fora": 0.6,
        "cantos_casa": 4.0, "cantos_fora": 7.5,
        "cartoes_casa": 2.0, "cartoes_fora": 1.2,
        "forma_casa": "DEVDD", "forma_fora": "VVVVV",
        "contexto": "Bayern grande favorito"
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
        "contexto": "Liverpool lider invicto"
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
        "contexto": "Arsenal favorito"
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
        "contexto": "Real Madrid em casa"
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
        "contexto": "Leverkusen invicto"
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
        "contexto": "Juve solida defensivamente"
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
        apostas.append(("Dupla 1X (" + jogo["casa"] + "/Emp)", prob_casa + prob_empate, "1.0u"))
    if prob_fora + prob_empate >= 75:
        apostas.append(("Dupla X2 (Emp/" + jogo["fora"] + ")", prob_fora + prob_empate, "1.0u"))
    if prob_gols["over25"] >= 70:
        apostas.append(("Over 2.5 Gols", prob_gols["over25"], "1.5u"))
    elif prob_gols["over25"] >= 55:
        apostas.append(("Over 2.5 Gols", prob_gols["over25"], "1.0u"))
    if prob_gols["over15"] >= 80:
        apostas.append(("Over 1.5 Gols", prob_gols["over15"], "1.0u"))
    if prob_gols["over25"] <= 35:
        apostas.append(("Under 2.5 Gols", 100 - prob_gols["over25"], "1.0u"))
    if prob_gols["btts"] >= 65:
        apostas.append(("Ambas Marcam", prob_gols["btts"], "1.0u"))
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
{jogo["contexto"]}

FORMA: {jogo["casa"]} {jogo["forma_casa"]} | {jogo["fora"]} {jogo["forma_fora"]}

--- RESULTADO ---
{jogo["casa"]}: {prob_casa}%
Empate: {prob_empate}%
{jogo["fora"]}: {prob_fora}%

Dupla 1X: {prob_casa + prob_empate}%
Dupla X2: {prob_empate + prob_fora}%

--- GOLS ({total_gols:.1f}) ---
Over 0.5: {prob_gols["over05"]}%
Over 1.5: {prob_gols["over15"]}%
Over 2.5: {prob_gols["over25"]}%
Over 3.5: {prob_gols["over35"]}%
BTTS: {prob_gols["btts"]}%

--- CANTOS ({total_cantos:.1f}) ---
Over 8.5: {prob_cantos["over85"]}%
Over 9.5: {prob_cantos["over95"]}%
Over 10.5: {prob_cantos["over105"]}%

--- CARTOES ({total_cartoes:.1f}) ---
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
    await update.message.reply_text("BOT DE ANALISE ESPORTIVA\n\nComandos:\n/hoje - Jogos de hoje\n/amanha - Jogos de amanha\n/premier - Premier League\n/laliga - LaLiga\n/bundesliga - Bundesliga\n/seriea - Serie A\n/jogos - Todos os jogos\n/melhores - Melhores apostas\n\nOu digite: Villarreal x Barcelona")

async def jogos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lista = "TODOS OS JOGOS:\n\n"
    for jogo, dados in JOGOS.items():
        lista += f"- {jogo.title()} ({dados['data']})\n"
    await update.message.reply_text(lista)

async def hoje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lista = "JOGOS DE HOJE (20/12):\n\n"
    for jogo, dados in JOGOS.items():
        if "20/12" in dados["data"]:
            p1, pe, p2 = calcular_prob_resultado(dados["forca_casa"], dados["forca_fora"], dados["gols_casa"], dados["gols_fora"], dados["gols_sofr_casa"], dados["gols_sofr_fora"])
            fav = dados["casa"] if p1 > p2 else dados["fora"]
            lista += f"{jogo.title()}\n  {dados['data']} | Fav: {fav} ({max(p1,p2)}%)\n\n"
    await update.message.reply_text(lista)

async def amanha(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lista = "JOGOS DE AMANHA (21/12):\n\n"
    for jogo, dados in JOGOS.items():
        if "21/12" in dados["data"]:
            p1, pe, p2 = calcular_prob_resultado(dados["forca_casa"], dados["forca_fora"], dados["gols_casa"], dados["gols_fora"], dados["gols_sofr_casa"], dados["gols_sofr_fora"])
            fav = dados["casa"] if p1 > p2 else dados["fora"]
            lista += f"{jogo.title()}\n  {dados['data']} | Fav: {fav} ({max(p1,p2)}%)\n\n"
    await update.message.reply_text(lista)

async def premier(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lista = "PREMIER LEAGUE:\n\n"
    for jogo, dados in JOGOS.items():
        if "Premier" in dados["liga"]:
            p1, pe, p2 = calcular_prob_resultado(dados["forca_casa"], dados["forca_fora"], dados["gols_casa"], dados["gols_fora"], dados["gols_sofr_casa"], dados["gols_sofr_fora"])
            fav = dados["casa"] if p1 > p2 else dados["fora"]
            lista += f"{jogo.title()}\n  {dados['data']} | Fav: {fav} ({max(p1,p2)}%)\n\n"
    await update.message.reply_text(lista)

async def laliga(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lista = "LALIGA:\n\n"
    for jogo, dados in JOGOS.items():
        if "LaLiga" in dados["liga"]:
            p1, pe, p2 = calcular_prob_resultado(dados["forca_casa"], dados["forca_fora"], dados["gols_casa"], dados["gols_fora"], dados["gols_sofr_casa"], dados["gols_sofr_fora"])
            fav = dados["casa"] if p1 > p2 else dados["fora"]
            lista += f"{jogo.title()}\n  {dados['data']} | Fav: {fav} ({max(p1,p2)}%)\n\n"
    await update.message.reply_text(lista)

async def bundesliga(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lista = "BUNDESLIGA:\n\n"
    for jogo, dados in JOGOS.items():
        if "Bundesliga" in dados["liga"]:
            p1, pe, p2 = calcular_prob_resultado(dados["forca_casa"], dados["forca_fora"], dados["gols_casa"], dados["gols_fora"], dados["gols_sofr_casa"], dados["gols_sofr_fora"])
            fav = dados["casa"] if p1 > p2 else dados["fora"]
            lista += f"{jogo.title()}\n  {dados['data']} | Fav: {fav} ({max(p1,p2)}%)\n\n"
    await update.message.reply_text(lista)

async def seriea(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lista = "SERIE A:\n\n"
    for jogo, dados in JOGOS.items():
        if "Serie A" in dados["liga"]:
            p1, pe, p2 = calcular_prob_resultado(dados["forca_casa"], dados["forca_fora"], dados["gols_casa"], dados["gols_fora"], dados["gols_sofr_casa"], dados["gols_sofr_fora"])
            fav = dados["casa"] if p1 > p2 else dados["fora"]
            lista += f"{jogo.title()}\n  {dados['data']} | Fav: {fav} ({max(p1,p2)}%)\n\n"
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
                todas.append((jogo_key, jogo["data"], ap, prob, un))
    todas.sort(key=lambda x: x[3], reverse=True)
    for i, (j, data, ap, prob, un) in enumerate(todas[:10], 1):
        lista += f"{i}. {j.title()}\n   {data}\n   {ap}\n   {prob}% | {un}\n\n"
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
    app.add_handler(CommandHandler("hoje", hoje))
    app.add_handler(CommandHandler("amanha", amanha))
    app.add_handler(CommandHandler("melhores", melhores))
    app.add_handler(CommandHandler("premier", premier))
    app.add_handler(CommandHandler("laliga", laliga))
    app.add_handler(CommandHandler("bundesliga", bundesliga))
    app.add_handler(CommandHandler("seriea", seriea))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mensagem))
    print("Bot iniciado!")
    app.run_polling()

if __name__ == "__main__":
    main()
