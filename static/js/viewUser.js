function showEditUsers(){
    const window = document.querySelector('#edit-user-window')
    window.style.display = 'flex'

    const nonFunctional = document.querySelectorAll('.non-functional-buttons')
    nonFunctional.forEach(element => {
        element.style.display = 'block'
    });

    const functional = document.querySelectorAll('.functional-buttons')
    functional.forEach(element => {
        element.style.display = 'none'
    });
}

function hideEditUsers(){
    const window = document.querySelector('#edit-user-window')
    window.style.display = 'none'

    const nonFunctional = document.querySelectorAll('.non-functional-buttons')
    nonFunctional.forEach(element => {
        element.style.display = 'none'
    });

    const functional = document.querySelectorAll('.functional-buttons')
    functional.forEach(element => {
        element.style.display = 'block'
    });
}

function showContact(){
    const window = document.querySelector('#contact-window')
    window.style.display = 'flex'
    
    const nonFunctional = document.querySelectorAll('.non-functional-buttons')
    nonFunctional.forEach(element => {
        element.style.display = 'block'
    });

    const functional = document.querySelectorAll('.functional-buttons')
    functional.forEach(element => {
        element.style.display = 'none'
    });
}

function hideContact(){
    const window = document.querySelector('#contact-window')
    window.style.display = 'none'
    
    const nonFunctional = document.querySelectorAll('.non-functional-buttons')
    nonFunctional.forEach(element => {
        element.style.display = 'none'
    });

    const functional = document.querySelectorAll('.functional-buttons')
    functional.forEach(element => {
        element.style.display = 'block'
    });
}