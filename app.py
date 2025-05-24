from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from sqlalchemy.orm import joinedload
import random



app = Flask(__name__)
app.secret_key = 'uY83$8g&lmQ1#9!sKpV0zB'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newflask.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Authors = db.Column(db.String(100), nullable=False)
    Summary = db.Column(db.Text, nullable=False)
    Rating = db.Column(db.Float, nullable=False)
    Learners = db.Column(db.Float, nullable=False)
    Picture = db.Column(db.Text, nullable=False)
    Link = db.Column(db.Text, nullable=False)
    Category = db.Column(db.String(100), nullable=False)


class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    birthdate = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    preference = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Recommends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    post = db.relationship('Post', backref='recommends', lazy=True)

class Click(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class View(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    rating = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route('/index')
@app.route('/')
@login_required
def index():


    recommendses = Recommends.query.options(joinedload(Recommends.post)).filter_by(user_id=current_user.id).all()
    recommends = random.sample(recommendses, min(len(recommendses), 6))  # выберет максимум 6 случайных

    posts = Post.query.order_by(Post.Learners.desc()).limit(6).all()

    clicks = Click.query.filter_by(user_id=current_user.id).all()
    post_ids = [click.post_id for click in clicks]

    # Получаем объекты Post по этим ID
    clicked_posts = Post.query.filter(Post.id.in_(post_ids)).all()

    return render_template('index.html', posts=posts, recommends=recommends, clicked_posts=clicked_posts)


# Страница входа
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = Users.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Успешный вход!', 'success')
            return redirect('/')
        else:
            flash('Неверное имя пользователя или пароль', 'danger')
            return render_template('login.html')

    return render_template('login.html')

# Выход
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаунта', 'info')
    return redirect('/login')

# Персонализированная страница после входа
@app.route('/dashboard')
@login_required
def dashboard():
    views = View.query.filter_by(user_id=current_user.id).all()
    view_ids = [view.post_id for view in views]

    # Получаем объекты Post по этим ID
    view_posts = Post.query.filter(Post.id.in_(view_ids)).all()

    return render_template('dashboard.html', user=current_user, view_posts=view_posts)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        birthdate_str = request.form['birthdate']
        gender = request.form['gender']
        preference = request.form['preference']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Проверка совпадения паролей
        if password != confirm_password:
            flash('Пароли не совпадают', 'danger')
            return render_template('registration.html')

        # Проверка на существующего пользователя
        if Users.query.filter_by(username=username).first() or Users.query.filter_by(email=email).first():
            flash('Пользователь с таким никнеймом или почтой уже существует', 'danger')
            return render_template('registration.html')

        # Преобразование даты
        try:
            birthdate = datetime.strptime(birthdate_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Неверный формат даты', 'danger')
            return render_template('registration.html')

        # Создание нового пользователя
        new_user = Users(
            username=username,
            email=email,
            birthdate=birthdate,
            gender=gender,
            preference=preference
        )
        new_user.set_password(password)

        try:
            # Сохраняем нового пользователя в базу данных
            db.session.add(new_user)
            db.session.commit()

            # Получаем курсы по категории, совпадающей с предпочтением пользователя
            matching_courses = Post.query.filter_by(Category=preference).all()

            # Создаём рекомендации для пользователя
            for course in matching_courses:
                recommendation = Recommends(user_id=new_user.id, post_id=course.id)
                db.session.add(recommendation)

            # Сохраняем рекомендации
            db.session.commit()

            # Успешная регистрация — входим в систему
            flash('Регистрация прошла успешно!', 'success')
            login_user(new_user)
            return redirect('/')

        except Exception as e:
            db.session.rollback()
            flash('Ошибка при сохранении пользователя', 'danger')
            print("Ошибка при сохранении пользователя:", e)
            return render_template('registration.html')

    return render_template('registration.html')




@app.route('/zapolneniye', methods=['POST', 'GET'])
def zapolneniye():
    if request.method == 'POST':
        name = request.form['name']

        authors = request.form['authors']
        summary = request.form['summary']
        rating = request.form['rating']
        learners = request.form['learner']
        picture = request.form['picture']
        link = request.form['link']
        category = request.form['category']

        post = Post(
            Name=name,
            Authors=authors,
            Summary=summary,
            Rating=rating,
            Learners=learners,
            Picture=picture,
            Link=link,
            Category=category)
        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/')

        except:
            return 'Ошибка!'

    else:
        return render_template('zapolneniye.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.route('/go_rec/<int:course_id>')
@login_required
def go_to_course_rec(course_id):
    course = Post.query.get(course_id)
    if not course:
        return redirect(course.Link)

    user_id = current_user.id

    # Проверка на существование записи в Click или View
    click_exists = Click.query.filter_by(user_id=user_id, post_id=course_id).first()
    view_exists = View.query.filter_by(user_id=user_id, post_id=course_id).first()

    if not click_exists and not view_exists:
        new_click = Click(user_id=user_id, post_id=course_id, timestamp=datetime.utcnow())
        db.session.add(new_click)
        db.session.commit()

    return redirect(course.Link)


@app.route('/go/<int:course_id>')
@login_required
def go_to_course(course_id):
    course = Post.query.get(course_id)
    if not course:
        return redirect(course.Link)

    user_id = current_user.id

    # Проверка на существование записи в Click или View
    click_exists = Click.query.filter_by(user_id=user_id, post_id=course_id).first()
    view_exists = View.query.filter_by(user_id=user_id, post_id=course_id).first()

    if not click_exists and not view_exists:
        new_click = Click(user_id=user_id, post_id=course_id, timestamp=datetime.utcnow())
        db.session.add(new_click)
        db.session.commit()

    return redirect(course.Link)


@app.route('/click/remove/<int:post_id>', methods=['POST'])
@login_required
def remove_click(post_id):
    click = Click.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    if click:
        db.session.delete(click)
        db.session.commit()
    return '', 204

@app.route('/view/save/<int:post_id>', methods=['POST'])
@login_required
def save_view(post_id):
    data = request.get_json()
    rating = data.get('rating')

    if rating not in [-1, 1]:
        return 'Invalid rating', 400

    click = Click.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    if click:
        view = View(
            user_id=current_user.id,
            post_id=post_id,
            rating=True if rating == 1 else False  # Boolean field
        )
        db.session.add(view)
        db.session.delete(click)
        db.session.commit()

    return '', 204


@app.route('/search')
def search():
    query = request.args.get('q', '')
    if query:
        results = Post.query.filter(Post.Summary.ilike(f'%{query}%')).all()
    else:
        results = []

    return render_template('search_results.html', query=query, results=results)




if __name__ == '__main__':
    app.run(debug = True)
