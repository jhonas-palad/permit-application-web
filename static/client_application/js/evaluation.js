import * as utils from '../../system_auth/js/utils.js';
const button_wrapper = $('.button-wrapper');
const url_gen = window.location.origin + '/staff/generate-permit';
const url_deny = window.location.origin + '/staff/deny-permit';
const csrftoken = utils.getCookie('csrftoken');
console.log(csrftoken);

const verify = $('#verify'), deny = $('#deny');

verify.on('click', e =>{
    console.log(verify.attr('pk'));
    generate_permit(verify.attr('pk'));
})
deny.on('click', e =>{
    console.log(deny.attr('pk'));
    deny_application(deny.attr('pk'));
})

const generate_permit = (pk) =>{
    let data = new FormData();
    data.append('csrfmiddlewaretoken', csrftoken);
    data.append('pk', pk);
    let xhr = new XMLHttpRequest();
    xhr.open('POST', url_gen);
    xhr.onload = e =>{
        const response = JSON.parse(xhr.responseText);
        $('#status-detail').html(response.status);
        button_wrapper.html(`<div class="msg-box">This form is already evaluated</div>`);
    }
    xhr.send(data);
    
}

const deny_application = (pk) =>{
    let data = new FormData();
    data.append('csrfmiddlewaretoken', csrftoken);
    data.append('pk', pk);
    let xhr = new XMLHttpRequest();
    xhr.open('POST', url_deny);
    xhr.onload = e =>{
        const response = JSON.parse(xhr.responseText);
        $('#status-detail').html(response.status);
        button_wrapper.html(`<div class="msg-box">This form is already evaluated</div>`);
    }
    xhr.send(data);
    
}