from phonemizer import phonemize
from phonemizer.separator import Separator

def convert_to_phonemes(text):
    # 将文本按空格分割成单词列表
    words = text.split()

    # 遍历单词列表，将除了 [sep] 之外的其他内容转换为音节
    converted_words = []
    for word in words:
        if word != '[sep]':
            # 对非 [sep] 单词进行音节转换
            phonemes = phonemize(
                word,
                language='en-us',
                backend='festival',
                separator=Separator(phone='_', word=' ', syllable=' @@'),
                strip=True,
                preserve_punctuation=True,
                njobs=4
            )
            converted_words.append(phonemes)
        else:
            # 将 [sep] 添加到转换后的单词列表
            converted_words.append('[sep]')

    # 将转换后的单词列表重新组合成文本
    converted_text = ' '.join(converted_words)
    return converted_text

# 使用示例
# text = 'forever trusting we [sep] and else matters [sep] never open myself this way [sep] life is ours we live it our way [sep] this words i just [sep] and nothing else matters [sep] trust i seek and i find in [sep] every day for a [sep] open mind for [sep] and else [sep] never cared for they [sep] never cared for what they know [sep] but i [sep] so close no matter how far [sep]'
# converted_text = convert_to_phonemes(text)
# print(converted_text)