const slider_names = Array.from($('.slider-name'));
const sliders = Array.from($('.slider'));



$('.slider-names').on('click', e =>{
    if(e.target.matches('[detail]')){
        slider_names[1].setAttribute('clicked', 'false');
        slider_names[0].setAttribute('clicked', 'true');

        sliders[1].classList.remove('active')
        sliders[1].classList.add('hidden');

        sliders[0].classList.remove('hidden')
        sliders[0].classList.add('active');

    }
    else if(e.target.matches('[image]')){
        slider_names[0].setAttribute('clicked', 'false');
        slider_names[1].setAttribute('clicked', 'true');

        sliders[0].classList.remove('active')
        sliders[0].classList.add('hidden');

        sliders[1].classList.remove('hidden')
        sliders[1].classList.add('active');

        
    }
})