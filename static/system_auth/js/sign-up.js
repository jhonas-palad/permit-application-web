import *  as utils from './utils.js';


const form = $('form');
const csrftoken = $('input[name=csrfmiddlewaretoken]');
const sign_up_btn = $('button[sign-up]');

let first_name, last_name ,email, username, password, confirm_pass;



first_name = utils.queryInput(form, 'first_name');
last_name = utils.queryInput(form, 'last_name');
email = utils.queryInput(form,'email');
username = utils.queryInput(form,'username');
password = utils.queryInput(form,'password');
confirm_pass = utils.queryInput(form,'confirm_pass');

form.on('submit', (e)=>{
    e.preventDefault();
    e.target.submit();
});

sign_up_btn.on('click', (e)=>{
    let valid_arr = [];

    
    // valid_arr.push(utils.emailUserHandler(email, true))
    // valid_arr.push(utils.emailUserHandler(username, true))
    valid_arr.push(utils.isValidName(first_name));
    valid_arr.push(utils.isValidName(last_name));
    valid_arr.push(utils.isValidEmail(email));
    valid_arr.push(utils.isValidUsername(username));
    valid_arr.push(utils.checkPassword(password));
    valid_arr.push(utils.checkConfirmPassword(confirm_pass, password));
        

    const check = (val) =>{
        return val;
    }
    console.log(valid_arr)
    if(!valid_arr.every(check)) return ;
    form.submit();
});


form.on('input', utils.debounce(e=>{
    const input = $(e.target);
    const id = input.attr('id');
    console.log(id);
    switch(id){
        case 'first_name_id':
            utils.isValidName(input);
            break;
        case 'last_name_id':
            utils.isValidName(input);
            break;
        case 'email_input_id':
            utils.emailUserHandler(input, false);
            break;
        case 'username_id':
            utils.emailUserHandler(input, false);
            break;
        case 'password_id':
            utils.checkPassword(input);
            break;
        case 'confirm_pass_id':
            utils.checkConfirmPassword(input, password);
            break;

    }

}))






// email.on('change', emailUserHandler);

// username.on('change', emailUserHandler);

// password.on('change', passwordHandler);

// confirm_pass.on('change', passwordHandler);

// sign_up_btn.on('click', submitHandler);



// function submitHandler(event){
//     console.log(validateAll())
//     if(!validateAll()){
//         return;
//     }
    
//     form.submit();

// }

// function validateAll(){
//     let inputs = [
//         email,
//         username,
//         password,
//         confirm_pass
//     ]
//     let valids = [];
//     for(var input of inputs){
//         valids.push(checkInput(input));
//     }
//     return valids.every(val =>{
//         return val;
//     })
// }

// function passwordHandler(event){
//     let pass1_val = password.val();
//     let pass2_val = confirm_pass.val();

//     if(pass1_val.length < 8){
//         password.siblings('div').text('Use 8 characters or more for your password');
//         markInvalid(password);
//         return;
//     }else{
//         removeInvalid(password)
//     }
//     if(!passwordMatched(pass1_val,pass2_val)) {
//         confirm_pass.siblings('div').text('Those password didn\'t matched');
//         markInvalid(confirm_pass)
//         return;
//     }else{
//         removeInvalid(confirm_pass)
//     }
// }



// const checkInput = (input)=>{
//     const name = input.attr('name');
//     const val = input.val();
//     if(val == ''){
        
//         if(name != 'confirm_pass'){
//             console.log(name);
//             markInvalid(input);
//         }
        
//         return false;
//     }
//     return !$(input).parent('.form-group').hasClass('invalid') && $(input).val();
// }
// const passwordMatched = (pass1, pass2) =>{
//     return pass1 == pass2
// }



