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

# ==========================================
# TOKEN
# ==========================================

TOKEN = "8702989629:AAGHgafvmYRUA_hfI-jrSWYdZ0uFcIALdQc"

# ==========================================
# LOGS
# ==========================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ==========================================
# ESTADOS USA
# ==========================================

USA_STATES = [

    "California",
    "Texas",
    "Florida",
    "New York",
    "Illinois",
    "New Jersey",
    "Nevada",
    "Arizona",
    "Georgia",
    "Washington",
]

# ==========================================
# DATOS REALES
# ==========================================

STATE_DATA = {

    "California": [

        {
            "city": "Los Angeles",
            "zip": "90001",
            "area": "213"
        },

        {
            "city": "San Diego",
            "zip": "92101",
            "area": "619"
        },

        {
            "city": "San Francisco",
            "zip": "94102",
            "area": "415"
        },
    ],

    "Texas": [

        {
            "city": "Houston",
            "zip": "77001",
            "area": "281"
        },

        {
            "city": "Dallas",
            "zip": "75201",
            "area": "214"
        },

        {
            "city": "Austin",
            "zip": "73301",
            "area": "512"
        },
    ],

    "Florida": [

        {
            "city": "Miami",
            "zip": "33101",
            "area": "305"
        },

        {
            "city": "Orlando",
            "zip": "32801",
            "area": "407"
        },

        {
            "city": "Tampa",
            "zip": "33601",
            "area": "813"
        },
    ],

    "New York": [

        {
            "city": "Buffalo",
            "zip": "14201",
            "area": "716"
        },

        {
            "city": "New York City",
            "zip": "10001",
            "area": "212"
        },

        {
            "city": "Rochester",
            "zip": "14602",
            "area": "585"
        },
    ],

    "Illinois": [

        {
            "city": "Chicago",
            "zip": "60601",
            "area": "312"
        },

        {
            "city": "Aurora",
            "zip": "60502",
            "area": "630"
        },

        {
            "city": "Naperville",
            "zip": "60540",
            "area": "331"
        },
    ],

    "New Jersey": [

        {
            "city": "Newark",
            "zip": "07102",
            "area": "973"
        },

        {
            "city": "Jersey City",
            "zip": "07302",
            "area": "201"
        },

        {
            "city": "Paterson",
            "zip": "07501",
            "area": "862"
        },
    ],

    "Nevada": [

        {
            "city": "Las Vegas",
            "zip": "88901",
            "area": "702"
        },

        {
            "city": "Reno",
            "zip": "89501",
            "area": "775"
        },
    ],

    "Arizona": [

        {
            "city": "Phoenix",
            "zip": "85001",
            "area": "602"
        },

        {
            "city": "Tucson",
            "zip": "85701",
            "area": "520"
        },
    ],

    "Georgia": [

        {
            "city": "Atlanta",
            "zip": "30301",
            "area": "404"
        },

        {
            "city": "Savannah",
            "zip": "31401",
            "area": "912"
        },
    ],

    "Washington": [

        {
            "city": "Seattle",
            "zip": "98101",
            "area": "206"
        },

        {
            "city": "Spokane",
            "zip": "99201",
            "area": "509"
        },
    ],
}

# ==========================================
# EMAILS
# ==========================================

EMAIL_DOMAINS = [

    "gmail.com",
    "hotmail.com",
    "outlook.com",
    "yahoo.com"
]

# ==========================================
# GENERAR TELEFONO
# ==========================================

def generate_phone(area_code):

    middle = random.randint(200, 999)

    last = random.randint(1000, 9999)

    return f"+1 ({area_code}) {middle}-{last}"

# ==========================================
# GENERAR EMAIL
# ==========================================

def generate_email(first, last):

    number = random.randint(10, 999)

    username = random.choice([

        f"{first}.{last}{number}",
        f"{first}{number}",
        f"{last}{number}",
        f"{first}_{last}",
        f"{first}{last}",
    ])

    username = username.lower()

    domain = random.choice(EMAIL_DOMAINS)

    return f"{username}@{domain}"

# ==========================================
# GENERAR DIRECCION
# ==========================================

def generate_address(state):

    fake = Faker("en_US")

    location = random.choice(
        STATE_DATA[state]
    )

    city = location["city"]

    zip_code = location["zip"]

    area_code = location["area"]

    first = fake.first_name()

    last = fake.last_name()

    full_name = f"{first} {last}"

    street = fake.street_address()

    phone = generate_phone(area_code)

    email = generate_email(first, last)

    return f"""
🦊 <b>FOX REVOLUTION</b>

🇺🇸 USA

👤 <b>Nombre:</b>
<code>{full_name}</code>

🏠 <b>Dirección:</b>
<code>{street}</code>

🏙 <b>Ciudad:</b>
<code>{city}</code>

🗺 <b>Estado:</b>
<code>{state}</code>

📮 <b>Código Postal:</b>
<code>{zip_code}</code>

📞 <b>Teléfono:</b>
<code>{phone}</code>

📧 <b>Correo:</b>
<code>{email}</code>
"""

# ==========================================
# START
# ==========================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [

        [
            InlineKeyboardButton(
                "🇺🇸 Estados Unidos",
                callback_data="usa"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    text = """
🦊 <b>FOX REVOLUTION BOT</b>

🌍 Generador Premium USA

Selecciona un país:
"""

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=reply_markup
    )

# ==========================================
# MOSTRAR ESTADOS
# ==========================================

async def usa_states(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    keyboard = []

    row = []

    for state in USA_STATES:

        row.append(

            InlineKeyboardButton(
                state,
                callback_data=f"state_{state}"
            )
        )

        if len(row) == 3:

            keyboard.append(row)

            row = []

    if row:

        keyboard.append(row)

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_text(
        "🇺🇸 Selecciona un estado:",
        reply_markup=reply_markup
    )

# ==========================================
# GENERAR
# ==========================================

async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    state = query.data.replace(
        "state_",
        ""
    )

    text = generate_address(state)

    keyboard = [

        [
            InlineKeyboardButton(
                "🔄 Generar Nuevo",
                callback_data=f"state_{state}"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text=text,
        parse_mode="HTML",
        reply_markup=reply_markup
    )

# ==========================================
# BOTONES
# ==========================================

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    data = query.data

    if data == "usa":

        await usa_states(update, context)

    elif data.startswith("state_"):

        await generate(update, context)

# ==========================================
# HELP
# ==========================================

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
❓ <b>AYUDA</b>

Usa /start para comenzar.

✅ Estados reales USA
✅ Ciudades reales
✅ ZIP Codes reales
✅ Códigos telefónicos reales
✅ Correos realistas
✅ Generador premium

⚡ Powered By Fox Revolution
"""

    await update.message.reply_text(
        text,
        parse_mode="HTML"
    )

# ==========================================
# MAIN
# ==========================================

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

# ==========================================
# RUN
# ==========================================

if __name__ == "__main__":
    main()
