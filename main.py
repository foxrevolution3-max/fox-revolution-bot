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

TOKEN = "TU_TOKEN_AQUI"

# =========================
# LOGS
# =========================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# =========================
# DATOS REALES USA
# =========================

REAL_USA_DATA = {

    "California": {
        "city": "Los Angeles",
        "zip": "90001",
        "area_codes": ["213"]
    },

    "Texas": {
        "city": "Dallas",
        "zip": "75201",
        "area_codes": ["214"]
    },

    "Florida": {
        "city": "Orlando",
        "zip": "32801",
        "area_codes": ["407"]
    },

    "New York": {
        "city": "Rochester",
        "zip": "14602",
        "area_codes": ["585"]
    },

    "Illinois": {
        "city": "Chicago",
        "zip": "60601",
        "area_codes": ["312"]
    },

    "Georgia": {
        "city": "Atlanta",
        "zip": "30301",
        "area_codes": ["404"]
    },

    "Nevada": {
        "city": "Las Vegas",
        "zip": "88901",
        "area_codes": ["702"]
    },

    "Washington": {
        "city": "Seattle",
        "zip": "98101",
        "area_codes": ["206"]
    },

    "Arizona": {
        "city": "Phoenix",
        "zip": "85001",
        "area_codes": ["602"]
    },

    "Utah": {
        "city": "Salt Lake City",
        "zip": "84101",
        "area_codes": ["801"]
    },

    "West Virginia": {
        "city": "Charleston",
        "zip": "25301",
        "area_codes": ["304"]
    },

    "Alabama": {
        "city": "Birmingham",
        "zip": "35203",
        "area_codes": ["205"]
    },

    "Alaska": {
        "city": "Anchorage",
        "zip": "99501",
        "area_codes": ["907"]
    },

    "Arkansas": {
        "city": "Little Rock",
        "zip": "72201",
        "area_codes": ["501"]
    },

    "Colorado": {
        "city": "Denver",
        "zip": "80201",
        "area_codes": ["303"]
    },

    "Connecticut": {
        "city": "Bridgeport",
        "zip": "06601",
        "area_codes": ["203"]
    },

    "Delaware": {
        "city": "Wilmington",
        "zip": "19801",
        "area_codes": ["302"]
    },

    "Hawaii": {
        "city": "Honolulu",
        "zip": "96801",
        "area_codes": ["808"]
    },

    "Idaho": {
        "city": "Boise",
        "zip": "83701",
        "area_codes": ["208"]
    },

    "Indiana": {
        "city": "Indianapolis",
        "zip": "46201",
        "area_codes": ["317"]
    },

    "Iowa": {
        "city": "Des Moines",
        "zip": "50301",
        "area_codes": ["515"]
    },

    "Kansas": {
        "city": "Wichita",
        "zip": "67201",
        "area_codes": ["316"]
    },

    "Kentucky": {
        "city": "Louisville",
        "zip": "40201",
        "area_codes": ["502"]
    },

    "Louisiana": {
        "city": "New Orleans",
        "zip": "70112",
        "area_codes": ["504"]
    },

    "Maine": {
        "city": "Portland",
        "zip": "04101",
        "area_codes": ["207"]
    },

    "Maryland": {
        "city": "Baltimore",
        "zip": "21201",
        "area_codes": ["410"]
    },

    "Massachusetts": {
        "city": "Boston",
        "zip": "02108",
        "area_codes": ["617"]
    },

    "Michigan": {
        "city": "Detroit",
        "zip": "48201",
        "area_codes": ["313"]
    },

    "Minnesota": {
        "city": "Minneapolis",
        "zip": "55401",
        "area_codes": ["612"]
    },

    "Mississippi": {
        "city": "Jackson",
        "zip": "39201",
        "area_codes": ["601"]
    },

    "Missouri": {
        "city": "Kansas City",
        "zip": "64101",
        "area_codes": ["816"]
    },

    "Montana": {
        "city": "Billings",
        "zip": "59101",
        "area_codes": ["406"]
    },

    "Nebraska": {
        "city": "Omaha",
        "zip": "68101",
        "area_codes": ["402"]
    },

    "New Hampshire": {
        "city": "Manchester",
        "zip": "03101",
        "area_codes": ["603"]
    },

    "New Jersey": {
        "city": "Newark",
        "zip": "07101",
        "area_codes": ["973"]
    },

    "New Mexico": {
        "city": "Albuquerque",
        "zip": "87101",
        "area_codes": ["505"]
    },

    "North Carolina": {
        "city": "Charlotte",
        "zip": "28201",
        "area_codes": ["704"]
    },

    "North Dakota": {
        "city": "Fargo",
        "zip": "58102",
        "area_codes": ["701"]
    },

    "Ohio": {
        "city": "Columbus",
        "zip": "43004",
        "area_codes": ["614"]
    },

    "Oklahoma": {
        "city": "Oklahoma City",
        "zip": "73101",
        "area_codes": ["405"]
    },

    "Oregon": {
        "city": "Portland",
        "zip": "97201",
        "area_codes": ["503"]
    },

    "Pennsylvania": {
        "city": "Philadelphia",
        "zip": "19019",
        "area_codes": ["215"]
    },

    "Rhode Island": {
        "city": "Providence",
        "zip": "02901",
        "area_codes": ["401"]
    },

    "South Carolina": {
        "city": "Columbia",
        "zip": "29201",
        "area_codes": ["803"]
    },

    "South Dakota": {
        "city": "Sioux Falls",
        "zip": "57101",
        "area_codes": ["605"]
    },

    "Tennessee": {
        "city": "Nashville",
        "zip": "37201",
        "area_codes": ["615"]
    },

    "Vermont": {
        "city": "Burlington",
        "zip": "05401",
        "area_codes": ["802"]
    },

    "Virginia": {
        "city": "Virginia Beach",
        "zip": "23450",
        "area_codes": ["757"]
    },

    "Wisconsin": {
        "city": "Milwaukee",
        "zip": "53201",
        "area_codes": ["414"]
    },

    "Wyoming": {
        "city": "Cheyenne",
        "zip": "82001",
        "area_codes": ["307"]
    }

}

