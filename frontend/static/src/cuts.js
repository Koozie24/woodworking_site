let toggle_kerf = 1;
let toggle_plan = 1;
const imperial_radio = document.getElementById('imperial-radio');
const metric_radio = document.getElementById('metric-radio');
const remove_board_button = document.getElementById('remove-board-button');

const board_container = document.getElementById('imperial-container');
const imperial_cut_container = document.getElementById('imperial-cut-container');
const metric_cut_container = document.getElementById('metric-cut-container');

const imperial_instructions = document.getElementById('imperial-instructions');
const metric_instructions = document.getElementById('metric-instructions');
const imperial_header = document.getElementById('imperial-header');
const metric_header = document.getElementById('metric-header');

let board_count = 1;
let imperial_cut_count = 1;
let metric_cut_count = 1;

imperial_radio.addEventListener('change', handle_toggle_input);
metric_radio.addEventListener('change', handle_toggle_input);

/*Function toggles a "?" button and displays information to explain kerf */
function display_kerf_info(){
    let current_state = document.querySelector('.kerf-message')

    if(toggle_kerf % 2 == 0){
        current_state.style.display = 'none';
    }
    if(toggle_kerf % 2 == 1){
        current_state.style.display = 'block';
    }

    toggle_kerf++;
}

function display_plan_info(){
    const current_state = document.querySelector('.plan-message');

    if(toggle_plan % 2 == 0){
        current_state.style.display = 'none';
    }
    if(toggle_plan % 2 == 1){
        current_state.style.display = 'block';
    }

    toggle_plan++;
}

/*function checks to see which radio button is checked*/
function handle_toggle_input(){

    let imp_label = Array.from(document.getElementsByClassName('imperial-label'));
    let metric_label = Array.from(document.getElementsByClassName('metric-label'));
    let fraction_selection = Array.from(document.getElementsByClassName('dimension-fraction-selection'));
    if(imperial_radio.checked){
        metric_instructions.style.display = 'none';
        imperial_instructions.style.display = 'block';
        imperial_header.style.display ='block';
        metric_header.style.display = 'none';
        imperial_cut_container.style.display = 'block';
        metric_cut_container.style.display = 'none';

        for(let i = 0; i < imp_label.length; i++){ //hide cm label and show inches label
            imp_label[i].style.display = 'inline';
            metric_label[i].style.display = 'none';
        }

        fraction_selection.forEach(div => div.style.display = 'block'); //show fractional selection areas
    }

    else{
        metric_instructions.style.display = 'block';
        imperial_instructions.style.display = 'none';
        imperial_header.style.display ='none';
        metric_header.style.display = 'block';
        imperial_cut_container.style.display = 'none';
        metric_cut_container.style.display = 'block';

        for(let i = 0; i < metric_label.length; i++){ //hide inches label and show cm label
            imp_label[i].style.display = 'none';
            metric_label[i].style.display = 'inline';
        }

        fraction_selection.forEach(div => div.style.display = 'none'); //hide fractional selection areas
        
    }
}

