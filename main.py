import logging

from parser import (
    get_topics, 
    get_href, 
    get_themes, 
    get_name,
    get_tag,
)
from config import TG_TOKEN

from telegram import (
    InlineKeyboardButton, 
    InlineKeyboardMarkup, 
    Update, 
    ReplyKeyboardMarkup, 
    ReplyKeyboardRemove,
    ParseMode
)

from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
    MessageHandler,
    Filters,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Stages
MAIN, GET, TYPE = range(3)
# Callback data
CMAIN, CGET, CGETBUTTON, CPOPULAR, CYOUR = range(5)
#dict of tops with links

def start(update: Update, context: CallbackContext) -> int: 
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)

    keyboard = [
        [
            InlineKeyboardButton("Popular themes", callback_data=str(CPOPULAR)),
        ],

        [
            InlineKeyboardButton("Your themes", callback_data=str(CYOUR)),
        ],

        #[
            #InlineKeyboardButton("exit", callback_data=str(CEXIT)),
        #],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Start handler, Choose a route", reply_markup=reply_markup)

    return TYPE

def start_over(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    user = update.callback_query.from_user
    query.answer()
    logger.info("User %s started_over the conversation.", user.first_name)

    keyboard = [
        [
            InlineKeyboardButton("Popular themes", callback_data=str(CPOPULAR)),
        ],

        [
            InlineKeyboardButton("Your themes", callback_data=str(CYOUR)),
        ],

        #[
            #InlineKeyboardButton("exit", callback_data=str(CEXIT)),
        #],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text("Hi, choose one.", reply_markup=reply_markup)

    return TYPE


def get(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    user = update.message.from_user

    logger.info("User %s in get func, got text: %s", user.first_name, text)

    reply_keyboard = [["1", "2", "3"]]

    tops = get_topics(text)
    text = "choose one of this topics:\n1)" + \
    get_href(tops[0]) + "\n2)" + get_href(tops[1]) + "\n3)" + get_href(tops[2])


    logger.info("text = %s", text)

    keyboard = [
        [
            InlineKeyboardButton("back", callback_data=str(CGET)),
        ],

        #[
            #InlineKeyboardButton("exit", callback_data=str(CEXIT)),
        #],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML,
    )

    return MAIN

def pre_get_popular(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    user = update.callback_query.from_user
    query.answer()

    logger.info("User %s in pre_get_popular func", user.first_name)

    #reply_keyboard = [["self", "relationships", "data-science"]]
    #reply_keyboard = [["s", "r", "d"]]
    themes = get_themes()
    keyboard = []
    for i in range(3):
        keyboard.append([
                InlineKeyboardButton(get_name(themes[i]), callback_data=str(get_tag(themes[i]))),
            ])

    keyboard.append(
        [
            InlineKeyboardButton("back", callback_data=str(CMAIN)),
        ],
    )

#    update.message.reply_text(
#        reply_markup=ReplyKeyboardMarkup(
#            reply_keyboard, 
#            one_time_keyboard=True, 
#            input_field_placeholder='Number of topic?',
#        ),
#   )
    reply_markup = InlineKeyboardMarkup(keyboard)
    print("before edit")
    query.edit_message_text(text="Enter theme pls:",
        reply_markup=reply_markup
    )

    return GET

def pre_get_your(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    user = update.callback_query.from_user
    query.answer()

    logger.info("User %s in pre_get_your func", user.first_name)

    #reply_keyboard = [["self", "relationships", "data-science"]]
    #reply_keyboard = [["s", "r", "d"]]
    keyboard = [
        [
            InlineKeyboardButton("self", callback_data=str("self")),
        ],

        [
            InlineKeyboardButton("programming", callback_data="programming"),
        ],

        [
            InlineKeyboardButton("back", callback_data=str(CMAIN)),
        ],
    ]

#    update.message.reply_text(
#        reply_markup=ReplyKeyboardMarkup(
#            reply_keyboard, 
#            one_time_keyboard=True, 
#            input_field_placeholder='Number of topic?',
#        ),
#   )
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text="Enter theme pls:",
        reply_markup=reply_markup
    )

    return GET

def exit_(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    user = update.callback_query.from_user
    query.answer()

    logger.info("User %s in exit func", user.first_name)

    return MAIN

def themes_buttons(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    user = update.callback_query.from_user
    query.answer()

    logger.info("User %s in themes_buttons func", user.first_name)

def show_tops(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    user = update.callback_query.from_user
    query.answer()

    logger.info("User %s in tops func, data is %s", user.first_name, query.data)

    tops = get_topics(query.data)
    text = "choose one of this topics:\n1)" + \
    get_href(tops[0]) + "\n2)" + get_href(tops[1]) + "\n3)" + get_href(tops[2])

    keyboard = [
        [
            InlineKeyboardButton("back", callback_data=str(CPOPULAR)),
        ],

        #[
            #InlineKeyboardButton("exit", callback_data=str(CEXIT)),
        #],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup,
    )

    return TYPE


def main():
    updater = Updater(TG_TOKEN)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", start)],
            states={
                MAIN: [
                        CallbackQueryHandler(start_over, pattern='^' + str(CMAIN) + '$'),
                        #CallbackQueryHandler(exit_, pattern='^' + str(CEXIT) + '$'),
                    ],
                GET: [
                        MessageHandler(
                            Filters.text & ~(Filters.command | Filters.regex('^Done$')), 
                            get,
                        ),
                        CallbackQueryHandler(start_over, pattern='^' + str(CMAIN) + '$'),
                        #CallbackQueryHandler(themes_buttons, pattern='^' + str(CGETBUTTON) + '$'),
                        #CallbackQueryHandler(self_, pattern='^' + str(CSELF) + '$'),
                        CallbackQueryHandler(show_tops),
                    ],
                TYPE: [
                        CallbackQueryHandler(pre_get_popular, pattern='^' + str(CPOPULAR) + '$'),
                        CallbackQueryHandler(pre_get_your, pattern='^' + str(CYOUR) + '$'),
                    ],
                },
            fallbacks=[CommandHandler("start", start)],
        )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
