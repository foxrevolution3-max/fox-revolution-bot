import logging
import random

from faker import Faker

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# =========================
# TOKEN
# =========================

TOKEN = "8702989629:AAGHgafvmYRUA_hfI-jrSWYdZ0uFcIALdQc"

# =========================
# LOGS
# =========================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# =========================
# PAISES + LOCALES
# =========================

COUNTRIES = {

    "🇺🇸 USA": "en_US",
    "🇲🇽 México": "es_MX",
    "🇦🇷 Argentina": "es_AR",
    "🇧🇷 Brasil": "pt_BR",
    "🇨🇦 Canadá": "en_CA",
    "🇪🇸 España": "es_ES",
}

# =========================
# CIUDADES REALES
# =========================

REAL_LOCATIONS = {

    "🇺🇸 USA": [

        {
            "city": "New York",
            "state": "New York",
            "postal": "10001"
        },

        {
            "city": "Los Angeles",
            "state": "California",
            "postal": "90001"
        },

        {
            "city": "Chicago",
            "state": "Illinois",
            "postal": "60601"
        },
    ],

    "🇲🇽 México": [

        {
            "city": "Ciudad de México",
            "state": "CDMX",
            "postal": "01000"
        },

        {
            "city": "Guadalajara",
            "state": "Jalisco",
            "postal": "44100"
        },

        {
            "city": "Monterrey",
            "state": "Nuevo León",
            "postal": "64000"
        },
    ],

    "🇦🇷 Argentina": [

        {
            "city": "Buenos Aires",
            "state": "Buenos Aires",
            "postal": "1000"
        },

        {
            "city": "Córdoba",
            "state": "Córdoba",
            "postal": "5000"
        },

        {
            "city": "Rosario",
            "state": "Santa Fe",
            "postal": "2000"
        },
    ],

    "🇧🇷 Brasil": [

        {
            "city": "São Paulo",
            "state": "São Paulo",
            "postal": "01000-000"
        },

        {
            "city": "Rio de Janeiro",
            "state": "Rio de Janeiro",
            "postal": "20000-000"
        },

        {
            "city": "Brasília",
            "state": "Distrito Federal",
            "postal": "70000-000"
        },
    ],

    "🇨🇦 Canadá": [

        {
            "city": "Toronto",
            "state": "Ontario",
            "postal": "M5V 3L9"
        },

        {
            "city": "Vancouver",
            "state": "British Columbia",
            "postal": "V5K 0A1"
        },

        {
            "city": "Montreal",
            "state": "Quebec",
            "postal": "H1A 0A1"
        },
    ],

    "🇪🇸 España": [

        {
            "city": "Madrid",
            "state": "Madrid",
            "postal": "28001"
        },

        {
            "city": "Barcelona",
            "state": "Cataluña",
            "postal": "08001"
        },

        {
            "city": "Valencia",
            "state": "Valencia",
            "postal": "46001"
        },
    ]
}

# =========================
# DOMINIOS EMAIL
# =========================

EMAIL_DOMAINS = [

    "gmail.com",
    "hotmail.com",
    "outlook.com",
    "yahoo.com",
]

# =========================
# GENERAR EMAIL
# =========================

def generate_email(first, last):

    number = random.randint(10, 999)

    formats = [

        f"{first}.{last}{number}",
        f"{first}{number}",
        f"{last}{number}",
        f"{first}_{last}",
        f"{first}{last}",
    ]

    username = random.choice(formats).lower()

    username = (
        username
        .replace(" ", "")
        .replace("á", "a")
        .replace("é", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ú", "u")
        .replace("ñ", "n")
    )

    domain = random.choice(EMAIL_DOMAINS)

    return f"{username}@{domain}"

# =========================
# GENERAR DIRECCION
# =========================

def generate_address(country_name, locale_code):

    fake = Faker(locale_code)

    location = random.choice(
        REAL_LOCATIONS[country_name]
    )

    city = location["city"]
    state = location["state"]
    postal = location["postal"]

    first_name = fake.first_name()
    last_name = fake.last_name()

    full_name = f"{first_name} {last_name}"

    street = fake.street_address()

    phone = fake.phone_number()

    email = generate_email(
        first_name,
        last_name
    )

    return f"""
🦊 <b>FOX REVOLUTION</b>

{country_name}

👤 <b>Nombre:</b>
<code>{full_name}</code>

🏠 <b>Dirección:</b>
<code>{street}</code>

🏙 <b>Ciudad:</b>
<code>{city}</code>

🗺 <b>Estado:</b>
<code>{state}</code>

📮 <b>Código Postal:</b>
<code>{postal}</code>

📞 <b>Teléfono:</b>
<code>{phone}</code>

📧 <b>Correo:</b>
<code>{email}</code>
"""

# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = []

    row = []

    for i, country in enumerate(
        COUNTRIES.keys(),
        start=1
    ):

        row.append(
            InlineKeyboardButton(
                country,
                callback_data=country
            )
        )

        if len(row) == 2:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    reply_markup = InlineKeyboardMarkup(keyboard)

    text = """
🦊 <b>FOX REVOLUTION BOT</b>

🌍 Generador Premium

Selecciona un país:
"""

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=reply_markup
    )

# =========================
# BOTONES
# =========================

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    country_name = query.data

    locale_code = COUNTRIES[country_name]

    text = generate_address(
        country_name,
        locale_code
    )

    keyboard = [

        [
            InlineKeyboardButton(
                "🔄 Nueva Dirección",
                callback_data=country_name
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=reply_markup
    )

# =========================
# HELP
# =========================

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
❓ <b>AYUDA</b>

Usa /start para comenzar.

✅ Ciudades reales
✅ Estados reales
✅ Códigos postales reales
✅ Correos similares al nombre
✅ Datos coherentes por país

⚡ Powered By Fox Revolution
"""

    await update.message.reply_text(
        text,
        parse_mode="HTML"
    )

# =========================
# MAIN
# =========================

def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("help", help_command)
    )

    app.add_handler(
        CallbackQueryHandler(button)
    )

    print("🦊 FOX REVOLUTION BOT INICIADO")

    app.run_polling()

# =========================
# RUN
# =========================

if __name__ == "__main__":
    main()