//add imperial cut to dom and append to imperial cut container
function add_imperial_cut(){
    const cut_groups = imperial_cut_container.querySelectorAll('.board-group');
    const get_index = cut_groups.length + 1;

    const new_cut_group = document.createElement('div');
    new_cut_group.classList.add('board-group');

    new_cut_group.innerHTML = `
        <strong><u>Cut Type ${get_index}:</u></strong><br><br>

            <div class="imperial-grid-container">
                <div class="dimension-labels">
                    <label for="cut-quantity-whole-${get_index}">Cut Quantity:</label>
                    <label for="length-cut-whole-${get_index}">Length (inches):</label>
                    <label for="width-cut-whole-${get_index}">Width (inches): </label>
                    <label for="height-cut-whole-${get_index}">Height (inches):</label>
                </div>

                <div class="dimension-input-area">
                    <input type="number" class="number-input" id="cut-quantity-whole-${get_index}" name="quantity[]" min="1" required>
                    <input type="number" class="number-input" id="length-cut-whole-${get_index}" name="length_whole[]" min="0" required>
                    <input type="number" class="number-input" id="width-cut-whole-${get_index}" name="width_whole[]" min="0" required>
                    <input type="number" class="number-input" id="height-cut-whole-${get_index}" name="height_whole[]" min="0" required>
                </div>

                <div class="dimension-fraction-selection">
                    <select class="fraction-select" id="hidden-select-${get_index}" name="hidden_select[]"></select>
                    <select class="fraction-select" id="length-cut-fraction-${get_index}" name="length_fraction[]">
                        ${generate_fractions()}
                    </select>
                    <select class="fraction-select" id="width-cut-fraction-${get_index}" name="width_fraction[]" >
                        ${generate_fractions()}
                    </select>
                    <select class="fraction-select" id="height-cut-fraction-${get_index}" name="height_fraction[]">
                        ${generate_fractions()}
                    </select>
                </div>
            </div>
    `;
    imperial_cut_container.appendChild(new_cut_group);
    const hidden_select = new_cut_group.querySelector(`#hidden-select-${get_index}`);
    hidden_select.style.visibility = 'hidden';
}

//add metric cut to dom and append to metric cut container
function add_metric_cut(){
    const cut_groups = metric_cut_container.querySelectorAll('.board-group');
    const get_index = cut_groups.length + 1;

    const new_cut_group = document.createElement('div');
    new_cut_group.classList.add('board-group');

    new_cut_group.innerHTML = `
       <strong><u>Cut Type ${get_index}:</u></strong><br><br>
                                
        <div class="metric-grid-container">
            <div class="metric-label-div">
                <label for="cut-quantity-metric-${get_index}">Cut Quantity:</label>
                <!-- LENGTH in centimeters, for example -->
                <label for="length-cut-metric-${get_index}">Length (cm):</label>
                <!-- WIDTH in cm -->
                <label for="width-cut-metric-${get_index}">Width (cm): </label>
                <!-- HEIGHT in cm -->
                <label for="height-cut-metric-${get_index}">Height (cm):</label>
            </div>

            <div class="metric-number-div">
                <input type="number" class="number-input" id="cut-quantity-metric-${get_index}" name="quantity[]" min="1" required>
                <!-- LENGTH in centimeters, for example -->
                <input type="number" step="0.01" class="number-input" id="length-cut-metric-${get_index}" name="length_cm[]" min="0">
                <!-- WIDTH in cm -->
                <input type="number" step="0.01" class="number-input" id="width-cut-metric-${get_index}" name="width_cm[]" min="0">
                <!-- HEIGHT in cm -->
                <input type="number" step="0.01" class="number-input" id="height-cut-metric-${get_index}" name="height_cm[]" min="0">
            </div>
        </div>
    `;
    metric_cut_container.appendChild(new_cut_group);
}

/*function gets length of cut groups imperial or metric based on argument passed, finds last index and removes it from the dom and decrements counter */
function remove_last_cut(unit_type){
    if(imperial_cut_count > 1 && unit_type == "imperial"){ //imperial measurement
        const cut_groups = imperial_cut_container.querySelectorAll('.board-group');
        const last_index = cut_groups.length - 1;
        const last_cut_group = cut_groups[last_index];

        imperial_cut_container.removeChild(last_cut_group);
        imperial_cut_count--;
    }
    if(metric_cut_count > 1 && unit_type == "metric"){ //metric measurement
        const cut_groups = metric_cut_container.querySelectorAll('.board-group');
        const last_index = cut_groups.length - 1;
        const last_cut_group = cut_groups[last_index];

        metric_cut_container.removeChild(last_cut_group);
        metric_cut_count--;
    }
}

//remove imperial or metric board based on radio utton checked
function remove_board(){
    //check at least 2 board entries
    if(board_count > 1){
        const board_groups = board_container.querySelectorAll('.board-group');
        const last_index = board_groups.length - 1;
        const last_board_group = board_groups[last_index];

        board_container.removeChild(last_board_group);
        board_count --;
    }
}

