from flask import Flask, render_template, request, redirect, url_for, session  # type: ignore
from flask_sqlalchemy import SQLAlchemy  # type: ignore

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer, nullable=False)

# Veritabanı olusutrma islemi
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    # Ortalama puani hesaplama yeri , sorun duzeltildi
    total_score = db.session.query(db.func.sum(User.score)).scalar()
    total_users = db.session.query(db.func.count(User.id)).scalar()
    highscore = total_score / total_users if total_users > 0 else 0  # Sıfıra bölme hatasından kaçınma

    if request.method == 'POST':
        username = request.form['username']
        score = calculate_score(request.form)
        session['username'] = username
        session['score'] = score

        user = User.query.filter_by(username=username).first()
        if user:
            user.score = max(user.score, score)
        else:
            user = User(username=username, score=score)
            db.session.add(user)
        db.session.commit()

        return redirect(url_for('result'))

    return render_template('quiz.html', highscore=highscore)

@app.route('/result')  
def result():
    username = session.get('username')
    score = session.get('score')
    user = User.query.filter_by(username=username).first()

    #ortalama ile hesaplatildi
    total_score = db.session.query(db.func.sum(User.score)).scalar()  
    total_users = db.session.query(db.func.count(User.id)).scalar()  
    highscore = total_score / total_users if total_users > 0 else 0  

    return render_template('result.html', score=score, highscore=highscore, user_highscore=user.score)

def calculate_score(form):
    
    score = 0
    if form.get('question1') == 'Olayı dinleyip yanıt vererek':
        score += 16
    if form.get('question2') == 'discord()':
        score += 16
    if form.get('question3') == 'OpenCV':
        score += 16
    if form.get('question4') == 'BeautifulSoup':
        score += 16
    if form.get('question5') == 'TensorFlow':
        score += 16
    if form.get('question6') == 'Web uygulamaları geliştirmek için':
        score += 20
    return score

if __name__ == '__main__':
    app.run(debug=True)

#kolay ama bilgiyi sğlam isteyen bir bolumdu





