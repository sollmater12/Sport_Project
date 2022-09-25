from flask import Flask, render_template, redirect, request, abort, make_response, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms.user import UserRegisterForm, LoginForm
from forms.coach import CoachRegisterForm
from forms.add_id import AddId
from data import db_session
from data.users import User
from data.coaches import Coach
from data.database_manager import Database

app = Flask("Sport_Project")
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'rest50567'
database_manager = Database()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/")
def index():
    if current_user.is_authenticated:
        return main_page()
    else:
        return render_template('html/authorisation/authorisation.html', title="Приложение")


@app.route('/choose_role')
def choose_role():
    return render_template("html/authorisation/choose_role.html")


@app.route('/register/client', methods=['GET', 'POST'])
def registration_client():
    form = UserRegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('html/authorisation/registration_user.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('html/authorisation/registration_user.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            nickname=form.nickname.data,
            email=form.email.data,
            age=form.age.data,
            country=form.country.data,
            coaches=''
        )
        user.set_password(form.password.data)

        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('html/authorisation/registration_user.html', title='Регистрация', form=form)


@app.route('/register/coach', methods=['GET', 'POST'])
def registration_coach():
    form = CoachRegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('html/authorisation/registration_coach.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('html/authorisation/registration_coach.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            nickname=form.nickname.data,
            email=form.email.data,
            age=form.age.data,
            country=form.country.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()

        coach = Coach(
            id=user.id,
            name=form.name.data,
            surname=form.surname.data,
            nickname=form.nickname.data,
            email=form.email.data,
            age=form.age.data,
            country=form.country.data,
            education=form.education.data,
            achievements=form.achievements.data,
            specialization=form.specialization.data,
            experience=form.experience.data,
            users=''
        )
        coach.set_password(form.password.data)

        db_sess.add(coach)
        db_sess.commit()
        return redirect('/login')
    return render_template('html/authorisation/registration_coach.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/main_page')
        return render_template('html/authorisation/login_user.html', message="Неправильный логин или пароль",
                               form=form)
    return render_template('html/authorisation/login_user.html', title='Авторизация', form=form)


@app.route('/main_page')
@login_required
def main_page():
    db_sess = db_session.create_session()
    check_coach = [db_sess.query(Coach).filter(Coach.id == current_user.id).first().id]
    if current_user.id in check_coach:
        return redirect('/main_page_coach')
    return redirect('/main_page_user')


@app.route('/main_page_user')
@login_required
def main_page_user():
    return render_template('html/main/user/main_page_user.html', title="Главная страница",
                           page_title='Главная страница')


@app.route('/main_page_coach')
@login_required
def main_page_coach():
    return render_template('html/main/coach/main_page_coach.html', title="Главная страница",
                           page_title='Главная страница')


@app.route('/profile_settings_user')
def profile_settings_user():
    return render_template('html/main/user/profile_settings_user.html', title="Настройки профиля",
                           page_title='Настройки профиля')


@app.route('/profile_settings_coach')
def profile_settings_coach():
    return render_template('html/main/coach/profile_settings_coach.html', title="Настройки профиля",
                           page_title='Настройки профиля')


@app.route('/settings_user')
def settings_user():
    return render_template('html/main/user/settings_user.html', title="Настройки", page_title='Настройки')


@app.route('/settings_coach')
def settings_coach():
    return render_template('html/main/coach/settings_coach.html', title="Настройки", page_title='Настройки')


@app.route('/clients', methods=['GET', 'POST'])
def clients():
    clients = database_manager.getClients(current_user.id)
    print(clients)
    addIdForm = AddId()
    if addIdForm.validate_on_submit():
        id = addIdForm.id.data
        if database_manager.checkUserId(id):
            if database_manager.checkUserInCoach(user_id=id, coach_id=current_user.id):
                return render_template('html/main/coach/clients.html', title="Клиенты", page_title='Клиенты',
                                       form=addIdForm, message="", clients=clients)
            return render_template('html/main/coach/clients.html', title="Клиенты", page_title='Клиенты',
                                   form=addIdForm, message="У вас уже добавлен данный пользователь")
        return render_template('html/main/coach/clients.html', title="Клиенты", page_title='Клиенты',
                               form=addIdForm, message="Данного id не существует")
    return render_template('html/main/coach/clients.html', title="Клиенты", page_title='Клиенты', form=addIdForm)


def main():
    db_session.global_init("db/blogs.db")
    app.run()


if __name__ == '__main__':
    main()
