import csv

from config import app_config


'''
On recupere le CSV de trad sous la forme 
"key;francais;english"
on le transforme en super dico :

{
'KEY_1': {'francais': 'bla1',
              'english': 'blah1'},
    'KEY_2': {'francais': 'bla2',
              'english': 'blah2'}
}

'''


class Texts:
    available_languages = set()
    trad_dict = {}
    chosen_language = ''

    def __init__(self, language='francais'):
        Texts.available_languages, Texts.trad_dict = Texts.set_language_and_trad_dict_from_csv(
            app_config.DATA_DIRECTORY + app_config.LOCALIZATION_FILE
        )

        if language and language in Texts.available_languages:
            Texts.chosen_language = language
        else:
            Texts.chosen_language = Texts.get_default_language()

        print(f'chosen language : {Texts.chosen_language}')
        print(f'trad dict : {Texts.trad_dict}')
        print(f'test : get NO_LANDMARK_THERE : {Texts.get_text("NO_LANDMARK_THERE")}')

    @staticmethod
    def get_default_language():
        languages = list(Texts.available_languages)
        if len(languages) > 0:
            return languages[0]
        else:
            raise NotImplementedError

    @staticmethod
    def get_available_languages():
        return Texts.available_languages

    @staticmethod
    def set_language(language):
        if language in list(Texts.get_available_languages()):
            Texts.chosen_language = language
        else:
            print('Language not available')

    @staticmethod
    def get_text(key):
        try:
            return Texts.trad_dict.get(key).get(Texts.chosen_language)
        except:
            return key

    @staticmethod
    def set_language_and_trad_dict_from_csv(path):
        with open(path, 'r', encoding='utf-8') as csv_file:
            trad_dict = csv.reader(csv_file, delimiter=';')
            header = next(trad_dict)

            available_languages = set()
            full_trad_dict = {}

            for row in trad_dict:
                if row:
                    trad_key = ''
                    row_dict = {}
                    for category, content in zip(header, row):
                        if category:
                            if category == 'key':
                                trad_key = content
                                # print('key is ', translation)
                            else:
                                available_languages.add(category)
                                row_dict.update({category: content})
                        full_trad_dict.update({trad_key: row_dict})

        return available_languages, full_trad_dict


# Creation au lancement de l'application.
Texts()
