print("test.py is executing...")

from flask import Flask, render_template
import os 

print("Flask imported successfully...")

app = Flask(__name__)

TEMPLATES_DIR = os.path.abspath("frontend/templates")
STATIC_DIR = os.path.abspath("frontend/static")
app= Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)

print("templates_dir: ", TEMPLATES_DIR)

@app.route('/')
def home():
    return render_template('index.html')



if __name__ == "__main__":
    print("Running Flask server...")
    app.run(debug=True)
