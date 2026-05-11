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

    "Alabama", "Alaska", "Arizona",
    "Arkansas", "California", "Colorado",

    "Connecticut", "Delaware", "Florida",
    "Georgia", "Hawaii", "Idaho",

    "Illinois", "Indiana", "Iowa",
    "Kansas", "Kentucky", "Louisiana",

    "Maine", "Maryland", "Massachusetts",
    "Michigan", "Minnesota", "Mississippi",

    "Missouri", "Montana", "Nebraska",
    "Nevada", "New Hampshire", "New Jersey",

    "New Mexico", "New York", "North Carolina",
    "North Dakota", "Ohio", "Oklahoma",

    "Oregon", "Pennsylvania", "Rhode Island",
    "South Carolina", "South Dakota", "Tennessee",

    "Texas", "Utah", "Vermont",
    "Virginia", "Washington", "West Virginia",

    "Wisconsin", "Wyoming"
]

# ==========================================
# DATOS REALES
# ==========================================

STATE_DATA = {

    "California": {
        "city": "Los Angeles",
        "zip": "90001",
        "area": "213"
    },

    "Texas": {
        "city": "Houston",
        "zip": "77001",
        "area": "281"
    },

    "Florida": {
        "city": "Miami",
        "zip": "33101",
        "area": "305"
    },

    "New York": {
        "city": "Buffalo",
        "zip": "14201",
        "area": "716"
    },

    "Illinois": {
        "city": "Chicago",
        "zip": "60601",
        "area": "312"
    },
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

    second = random.randint(200, 999)

    third = random.randint(1000, 9999)

    return f"+1 ({area_code}) {second}-{third}"

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

    if state in STATE_DATA:

        data = STATE_DATA[state]

        city = data["city"]

        zip_code = data["zip"]

        area_code = data["area"]

    else:

        city = fake.city()

        zip_code = fake.zipcode()

        area_code = random.choice([

            "205", "907", "480",
            "501", "302", "208",
            "515", "620", "270",
            "225", "207", "410"
        ])

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

🌍 Generador de Direcciones USA

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

        # 👇 3 BOTONES POR FILA

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

    # 👇 ACTUALIZA EL MISMO MENSAJE

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
