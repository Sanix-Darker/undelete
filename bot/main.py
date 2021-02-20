from bot.utils import (
    start_handler,
    help_handler,
    echo_handler,
    presentation,
    dispatcher,
    updater
)


if __name__ == "__main__":
    presentation()

    # dispatchers...
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(echo_handler)

    # updater
    updater.start_polling()
    updater.idle()
