import json
import random
from flask import Flask, render_template, redirect
from extra_files.finder import get_png
from data import db_session
from data.users import User
from data.forms import RegisterForm, LoginForm, RecoveryForm, FinalRecoveryForm
from flask_login import LoginManager, login_user, logout_user, login_required
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
msg = MIMEMultipart()


@login_manager.user_loader
def load_user(id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(id)


@app.route("/")
def index():
    files_to_delete = ['manpupuner.jpg', 'plato_putorana.jpg', 'cave.jpg']
    for file in files_to_delete:
        if os.path.exists(f'static/img/{file}'):
            os.remove(f'static/img/{file}')
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
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/recovery', methods=['GET', 'POST'])
def recovery():
    form = RecoveryForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data, User.name == form.name.data).first()
        if user:
            to_email = 'danielyan0520@gmail.com'
            message = 'hi smth interesting'
            from_email = 'witcheshut@mail.ru'
            password = 'ejtkcTCZXiBBT7dHkLQM'

            msg.attach(MIMEText(message, 'plain'))

            server = smtplib.SMTP('smtp.mail.ru: 25')  # эту часть лучше не трогать
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, to_email, message)
            server.quit()
            return redirect('/frecovery')
    return render_template('recovery.html', title='Восстановление пароля', form=form)


@app.route('/frecovery', methods=['GET', 'POST'])
def frecovery():
    # сообщи, когда полностью доделаешь, я код причешу!
    form = FinalRecoveryForm()
    # if form.validate_on_submit():
    #     db_sess = db_session.create_session()
    #     user = db_sess.query(User).filter(User.email == form.email.data).first()
    #     if user:
    #         form.password.data = User.set_password()
    #     return redirect('/login')
    # return render_template('recovery1.html', title='Восстановление пароля', form=form)


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
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/power_places')
def show_shops():
    coords = [["94.315662%2C68.340233", '6', 'plato_putorana.jpg', 'Плато Путорана (Красноярский край)'],
              ["59.298585%2C62.257436", '15', 'manpupuner.jpg', 'Столбы выветривания (Республика Коми)'],
              ["57.006969%2C57.440527", '16', 'cave.jpg', 'Кунгурская ледяная пещера (Пермский край)']]
    images = []
    for coord in coords:
        img = get_png(*coord[:-1])
        images.append([img, coord[-1]])
    return render_template("power_places.html", title='Магазины', images=images)


@app.route('/prediction/<pred_type>')
def prediction(pred_type):
    if pred_type == 'choice':
        pred_type = None
        return render_template("prediction.html", title="Расклад", type=pred_type)
    elif pred_type == 'cards':
        with open('static/json/all_cards.json', encoding='utf-8') as file:
            data = json.load(file)
            cards = random.sample(list(data["Карты игральные"]), 3)
        new_cards = []
        for i in cards:
            new_cards.append((i, data["Карты игральные"][i]["описание"], data["Карты игральные"][i]["изображение"]))
        return render_template("prediction.html", title='Гадание на игральных картах',
                               type=pred_type, cards=new_cards)
    elif pred_type == 'tarot':
        with open('static/json/all_cards.json', encoding='utf-8') as file:
            data = json.load(file)
            cards = random.sample(list(data["Карты Таро"]), 3)
        new_cards = []
        for i in cards:
            new_cards.append((i, data["Карты Таро"][i]["описание"], data["Карты Таро"][i]["изображение"]))
        return render_template("prediction.html", title='Гадание на Таро',
                               type=pred_type, cards=new_cards)
    elif pred_type == 'special':
        return render_template("prediction.html", title="Специалисты", type=pred_type)


def main():
    name_db = 'webproject.db'
    db_session.global_init(f"db/{name_db}")
    app.run(port=5050)


if __name__ == '__main__':
    main()
