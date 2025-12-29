from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8538748627:AAGaOYs-V17YITSPENRWWPTJSvVY4ZssCos"

# DADOS REAIS - 30/12/2025 - Fontes: OddsShark, FootballWhispers, Sportskeeda
JOGOS = {
    "burnley x newcastle": {
        "liga": "Premier League", "data": "30/12 - 14h30",
        "casa": "Burnley", "fora": "Newcastle",
        "forca_casa": 45, "forca_fora": 75,
        "gols_casa": 0.5, "gols_fora": 1.8,
        "gols_sofr_casa": 1.8, "gols_sofr_fora": 0.9,
        "cantos_casa": 4.0, "cantos_fora": 5.5,
        "cartoes_casa": 2.2, "cartoes_fora": 1.6,
        "forma_casa": "LLLLLD", "forma_fora": "WDWWLW",
        "posicao_casa": 19, "posicao_fora": 5,
        "h2h_gols": 2.3,
        "odds_casa": 4.50, "odds_empate": 3.80, "odds_fora": 1.69,
        "contexto": "Newcastle FAVORITO. Burnley em crise, luta contra rebaixamento."
    },
    "chelsea x bournemouth": {
        "liga": "Premier League", "data": "30/12 - 14h30",
        "casa": "Chelsea", "fora": "Bournemouth",
        "forca_casa": 78, "forca_fora": 62,
        "gols_casa": 2.0, "gols_fora": 1.2,
        "gols_sofr_casa": 1.3, "gols_sofr_fora": 2.1,
        "cantos_casa": 5.5, "cantos_fora": 4.5,
        "cartoes_casa": 1.8, "cartoes_fora": 1.9,
        "forma_casa": "LDWDLD", "forma_fora": "LDDDLL",
        "posicao_casa": 4, "posicao_fora": 13,
        "h2h_gols": 3.0,
        "odds_casa": 1.57, "odds_empate": 4.20, "odds_fora": 5.25,
        "contexto": "Chelsea FAVORITO. Bournemouth 9 jogos sem vencer! Sofreu 3+ gols em 6 jogos fora."
    },
    "forest x everton": {
        "liga": "Premier League", "data": "30/12 - 14h30",
        "casa": "Forest", "fora": "Everton",
        "forca_casa": 65, "forca_fora": 62,
        "gols_casa": 1.2, "gols_fora": 1.1,
        "gols_sofr_casa": 1.4, "gols_sofr_fora": 1.3,
        "cantos_casa": 4.5, "cantos_fora": 4.2,
        "cartoes_casa": 1.8, "cartoes_fora": 2.0,
        "forma_casa": "LLWLWL", "forma_fora": "DLLWWL",
        "posicao_casa": 10, "posicao_fora": 15,
        "h2h_gols": 2.0,
        "odds_casa": 2.10, "odds_empate": 3.25, "odds_fora": 3.60,
        "contexto": "Forest leve favorito. H2H: Under 2.5 em 8 de 10 jogos!"
    },
    "west ham x brighton": {
        "liga": "Premier League", "data": "30/12 - 14h30",
        "casa": "West Ham", "fora": "Brighton",
        "forca_casa": 55, "forca_fora": 68,
        "gols_casa": 1.0, "gols_fora": 1.4,
        "gols_sofr_casa": 1.8, "gols_sofr_fora": 1.3,
        "cantos_casa": 4.2, "cantos_fora": 5.0,
        "cartoes_casa": 1.8, "cartoes_fora": 1.6,
        "forma_casa": "LLLDLL", "forma_fora": "LDLDLW",
        "posicao_casa": 14, "posicao_fora": 9,
        "h2h_gols": 2.2,
        "odds_casa": 3.12, "odds_empate": 3.40, "odds_fora": 2.12,
        "contexto": "Brighton FAVORITO. West Ham em crise total!"
    },
    "arsenal x aston villa": {
        "liga": "Premier League", "data": "30/12 - 15h15",
        "casa": "Arsenal", "fora": "Aston Villa",
        "forca_casa": 88, "forca_fora": 85,
        "gols_casa": 2.2, "gols_fora": 2.0,
        "gols_sofr_casa": 0.7, "gols_sofr_fora": 0.9,
        "cantos_casa": 6.0, "cantos_fora": 5.5,
        "cartoes_casa": 1.5, "cartoes_fora": 1.6,
        "forma_casa": "WWWLWD", "forma_fora": "WWWWWW",
        "posicao_casa": 2, "posicao_fora": 3,
        "h2h_gols": 2.8,
        "odds_casa": 1.47, "odds_empate": 4.33, "odds_fora": 7.00,
        "contexto": "JOGAO! Arsenal favorito. Villa com 11 VITORIAS SEGUIDAS em todas competicoes!"
    },
    "man utd x wolves": {
        "liga": "Premier League", "data": "30/12 - 15h15",
        "casa": "Man Utd", "fora": "Wolves",
        "forca_casa": 72, "forca_fora": 35,
        "gols_casa": 1.6, "gols_fora": 0.5,
        "gols_sofr_casa": 1.2, "gols_sofr_fora": 2.2,
        "cantos_casa": 5.2, "cantos_fora": 3.0,
        "cartoes_casa": 1.8, "cartoes_fora": 2.2,
        "forma_casa": "WLDWDW", "forma_fora": "LLLLLL",
        "posicao_casa": 7, "posicao_fora": 20,
        "h2h_gols": 2.5,
        "odds_casa": 1.33, "odds_empate": 5.60, "odds_fora": 9.00,
        "contexto": "Man Utd GRANDE FAVORITO. Wolves LANTERNA com 6+ derrotas seguidas!"
    },
}
def calcular_prob_resultado(jogo):
    odds_casa = jogo["odds_casa"]
    odds_empate = jogo["odds_empate"]
    odds_fora = jogo["odds_fora"]
    prob_casa = round((1 / odds_casa) * 100 * 0.92)
    prob_empate = round((1 / odds_empate) * 100 * 0.92)
    prob_fora = round((1 / odds_fora) * 100 * 0.92)
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
    prob_btts = min(80, (jogo["gols_casa"] * 25) + (jogo["gols_fora"] * 25) - 15)
    return {"over05": round(max(30, prob_over05)), "over15": round(max(25, prob_over15)), "over25": round(max(20, prob_over25)), "over35": round(max(15, prob_over35)), "btts": round(max(25, min(80, prob_btts)))}

