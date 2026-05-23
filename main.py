from flask import Flask, render_template

app = Flask(__name__, 
    template_folder='templates', 
    static_folder='static',
    static_url_path='/static'
)

@app.route('/')
@app.route('/index')
def public():
    return render_template('public.html')

@app.route('/login')
def login():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/test')
def api_test():
    return {'status': 'ok', 'message': 'API test'}

if __name__ == '__main__':
    app.run(debug=False)
