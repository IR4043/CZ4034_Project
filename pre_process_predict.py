import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
import pandas as pd
import contractions
import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

nltk.download("stopwords")
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')


def pre_process_df(df):
    pattern = re.compile("[^\x00-\x7F]+")
    df['title'] = df['title'].apply(lambda x: pattern.sub('', str(x)))
    df['reviewDescription'] = df['reviewDescription'].apply(lambda x: pattern.sub('', str(x)))
    df['text'] = df.apply(lambda row: row['title'] + ' ' + row['reviewDescription'], axis=1)
    df.drop(['title', 'reviewDescription'], axis=1, inplace=True)
    df['text_cleaned'] = df['text'].str.lower()
    df['text_cleaned'] = df['text_cleaned'].apply(lambda x: ' '.join([contractions.fix(word) for word in x.split()]))
    df['text_cleaned'] = df['text_cleaned'].replace(
        ':\)|;\)|:-\)|\(-:|:-D|=D|:P|xD|X-p|\^\^|:-*|\^\.\^|\^\-\^|\^\_\^|\,-\)|\)-:|:\'\(|:\(|:-\('
        '|:\S|T\.T|\.\_\.|:<|:-\S|:-<|\*\-\*|:O|=O|=\-O|O\.o|XO|O\_O|:-\@|=/|:/|X\-\(|>\.<|>=\(|D:|=^.^=|0_o,'
        r'', regex=True)

    # remove punctuations
    df['text_cleaned'] = df['text_cleaned'].str.replace(r'[^\w\s]+', '')
    df['text_cleaned'] = df['text_cleaned'].apply(preprocess_text)
    df['text_cleaned'] = df['text_cleaned'].apply(remove_stopwords)
    # tokenize column to prepare lemmatization
    df['text_tokenize'] = df['text_cleaned'].apply(word_tokenize)

    # Lemmatize Tweet
    df['text_lemmatized'] = df['text_tokenize'].apply(nltk.tag.pos_tag)

    df['text_lemmatized'] = df['text_lemmatized'].apply(
        lambda x: [(word, get_wordnet_pos(pos_tag)) for (word, pos_tag) in x])

    # apply NLTK lemmatization
    wnl = WordNetLemmatizer()
    df['text_lemmatized'] = df['text_lemmatized'].apply(lambda x: [wnl.lemmatize(word, tag) for word, tag in x])

    # convert back to strings
    df['text_lemmatized'] = [' '.join(map(str, l)) for l in df['text_lemmatized']]
    df['text'] = df['text_lemmatized']
    df = df.drop(columns=['text_cleaned', 'text_tokenize', 'text_lemmatized'])

    return df


def preprocess_text(text):
    slangs_df = pd.read_csv(r'Slangs.csv')

    # Create a dictionary with slangs as keys and their corresponding text as values
    slangs_dict = {}
    for index, row in slangs_df.iterrows():
        slangs_dict[row['Slang']] = row['Text']
    words = text.split()
    new_words = []
    for word in words:
        if word in slangs_dict:
            new_words.append(slangs_dict[word])
        else:
            new_words.append(word)
    return " ".join(new_words)


def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    filtered_text = []
    for word in text.split():
        if word.lower() not in stop_words:
            filtered_text.append(word.lower())
    return " ".join(filtered_text)


def get_wordnet_pos(treebank_tag):
    """
    Map POS tag to first character used by WordNetLemmatizer
    """
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN  # return NOUN as default


if __name__ == "__main__":
    df = pd.read_csv("2star_reviews_1.csv")
    new_df = pre_process_df(df)
    print(new_df)
