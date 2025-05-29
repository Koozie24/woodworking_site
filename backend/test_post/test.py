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

#helper function to take inputs from cut optimizer form and form board and cut dimensions. returns a list of lists. Each sublist is a dimension in L x W x H.
def form_board_dimensions(whole_len, whole_width, whole_height, frac_len, frac_width, frac_height, cut=False, quantity=0):
    n = len(whole_len) #get number of boards input by user
    board_list = [] #init empty container
    
    for i in range(n): #iterate over number of boards input
        length = float(whole_len[i]) + float(frac_len[i]) #conjoin fraction + whole number for each dimension
        width = float(whole_width[i]) + float(frac_width[i])
        height = float(whole_height[i]) + float(frac_height[i])
        if(cut == False): #default argument for stock dimensions
            current = [length, width, height] #initialize as a list
        else: #otherwise cut dimensions
            current = [int(quantity[i]), length, width, height] #initialize as a list
        
        board_list.append(current) #append to list of lists.
        
    return board_list

@app.route('/handle_submit_cut_form', methods=['POST'])
def handle_submit_cut_form():
    board_lengths_whole = request.form.getlist('length_whole[]')
    board_length_fraction = request.form.getlist("length_fraction[]")
    cut_lengths_whole = request.form.getlist('cut_length_whole[]')
    cut_length_fraction = request.form.getlist("cut_length_fraction[]")
    
    board_widths_whole = request.form.getlist('width_whole[]')
    board_width_fraction = request.form.getlist('width_fraction[]')
    cut_widths_whole = request.form.getlist("cut_width_whole[]")
    cut_width_fraction = request.form.getlist("cut_width_fraction[]")
    
    board_heights_whole = request.form.getlist('height_whole[]')
    board_height_fraction = request.form.getlist("height_fraction[]")
    cut_heights_whole = request.form.getlist('cut_height_whole[]')
    cut_height_fraction = request.form.getlist("cut_height_fraction[]")
    
    cut_quantitiy = request.form.getlist('quantity[]')
    kerf = request.form.get('kerf-type')
    units = request.form.get('units')

    stock_list = form_board_dimensions(board_lengths_whole, board_widths_whole, board_heights_whole, board_length_fraction, board_width_fraction, board_height_fraction)
    cut_list = form_board_dimensions(cut_lengths_whole, cut_widths_whole, cut_heights_whole, cut_length_fraction, cut_width_fraction, cut_height_fraction, cut=True, quantity=cut_quantitiy)
    print("Whole lengths:", board_lengths_whole)
    print("Frac lengths:", board_length_fraction)
    
    print("Whole widths:", board_widths_whole)
    print("frac widths:", board_width_fraction)
    
    print("Whole heights:", board_heights_whole)
    print("frac heights:", board_height_fraction)
    
    print("cut length:", cut_lengths_whole)
    print("frac length:", cut_length_fraction)
    
    print("cut width:", cut_widths_whole)
    print("frac width:", cut_width_fraction)
    
    print("cut height:", cut_heights_whole)
    print("frac height:", cut_height_fraction)

    print("Cut quantity:", cut_quantitiy)
    print("Kerf:", kerf)
    print("Units:", units)
    
    print("Stock Material:", stock_list)
    print("Cuts Needed:", cut_list)
    
    return render_template('cuts.html')
if __name__ == "__main__":
    print("Running Flask server...")
    app.run(debug=True)
