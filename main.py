from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def base():
    return render_template('base.html', title='Главная')


@app.route('/index')
def index():
    return "Привет, Яндекс!"


def main():
    app.run(port=5000)


if __name__ == '__main__':
    main()
