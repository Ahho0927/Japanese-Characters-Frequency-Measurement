"""import pykakasi to convert kanji or katakana to hiragana"""
from re import sub
from tqdm import tqdm
from os import system
import inspect

from datasets import load_dataset
from pykakasi import kakasi
kks = kakasi()

def retrieve_name(var) -> str:
    """A function that returns name of variable in string.
    """
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var][0]

HIRAGANA, KATAKANA, ROMAJI = '', '', ''
for decimal_unicode in range(12352, 12447 +1):
    HIRAGANA += chr(decimal_unicode)
for decimal_unicode in range(12448, 12543 +1):
    KATAKANA += chr(decimal_unicode)
for decimal_unicode in range(97, 122 +1):
    ROMAJI += chr(decimal_unicode)

# print(HIRAGANA, KATAKANA, ROMAJI)

# ====================================================
system('cls')

print('Loading Datas...')

try:
    with open('data.txt', 'r', encoding='utf-8') as f:
        conversation = f.readlines()

except FileNotFoundError:
    dataset = load_dataset("izumi-lab/llm-japanese-dataset", revision="main")

    conversation = []
    for data in tqdm(dataset['train'], desc='Extracting Conversations'):
        for sentence in data.values():
            sentence = sub('[^\u3300-\u33ff\ufe30-\ufe4f\uf900-\ufaff\U0002F800-\U0002fa1f\u2e80-\u2eff\u3040-\u309f\u30a0-\u30ff\u4e00-\u9fff\u3400-\u4dbf\U00020000-\U0002a6df\U0002a700-\U0002b73f\U0002b740-\U0002b81f\U0002b820-\U0002ceaf]', '', sentence)
            sentence = sub('・', '', sentence)
            conversation.append(sentence)

print('Loading Complete!\n')


# Because the Kanji has so many characters including many unsual ones,
# kanji_count stores only used characters in dataset.
kanji_count = {}
for sentence in tqdm(conversation, desc='Counting Kanji'):
    sentence = sub('[^\u3300-\u33ff\ufe30-\ufe4f\uf900-\ufaff\U0002F800-\U0002fa1f\u2e80-\u2eff\u4e00-\u9fff\u3400-\u4dbf\U00020000-\U0002a6df\U0002a700-\U0002b73f\U0002b740-\U0002b81f\U0002b820-\U0002ceaf]', '', sentence)
    for letter in sentence:
        try:
            kanji_count[letter] += 1
        except KeyError:
            kanji_count[letter] = 1

katakana_count = {letter: 0 for letter in KATAKANA}
for sentence in tqdm(conversation, desc='Counting Katakana'):
    sentence = sub('[^\u30a0-\u30ff]', '', sentence)
    for letter in sentence:
        katakana_count[letter] += 1

print('Count Complete!\n')


print('Converting into Hiragana and Counting...')

# Not only Kanji but also Katakana will be converted into hiragana. (pykakasi)
hiragana_count = {letter: 0 for letter in HIRAGANA}
romaji_count = {letter: 0 for letter in ROMAJI}
for sentence in tqdm(conversation, desc='In Proccess...'):
    sentence_converted = kks.convert(sentence)
    for word in sentence_converted:
        for letter in word['hira']: # HIRAGANA
            if letter in HIRAGANA:
                hiragana_count[letter] += 1
        for letter in word['hepburn']: # ROMAJI
            if letter in ROMAJI:
                romaji_count[letter] += 1

print('Convertion Complete!\n')


