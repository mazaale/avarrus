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

clitics_end = [
    'ги',
    'гури',
    'гъун',
    'гIаги',
    'гIан',
    'гIанаб',
    'гIанав',
    'гIанай',
    'гIанасеб',
    'гIанасев',
    'гIанасей',
    'духъ',
    'ккун',
    'кьераб',
    'лъила',
    'махIаб',
    'ни',
    'ниги',
    'тIалаяб',
    'уна',
    'хун',
    'хIа',
    'хIалаб',
    'цибилаб',
    'цин',
    'чи',
    'щинаб'
]
clitics_beg = [
    'балугъ',
    'гьин',
    'гIада',
    'нахъ'
]

def clean_query(query):
    query = re.sub('[1\|l]', 'I', query)
    query = re.sub('[^Iа-яА-Я\- ]', "", query).strip()
    return query.lower().replace("i", "I")

def search_engine(query, genre):
    if genre == "avarrus":
        df_sub = df_avar
    else:
        df_sub = df_rus

    query_list = []
    if query in clitics_beg or query in clitics_end:
        query_list = [query]
    else:
        query_list = [query]
        for c_end in clitics_end:
            if query.endswith(c_end):
                query_list.append(query[:-len(c_end)])
                query_list.append(c_end)
        for c_beg in clitics_beg:
            if query.startswith(c_beg):
                query_list.append(query[len(c_beg):])
                query_list.append(c_beg)

    ix_list = []
    for query in query_list:
        ix_list.extend(df_sub.loc[df_sub['word'] == query, 'big_ix'].to_list())
    fortemplate = df.loc[ix_list].to_dict(orient='records')
    
    return fortemplate

def letter_contents(query):
    return df.loc[df['first_letters'] == query].to_dict(orient='records')

def extract_list(records, column):
    return [x[column] for x in records]