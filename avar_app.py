from flask import Flask, render_template, request
app = Flask(__name__)
from my_scripts import df, df_avar, df_rus, clean_query, search_engine, extract_list

FOUND = {}

@app.route('/')
def mainpage():
    return render_template("main.html")

@app.route('/searchresult', methods=['get'])
def search():
    query = clean_query(str(request.args.get('loc')))
    
    genre = str(request.args.get('genre'))
    fortemplate = search_engine(query, genre)
    FOUND = fortemplate
    return render_template("searchresult.html", query=query, fortemplate=fortemplate)


@app.route("/word/<word_index>")
def showword(word_index):
    word = df.loc[int(word_index)].to_dict()
    return render_template("wordinfo.html", word=word)

if __name__ == '__main__':
    app.run(debug=True)