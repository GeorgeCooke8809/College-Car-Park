function showEditSpaces(){
    const closeButton = document.querySelector('.close-button')
    closeButton.style.display = 'flex'

    const editButton = document.querySelector('.edit-button')
    editButton.style.display = 'none'

    const inUseDiv = document.querySelector('#spaces-in-use-form')
    inUseDiv.style.display = 'flex'
}

function hideEditSpaces(){
    const closeButton = document.querySelector('.close-button')
    closeButton.style.display = 'none'

    const editButton = document.querySelector('.edit-button')
    editButton.style.display = 'flex'

    const inUseDiv = document.querySelector('#spaces-in-use-form')
    inUseDiv.style.display = 'none'
}