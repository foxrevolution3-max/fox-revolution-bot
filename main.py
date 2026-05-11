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

# =====================================
# TOKEN
# =====================================

TOKEN = "8702989629:AAGHgafvmYRUA_hfI-jrSWYdZ0uFcIALdQc"

# =====================================
# LOGS
# =====================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# =====================================
# FAKER
# =====================================

fake = Faker("en_US")

# =====================================
# ESTADOS USA
# =====================================

USA_STATES = {

    "California": [
        ("Los Angeles", "90001"),
        ("San Diego", "92101"),
        ("San Francisco", "94101"),
    ],

    "Texas": [
        ("Houston", "77001"),
        ("Dallas", "75201"),
        ("Austin", "73301"),
    ],

    "Florida": [
        ("Miami", "33101"),
        ("Orlando", "32801"),
        ("Tampa", "33601"),
    ],

    "New York": [
        ("New York City", "10001"),
        ("Buffalo", "14201"),
        ("Albany", "12201"),
    ],

    "Illinois": [
        ("Chicago", "60601"),
        ("Aurora", "60502"),
        ("Naperville", "60540"),
    ],

    "Arizona": [
        ("Phoenix", "85001"),
        ("Tucson", "85701"),
        ("Mesa", "85201"),
    ],

    "Nevada": [
        ("Las Vegas", "88901"),
        ("Reno", "89501"),
        ("Henderson", "89002"),
    ],

    "Georgia": [
        ("Atlanta", "30301"),
        ("Savannah", "31401"),
        ("Augusta", "30901"),
    ],

    "Washington": [
        ("Seattle", "98101"),
        ("Tacoma", "98401"),
        ("Spokane", "99201"),
    ],

    "Colorado": [
        ("Denver", "80201"),
        ("Aurora", "80010"),
        ("Boulder", "80301"),
    ],

    "Ohio": [
        ("Columbus", "43004"),
        ("Cleveland", "44101"),
        ("Cincinnati", "45201"),
    ],

    "North Carolina": [
        ("Charlotte", "28201"),
        ("Raleigh", "27601"),
        ("Durham", "27701"),
    ],

    "Virginia": [
        ("Virginia Beach", "23450"),
        ("Richmond", "23173"),
        ("Norfolk", "23501"),
    ],

    "Pennsylvania": [
        ("Philadelphia", "19019"),
        ("Pittsburgh", "15201"),
        ("Allentown", "18101"),
    ],

    "Michigan": [
        ("Detroit", "48201"),
        ("Grand Rapids", "49501"),
        ("Lansing", "48901"),
    ],

    "New Jersey": [
        ("Newark", "07101"),
        ("Jersey City", "07302"),
        ("Paterson", "07501"),
    ],

    "Massachusetts": [
        ("Boston", "02108"),
        ("Cambridge", "02138"),
        ("Salem", "01970"),
    ],

    "Tennessee": [
        ("Nashville", "37201"),
        ("Memphis", "37501"),
        ("Knoxville", "37901"),
    ],

    "Indiana": [
        ("Indianapolis", "46201"),
        ("Fort Wayne", "46801"),
        ("Evansville", "47701"),
    ],

    "Missouri": [
        ("Kansas City", "64101"),
        ("St. Louis", "63101"),
        ("Springfield", "65801"),
    ],
}

# =====================================
# EMAILS
# =====================================

EMAIL_DOMAINS = [
    "gmail.com",
    "hotmail.com",
    "outlook.com",
    "yahoo.com",
]

# =====================================
# GENERAR EMAIL
# =====================================

def generate_email(first, last):

    number = random.randint(10, 999)

    username = random.choice([
        f"{first}{last}",
        f"{first}.{last}",
        f"{first}_{last}",
        f"{first}{number}",
        f"{last}{number}",
    ]).lower()

    domain = random.choice(EMAIL_DOMAINS)

    return f"{username}@{domain}"

# =====================================
# GENERAR DIRECCION
# =====================================

def generate_address(state):

    city, postal = random.choice(
        USA_STATES[state]
    )

    first = fake.first_name()
    last = fake.last_name()

    fullname = f"{first} {last}"

    street = fake.street_address()

    phone = fake.phone_number()

    email = generate_email(first, last)

    return f"""
🦊 <b>FOX REVOLUTION</b>

🇺🇸 USA

👤 <b>Name:</b>
<code>{fullname}</code>

🏠 <b>Address:</b>
<code>{street}</code>

🏙 <b>City:</b>
<code>{city}</code>

🗺 <b>State:</b>
<code>{state}</code>

📮 <b>ZIP Code:</b>
<code>{postal}</code>

📞 <b>Phone:</b>
<code>{phone}</code>

📧 <b>Email:</b>
<code>{email}</code>
"""

# =====================================
# START
# =====================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton(
                "🇺🇸 United States",
                callback_data="usa"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    text = """
🦊 <b>FOX REVOLUTION BOT</b>

🌍 USA Address Generator

Select country:
"""

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=reply_markup
    )

# =====================================
# BOTONES
# =====================================

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    data = query.data

    # MOSTRAR ESTADOS
    if data == "usa":

        keyboard = []

        row = []

        for i, state in enumerate(
            USA_STATES.keys(),
            start=1
        ):

            row.append(
                InlineKeyboardButton(
                    state,
                    callback_data=state
                )
            )

            # 🔥 3 BOTONES POR FILA
            if len(row) == 3:

                keyboard.append(row)

                row = []

        if row:
            keyboard.append(row)

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text(
            "🇺🇸 Select a state:",
            reply_markup=reply_markup
        )

        return

    # GENERAR DIRECCION
    state = data

    text = generate_address(state)

    keyboard = [
        [
            InlineKeyboardButton(
                "🔄 Generate New",
                callback_data=state
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=reply_markup
    )

# =====================================
# HELP
# =====================================

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
🦊 <b>FOX REVOLUTION BOT</b>

Use /start to begin.

✅ Real USA states
✅ Real cities
✅ Real ZIP codes
✅ Realistic emails
✅ Random phones
✅ Premium generator
"""

    await update.message.reply_text(
        text,
        parse_mode="HTML"
    )

# =====================================
# MAIN
# =====================================

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

    print("🦊 FOX REVOLUTION BOT STARTED")

    app.run_polling()

# =====================================
# RUN
# =====================================

if __name__ == "__main__":
    main()
