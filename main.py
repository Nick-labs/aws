import os
import datetime

from flask import Flask, render_template, redirect
from data import db_session

from data.users import User
from data.news import News
from data.jobs import Jobs

from forms.user import RegisterForm
from waitress import serve

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def add_users(db):
    db_sess = db

    user = User()
    user.name = "Ridley"
    user.surname = "Scott"
    user.age = 21
    user.position = "captain"
    user.speciality = "research engineer"
    user.address = "module_1"
    user.email = "scott_chief@mars.org"
    db_sess.add(user)

    user2 = User()
    user2.name = "Ilon"
    user2.surname = "DontMask"
    user2.age = 45
    user2.position = "sailor"
    user2.speciality = "engineer"
    user2.address = "module_1"
    user2.email = "ilon_mars@mars.org"
    db_sess.add(user2)

    user3 = User()
    user3.name = "NoName"
    user3.surname = "NoName"
    user3.age = 19
    user3.position = "sailor"
    user3.speciality = "No"
    user3.address = "module_2"
    user3.email = "NoName@mars.org"
    db_sess.add(user3)

    user4 = User()
    user4.name = "Saimon"
    user4.surname = "Romanov"
    user4.age = 16
    user4.position = "chief assistant"
    user4.speciality = "robotics engineer"
    user4.address = "module_1"
    user4.email = "mars_bez_putina@mars.org"
    db_sess.add(user4)

    user5 = User()
    user5.name = "404"
    user5.surname = "404"
    user5.age = 404
    user5.position = "sailor"
    user5.speciality = "kettle"
    user5.address = "module_3"
    user5.email = "404_kettle@mars.org"
    db_sess.add(user5)

    db_sess.commit()


def add_jobs(db):
    db_sess = db
    """team_leader 1
job deployment of residential modules 1 and 2
work_size 15
collaborators 2, 3
start_date (now)
is_finished False"""
    jobs = Jobs()
    jobs.team_leader = 1
    jobs.job = "deployment of residential modules 1 and 2"
    jobs.work_size = 15
    jobs.collaborators = "2, 3"
    jobs.start_date = datetime.datetime.now()
    jobs.is_finished = False
    db_sess.add(jobs)

    db_sess.commit()


def add_news(db):
    db_sess = db

    news = News(title="Первая новость", content="Привет блог!",
                user_id=1, is_private=False)
    db_sess.add(news)

    user = db_sess.query(User).filter(User.id == 1).first()
    news2 = News(title="Вторая новость", content="Уже вторая запись!",
                 user=user, is_private=False)
    db_sess.add(news2)

    user2 = db_sess.query(User).filter(User.id == 1).first()
    news3 = News(title="Личная запись", content="Эта запись личная",
                 is_private=False)
    user2.news.append(news3)

    db_sess.commit()


@app.route("/")
@app.route("/index")
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index.html", news=news)


@app.route("/t")
@app.route("/jobs")
def table_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs)
    return render_template("table_jobs.html", jobs=jobs)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


def main():
    db_session.global_init("db/blogs.sqlite")
    db_sess = db_session.create_session()

    # add_users(db_sess)
    # add_jobs(db_sess)
    # add_news(db_sess)

    #
    # user = User()
    # user.name = "Пользователь 1"
    # user.about = "биография пользователя 1"
    # user.email = "email@email.ru"
    # db_sess.add(user)

    #
    # db_sess.commit()
    #
    # user = db_sess.query(User).first()
    # print(user.name)
    app.run(port=8888, host='127.0.0.1')

    # port = int(os.environ.get('PORT', 5000))
    # # app.run(port=port, host="0.0.0.0")
    #
    # # с дефаултными значениями будет не более 4 потов
    # serve(app, port=port, host="0.0.0.0")


if __name__ == '__main__':
    main()

"""git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/Dragonfly774/flask_alch.git
git push -u origin main"""
