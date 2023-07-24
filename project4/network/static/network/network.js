function submit_handler(){
    const edited_content = document.querySelector('#edited-post').value;
    const id = document.querySelector('#button-edit').dataset.id;
    console.log(edited_content);
    fetch(`edit/${id}`, {
        method: 'POST',
        body: JSON.stringify({
            edited_post: edited_content,
        })
    })
    .then(response => response.json())
    .then(json => console.log(json))
    document.querySelector(`#button-close-${id}`).click();
    document.querySelector(`#post-content-${id}`).innerHTML = edited_content;
}



    


