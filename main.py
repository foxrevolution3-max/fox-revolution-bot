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

# ==================================================
# TOKEN
# ==================================================

TOKEN = "8702989629:AAGHgafvmYRUA_hfI-jrSWYdZ0uFcIALdQc"

# ==================================================
# LOGS
# ==================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ==================================================
# ESTADOS USA
# ==================================================

USA_STATES = [

    "Alabama", "Alaska", "Arizona", "Arkansas",
    "California", "Colorado", "Connecticut",
    "Delaware", "Florida", "Georgia", "Hawaii",
    "Idaho", "Illinois", "Indiana", "Iowa",
    "Kansas", "Kentucky", "Louisiana", "Maine",
    "Maryland", "Massachusetts", "Michigan",
    "Minnesota", "Mississippi", "Missouri",
    "Montana", "Nebraska", "Nevada",
    "New Hampshire", "New Jersey", "New Mexico",
    "New York", "North Carolina", "North Dakota",
    "Ohio", "Oklahoma", "Oregon",
    "Pennsylvania", "Rhode Island",
    "South Carolina", "South Dakota",
    "Tennessee", "Texas", "Utah",
    "Vermont", "Virginia", "Washington",
    "West Virginia", "Wisconsin", "Wyoming"

]

# ==================================================
# DATOS REALES
# ==================================================

REAL_DATA = {

    "California": {
        "cities": [
            ("Los Angeles", "90001", "213"),
            ("San Diego", "92101", "619"),
            ("San Francisco", "94102", "415"),
        ]
    },

    "Texas": {
        "cities": [
            ("Houston", "77001", "713"),
            ("Dallas", "75201", "214"),
            ("Austin", "73301", "512"),
        ]
    },

    "Florida": {
        "cities": [
            ("Miami", "33101", "305"),
            ("Orlando", "32801", "407"),
            ("Tampa", "33601", "813"),
        ]
    },

    "New York": {
        "cities": [
            ("New York City", "10001", "212"),
            ("Buffalo", "14201", "716"),
            ("Rochester", "14602", "585"),
        ]
    },

    "Illinois": {
        "cities": [
            ("Chicago", "60601", "312"),
            ("Aurora", "60502", "331"),
            ("Naperville", "60540", "630"),
        ]
    },

    "Nevada": {
        "cities": [
            ("Las Vegas", "88901", "702"),
            ("Reno", "89501", "775"),
        ]
    },

    "Arizona": {
        "cities": [
            ("Phoenix", "85001", "602"),
            ("Tucson", "85701", "520"),
        ]
    },

    "Georgia": {
        "cities": [
            ("Atlanta", "30301", "404"),
            ("Savannah", "31401", "912"),
        ]
    },

    "Washington": {
        "cities": [
            ("Seattle", "98101", "206"),
            ("Spokane", "99201", "509"),
        ]
    },

    "New Jersey": {
        "cities": [
            ("Newark", "07101", "973"),
            ("Jersey City", "07302", "201"),
        ]
    },

    "Pennsylvania": {
        "cities": [
            ("Philadelphia", "19019", "215"),
            ("Pittsburgh", "15201", "412"),
        ]
    },

    "Michigan": {
        "cities": [
            ("Detroit", "48201", "313"),
            ("Grand Rapids", "49503", "616"),
        ]
    },

    "Massachusetts": {
        "cities": [
            ("Boston", "02108", "617"),
            ("Cambridge", "02138", "857"),
        ]
    },

    "Tennessee": {
        "cities": [
            ("Nashville", "37201", "615"),
            ("Memphis", "37501", "901"),
        ]
    },

    "Indiana": {
        "cities": [
            ("Indianapolis", "46201", "317"),
            ("Fort Wayne", "46802", "260"),
        ]
    },

    "Missouri": {
        "cities": [
            ("Kansas City", "64101", "816"),
            ("St. Louis", "63101", "314"),
        ]
    },
}

# ==================================================
# EMAILS
# ==================================================

EMAIL_DOMAINS = [
    "gmail.com",
    "hotmail.com",
    "outlook.com",
    "yahoo.com",
]

# ==================================================
# EMAIL
# ==================================================

def generate_email(first, last):

    number = random.randint(10, 999)

    username = random.choice([
        f"{first}.{last}{number}",
        f"{first}_{last}",
        f"{first}{last}",
        f"{first}{number}",
    ]).lower()

    domain = random.choice(EMAIL_DOMAINS)

    return f"{username}@{domain}"

# ==================================================
# TELEFONO
# ==================================================

def generate_phone(area):

    part1 = random.randint(200, 999)
    part2 = random.randint(1000, 9999)

    return f"+1 ({area}) {part1}-{part2}"

# ==================================================
# GENERAR DIRECCION
# ==================================================

def generate_address(state):

    fake = Faker("en_US")

    if state not in REAL_DATA:
        city = fake.city()
        zip_code = fake.zipcode()
        area = "000"

    else:
        city, zip_code, area = random.choice(
            REAL_DATA[state]["cities"]
        )

    first = fake.first_name()
    last = fake.last_name()

    full_name = f"{first} {last}"

    street = fake.street_address()

    phone = generate_phone(area)

    email = generate_email(first, last)

    return f"""
🦊 <b>FOX REVOLUTION</b>

🇺🇸 USA

👤 <b>Nombre:</b>
{full_name}

🏠 <b>Dirección:</b>
{street}

🏙 <b>Ciudad:</b>
{city}

🗺 <b>Estado:</b>
{state}

📮 <b>Código Postal:</b>
{zip_code}

📞 <b>Teléfono:</b>
{phone}

📧 <b>Correo:</b>
{email}
"""

# ==================================================
# START
# ==================================================

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

# ==================================================
# MOSTRAR ESTADOS
# ==================================================

async def show_states(query):

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
        "🇺🇸 <b>Selecciona un estado:</b>",
        parse_mode="HTML",
        reply_markup=reply_markup
    )

# ==================================================
# BOTONES
# ==================================================

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    data = query.data

    # ABRIR ESTADOS
    if data == "usa":

        await show_states(query)
        return

    # GENERAR
    if data.startswith("state_"):

        state = data.replace("state_", "")

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

        await query.message.reply_text(
            text,
            parse_mode="HTML",
            reply_markup=reply_markup
        )

# ==================================================
# HELP
# ==================================================

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
❓ <b>AYUDA</b>

Usa /start para comenzar.

✅ Estados reales
✅ Ciudades reales
✅ ZIP reales
✅ Área telefónica real
✅ Correos coherentes
✅ Generación premium USA

🦊 Powered By Fox Revolution
"""

    await update.message.reply_text(
        text,
        parse_mode="HTML"
    )

# ==================================================
# MAIN
# ==================================================

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

# ==================================================
# RUN
# ==================================================

if __name__ == "__main__":
    main()
