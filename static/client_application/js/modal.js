import * as utils from '../../system_auth/js/utils.js';

const add_line_url = window.location.href + '/add-business-line';
const modal_add = $('.modal[add]');
const modal_title = modal_add.find('.modal-title');
const show_modal_add = $('#show-modal-add');
const modal_inputs = modal_add.find('input');
const add_row = modal_add.find('#add-row');
const update_row = modal_add.find('#update-row');
const delete_row = modal_add.find('#delete-row');

var table = $('#business-line-table')[0];

let modal_close = modal_add.find('.modal-close-btn');

modal_close.on('click', e =>{
    closeModal(modal_add, Array.from(modal_inputs));
})


show_modal_add.on('click', e =>{
    $('.double-btn').removeClass('show');
    $('.solo-btn').addClass('show');

    showModal();
    
})




add_row.on('click', e=>{
    console.log('asdasd');
    insert();
})

const csrftoken = utils.getCookie('csrftoken');

[...$('.body-row')].forEach((row)=>{

    row.onclick = (e) =>{
        view_row(row);
    }
}); 


const insert = (_table = table) =>{
    
    let data = new FormData();
    let inputs = Array.from(modal_inputs);
    let valids = [];
    inputs.forEach(input =>{
        let _input = $(input);
        if(_input.prop('required')){
            const valid = handleRequired(_input);
            if(!valid){
                _input.on('change', e =>{
                    handleRequired($(e.target));
                });
            }
            valids.push(valid);
        }
        data.append(_input.attr('name'), _input.val());
    });
    if(!valids.every(valid =>{return valid})){
        return;
    }
    data.append('csrfmiddlewaretoken', csrftoken);

    let xhr = new XMLHttpRequest();
    xhr.open('POST',add_line_url);
    
    xhr.onload = (e) =>{
        console.log(xhr.responseText);
        const response = JSON.parse(xhr.responseText);
        const col_len = _table.rows[0].cells.length;
        
        let new_row = _table.insertRow(1);
        new_row.classList.add('body-row');
        new_row.setAttribute('pk',response['pk']);
        new_row.setAttribute('index', 1);
        if (_table.rows.length > 2){
            for(let i = 2; i < _table.rows.length; i++){
                let cur_index = table.rows[i].getAttribute('index');
                cur_index++;
                table.rows[i].setAttribute('index', cur_index);

            }
        }
        
        new_row.onclick = e =>{
            console.log('view');
            view_row(new_row);
        }
        const keys = Object.keys(response);
        for(let index = 1; index <=col_len; index++){
            let div = document.createElement('div');
            let cell = new_row.insertCell(index-1);
            div.classList.add('table-data');
            const key = keys[index];
            
            div.innerHTML = response[key];
            cell.setAttribute('value', response[key]);

            cell.appendChild(div);
        }

    }
    xhr.send(data);

    
    closeModal(modal_add, inputs);




}
const showModal = (modal = modal_add) => {
    $(modal).addClass('show');
}

var ii = 0;
var iii = 0;


const view_row = (tr) =>{
    //edit button
    console.log(tr);
    modal_title.html(`<h3>Showing row no. ${tr.index} with pk of ${tr.pk}</h3>`);
    let inputs = Array.from(modal_inputs);
    const table_index = parseInt(tr.getAttribute('index'));
    
    const cells = table.rows[table_index].cells;
    const len = cells.length;
    for(let i = 0; i < len; i++){
        inputs[i].value = cells[i].getAttribute('value');
    }

    $('.solo-btn').removeClass('show');
    $('.double-btn').addClass('show');
    
    $('#update-row')[0].onclick = (e) => {
        console.log('Update-row', iii++);
        update(tr);
    };

    $('#delete-row')[0].onclick = (e) => {
    
        console.log('Delete-row',tr, ii++);
        delete_row_handler(tr);
    };
    showModal(modal_add);
}   
const update = (tr) =>{
    let inputs = Array.from(modal_inputs);
    let valids = [];
    inputs.forEach(input =>{
        let _input = $(input);
        if(_input.prop('required')){
            const valid = handleRequired(_input);
            if(!valid){
                _input.on('change', e =>{
                    handleRequired($(e.target));
                });
            }
            valids.push(valid);
        }
    });
    if(!valids.every(valid =>{return valid})){
        return;
    }
    const url = window.location.href + '/update-business-line';
    let data = new FormData();
    let xhr = new XMLHttpRequest();
    const csrftoken = utils.getCookie('csrftoken');


    data.append('csrfmiddlewaretoken', csrftoken);
    data.append('pk', tr.getAttribute('pk'));
    for(let input of inputs){
        let _input = $(input);
        data.append(_input.attr('name'), _input.val());
    }

    xhr.open('POST', url);
    xhr.onload = (e) =>{
        if(xhr.status == 200){
            console.log('UPDATE',xhr.responseText);
            const response = JSON.parse(xhr.responseText);
            const cell_len = tr.cells.length;
            const keys = Object.keys(response);
            for(let i = 0; i < cell_len; i++){
                const val = response[keys[i]];
                $(tr.cells[i]).children('.table-data').text(val);
                tr.cells[i].setAttribute('value',val);
            }
            
        }
        
    }
    xhr.send(data);

    closeModal(modal_add);
}

const delete_row_handler = (tr) =>{
    const url = window.location.href + '/delete-business-line';
    let xhr = new XMLHttpRequest();
    
    let data = new FormData();
    data.append('pk', tr.getAttribute('pk'));
    data.append('csrfmiddlewaretoken', csrftoken);

    xhr.open('POST', url);
    xhr.onload = (e) =>{
        if(xhr.status == 200){
            const index = parseInt(tr.getAttribute('index'));
            
            let rows = table.rows;
            const curr_len = rows.length - 1;  

            if(index < curr_len){
                for(var i = index + 1; i <=curr_len; i++) {

                    let cur_index = parseInt(rows[i].getAttribute('index'));
                    cur_index--;
                    rows[i].setAttribute('index', cur_index);

                }
            } 
            table.deleteRow(index);
            
        }
    }
    xhr.send(data);
    closeModal(modal_add);

}


const handleRequired = (input) =>{
    if(utils.isBlank(input.val())){
        utils.showInvalid(input, 'This field is required');
        return false;
    }else{
        utils.showValid(input, 'Accepted');
    }
    return true;
}

const closeModal = (modal, inputs = Array.from(modal_inputs))=>{
    modal.removeClass('show');
    console.log(inputs);
    clearInputs(inputs);
}

const clearInputs = (inputs) =>{
    inputs.forEach(input =>{
        if(input.parentElement.classList.contains('invalid')){
            input.parentElement.classList.remove('invalid');
        }
        if(input.parentElement.classList.contains('valid')){
            input.parentElement.classList.remove('valid');
        }
        input.value = '';
    })

}