def calcular_prob_cantos(jogo):
    media_cantos = jogo["cantos_casa"] + jogo["cantos_fora"]
    prob_over85 = min(85, 30 + (media_cantos - 8.5) * 15)
    prob_over95 = min(75, 25 + (media_cantos - 9.5) * 12)
    prob_over105 = min(65, 20 + (media_cantos - 10.5) * 10)
    return {"over85": round(max(20, prob_over85)), "over95": round(max(15, prob_over95)), "over105": round(max(10, prob_over105))}

def calcular_prob_cartoes(jogo):
    media_cartoes = jogo["cartoes_casa"] + jogo["cartoes_fora"]
    prob_over25 = min(85, 30 + (media_cartoes - 2.5) * 20)
    prob_over35 = min(75, 20 + (media_cartoes - 3.5) * 15)
    prob_over45 = min(60, 15 + (media_cartoes - 4.5) * 10)
    return {"over25": round(max(20, prob_over25)), "over35": round(max(15, prob_over35)), "over45": round(max(10, prob_over45))}

def encontrar_melhor_aposta(jogo, prob_casa, prob_empate, prob_fora, prob_gols, prob_cantos, prob_cartoes):
    apostas = []
    if prob_casa >= 65:
        apostas.append(("Vitoria " + jogo["casa"], prob_casa, "1.5u"))
    elif prob_casa >= 55:
        apostas.append(("Vitoria " + jogo["casa"], prob_casa, "1.0u"))
    if prob_fora >= 65:
        apostas.append(("Vitoria " + jogo["fora"], prob_fora, "1.5u"))
    elif prob_fora >= 55:
        apostas.append(("Vitoria " + jogo["fora"], prob_fora, "1.0u"))
    if prob_casa + prob_empate >= 75 and prob_casa < 60:
        apostas.append(("Dupla 1X (" + jogo["casa"] + " ou Emp)", prob_casa + prob_empate, "1.0u"))
    if prob_fora + prob_empate >= 75 and prob_fora < 60:
        apostas.append(("Dupla X2 (Emp ou " + jogo["fora"] + ")", prob_fora + prob_empate, "1.0u"))
    if prob_gols["over25"] >= 65:
        apostas.append(("Over 2.5 Gols", prob_gols["over25"], "1.5u" if prob_gols["over25"] >= 75 else "1.0u"))
    elif prob_gols["over15"] >= 78:
        apostas.append(("Over 1.5 Gols", prob_gols["over15"], "1.0u"))
    if prob_gols["over25"] <= 40:
        apostas.append(("Under 2.5 Gols", 100 - prob_gols["over25"], "1.0u"))
    if prob_gols["btts"] >= 60:
        apostas.append(("BTTS (Ambas Marcam)", prob_gols["btts"], "1.0u"))
    if prob_cantos["over95"] >= 60:
        apostas.append(("Over 9.5 Cantos", prob_cantos["over95"], "1.0u"))
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

--- RESULTADO (Odds Reais) ---
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
    await update.message.reply_text("BOT DE ANALISE ESPORTIVA\nDados: OddsShark, FootballWhispers (30/12)\n\nComandos:\n/jogos - Todos os jogos\n/melhores - Melhores apostas\n/premier - Premier League\n\nOu digite: Arsenal x Aston Villa")

async def jogos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lista = "JOGOS 30/12 - PREMIER LEAGUE:\n\n"
    for jogo_key, dados in JOGOS.items():
        p1, pe, p2 = calcular_prob_resultado(dados)
        fav = dados["casa"] if p1 > p2 else dados["fora"]
        prob_fav = max(p1, p2)
        lista += f"{jogo_key.title()}\n  {dados['data']}\n  Favorito: {fav} ({prob_fav}%)\n\n"
    await update.message.reply_text(lista)

async def melhores(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lista = "MELHORES APOSTAS 30/12:\n\n"
    todas = []
    for jogo_key, jogo in JOGOS.items():
        p1, pe, p2 = calcular_prob_resultado(jogo)
        pg = calcular_prob_gols(jogo)
        pc = calcular_prob_cantos(jogo)
        pca = calcular_prob_cartoes(jogo)
        melhores_jogo = encontrar_melhor_aposta(jogo, p1, pe, p2, pg, pc, pca)
        for ap, prob, un in melhores_jogo:
            if prob >= 55:
                todas.append((jogo_key, jogo["data"], ap, prob, un))
    todas.sort(key=lambda x: x[3], reverse=True)
    for i, (j, data, ap, prob, un) in enumerate(todas[:12], 1):
        conf = "ALTA" if prob >= 65 else "MEDIA"
        lista += f"{i}. {j.title()}\n   {data}\n   {ap}\n   {prob}% | {conf} | {un}\n\n"
    await update.message.reply_text(lista)

async def premier(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lista = "PREMIER LEAGUE 30/12:\n\n"
    for jogo_key, dados in JOGOS.items():
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
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mensagem))
    print("Bot iniciado!")
    app.run_polling()

if __name__ == "__main__":
    main()
