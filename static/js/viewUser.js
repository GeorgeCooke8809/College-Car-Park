function hideFunctionalButtons(){
    const nonFunctional = document.querySelectorAll('.non-functional-buttons')
    nonFunctional.forEach(element => {
        element.style.display = 'block'
    });

    const functional = document.querySelectorAll('.functional-buttons')
    functional.forEach(element => {
        element.style.display = 'none'
    });
}

function showFunctionalButtons(){
    const nonFunctional = document.querySelectorAll('.non-functional-buttons')
    nonFunctional.forEach(element => {
        element.style.display = 'none'
    });

    const functional = document.querySelectorAll('.functional-buttons')
    functional.forEach(element => {
        element.style.display = 'block'
    });
}

function showEditUsers(){
    const window = document.querySelector('#edit-user-window')
    window.style.display = 'flex'

    hideFunctionalButtons()
}

function hideEditUsers(){
    const window = document.querySelector('#edit-user-window')
    window.style.display = 'none'

    showFunctionalButtons()
} 

function showContact(){
    const window = document.querySelector('#contact-window')
    window.style.display = 'flex'
    
    hideFunctionalButtons()
}

function hideContact(){
    const window = document.querySelector('#contact-window')
    window.style.display = 'none'
    
    showFunctionalButtons()
}

function showBooking(){
    const window = document.querySelector('#add-booking-type-window')
    window.style.display = 'flex'
    
    hideFunctionalButtons()
}

function hideBooking(){
    const window = document.querySelector('#add-booking-type-window')
    window.style.display = 'none'

    const dayPassWindow = document.querySelector('#add-day-pass-window')
    dayPassWindow.style.display = 'none'

    const seasonPassWindow = document.querySelector('#add-season-pass-window')
    seasonPassWindow.style.display = 'none'

    const unlimitedPassWindow = document.querySelector('#add-unlimited-pass-window')
    unlimitedPassWindow.style.display = 'none'
    
    showFunctionalButtons()
}

function showDayPassBooking(){
    const oldWindow = document.querySelector('#add-booking-type-window')
    oldWindow.style.display = 'none'
    
    const newWindow = document.querySelector('#add-day-pass-window')
    newWindow.style.display = 'flex'
}

function showSeasonPassBooking(){
    const oldWindow = document.querySelector('#add-booking-type-window')
    oldWindow.style.display = 'none'
    
    const newWindow = document.querySelector('#add-season-pass-window')
    newWindow.style.display = 'flex'
}

function showUnlimitedPassBooking(){
    const oldWindow = document.querySelector('#add-booking-type-window')
    oldWindow.style.display = 'none'
    
    const newWindow = document.querySelector('#add-unlimited-pass-window')
    newWindow.style.display = 'flex'
}