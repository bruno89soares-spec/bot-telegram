from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8538748627:AAGaOYs-V17YITSPENRWWPTJSvVY4ZssCos"

JOGOS = {
    "newcastle x chelsea": {
        "liga": "Premier League",
        "data": "20/12 - 09h30",
        "gols_casa": 1.8, "gols_fora": 2.2,
        "cantos_casa": 5.5, "cantos_fora": 5.8,
        "cartoes_casa": 1.6, "cartoes_fora": 1.9,
        "contexto": "Newcastle em casa forte, Chelsea em boa fase"
    },
    "bournemouth x burnley": {
        "liga": "Premier League",
        "data": "20/12 - 12h00",
        "gols_casa": 1.6, "gols_fora": 1.2,
        "cantos_casa": 5.0, "cantos_fora": 4.5,
        "cartoes_casa": 1.8, "cartoes_fora": 2.0,
        "contexto": "Bournemouth favorito em casa"
    },
    "manchester city x west ham": {
        "liga": "Premier League",
        "data": "20/12 - 12h00",
        "gols_casa": 2.8, "gols_fora": 1.0,
        "cantos_casa": 7.2, "cantos_fora": 3.5,
        "cartoes_casa": 1.2, "cartoes_fora": 1.8,
        "contexto": "City em crise mas favorito em casa"
    },
    "wolves x brentford": {
        "liga": "Premier League",
        "data": "20/12 - 12h00",
        "gols_casa": 1.4, "gols_fora": 1.8,
        "cantos_casa": 4.8, "cantos_fora": 5.2,
        "cartoes_casa": 2.0, "cartoes_fora": 1.8,
        "contexto": "Wolves em ma fase, Brentford consistente"
    },
    "tottenham x liverpool": {
        "liga": "Premier League",
        "data": "20/12 - 14h30",
        "gols_casa": 2.1, "gols_fora": 2.6,
        "cantos_casa": 5.5, "cantos_fora": 6.2,
        "cartoes_casa": 1.8, "cartoes_fora": 1.5,
        "contexto": "CLASSICO! Liverpool lider, Tottenham irregular"
    },
    "everton x arsenal": {
        "liga": "Premier League",
        "data": "20/12 - 17h00",
        "gols_casa": 1.2, "gols_fora": 2.4,
        "cantos_casa": 4.0, "cantos_fora": 6.5,
        "cartoes_casa": 2.2, "cartoes_fora": 1.6,
        "contexto": "Arsenal favorito, Everton em dificuldades"
    },
    "real madrid x sevilla": {
        "liga": "LaLiga",
        "data": "20/12 - 17h00",
        "gols_casa": 2.5, "gols_fora": 1.0,
        "cantos_casa": 6.5, "cantos_fora": 4.0,
        "cartoes_casa": 2.0, "cartoes_fora": 2.5,
        "contexto": "Real Madrid em casa, Sevilla em ma fase"
    },
    "osasuna x alaves": {
        "liga": "LaLiga",
        "data": "20/12 - 14h30",
        "gols_casa": 1.4, "gols_fora": 1.0,
        "cantos_casa": 5.0, "cantos_fora": 4.2,
        "cartoes_casa": 2.5, "cartoes_fora": 2.8,
        "contexto": "Jogo equilibrado, times de meio de tabela"
    },
    "levante x real sociedad": {
        "liga": "LaLiga",
        "data": "20/12 - 12h15",
        "gols_casa": 1.2, "gols_fora": 1.8,
        "cantos_casa": 4.5, "cantos_fora": 5.5,
        "cartoes_casa": 2.0, "cartoes_fora": 1.8,
        "contexto": "Real Sociedad favorito fora de casa"
    },
    "rb leipzig x bayer leverkusen": {
        "liga": "Bundesliga",
        "data": "20/12 - 14h30",
        "gols_casa": 2.2, "gols_fora": 2.4,
        "cantos_casa": 5.8, "cantos_fora": 5.5,
        "cartoes_casa": 1.8, "cartoes_fora": 1.6,
        "contexto": "CLASSICO! Dois gigantes alemaes"
    },
    "augsburg x werder bremen": {
        "liga": "Bundesliga",
        "data": "20/12 - 11h30",
        "gols_casa": 1.6, "gols_fora": 1.8,
        "cantos_casa": 4.8, "cantos_fora": 5.2,
        "cartoes_casa": 2.0, "cartoes_fora": 1.8,
        "contexto": "Jogo equilibrado"
    },
    "stuttgart x hoffenheim": {
        "liga": "Bundesliga",
        "data": "20/12 - 11h30",
        "gols_casa": 2.0, "gols_fora": 1.5,
        "cantos_casa": 5.5, "cantos_fora": 4.8,
        "cartoes_casa": 1.8, "cartoes_fora": 2.2,
        "contexto": "Stuttgart favorito em casa"
    },
    "wolfsburg x freiburg": {
        "liga": "Bundesliga",
        "data": "20/12 - 11h30",
        "gols_casa": 1.6, "gols_fora": 1.4,
        "cantos_casa": 5.0, "cantos_fora": 5.2,
        "cartoes_casa": 1.6, "cartoes_fora": 1.8,
        "contexto": "Jogo equilibrado, times consistentes"
    },
    "juventus x roma": {
        "liga": "Serie A",
        "data": "20/12 - 16h45",
        "gols_casa": 1.8, "gols_fora": 1.4,
        "cantos_casa": 5.5, "cantos_fora": 5.0,
        "cartoes_casa": 2.2, "cartoes_fora": 2.5,
        "contexto": "CLASSICO! Derby italiano"
    },
    "lazio x cremonese": {
        "liga": "Serie A",
        "data": "20/12 - 14h00",
        "gols_casa": 2.2, "gols_fora": 0.8,
        "cantos_casa": 6.0, "cantos_fora": 3.5,
        "cartoes_casa": 1.8, "cartoes_fora": 2.0,
        "contexto": "Lazio grande favorito em casa"
    },
    "fontenay x psg": {
        "liga": "Copa da Franca",
        "data": "20/12 - 17h00",
        "gols_casa": 0.5, "gols_fora": 3.5,
        "cantos_casa": 2.5, "cantos_fora": 8.0,
        "cartoes_casa": 2.0, "cartoes_fora": 1.2,
        "contexto": "PSG grande favorito contra time menor"
    },
    "lyon duchere x toulouse": {
        "liga": "Copa da Franca",
        "data": "20/12 - 14h00",
        "gols_casa": 0.8, "gols_fora": 2.5,
        "cantos_casa": 3.0, "cantos_fora": 6.5,
        "cartoes_casa": 1.8, "cartoes_fora": 1.5,
        "contexto": "Toulouse favorito"
    },
}
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
    
    total_gols = jogo["gols_casa"] + jogo["gols_fora"]
    total_cantos = jogo["cantos_casa"] + jogo["cantos_fora"]
    total_cartoes = jogo["cartoes_casa"] + jogo["cartoes_fora"]
    
    if total_gols >= 3.0:
        melhor_aposta = "Over 2.5 Gols"
        confianca = "ALTA"
        unidades = "1.5u"
    elif total_gols >= 2.5:
        melhor_aposta = "Over 2.5 Gols"
        confianca = "MEDIA-ALTA"
        unidades = "1.0u"
    elif total_gols < 2.0:
        melhor_aposta = "Under 2.5 Gols"
        confianca = "MEDIA"
        unidades = "1.0u"
    else:
        melhor_aposta = "BTTS (Ambas Marcam)"
        confianca = "MEDIA"
        unidades = "0.5u"
    
    analise = f"""
ANALISE: {jogo_key.upper()}
Liga: {jogo["liga"]}
Data: {jogo["data"]}

CONTEXTO:
{jogo["contexto"]}

ESTATISTICAS (Media ultimos 5 jogos):

GOLS:
- Casa: {jogo["gols_casa"]:.1f} | Fora: {jogo["gols_fora"]:.1f}
- Total esperado: {total_gols:.1f}
- Veredicto: {"Over 2.5" if total_gols > 2.5 else "Under 2.5"}

CANTOS:
- Casa: {jogo["cantos_casa"]:.1f} | Fora: {jogo["cantos_fora"]:.1f}
- Total esperado: {total_cantos:.1f}
- Veredicto: {"Over 9.5" if total_cantos > 9.5 else "Under 9.5"}

CARTOES:
- Casa: {jogo["cartoes_casa"]:.1f} | Fora: {jogo["cartoes_fora"]:.1f}
- Total esperado: {total_cartoes:.1f}
- Veredicto: {"Over 3.5" if total_cartoes > 3.5 else "Under 3.5"}

RECOMENDACAO FanDuel:
- Aposta: {melhor_aposta}
- Confianca: {confianca}
- Unidades: {unidades}
"""
    return analise

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "BOT DE ANALISE ESPORTIVA\n\n"
        "Comandos disponiveis:\n\n"
        "/premier - Premier League\n"
        "/laliga - LaLiga\n"
        "/bundesliga - Bundesliga\n"
        "/seriea - Serie A\n"
        "/ligue1 - Ligue 1\n\n"
        "/jogos - Todos os jogos\n"
        "/melhores - Melhores apostas\n\n"
        "Ou digite o jogo:\n"
        "Ex: Tottenham x Liverpool"
    )

