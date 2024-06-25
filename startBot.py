from config.bot import application
from telegram import Update

def main() -> None:
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

