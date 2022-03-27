import json
import random
from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from data.forms import RegisterForm, LoginForm
from flask_login import LoginManager, login_user, logout_user, login_required
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(id)


@app.route("/")
def index():
    with open("static/txt/about.txt", "r", encoding="utf-8") as about:
        data_about = about.read()
    with open("static/txt/terms.txt", "r", encoding="utf-8") as terms:
        data_terms = terms.readlines()
    data_terms = list(map(lambda x: x.rstrip(), data_terms))
    session = db_session.create_session()
    return render_template("main.html", title='Главная', about=data_about, terms=data_terms)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            print('1')
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.confirm.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.login.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.login.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        print(0)
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/prediction/<pred_type>')
def prediction(pred_type):
    if pred_type == 'choice':
        pred_type = None
        return render_template("prediction.html", title="Расклад", type=pred_type)
    elif pred_type == 'cards':
        with open('static/json/all_cards.json', encoding='utf-8') as file:
            data = json.load(file)
            cards = random.sample(list(data["Карты игральные"]), 2)
        new_cards = []
        for i in cards:
            new_cards.append((i, data["Карты игральные"][i]["описание"], data["Карты игральные"][i]["изображение"]))
        return render_template("prediction.html", title='Гадание на игральных картах',
                               type=pred_type, cards=new_cards)
    elif pred_type == 'tarot':
        with open("static/txt/taro.txt", "r", encoding="utf-8") as cards:
            data_cards = cards.readlines()
            new_cards = random.sample(data_cards, k=3)
            for num, card in enumerate(new_cards):
                new_cards[num] = card.replace('\n', '')
            return render_template("prediction.html", title='Гадание на Таро',
                                   type=pred_type, cards=new_cards)
    elif pred_type == 'special':
        return render_template("prediction.html", title="Специалисты", type=pred_type)


def main():
    name_db = 'webproject.db'
    db_session.global_init(f"db/{name_db}")
    app.run(port=5000)


if __name__ == '__main__':
    main()