# =========================
# EMAILS
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

    username = random.choice([

        f"{first}.{last}{number}",
        f"{first}_{last}",
        f"{first}{number}",
        f"{last}{number}",
        f"{first}{last}"

    ]).lower()

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
# GENERAR TELEFONO
# =========================

def generate_phone(area_code):

    middle = random.randint(200, 999)
    last = random.randint(1000, 9999)

    return f"+1 ({area_code}) {middle}-{last}"

# =========================
# GENERAR DATOS
# =========================

def generate_address(state_name):

    fake = Faker("en_US")

    data = REAL_USA_DATA[state_name]

    city = data["city"]
    zip_code = data["zip"]
    area_code = random.choice(data["area_codes"])

    first_name = fake.first_name()
    last_name = fake.last_name()

    full_name = f"{first_name} {last_name}"

    street = fake.street_address()

    phone = generate_phone(area_code)

    email = generate_email(
        first_name,
        last_name
    )

    return f"""
🦊 <b>FOX REVOLUTION</b>

🇺🇸 <b>USA</b>

👤 <b>Nombre:</b>
<code>{full_name}</code>

🏠 <b>Dirección:</b>
<code>{street}</code>

🏙 <b>Ciudad:</b>
<code>{city}</code>

🗺 <b>Estado:</b>
<code>{state_name}</code>

📮 <b>Código Postal:</b>
<code>{zip_code}</code>

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

    states = list(REAL_USA_DATA.keys())

    for i, state in enumerate(states, start=1):

        row.append(
            InlineKeyboardButton(
                state,
                callback_data=state
            )
        )

        if len(row) == 3:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    reply_markup = InlineKeyboardMarkup(keyboard)

    text = """
🦊 <b>FOX REVOLUTION BOT</b>

🌎 <b>Generador Premium USA</b>

🇺🇸 Selecciona un estado:
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

    state_name = query.data

    text = generate_address(state_name)

    keyboard = [[

        InlineKeyboardButton(
            "🔄 Generar Nuevo",
            callback_data=state_name
        )

    ]]

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

✅ Estados reales USA
✅ Ciudades reales
✅ ZIP reales
✅ Area Codes reales
✅ Formato USA correcto
✅ Correos automáticos
✅ Teléfonos coherentes

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
