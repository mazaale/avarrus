import re
import pandas as pd

df = pd.read_json("mega_json_3000.json", orient="records")
def firstLetters(list_):
    first_letters = []
    for x in list_:
        x = x.lower().strip('-')
        if re.match("[^кхглтчц]", x):
            first_letters.append(x[0])
        else:
            if re.match('[кхг]', x):
                if x[1] in "iъь":
                    first_letters.append(x[:2])
                else:
                    first_letters.append(x[0])
            elif re.match('[тцч]', x):
                if x[1] == "i":
                    first_letters.append(x[:2])
                else:
                    first_letters.append(x[0])
            else:
                if x[1] == "ъ":
                    first_letters.append(x[:2])
                else:
                    first_letters.append(x[0])
    return(first_letters)

df['first_letters'] = firstLetters(df['base'].to_list())
df['index'] = df.index
df_rus = pd.read_json('df_rus.json', orient='index')
df_avar = pd.read_json('df_avar.json', orient='index')

def clean_query(query):
    query = re.sub('[1\|l]', 'I', query)
    query = re.sub('[^Iа-яА-Я\- ]', "", query).strip()
    return query.lower()

def search_engine(query, genre):
    if genre == "avarrus":
        df_sub = df_avar
    else:
        df_sub = df_rus

    ix_list = df_sub.loc[df_sub['word'] == query, 'big_ix'].to_list()
    fortemplate = df.loc[ix_list].to_dict(orient='records')
    return fortemplate

def extract_list(records, column):
    return [x[column] for x in records]