function showBooking(){
    const window = document.querySelector('#add-booking-type-window')
    window.style.display = 'flex'
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