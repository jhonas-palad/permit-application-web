import * as utils from '../../system_auth/js/utils.js';

const form = $('form');
const btn = $('#submit-btn');
const upload_url = window.location.href + '/upload-image';
const remove_url = window.location.href + '/remove-image';
const csrf_token = utils.getCookie('csrftoken');
console.log(upload_url, remove_url);
btn.click(e=>{
    form.submit();
})
form.on('submit', e=>{
    
    e.preventDefault();
    e.target.submit();
    
});

[...$('button[uploaded]')].forEach((btn)=>{
    
    btn.onclick = (e) =>{
        const _id = btn.id;
        console.log(btn.id)
        let data = new FormData();

        data.append('remove', true);
        // data.append('filename', e.target.for);
        data.append('file_pk', _id);
        data.append('csrfmiddlewaretoken', csrf_token);

        let _xhr = new XMLHttpRequest();

        _xhr.open('POST', remove_url);

        _xhr.onload = (e) =>{
            console.log(_xhr.responseText);
            if(_xhr.status == 200){
                btn.parentElement.remove();
            }
            
        };
        
        _xhr.onerror = (e) =>{
            console.log('ERROR',e)
        }
        _xhr.send(data);
    }
})




$('.file-input').on('change', e=>{
    let allowed_mime_types = [];
    let allowed_size_mb = 100 * 1024 * 1024;

    let files_input = Array.from($('.file-input')[0].files);
    let files_length = files_input.length;

    if(files_length == 0){
        alert('No files selected');
        return;
    }

    for(let i = 0; i < files_length; i++){
        let file = files_input[i];
        

        if(file.size > allowed_size_mb){
            alert('Exceed size' + file.name);
            return;
        }

        
        let uniq = 'id-' + btoa(file.name).replace(/=/g, '');
        let filetype = (/(image.*)+$/.test(file.type)) ? 'image' : 'pdf';
        
        let li_code = `
            <div class="thumbnail">
                <ion-icon name="document"></ion-icon>
                <ion-icon name="image"></ion-icon>
                <span class="completed">
                    <ion-icon name="checkmark"></ion-icon>
                </span>

            </div>
            <div class="properties">
                <span class="title"><strong>${file.name}</strong></span>
                <span class="size">${utils.bytesToSize(file.size)}</span>
                <span class="progress">
                    <span class="buffer"></span>
                    <span class="percentage"></span>
                </span>
            </div>
            <button type="button" class="remove">
                <ion-icon name="close"></ion-icon>
            </button>
        `;

        let li = document.createElement('li');
        li.classList.add('file-list');
        li.classList.add(filetype);
        li.id = uniq;
        li.innerHTML = li_code
        
        $('.list-upload ul').append(li)

        
        let li_element = $('#'+uniq);
        let name = li_element.find('.title strong');
        let size = li_element.find('.size');
        


        var upload_data = new FormData();
        upload_data.append('upload', true);
        upload_data.append('filename', file.name);
        upload_data.append('requirement', file);
        upload_data.append('csrfmiddlewaretoken',csrf_token);



        
        var xhr = new XMLHttpRequest();
        
        //Initialize the request
        xhr.open('POST', upload_url);
        
        xhr.upload.onprogress = (e) =>{
            let li_el = $('#' + uniq);
            let percentage = Math.ceil((e.loaded / e.total) * 100);
            
            li_el.find('.buffer').css('width', percentage + '%');
            li_el.find('.percentage').html(percentage + '%');

            if(e.loaded == e.total){
                
                li_el.find('.completed').css('display', 'flex');
                let remove_btn = li_el.find('.remove');
                remove_btn.css('display', 'flex');
                remove_btn.on('click', e => {
                    
                    let data = new FormData();

                    data.append('remove', true);
                    data.append('filename', file.name);
                    data.append('csrfmiddlewaretoken', csrf_token);

                    let _xhr = new XMLHttpRequest();

                    _xhr.open('POST', remove_url);

                    _xhr.onload = (e) =>{
                        console.log(xhr.responseText);
                        if(_xhr.status == 200){
                            li_el.remove();
                        }
                        
                    };
                    
                    _xhr.onerror = (e) =>{
                        console.log('ERROR',e)
                    }
                    _xhr.send(data);
                });
            }
            
        }

        xhr.onload = (e) =>{
            if(xhr.status == 200){
                const response = JSON.parse(xhr.responseText);
                console.log(response.image_pk, file.name);
                
            }
            
        }
        xhr.send(upload_data);
        
    }

});