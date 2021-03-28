from flask import Flask, render_template, request
app = Flask(__name__)
from my_scripts import df, df_avar, df_rus, clean_query, search_engine, extract_list, letter_contents

FOUND = {}
ALPHABETA_START = "__x__x"

@app.route('/')
@app.route('/main.html')
@app.route('/mainnone.html')
def mainpage():
    return render_template("main.html")

@app.route('/searchresult', methods=['get'])
def search():
    raw_query = str(request.args.get('loc'))
    
    if not raw_query.startswith(ALPHABETA_START):
        query = clean_query(raw_query)
    
        genre = str(request.args.get('genre'))
        fortemplate = search_engine(query, genre)
    else:
        query = raw_query[6:].lower()
        fortemplate = letter_contents(query=query)

    FOUND = fortemplate
    if len(fortemplate) > 0:
        return render_template("searchresult.html", query=query, fortemplate=fortemplate)
    else:
        return render_template("mainnone.html")

@app.route("/word/<word_index>")
def showword(word_index):
    word = df.loc[int(word_index)].to_dict()
    word_link = ', '.join(word['link'])
    return render_template("wordinfo.html", word=word, word_link=word_link)

if __name__ == '__main__':
    import os
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