async def jogos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lista = "JOGOS DISPONIVEIS:\n\n"
    ligas = {}
    for jogo, dados in JOGOS.items():
        liga = dados["liga"]
        if liga not in ligas:
            ligas[liga] = []
        ligas[liga].append(f"- {jogo.title()} ({dados['data']})")
    for liga, jogos_lista in ligas.items():
        lista += f"{liga}:\n"
        for j in jogos_lista:
            lista += f"{j}\n"
        lista += "\n"
    await update.message.reply_text(lista)

async def premier(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lista = "PREMIER LEAGUE:\n\n"
    for jogo, dados in JOGOS.items():
        if "Premier" in dados["liga"]:
            total_gols = dados["gols_casa"] + dados["gols_fora"]
            lista += f"{jogo.title()}\n"
            lista += f"  {dados['data']} - Gols esp: {total_gols:.1f}\n\n"
    lista += "Digite o nome do jogo para analise completa"
    await update.message.reply_text(lista)

async def laliga(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lista = "LALIGA:\n\n"
    for jogo, dados in JOGOS.items():
        if "LaLiga" in dados["liga"]:
            total_gols = dados["gols_casa"] + dados["gols_fora"]
            lista += f"{jogo.title()}\n"
            lista += f"  {dados['data']} - Gols esp: {total_gols:.1f}\n\n"
    lista += "Digite o nome do jogo para analise completa"
    await update.message.reply_text(lista)

async def bundesliga(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lista = "BUNDESLIGA:\n\n"
    for jogo, dados in JOGOS.items():
        if "Bundesliga" in dados["liga"]:
            total_gols = dados["gols_casa"] + dados["gols_fora"]
            lista += f"{jogo.title()}\n"
            lista += f"  {dados['data']} - Gols esp: {total_gols:.1f}\n\n"
    lista += "Digite o nome do jogo para analise completa"
    await update.message.reply_text(lista)

async def seriea(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lista = "SERIE A:\n\n"
    for jogo, dados in JOGOS.items():
        if "Serie A" in dados["liga"]:
            total_gols = dados["gols_casa"] + dados["gols_fora"]
            lista += f"{jogo.title()}\n"
            lista += f"  {dados['data']} - Gols esp: {total_gols:.1f}\n\n"
    lista += "Digite o nome do jogo para analise completa"
    await update.message.reply_text(lista)

async def ligue1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lista = "LIGUE 1 / COPA DA FRANCA:\n\n"
    for jogo, dados in JOGOS.items():
        if "Franca" in dados["liga"]:
            total_gols = dados["gols_casa"] + dados["gols_fora"]
            lista += f"{jogo.title()}\n"
            lista += f"  {dados['data']} - Gols esp: {total_gols:.1f}\n\n"
    lista += "Digite o nome do jogo para analise completa"
    await update.message.reply_text(lista)

async def melhores(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lista = "MELHORES APOSTAS DO DIA:\n\n"
    apostas = []
    for jogo, dados in JOGOS.items():
        total_gols = dados["gols_casa"] + dados["gols_fora"]
        if total_gols >= 2.8:
            apostas.append((jogo, dados, total_gols))
    apostas.sort(key=lambda x: x[2], reverse=True)
    for i, (jogo, dados, total) in enumerate(apostas[:5], 1):
        lista += f"{i}. {jogo.title()}\n"
        lista += f"   {dados['liga']}\n"
        lista += f"   Gols esp: {total:.1f}\n"
        lista += f"   Aposta: Over 2.5 Gols\n"
        lista += f"   Confianca: ALTA\n\n"
    lista += "Digite o nome do jogo para analise completa"
    await update.message.reply_text(lista)

async def mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.lower().strip()
    texto = texto.replace(" vs ", " x ").replace(" - ", " x ")
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
    app.add_handler(CommandHandler("bundesliga", bundesliga))
    app.add_handler(CommandHandler("seriea", seriea))
    app.add_handler(CommandHandler("ligue1", ligue1))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mensagem))
    print("Bot iniciado!")
    app.run_polling()

if __name__ == "__main__":
    main()
