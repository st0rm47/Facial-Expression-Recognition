from flask import Flask, request, render_template, session, redirect

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/static')   

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/demo')
def demo():
    return render_template('demo.html')

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000, debug = True)
    