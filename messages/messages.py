import configparser

language_path = configparser.ConfigParser(allow_no_value=True, delimiters=('=',))

current_language = "EN"
path_language = {
    "RU": "messages/messages_ru.properties",
    "EN": "messages/messages_en.properties",
}


def getLanguagePath(language: str):
    return path_language[current_language]


def setLanguage(value):
    global current_language
    if value in path_language.keys():
        current_language = value
    else:
        raise ValueError()


def getLanguage():
    return current_language


def message(text: str, key) -> str:
    language_path.read(getLanguagePath(current_language), encoding='utf-8')
    return str(language_path[key][text])


def message(text: str, key, *args) -> str:
    language_path.read(getLanguagePath(current_language), encoding='utf-8')
    return str(language_path[key][text]).format(*args)
