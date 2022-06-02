import *  as utils from './utils.js';

const form = $('form');
let email_user, password_login, sign_in = $('[sign-in]');
const url = window.location.href;

console.log(sign_in);


email_user = utils.queryInput(form,'email_user');
password_login = utils.queryInput(form,'password_login');


form.on('submit', e=>{
    e.preventDefault();
    e.target.submit();
});




sign_in.on('click', (e)=>{
    let valid_arr = [];

    valid_arr.push(isInvalid(email_user));
    valid_arr.push(isInvalid(password_login));

    if(!valid_arr.every(val =>{return val})){
        console.log(valid_arr);
        return;
    }
    form.submit();
})

const isInvalid = (input)=>{
    
    let value = input.val();
    console.log(value);
    const verbose = (input.attr('name') === 'password_login') ? 'Password' : 'Email or Username';
    if(utils.isBlank(value)){
        utils.showInvalid(input, `Please enter your ${verbose} `);
        return false;
    }else{
        utils.showValid(input, ``);
        return true;
    }
}

// naive approach
