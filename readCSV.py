from googletrans import Translator
import pandas as pd
import transliterate as tl
import csv
import re
import timeit

# create translator
translator = Translator()

# read csv file
file = pd.read_csv("processed_test_comments_formatted.csv", encoding="utf-8")

# read message column
comments = file["MESSAGE"]
ID = file["ID"]
likes = file["LIKE_COUNT"]

# csv file fields
fieldnames = ["ID", "LIKE_COUNT", "MESSAGE"]

# list for expected languages and dict for typos
list_langs = ["en", "ka", "ru", "pl", "tr"]
list_ka = {"ბიჩებო": "ბიჭებო",
           "საკარტველო": "საქართველო",
           "საკართველო": "საქართველო",
           "საქარტველო": "საქართველო",
           "კარტული": "ქართული",
           "კართული": "ქართული",
           "ქარტული": "საქართველო",
           "ამაკ": "ამაყ",
           "ცონ": "წონ",
           "გიჯ": "გიჟ",
           "ქხო": "ცხო",
           "არაპერ": "არაფერ",
           "თკვენ": "თქვენ",
           "თამაჩჩ": "თამაშშ",
           "მეთი": "მეტი",
           "დავამათ": "დავამატ",
           "გაიჩედა": "გაიჭედა",
           "ცოთა": "ცოტა",
           "თერმინალ": "ტერმინალ",
           "მოგითხა": "მოგიტყა",
           "ჩაგარა": "ჭაღარა",
           "მთაცმინდა": "მთაწმინდა",
           "ჯველ": "ჭველ"

           }


# detect which language is this
def detect_language(text):
    if len(text.lang) > 1:
        return "hi"
    if text.confidence < 60:
        return "hi"
    return text.lang


# change latin words to georgian words and remove typo
def change_typo(sentence):
    changed = tl.translit(sentence, "ru", reversed=True)
    changed = tl.translit(changed, "ka")

    lst_keys = list(list_ka.keys())
    for i in range(len(list_ka)):
        if changed.find(lst_keys[i]) != -1:
            changed = str.replace(changed, lst_keys[i], list_ka[lst_keys[i]])
    return changed


# change typo for georgian words
def change_typo_georgianOnly(sentence):
    changed = sentence
    lst_keys = list(list_ka.keys())
    for i in range(len(list_ka)):
        if changed.find(lst_keys[i]) != -1:
            changed = str.replace(changed, lst_keys[i], list_ka[lst_keys[i]])
    return changed


def createEnglishCSV():
    # rows to insert into csv file
    rows = []

    for i in range(len(comments)):
        sentence = comments[i]
        curr_id = ID[i]
        curr_like_count = likes[i]

        curr_lang = detect_language(translator.detect(sentence))
        changed = sentence

        if curr_lang not in list_langs:
            changed = change_typo(sentence)

        if curr_lang == "ka":
            changed = change_typo_georgianOnly(sentence)

        # translate
        changed = (translator.translate(changed, "en")).text

        # remove extra smiles
        changed = re.sub(r'[^A-Za-z0-9 ]+', '', changed)

        # + csv
        data = {'ID': curr_id,
                'LIKE_COUNT': curr_like_count,
                'MESSAGE': changed}

        rows.append(data)
        print(data)

    with open('tempCSV.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == '__main__':
    start_time = timeit.default_timer()
    createEnglishCSV()
    print(timeit.default_timer() - start_time)
    pass
