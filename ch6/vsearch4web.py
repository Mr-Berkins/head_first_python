from flask import Flask, render_template, request, escape
from vsearch import search4letters

app = Flask(__name__)

# added under line nine


def log_request(req: 'flask_request', res: str) -> None:
    with open('vsearch.log', 'a') as log:
        print(req.form, req.remote_addr, req.user_agent, res, file=log, sep="|")

        # Page 264 Adjusting Log Request--
        # print(str(dir(req)), res, file=log)
        # print(req.form, file=log)
        # print(req.remote_addr, file=log)
        # print(req.user_agent, file=log)
        # print(res, file=log)

# @app.route('/')
# def hello() -> str:
#   return 'Hello world from Flask!'


@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your results:'
    results = str(search4letters(phrase, letters))
    log_request(request, results)
    return render_template('results.html',
                           the_title=title,
                           the_phrase=phrase,
                           the_letters=letters,
                           the_results=results,)


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html',
                           the_title='Welcome to search4letters on the web!')


@app.route('/viewlog')
def view_the_log() -> 'html':  # changed from str to html
    contents = []
    with open('vsearch.log') as log:
        for line in log:
            contents.append([])
            for item in line.split('|'):
                contents[-1].append(escape(item))
    titles = ('Form Data', 'Remote_addr', 'user_agent', 'Results')
    return render_template('viewlog.html',
                           the_title='View Log',
                           the_row_titles=titles,
                           the_data=contents,)


# old return str(contents)
# Page 273 old       contents = log.read()
#    return escape(contents)
if __name__ == '__main__':
    app.run(debug=True)