//remove imperial or metric cut tpye base on radio button checkecd
function remove_cut(){
    if(imperial_radio.checked){
        remove_last_cut("imperial");
    }
    else{
        remove_last_cut("metric");
    }
}
//handles addition of new metric or imperial board based on which radio button is checked
//increments board count
function new_board_entry(){
    const board_groups = board_container.querySelectorAll('.board-group');
    const get_index = board_groups.length + 1;

    const new_board_group = document.createElement('div');
    new_board_group.classList.add('board-group');

    new_board_group.innerHTML = `
        <!-- Initial board inputs -->
        <strong><u>Board ${get_index}:</u></strong><br><br>

        <div class="imperial-grid-container">
            <div class="dimension-labels">
                <label for="length-whole-${get_index}">Length <span class="imperial-label">(inches): </span> <span class="metric-label">(cm): </span></label>
                <label for="width-whole-${get_index}">Width <span class="imperial-label">(inches): </span> <span class="metric-label">(cm): </span></label>
                <label for="height-whole-${get_index}">Height <span class="imperial-label">(inches): </span> <span class="metric-label">(cm): </span></label>
            </div>

            <div class="dimension-input-area">
                <input type="number" class="number-input" id="length-whole-${get_index}" name="length_whole[]" placeholder="e.g. 5" min="0" required>
                <input type="number" class="number-input" id="width-whole-${get_index}" name="width_whole[]" placeholder="e.g. 2" min="0" required>
                <input type="number" class="number-input" id="height-whole-${get_index}" name="height_whole[]" placeholder="e.g. 1" min="0" required>
            </div>

            <div class="dimension-fraction-selection">
                <select class="fraction-select" id="length-fraction-${get_index}" name="length_fraction[]">
                    ${generate_fractions()}
                </select>
                <select class="fraction-select" id="width-fraction-${get_index}" name="width_fraction[]" >
                    ${generate_fractions()}
                </select>
                <select class="fraction-select" id="height-fraction-${get_index}" name="height_fraction[]">
                    ${generate_fractions()}
                </select>
            </div>
        </div>
    `;
    board_container.appendChild(new_board_group);
    board_count++;
    handle_toggle_input();
}

//handles addiotion of new cuts based on which radio is selected and increments cut counter
function new_cut_entry(){
    if(imperial_radio.checked){
        add_imperial_cut();
        imperial_cut_count++;
    }
    else{
        add_metric_cut();
        metric_cut_count++;
    }
}


function generate_fractions(){
        const fractions = [
            { value: "0", label: "0" }, { value: "0.03125", label: "1/32" }, { value: "0.0625", label: "1/16" },
            { value: "0.09375", label: "3/32" }, { value: "0.125", label: "1/8" }, { value: "0.15625", label: "5/32" },
            { value: "0.1875", label: "3/16" }, { value: "0.21875", label: "7/32" }, { value: "0.25", label: "1/4" },
            { value: "0.28125", label: "9/32" }, { value: "0.3125", label: "5/16" }, { value: "0.34375", label: "11/32" },
            { value: "0.375", label: "3/8" }, { value: "0.40625", label: "13/32" }, { value: "0.4375", label: "7/16" },
            { value: "0.46875", label: "15/32" }, { value: "0.5", label: "1/2" }, { value: "0.53125", label: "17/32" },
            { value: "0.5625", label: "9/16" }, { value: "0.59375", label: "19/32" }, { value: "0.625", label: "5/8" },
            { value: "0.65625", label: "21/32" }, { value: "0.6875", label: "11/16" }, { value: "0.71875", label: "23/32" },
            { value: "0.75", label: "3/4" }, { value: "0.78125", label: "25/32" }, { value: "0.8125", label: "13/16" },
            { value: "0.84375", label: "27/32" }, { value: "0.875", label: "7/8" }, { value: "0.90625", label: "29/32" },
            { value: "0.9375", label: "15/16" }, { value: "0.96875", label: "31/32" }
        ];
        return fractions.map(f => `<option value="${f.value}">${f.label}</option>`).join('');
}

handle_toggle_input(); //call once on page load