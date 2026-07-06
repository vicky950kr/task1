import sqlite3, random, string
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        short_id = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        db = get_db()
        db.execute('INSERT INTO urls (original_url, short_id) VALUES (?, ?)', (url, short_id))
        db.commit()
        return f"Shortened URL: {request.host_url}{short_id}"
    return render_template('index.html')

@app.route('/<short_id>')
def url_redirect(short_id):
    db = get_db()
    url_data = db.execute('SELECT original_url FROM urls WHERE short_id = ?', (short_id,)).fetchone()
    if url_data:
        return redirect(url_data['original_url'])
    return "URL not found", 404

if __name__ == "__main__":
    app.run(debug=True)