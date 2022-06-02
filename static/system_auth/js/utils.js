export const greetings = 'HELLO';
export const isBlank = value => {return value === ''};

export const isBetween = (len, min, max) => {
    return len > min || len < max
}
export const isMobile = (value) =>{
    return /^\d{11}$/.test(value);
}
export const isName = (val) =>{
    // const val = name.val()
    return /^[a-zA-Z]+$/.test(val)
}
export const isValidName = (name_input)=>{
    console.log(name_input)
    const name_val = name_input.val().split(' ');
    const name = name_input.attr('name');
    let verbose = (name == 'first_name') ? 'First Name' : 'Last Name';
    let valid = true;
    for(let val of name_val){
        if(isBlank(val)){
            showInvalid(name_input, `Please enter your ${verbose}`);
            return !valid;
        }
        if(!isName(val)){
            showInvalid(name_input, `${verbose} must only contain letters`);
            return !valid;
        }
    }
   
    showValid(name_input, `Accepted`);
    
    return valid;
}   
export const isEmail = (val) =>{
    // const val = email.val()
    return /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(val);
}

export const isUsername = (val) => {
    // const val = username.val();
    return /^\w+$/.test(val);
}

export const isValidEmail = (email_input) => {
    const email = email_input.val();
    let valid = true;

    if(isBlank(email)) {
        showInvalid(email_input, 'Please provide an email');
        return !valid;
    }
    if(!isEmail(email)){
        showInvalid(email_input, `${email} is not a valid email`);
        return !valid;
    }
    
    if(!email_input.parent('.form-group').hasClass('valid')){
        valid = emailUserHandler(email_input, true);
        
    }

    return valid;

    
}
export const isValidUsername = (username_input) => {
    const username = username_input.val();
    let valid = true;

    if(isBlank(username)) {
        showInvalid(username_input, 'Please provide an username');
        return !valid;
    }
    if(!isUsername(username)){
        showInvalid(username_input, `${username} is not a valid username`);
        return !valid;
    }
    
    if(!username_input.parent('.form-group').hasClass('valid')){
        
        valid = emailUserHandler(username_input, true);
        console.log(valid);
        
    }
    return valid;
    
}


export const isPasswordSecure = (password) => {

    // const re = new RegExp("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})");
    return leastEightChar(password) && hasOneNumber(password) && hasUpperCase(password);
    
}



export const leastEightChar = (password) =>{
    return password.length >= 8;
}
export const hasOneNumber = (password) => {
    return /(?=.*[0-9])/.test(password);
}
export const hasUpperCase = (password) => {
    return /(?=.*[A-Z])/.test(password);
}

export const showValid = (input, msg) => {
    let form_group = input.parent();
    form_group.removeClass('invalid').addClass('valid');
    form_group.find('div.input-msg').text(msg);    
}

export const showInvalid = (input, msg) => {
    let form_group = input.parent();
    form_group.removeClass('valid').addClass('invalid');
    form_group.find('div.input-msg').text(msg);    
}


export function queryInput(form,input){
    return $(form).find(`input[name=${input}]`);
}

export const debounce = (callback, delay = 1000) =>{
    let timeout;

    return (...args) => {
        
        clearTimeout(timeout);
        

        timeout = setTimeout(()=>{
            callback(...args);
        }, delay);
    }
}


export const checkPassword = (password_input) => {
    const password = password_input.val();
    let valid = false;
 
    if(isBlank(password)){
        showInvalid(password_input, 'Password is cannot be blank');
    }else if(!leastEightChar(password)){
        showInvalid(password_input, 'Password should be at least 8 characters');
    }else if(!hasOneNumber(password)){
        showInvalid(password_input, 'Password should contain at least one number');
    }else if(!hasUpperCase(password)){
        showInvalid(password_input, 'Password should contain at least one upper case character');
    }else{
        showValid(password_input, 'Password is valid');
        valid = true;
    }
    return valid;
    
}

export const checkConfirmPassword = (confirm_pass_input, password_input) =>{
    let valid = false;
    const confirm_pass = confirm_pass_input.val();
    const password = password_input.val();


    if(isBlank(password)){    
        showInvalid(password_input, 'Password is cannot be blank');
        return valid;
    }   
    if(isBlank(confirm_pass)){
        showInvalid(confirm_pass_input, 'Please enter the password again');
    }else if(password !== confirm_pass){
        showInvalid(confirm_pass_input, 'Those passwords doesn\'t match');
    }else{
        showValid(confirm_pass_input, 'Password matched');
        valid = true;
    }
    return valid;
}

// var emailCache = {
//     data: {},
//     contains: (email) =>{
//         return emailCache.hasOwnProperty(email) && emailCache.data[email] !== null;
//     },
//     get: (email) =>{
//         return emailCache.data[email];
//     }, 
//     set: (email, )

// };
// CONSTANT REQUEST PROBLEM
export const emailUserHandler = (input, validation)=>{

    const name = input.attr('name');
    let value = input.val();
    let valid = false;

    if(!validation){
        if(isBlank(value)) {
            showInvalid(input, `Please provide an ${name}`);
            return;
        }   
    
        if(name == 'email'){
            if(!isEmail(value)){
                showInvalid(input, `${value} is not a valid email`);
                return ;
            }
        }
        if(name == 'username'){
            if(!isUsername(value)){
                showInvalid(input, `${value} is not a valid username`);
                return;
            }
        }
    }
    

    $.ajax(
        {
            url: window.location.href,
            type:'GET',
            dataType: 'json',
            async: false,
            cache: true,
            data: {
                validation: true,
                name : name, 
                value: value,
            },
            beforeSend: () =>{

            },
            success: (response) =>{
                if(response.taken && response.name == name){
                    showInvalid(input, `${value} is already taken`);  
                    
                }else{
                    showValid(input, `${value} is accepted`);
                    valid = true;
                    
                }  
               
                
            },
            

        }
    );
    return valid;
}

export const getCookie = (name) =>{
    let cookieValue = null;

    if(document.cookie && document.cookie !==''){
        const cookies = document.cookie.split(';');
        
        const cookie_len = cookies.length;
        for(let i = 0; i < cookie_len; i++){
            const cookie = cookies[i].trim();
            
            if(cookie.substring(0, name.length + 1) === (name + '=')){
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

export const bytesToSize = (bytes) =>{
    let sizes = ['Bytes', 'KB', 'MB', 'GB'];
    if(bytes == 0) return '0 Byte';
    let i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
    return Math.round(bytes/ Math.pow(1024, i), 2) + ' ' + sizes[i];
}