with open('results/result_hiragana.txt', 'w+', encoding='utf-8') as f:
    for _ in range(2):
        i = 0
        for key, value in tqdm(hiragana_count.items(), desc='Saving result_hiragana.txt'):
            if i == 5:
                f.write('\n')
                i = 0
            i += 1

            value = str(value) + ' '*(15 - len(str(value)))
            f.write(f'{key} : {value}')
        f.write('\n\n')

        hiragana_count = dict(sorted(hiragana_count.items(), key=lambda x:x[1], reverse=True))

    f.write(f'あ段 : {hiragana_count['あ'] + hiragana_count['か'] + hiragana_count['が'] + hiragana_count['さ'] + hiragana_count['ざ'] + hiragana_count['た'] + hiragana_count['だ'] + hiragana_count['な'] + hiragana_count['は'] + hiragana_count['ば'] + hiragana_count['ぱ'] + hiragana_count['ま'] + hiragana_count['や'] + hiragana_count['ら'] + hiragana_count['わ']}\n')
    f.write(f'い段 : {hiragana_count['い'] + hiragana_count['き'] + hiragana_count['ぎ'] + hiragana_count['し'] + hiragana_count['じ'] + hiragana_count['ち'] + hiragana_count['ぢ'] + hiragana_count['に'] + hiragana_count['ひ'] + hiragana_count['び'] + hiragana_count['ぴ'] + hiragana_count['み'] +                        hiragana_count['り']}\n')
    f.write(f'う段 : {hiragana_count['う'] + hiragana_count['く'] + hiragana_count['ぐ'] + hiragana_count['す'] + hiragana_count['ず'] + hiragana_count['つ'] + hiragana_count['づ'] + hiragana_count['ぬ'] + hiragana_count['ふ'] + hiragana_count['ぶ'] + hiragana_count['ぷ'] + hiragana_count['む'] + hiragana_count['ゆ'] + hiragana_count['る']}\n')
    f.write(f'え段 : {hiragana_count['え'] + hiragana_count['け'] + hiragana_count['げ'] + hiragana_count['せ'] + hiragana_count['ぜ'] + hiragana_count['て'] + hiragana_count['で'] + hiragana_count['ね'] + hiragana_count['へ'] + hiragana_count['べ'] + hiragana_count['ぺ'] + hiragana_count['め'] +                        hiragana_count['れ']}\n')
    f.write(f'お段 : {hiragana_count['お'] + hiragana_count['こ'] + hiragana_count['ご'] + hiragana_count['そ'] + hiragana_count['ぞ'] + hiragana_count['と'] + hiragana_count['ど'] + hiragana_count['の'] + hiragana_count['ほ'] + hiragana_count['ぼ'] + hiragana_count['ぽ'] + hiragana_count['も'] + hiragana_count['よ'] + hiragana_count['ろ'] + hiragana_count['を']}\n')
    f.write('\n')
    f.write(f'あ行 : {hiragana_count['あ'] + hiragana_count['い'] + hiragana_count['う'] + hiragana_count['え'] + hiragana_count['お']}\n')
    f.write(f'か行 : {hiragana_count['あ'] + hiragana_count['き'] + hiragana_count['く'] + hiragana_count['け'] + hiragana_count['こ']}\n')
    f.write(f'が行 : {hiragana_count['あ'] + hiragana_count['ぎ'] + hiragana_count['ぐ'] + hiragana_count['げ'] + hiragana_count['ご']}\n')
    f.write(f'さ行 : {hiragana_count['あ'] + hiragana_count['し'] + hiragana_count['す'] + hiragana_count['せ'] + hiragana_count['そ']}\n')
    f.write(f'ざ行 : {hiragana_count['あ'] + hiragana_count['じ'] + hiragana_count['ず'] + hiragana_count['ぜ'] + hiragana_count['ぞ']}\n')
    f.write(f'た行 : {hiragana_count['あ'] + hiragana_count['ち'] + hiragana_count['つ'] + hiragana_count['て'] + hiragana_count['と']}\n')
    f.write(f'だ行 : {hiragana_count['あ'] + hiragana_count['ぢ'] + hiragana_count['づ'] + hiragana_count['で'] + hiragana_count['ど']}\n')
    f.write(f'な行 : {hiragana_count['あ'] + hiragana_count['に'] + hiragana_count['ぬ'] + hiragana_count['ね'] + hiragana_count['の']}\n')
    f.write(f'は行 : {hiragana_count['あ'] + hiragana_count['ひ'] + hiragana_count['ふ'] + hiragana_count['へ'] + hiragana_count['ほ']}\n')
    f.write(f'ば行 : {hiragana_count['あ'] + hiragana_count['び'] + hiragana_count['ぶ'] + hiragana_count['べ'] + hiragana_count['ぼ']}\n')
    f.write(f'ぱ行 : {hiragana_count['あ'] + hiragana_count['ぴ'] + hiragana_count['ぷ'] + hiragana_count['ぺ'] + hiragana_count['ぽ']}\n')
    f.write(f'ま行 : {hiragana_count['あ'] + hiragana_count['み'] + hiragana_count['む'] + hiragana_count['め'] + hiragana_count['も']}\n')
    f.write(f'や行 : {hiragana_count['あ'] +                        hiragana_count['ゆ'] +                        hiragana_count['よ']}\n')
    f.write(f'ら行 : {hiragana_count['あ'] + hiragana_count['り'] + hiragana_count['る'] + hiragana_count['れ'] + hiragana_count['ろ']}\n')
    f.write(f'わ行 : {hiragana_count['あ'] +                                                                      hiragana_count['を']}\n')

with open('results/result_katakana.txt', 'w+', encoding='utf-8') as f:
    for _ in range(2):
        i = 0
        for key, value in tqdm(katakana_count.items(), desc='Saving result_katakana.txt'):
            if i == 5:
                f.write('\n')
                i = 0
            i += 1

            value = str(value) + ' '*(15 - len(str(value)))
            f.write(f'{key} : {value}')
        f.write('\n\n')

        katakana_count = dict(sorted(katakana_count.items(), key=lambda x:x[1], reverse=True))


with open('results/result_romaji.txt', 'w+', encoding='utf-8') as f:
    for _ in range(2):
        i = 0
        for key, value in tqdm(romaji_count.items(), desc='Saving result_romaji.txt'):
            if i == 5:
                f.write('\n')
                i = 0
            i += 1

            value = str(value) + ' '*(15 - len(str(value)))
            f.write(f'{key} : {value}')
        f.write('\n\n')

        romaji_count = dict(sorted(romaji_count.items(), key=lambda x:x[1], reverse=True))


with open('results/result_kanji.txt', 'w+', encoding='utf-8') as f:
    kanji_count = dict(sorted(kanji_count.items(), key=lambda x:x[1], reverse= True))
    i = 0
    for key, value in tqdm(kanji_count.items(), desc='Saving result_kanji.txt'):
        if i == 5:
            f.write('\n')
            i = 0
        i += 1

        value = str(value) + ' '*(15 - len(str(value)))
        f.write(f'{key} : {value}')
    f.write('\n')



print('Save Complete!')