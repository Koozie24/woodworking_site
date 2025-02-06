let toggle_kerf = 1;
const imperial_radio = document.getElementById('imperial-radio');
const metric_radio = document.getElementById('metric-radio');
const remove_board_button = document.getElementById('remove-board-button');

const imperial_container = document.getElementById('imperial-container');
const metric_container = document.getElementById('metric-container');
const imperial_instructions = document.getElementById('imperial-instructions');
const metric_instructions = document.getElementById('metric-instructions');
const imperial_header = document.getElementById('imperial-header');
const metric_header = document.getElementById('metric-header');

let imperial_board_count = 1;
let metric_board_count = 1;
console.log(imperial_board_count);

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

/*function checks to see which radio button is checked*/
function handle_toggle_input(){
    if(imperial_radio.checked){
        imperial_container.style.display = 'block';
        metric_container.style.display = 'none';
        metric_instructions.style.display = 'none';
        imperial_instructions.style.display = 'block';
        imperial_header.style.display ='block';
        metric_header.style.display = 'none';
    }

    else{
        metric_container.style.display = 'block';
        imperial_container.style.display = 'none';
        metric_instructions.style.display = 'block';
        imperial_instructions.style.display = 'none';
        imperial_header.style.display ='none';
        metric_header.style.display = 'block';
    }
}

function remove_imperial_board(){
    const board_groups = imperial_container.querySelectorAll('.board-group');

    //check at least 2 board entries
    if(board_groups.length > 1){
        const last_index = board_groups.length - 1;

        const last_board_group = board_groups[last_index];

        imperial_container.removeChild(last_board_group);
        imperial_board_count --;
    }
}

