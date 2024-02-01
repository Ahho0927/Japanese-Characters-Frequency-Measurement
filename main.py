"""import pykakasi to convert kanji or katakana to hiragana"""
from tqdm import tqdm
from re import sub
from pykakasi import kakasi
kks = kakasi()


HIRAGANA, KATAKANA, ROMAJI = '', '', ''
for decimal_unicode in range(12352, 12447 +1):
    HIRAGANA += chr(decimal_unicode)
for decimal_unicode in range(12448, 12543 +1):
    KATAKANA += chr(decimal_unicode)
for decimal_unicode in range(97, 122 +1):
    ROMAJI += chr(decimal_unicode)

# print(HIRAGANA, KATAKANA, ROMAJI)

print('Loading Datas...')

from datasets import load_dataset

dataset = load_dataset("izumi-lab/llm-japanese-dataset", revision="main")

print('Loading Complete!\n')

conversation = []
i = 0
for data in tqdm(dataset['train'], desc='Extracting Conversations'):
    i += 1
    for sentence in data.values():
        sentence = sub('[^\u3300-\u33ff\ufe30-\ufe4f\uf900-\ufaff\U0002F800-\U0002fa1f\u2e80-\u2eff\u3040-\u309f\u30a0-\u30ff\u4e00-\u9fff\u3400-\u4dbf\U00020000-\U0002a6df\U0002a700-\U0002b73f\U0002b740-\U0002b81f\U0002b820-\U0002ceaf]', '', sentence)
        sentence = sub('・', '', sentence)
        conversation.append(sentence)
    if i > 100000:
        break

print('Extraction Complete!\n')


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


print('Converting into Hiragana...')

# Not only Kanji but also Katakana will be converted into hiragana. (pykakasi)
hiragana_count = {letter: 0 for letter in HIRAGANA}
romaji_count = {letter: 0 for letter in ROMAJI}
for sentence in tqdm(conversation, desc='Converting...'):
    sentence_converted = kks.convert(sentence)
    for word in sentence_converted:
        for letter in word['hira']: # HIRAGANA
            if letter in HIRAGANA:
                hiragana_count[letter] += 1
        for letter in word['hepburn']: # ROMAJI
            if letter in ROMAJI:
                romaji_count[letter] += 1

print('Convertion Complete!\n')


with open('result.txt', 'w+', encoding='utf-8') as f:
    for name in tqdm([hiragana_count, katakana_count, romaji_count, kanji_count], desc='Saving...'):
        i = 0
        for key, value in tqdm(name.items()):
            i += 1
            if i == 5:
                f.write('\n')
                i = 0
            value = str(value) + ' '*(15 - len(str(value)))
            f.write(f'{key} : {value}')
        f.write('\n')

print('Save Complete!')
