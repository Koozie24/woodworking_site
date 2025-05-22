from flask import Flask, render_template, request
import os 

app = Flask(__name__)

TEMPLATES_DIR = os.path.abspath("frontend/templates")
STATIC_DIR = os.path.abspath("frontend/static")
app= Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)

#defining routes for html pages in templates
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/cuts')
def cuts():
    return render_template('cuts.html')
@app.route('/identify')
def identify():
    return render_template('identify.html')
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/plans')
def plans():
    return render_template('plans.html')

@app.route('/handle_submit_cut_form', methods=['POST'])
def handle_submit_cut_form():
    kerf_size = request.form.get('kerf-type')
    
    print(kerf_size)
if __name__ == "__main__":
    print("Running Flask server...")
    app.run(debug=True)