function add_imperial_board(){
    const board_groups = imperial_container.querySelectorAll('.board-group');
    const get_index = board_groups.length + 1;

    const new_board_group = document.createElement('div');
    new_board_group.classList.add('board-group');

    new_board_group.innerHTML = `
        <strong><u>Board ${get_index}:</u></strong><br><br>
        
        <!-- LENGTH -->
        <label for="length-whole-${get_index}">Length (inches):</label>
        <input type="number" id="length-whole-${get_index}" name="length_whole[]" placeholder="e.g. 5" min="0" required>
        <select id="length-fraction-${get_index}" name="length_fraction[]">
            <option value="0">0</option>
                <option value="0.03125">1/32</option>
                <option value="0.0625">1/16</option>
                <option value="0.09375">3/32</option>
                <option value="0.125">1/8</option>
                <option value="0.15625">5/32</option>
                <option value="0.1875">3/16</option>
                <option value="0.21875">7/32</option>
                <option value="0.25">1/4</option>
                <option value="0.28125">9/32</option>
                <option value="0.3125">5/16</option>
                <option value="0.34375">11/32</option>
                <option value="0.375">3/8</option>
                <option value="0.40625">13/32</option>
                <option value="0.4375">7/16</option>
                <option value="0.46875">15/32</option>
                <option value="0.5">1/2</option>
                <option value="0.53125">17/32</option>
                <option value="0.5625">9/16</option>
                <option value="0.59375">19/32</option>
                <option value="0.625">5/8</option>
                <option value="0.65625">21/32</option>
                <option value="0.6875">11/16</option>
                <option value="0.71875">23/32</option>
                <option value="0.75">3/4</option>
                <option value="0.78125">25/32</option>
                <option value="0.8125">13/16</option>
                <option value="0.84375">27/32</option>
                <option value="0.875">7/8</option>
                <option value="0.90625">29/32</option>
                <option value="0.9375">15/16</option>
                <option value="0.96875">31/32</option>
        </select>
        <br><br>
    
        <!-- WIDTH -->
        <label for="width-whole-${get_index}">Width (inches):</label>
        <input type="number" id="width-whole-${get_index}" name="width_whole[]" placeholder="e.g. 2" min="0" required>
        <select id="width-fraction-${get_index}" name="width_fraction[]" >
            <option value="0">0</option>
                <option value="0.03125">1/32</option>
                <option value="0.0625">1/16</option>
                <option value="0.09375">3/32</option>
                <option value="0.125">1/8</option>
                <option value="0.15625">5/32</option>
                <option value="0.1875">3/16</option>
                <option value="0.21875">7/32</option>
                <option value="0.25">1/4</option>
                <option value="0.28125">9/32</option>
                <option value="0.3125">5/16</option>
                <option value="0.34375">11/32</option>
                <option value="0.375">3/8</option>
                <option value="0.40625">13/32</option>
                <option value="0.4375">7/16</option>
                <option value="0.46875">15/32</option>
                <option value="0.5">1/2</option>
                <option value="0.53125">17/32</option>
                <option value="0.5625">9/16</option>
                <option value="0.59375">19/32</option>
                <option value="0.625">5/8</option>
                <option value="0.65625">21/32</option>
                <option value="0.6875">11/16</option>
                <option value="0.71875">23/32</option>
                <option value="0.75">3/4</option>
                <option value="0.78125">25/32</option>
                <option value="0.8125">13/16</option>
                <option value="0.84375">27/32</option>
                <option value="0.875">7/8</option>
                <option value="0.90625">29/32</option>
                <option value="0.9375">15/16</option>
                <option value="0.96875">31/32</option>
        </select>
        <br><br>
    
        <!-- HEIGHT -->
        <label for="height-whole-${get_index}">Height (inches):</label>
        <input type="number" id="height-whole-${get_index}" name="height_whole[]" placeholder="e.g. 1" min="0" required>
        <select id="height-fraction-${get_index}" name="height_fraction[]">
            <option value="0">0</option>
                <option value="0.03125">1/32</option>
                <option value="0.0625">1/16</option>
                <option value="0.09375">3/32</option>
                <option value="0.125">1/8</option>
                <option value="0.15625">5/32</option>
                <option value="0.1875">3/16</option>
                <option value="0.21875">7/32</option>
                <option value="0.25">1/4</option>
                <option value="0.28125">9/32</option>
                <option value="0.3125">5/16</option>
                <option value="0.34375">11/32</option>
                <option value="0.375">3/8</option>
                <option value="0.40625">13/32</option>
                <option value="0.4375">7/16</option>
                <option value="0.46875">15/32</option>
                <option value="0.5">1/2</option>
                <option value="0.53125">17/32</option>
                <option value="0.5625">9/16</option>
                <option value="0.59375">19/32</option>
                <option value="0.625">5/8</option>
                <option value="0.65625">21/32</option>
                <option value="0.6875">11/16</option>
                <option value="0.71875">23/32</option>
                <option value="0.75">3/4</option>
                <option value="0.78125">25/32</option>
                <option value="0.8125">13/16</option>
                <option value="0.84375">27/32</option>
                <option value="0.875">7/8</option>
                <option value="0.90625">29/32</option>
                <option value="0.9375">15/16</option>
                <option value="0.96875">31/32</option>
        </select>
        <br><br>
    `;
    imperial_container.appendChild(new_board_group);
}

function remove_board(){
    if(imperial_radio.checked){
        remove_imperial_board();
        console.log(imperial_board_count);
    }
}
function add_metric_board(){
    const board_groups = metric_container.querySelectorAll('.board-group');
    const get_index = board_groups.length + 1;

    const new_board_group = document.createElement('div');
    new_board_group.classList.add('board-group');

    new_board_group.innerHTML = `
        <strong><u>Board ${get_index}:</u></strong><br><br>
        
        <!-- LENGTH in centimeters, for example -->
        <label for="length-metric-${get_index}">Length (cm):</label>
        <input type="number" step="0.01" id="length-metric-${get_index}" name="length_cm[]" placeholder="e.g. 12.7" min="0">
        <br><br>
    
        <!-- WIDTH in cm -->
        <label for="width-metric-${get_index}">Width (cm):</label>
        <input type="number" step="0.01" id="width-metric-${get_index}" name="width_cm[]" placeholder="e.g. 5.08" min="0">
        <br><br>
    
        <!-- HEIGHT in cm -->
        <label for="height-metric-${get_index}">Height (cm):</label>
        <input type="number" step="0.01" id="height-metric-${get_index}" name="height_cm[]" placeholder="e.g. 2.54" min="0">
    `;
    metric_container.appendChild(new_board_group);
}

function new_board_entry(){
    if(imperial_radio.checked){
        add_imperial_board();
        imperial_board_count++;
        console.log(imperial_board_count);
    }
    else{
        add_metric_board();
    }
}

handle_toggle_input(); //call once on page load