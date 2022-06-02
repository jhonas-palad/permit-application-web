let next = $('button[name=next]');
let prev = $('button[name=prev]');
let current_page = $('#current-page');
let prev_group = $('#prev-group');
let next_group = $('#next-group');
let application_list = $('#application-list');
let loader = $('.loader');
const is_staff = window.location.pathname == '/staff/';

console.log(loader);
const get_page = (page,btn) => {

    loader.css('opacity',1);
    application_list.empty();
    url = `${window.location.href}?page=${page}`
    let xhr = new XMLHttpRequest()
    console.log(page);
    xhr.open('GET', url)
    xhr.onprogress = (e) =>{
        if (e.loaded === e.total){
            loader.css('opacity', 0);
        }
    }
    xhr.onload = (e) =>{
        
        if(xhr.status == 200){
            response = JSON.parse(xhr.responseText);

            for(var i = 0; i < response.len ; i++){
                let data = response[i];
                console.log(data);
                const index = data.index;
                const pk = data.pk;
                const name = data.name;
                const date = data.submission_datetime[0];
                const time = data.submission_datetime[1];
                const status_cls = data.status[0];
                const status = data.status[1];

                let div = document.createElement('div');
                div.classList.add('row-card');
                div.classList.add('data');

                const data_col1 = create_data_col(false, [index]);
                const data_col2 = create_data_col(false, [name]);
                const data_col3 = create_data_col(true, [date, time]);
                let data_col4 = create_data_col(false, [status]);
                data_col4.classList.add(status_cls);
                

                div.appendChild(data_col1);
                div.appendChild(data_col2);
                div.appendChild(data_col3);
                div.appendChild(data_col4);
                
                let data_col5 = document.createElement('div');
                data_col5.classList.add('data-col');

                let a = document.createElement('a');
                a.classList.add('button-data-col');
                if (is_staff){
                    a.setAttribute('href', window.location.origin + `/staff/view-application/${pk}`);
                    a.innerHTML = 'Evaluate';
                }else{
                    a.setAttribute('href', window.location.origin + `/client/permit-application/summary/${pk}`);
                    a.innerHTML = 'View';
                }

                data_col5.appendChild(a);
                div.appendChild(data_col5);

                application_list.append(div);
                
            }

            current_page.html(page);
            if(response.has_prev){
                prev_group.removeClass('hidden');
                prev.attr('page', response.prev_page);
            }else{
                prev_group.addClass('hidden');
            }

            if(response.has_next){
                next_group.removeClass('hidden');
                next.attr('page', response.next_page);
            }else{
                next_group.addClass('hidden');
            }
            

            console.log(response);

        }
        
    }

    xhr.send();

}

const get_application = (pk) => {
    console.log(pk);
}


const create_data_col = (is_third_col, values) =>{
    let div = document.createElement('div');
    div.classList.add('data-col');
    
    let p1 = document.createElement('p');
    if (is_third_col){
        console.log("ASDASD");
        p1.classList.add('date');
        
        let p2 = document.createElement('p');
        p2.classList.add('time');
        
        p1.innerHTML = values[0];
        p2.innerHTML = values[1];

        div.appendChild(p1);
        div.appendChild(p2);
        
    }else{
        p1.innerHTML = values[0];
        div.appendChild(p1);
    }
    
    
    return div;

    
   
  

}