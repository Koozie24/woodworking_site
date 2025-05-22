from flask import Flask, request, render_template
import os

TEMPLATES_DIR = os.path.abspath("../frontend/templates")
STATIC_DIR = os.path.abspath("../frontend/static")
app= Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)

@app.route('/')

def my_form():
    return render_template('cuts.html')

@app.route('/', methods=['POST'])

def my_form_post():
    cut_value = request.form['quantity']
    
    return cut_value

if __name__ == "__main__":
    app.run(debug=True)
    print("post.py is executing")