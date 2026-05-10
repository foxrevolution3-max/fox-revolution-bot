from faker import Faker
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

# TOKEN
TOKEN = "8702989629:AAGHgafvmYRUA_hfI-jrSWYdZ0uFcIALdQc"

# PAÍSES COMPATIBLES
COUNTRIES = {

    "us": "🇺🇸 Estados Unidos",
    "ca": "🇨🇦 Canadá",
    "mx": "🇲🇽 México",
    "es": "🇪🇸 España",
    "ar": "🇦🇷 Argentina",
    "co": "🇨🇴 Colombia",
    "cl": "🇨🇱 Chile",
    "pe": "🇵🇪 Perú",
    "br": "🇧🇷 Brasil",

    "fr": "🇫🇷 Francia",
    "de": "🇩🇪 Alemania",
    "it": "🇮🇹 Italia",
    "gb": "🇬🇧 Reino Unido",
    "nl": "🇳🇱 Países Bajos",
    "be": "🇧🇪 Bélgica",
    "pl": "🇵🇱 Polonia",
    "ru": "🇷🇺 Rusia",
    "tr": "🇹🇷 Turquía",

    "jp": "🇯🇵 Japón",
    "kr": "🇰🇷 Corea del Sur",
    "cn": "🇨🇳 China",
    "in": "🇮🇳 India",
    "th": "🇹🇭 Tailandia",
    "id": "🇮🇩 Indonesia",

    "sa": "🇸🇦 Arabia Saudita",
    "ae": "🇦🇪 Emiratos Árabes",

    "za": "🇿🇦 Sudáfrica",
    "ng": "🇳🇬 Nigeria",

    "au": "🇦🇺 Australia",
    "nz": "🇳🇿 Nueva Zelanda"
}

# LOCALES
LOCALES = {

    "us": "en_US",
    "ca": "en_CA",
    "mx": "es_MX",
    "es": "es_ES",
    "ar": "es_AR",
    "co": "es_CO",
    "cl": "es_CL",
    "pe": "es_PE",
    "br": "pt_BR",

    "fr": "fr_FR",
    "de": "de_DE",
    "it": "it_IT",
    "gb": "en_GB",
    "nl": "nl_NL",
    "be": "fr_BE",
    "pl": "pl_PL",
    "ru": "ru_RU",
    "tr": "tr_TR",

    "jp": "ja_JP",
    "kr": "ko_KR",
    "cn": "zh_CN",
    "in": "en_IN",
    "th": "th_TH",
    "id": "id_ID",

    "sa": "ar_SA",
    "ae": "ar_AE",

    "za": "en_ZA",
    "ng": "en_NG",

    "au": "en_AU",
    "nz": "en_NZ"
}

# CÓDIGOS TELEFÓNICOS
PHONE_CODES = {

    "en_US": "+1",
    "en_CA": "+1",
    "es_MX": "+52",
    "es_ES": "+34",
    "es_AR": "+54",
    "es_CO": "+57",
    "es_CL": "+56",
    "es_PE": "+51",
    "pt_BR": "+55",

    "fr_FR": "+33",
    "de_DE": "+49",
    "it_IT": "+39",
    "en_GB": "+44",
    "nl_NL": "+31",
    "fr_BE": "+32",
    "pl_PL": "+48",
    "ru_RU": "+7",
    "tr_TR": "+90",

    "ja_JP": "+81",
    "ko_KR": "+82",
    "zh_CN": "+86",
    "en_IN": "+91",
    "th_TH": "+66",
    "id_ID": "+62",

    "ar_SA": "+966",
    "ar_AE": "+971",

    "en_ZA": "+27",
    "en_NG": "+234",

    "en_AU": "+61",
    "en_NZ": "+64"
}

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    mensaje = """
╔══════════════════════╗
      🦊 FOX REVOLUTION
╚══════════════════════╝

🔥 Generador Premium
de Direcciones Fake

━━━━━━━━━━━━━━━━━━

📌 COMANDOS

🌍 /address
➜ Elegir país

🎲 /random
➜ Dirección aleatoria

❓ /help
➜ Ayuda

━━━━━━━━━━━━━━━━━━

⚡ Powered By Fox Revolution
"""

    await update.message.reply_text(mensaje)

# HELP
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    texto = """
📌 AYUDA DEL BOT

🌍 /address
➜ Elegir país y generar dirección

🎲 /random
➜ Generar dirección aleatoria

❓ /help
➜ Mostrar ayuda
"""

    await update.message.reply_text(texto)

# GENERAR DIRECCIÓN
def generar_direccion(locale_code):

    fake = Faker(locale_code)

    nombre = fake.name()
    direccion = fake.street_address()
    ciudad = fake.city()

    try:
        estado = fake.state()
    except:
        estado = "No disponible"

    codigo = fake.postcode()

    codigo_pais = PHONE_CODES.get(locale_code, "+1")

    telefono = fake.msisdn()[:9]

    telefono = (
        f"{codigo_pais} "
        f"{telefono[:3]}-"
        f"{telefono[3:6]}-"
        f"{telefono[6:]}"
    )

    return f"""
👤 Nombre:
{nombre}

🏠 Dirección:
{direccion}

🏙 Ciudad:
{ciudad}

📍 Estado:
{estado}

📮 Código Postal:
{codigo}

📞 Teléfono:
{telefono}
"""

# ADDRESS
async def address(update: Update, context: ContextTypes.DEFAULT_TYPE):

    botones = []

    fila = []

    for country_key, country_name in COUNTRIES.items():

        fila.append(
            InlineKeyboardButton(
                country_name,
                callback_data=country_key
            )
        )

        if len(fila) == 3:
            botones.append(fila)
            fila = []

    if fila:
        botones.append(fila)

    reply_markup = InlineKeyboardMarkup(botones)

    await update.message.reply_text(
        "🌍 ELIGE UN PAÍS",
        reply_markup=reply_markup
    )

# BOTONES
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    country_key = query.data

    locale_code = LOCALES[country_key]

    country_name = COUNTRIES[country_key]

    direccion = generar_direccion(locale_code)

    botones = [
        [
            InlineKeyboardButton(
                "🔄 Nueva Dirección",
                callback_data=country_key
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(botones)

    await query.edit_message_text(
        f"""
🦊 FOX REVOLUTION

{country_name}

{direccion}
""",
        reply_markup=reply_markup
    )

# RANDOM
async def random_address(update: Update, context: ContextTypes.DEFAULT_TYPE):

    import random

    country_key = random.choice(list(COUNTRIES.keys()))

    locale_code = LOCALES[country_key]

    country_name = COUNTRIES[country_key]

    direccion = generar_direccion(locale_code)

    await update.message.reply_text(
        f"""
🎲 DIRECCIÓN ALEATORIA

{country_name}

{direccion}
"""
    )

# MAIN
def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("address", address))
    app.add_handler(CommandHandler("random", random_address))
    app.add_handler(CallbackQueryHandler(button))

    print("🦊 FOX REVOLUTION BOT INICIADO")

    app.run_polling()

if __name__ == "__main__":
    main()
