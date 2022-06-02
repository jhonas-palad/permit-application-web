import * as utils from '../../system_auth/js/utils.js';

const form = $('#main-form');
const text_inputs = $('input[type=text]');
const number_inputs = $('input[type=number]');
const submit_btn = $('#submit-btn');
let valid_container = new Object();


if($('#id_business_type').val() !== '3')
    $('#id_corporation_type').prop('disabled', true);

$('#id_subdivision').prop('required', true);
$('#id_street').prop('required', true);
$('#id_block_no').prop('required', true);

form.submit( e =>{
    e.preventDefault();
    e.target.submit();
})

submit_btn.click( e =>{

    if(!validateEverything()) {
        alert('Some fields are not valid or doesn\'t have value');
        return;
    }
    

    form.submit();
})

function notBlank(input, verbose_name){
    let valid = true;
    if(utils.isBlank(input.val())){
        utils.showInvalid(input, `${verbose_name} cannot be blank`);
        valid = false;
    }else{
        utils.showValid(input, `${verbose_name} accepted`);
    }
    return valid;
}

form.on('input', utils.debounce(e=>{
    const _input = $(e.target);
    console.log(_input);
    const id = _input.attr('id');
    console.log(id);
    let verbose_name = 'This Field';
    switch(id){
        case 'id_business_name':
            verbose_name = 'Business Name';
            valid_container[id] = notBlank(_input, verbose_name);
            break;
        case 'id_trade_name':
            verbose_name = 'Trade Name';
            valid_container[id] = notBlank(_input, verbose_name);
            
            break;
        case 'id_registration_number':
            verbose_name = 'Registration Number';
            valid_container[id] = notBlank(_input, verbose_name);
            
            break;
        case 'id_tax_id_number':
            verbose_name = 'Tax Identification Number';
            valid_container[id] = notBlank(_input, verbose_name);
            
            break;
        case 'id_tel_no':
            verbose_name = 'Tel No.';
            let tel_valid = true;
            if(notBlank(_input, verbose_name) && !utils.isMobile(_input.val())){
                utils.showInvalid(_input, `${_input.val()} is not a ${verbose_name}`);
                tel_valid = false;
            };
            valid_container[id] = tel_valid;
            
            break;
        case 'id_mobile_no':
            verbose_name = 'Mobile No.';
            let mobile_valid = true;
            if(notBlank(_input, verbose_name) && !utils.isMobile(_input.val())){
                utils.showInvalid(_input, `${_input.val()} is not a ${verbose_name}`);
                mobile_valid = false;
            };
            valid_container[id] = mobile_valid;
            
            break;
        case 'id_email_address':
            verbose_name = 'Email Address';
            let email_valid = true;
            if(notBlank(_input, verbose_name) && !utils.isEmail(_input.val())){
                utils.showInvalid(_input, `${_input.val()} is not an ${verbose_name}`);
                email_valid = false;
            };
            valid_container[id] = email_valid;
            
            break;
        case 'id_house_bldg_no':
            verbose_name = 'House/Bldg No.';
            valid_container[id] = notBlank(_input, verbose_name);
            
            break;
        case 'id_blgd_name':
            verbose_name = 'Building Name';
            valid_container[id] = notBlank(_input, verbose_name);
            
            break;
        case 'id_block_no':
            verbose_name = 'Block No.';
            valid_container[id] = true;
            break;
        case 'id_subdivision':
            verbose_name = 'Subdivision';
            valid_container[id] = true;
            
            break;
        case 'id_street':
            valid_container[id] = true;
            verbose_name = 'Street';
            
            break;
        case 'id_barangay':
            verbose_name = 'Barangay';
            valid_container[id] = notBlank(_input, verbose_name);
            
            break;
        case 'id_city':
            verbose_name = 'City';
            valid_container[id] = notBlank(_input, verbose_name);
            
            break;
        case 'id_province':
            verbose_name = 'Province';
            valid_container[id] = notBlank(_input, verbose_name);
            
            break;
        case 'id_zip_code':
            verbose_name = 'Zip Code';
            valid_container[id] = notBlank(_input, verbose_name);
            
            break;
        case 'id_surname':
            verbose_name = 'Surname';
            let surname_valid = true;
            if(notBlank(_input, verbose_name) && !utils.isName(_input.val())){
                utils.showInvalid(_input, `${_input.val()} is not an ${verbose_name}`);
                surname_valid = false;
            };
            valid_container[id] = surname_valid;
            
            break;
        case 'id_given_name':
            verbose_name = 'Given Name';
            let given_valid = true;
            if(notBlank(_input, verbose_name) && !utils.isName(_input.val())){
                utils.showInvalid(_input, `${_input.val()} is not an ${verbose_name}`);
                given_valid = false;
            };
            valid_container[id] = given_valid;
            
            break;
        case 'id_middle_name':
            verbose_name = 'Middle Name';
            let middle_valid = true;
            if(notBlank(_input, verbose_name) && !utils.isName(_input.val())){
                utils.showInvalid(_input, `${_input.val()} is not an ${verbose_name}`);
                middle_valid = false;
            };
            valid_container[id] = middle_valid;
            
            break;
        case 'id_tax_declaration':
            verbose_name = 'Tax declaration';
            valid_container[id] = notBlank(_input, verbose_name);
            
            break;
        case 'id_capital_investment':
            verbose_name = 'Paid up Capital';
            valid_container[id] = notBlank(_input, verbose_name);
            
            break;
        case 'id_business_area':
            verbose_name = 'Business Area';
            valid_container[id] = notBlank(_input, verbose_name);
            
            break;
        case 'id_total_floor_area':
            verbose_name = 'Total Floor area';
            valid_container[id] = notBlank(_input, verbose_name);
            
            break;
        case 'id_property_ident_no':
            verbose_name = 'Property ID no.'
            valid_container[id] = notBlank(_input, verbose_name);
            break;
        case 'id_female_emp_count':
            verbose_name = 'Female No.';
            valid_container[id] = notBlank(_input, verbose_name);
            
            break;
        case 'id_male_emp_count':
            verbose_name = 'Male No.';
            valid_container[id] = notBlank(_input, verbose_name);
            
            break;
        case 'id_tanauan_emp_count':
            verbose_name = 'Tanauan Emp No.';
            valid_container[id] = notBlank(_input, verbose_name);
            
            break;
        case 'id_van_truck_count':
            verbose_name = 'Van/Truck No.';
            valid_container[id] = notBlank(_input, verbose_name);
            
            break;
        case 'id_motorcycle_count':
            verbose_name = 'Motorcycle No.';
            valid_container[id] = notBlank(_input, verbose_name);
            break;
        case 'id_business_type':
            
            if(_input.val() === '3'){
                $('#id_corporation_type').prop('disabled', false);
            }else{
                $('#id_corporation_type').prop('disabled', true);
            }
            verbose_name = 'Business Type';

            valid_container[id] = true;
            break;
        case 'id_corporation_type':
            verbose_name = 'Corporation Type';
            valid_container[id] = true;
            break;
        case 'id_sex':
            verbose_name = 'Sex';
            
            valid_container[id] = true;
            break;
        case 'id_owned':
            verbose_name = 'Owned';
            if(_input.prop('checked')){
                let xhr = new XMLHttpRequest();
                xhr.open('GET', window.location.href + '/get-name');
                xhr.onload = (e) =>{
                    if (xhr.status === 200){
                        const response = JSON.parse(xhr.responseText);
                        $('#id_surname')[0].value = response.surname;
                        $('#id_given_name')[0].value = response.given_name;
                    }
                }
                xhr.send();
            }
            
            
            valid_container[id] = true;
            break;
        case 'id_rented':
            verbose_name = 'Rented';
            valid_container[id] = true;
            break;
        case 'id_tax_incentives':
            verbose_name = 'Tax Incentives';
            valid_container[id] = true;
            break;

    }

}, 200));
valid_container.id_block_no = true;
valid_container.id_subdivision = true;
valid_container.id_street = true;
valid_container.business_type_id = true;
valid_container.id_corporation = true;
valid_container.id_sex = true;
valid_container.id_owned = true;
valid_container.id_rented = true;
valid_container.id_tax_incentives = true;



function validateEverything(){
    let valid = [];
    for(let k in valid_container){
        
        valid.push(valid_container[k]);
    }
    
    console.log(valid_container);
    
    for(let text_input of text_inputs){
        if(text_input.id in valid_container){
            continue;
        }else{
            valid.push(notBlank($(text_input), 'This field'));
        }
    }
    for(let number_input of number_inputs){
        if(number_input.id in valid_container){
            continue;
        }else{
            valid.push(notBlank($(number_input), 'This field'));
        }
    }
    console.log(valid);
    const all_valid = valid.every((val) =>{
        return val;
    });
  
    
    
    return all_valid;
}


