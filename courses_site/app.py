from flask import Flask, render_template, request, redirect, url_for
from database import get_db_connection, log_interaction

app = Flask(__name__, static_folder='static', static_url_path='/static')

# Главная страница (рекомендации для пользователя)
@app.route('/')
def index():
    user_id = 1  # Пока берём первого пользователя (позже добавим авторизацию)
    
    # Получаем курсы из БД (пока все, потом добавим рекомендации)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses ORDER BY RANDOM() LIMIT 10;")
    courses = cursor.fetchall()
    cursor.close()
    conn.close()
    

    return render_template('index.html', courses=courses)

# Обработка клика по курсу (запись в interactions)
@app.route('/course/<int:course_id>')
def course_click(course_id):
    user_id = 1  # Пока берём первого пользователя
    log_interaction(user_id, course_id)  # Записываем взаимодействие
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT link FROM courses WHERE course_id = %s;", (course_id,))
    course_link = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return redirect(course_link)  # Перенаправляем на курс

if __name__ == '__main__':
    app.run(debug=True)