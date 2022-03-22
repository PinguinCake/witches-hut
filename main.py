from flask import Flask, render_template
from data import db_session

app = Flask(__name__)


@app.route('/')
def base():
    return render_template('base.html', title='Главная')


@app.route('/index')
def index():
    return "Привет, Яндекс!"


def main():
    name_db = 'mars_explorer.db'
    db_session.global_init(f"db/{name_db}")
    app.run(port=5000)


if __name__ == '__main__':
    main()
