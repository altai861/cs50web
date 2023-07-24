document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-detail-view').style.display = 'none';


  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  document.querySelector('#compose-form').addEventListener('submit', ()=>{
    event.preventDefault();
    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;

    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: recipients,
          subject: subject,
          body: body
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
        load_mailbox('sent');
    });
  })
}

function load_mailbox(mailbox) {

  
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-detail-view').style.display = 'none';


  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  if (mailbox === 'inbox'){
    fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      // Print emails  
      emails.forEach(email => {
        const single_email = document.createElement('li');
        single_email.className = 'list-group-item d-flex justify-content-between align-items-start';
        if (email.read == true){
          single_email.style.backgroundColor = '#ffe6e6';
        }else{
          single_email.style.backgroundColor = 'white';
        }
        single_email.innerHTML = `<div class="ms-2 me-auto">
              <div class="fw-bold"><strong>${email["sender"]}</strong></div>
                ${email["subject"]}
              </div>
              <span class="badge bg-primary rounded-pill">${email["timestamp"]}</span>`;
        single_email.addEventListener('click', function(){
          view_email(email.id);
        });
        document.querySelector('#emails-view').append(single_email);
      });
    });
  }
  else if(mailbox === 'sent'){
    fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      // Print emails  
      emails.forEach(email => {
        const single_email = document.createElement('li');
        single_email.className = 'list-group-item d-flex justify-content-between align-items-start';
        
        
        single_email.innerHTML = `<div class="ms-2 me-auto">
              <div class="fw-bold"><strong>${email["sender"]}</strong></div>
                ${email["subject"]}
              </div>
              <span class="badge bg-primary rounded-pill">${email["timestamp"]}</span>`;
        single_email.addEventListener('click', function(){
          view_sent_email(email.id);
        });
        document.querySelector('#emails-view').append(single_email);
      });
    });
  }
  else if (mailbox === 'archive'){
    fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      // Print emails  
      emails.forEach(email => {
        const single_email = document.createElement('li');
        single_email.className = 'list-group-item d-flex justify-content-between align-items-start';
        if (email.read == true){
          single_email.style.backgroundColor = '#ffe6e6';
        }else{
          single_email.style.backgroundColor = 'white';
        }
        single_email.innerHTML = `<div class="ms-2 me-auto">
              <div class="fw-bold"><strong>${email["sender"]}</strong></div>
                ${email["subject"]}
              </div>
              <span class="badge bg-primary rounded-pill">${email["timestamp"]}</span>`;
        single_email.addEventListener('click', function(){
          view_archive_email(email.id);
        });
        document.querySelector('#emails-view').append(single_email);
      });
    });
  }
  
      // ... do something else with emails ...
}


function view_archive_email(id){
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-detail-view').style.display = 'block';

  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
      // Print email
      
      document.querySelector('#email-detail-view').innerHTML = `<div><strong>From:</strong> ${email.sender}</div>
      <div><strong>To:</strong> ${email.recipients}</div>
      <div><strong>Subject:</strong> ${email.subject}</div>
      <div><strong>Time:</strong> ${email.timestamp}</div>      
      <hr>
      <div style="font-size: 40px">${email.body}</div>
      `;
      const archive_button = document.createElement('button');
      archive_button.innerHTML = 'Unarchive';
      archive_button.className = 'btn btn-danger'
      
      archive_button.addEventListener('click', function() {
        fetch(`/emails/${id}`, {
          method: 'PUT',
          body: JSON.stringify({
              archived: false
          })
          
        })
        location.reload();
        load_mailbox('inbox');
      });
      document.querySelector('#email-detail-view').append(archive_button);
      
      console.log(email);

      // ... do something else with email ...
  });

}



function view_email(id){
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-detail-view').style.display = 'block';

  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })

  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
      // Print email
      
      document.querySelector('#email-detail-view').innerHTML = `<div><strong>From:</strong> ${email.sender}</div>
      <div><strong>To:</strong> ${email.recipients}</div>
      <div><strong>Subject:</strong> ${email.subject}</div>
      <div><strong>Time:</strong> ${email.timestamp}</div>      
      <hr>
      <div style="font-size: 40px">${email.body}</div>
      `;
      const archive_button = document.createElement('button');
      archive_button.innerHTML = 'Archive';
      archive_button.className = 'btn btn-success';
      
      archive_button.addEventListener('click', function() {
        fetch(`/emails/${id}`, {
          method: 'PUT',
          body: JSON.stringify({
              archived: true
          })
          
        })
        location.reload();
        load_mailbox('inbox');
      });
      document.querySelector('#email-detail-view').append(archive_button);

      const reply_button = document.createElement('button');
      reply_button.innerHTML = 'Reply';
      reply_button.className = 'btn btn-primary';
      
      reply_button.addEventListener('click', function() {
        compose_email();
        document.querySelector('#compose-recipients').value = `${email.sender}`;
        let first_word = email.subject.split(" ", 1);
        console.log(first_word);
        if (first_word[0] === 'Re:'){
          document.querySelector('#compose-subject').value = `${email.subject}`;
        }
        else{
          document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
        }
        document.querySelector('#compose-body').value = `On ${email.timestamp}, ${email.sender} wrote: ${email.body}`;
      });
      document.querySelector('#email-detail-view').append(reply_button);
      
      console.log(email);

      // ... do something else with email ...
  });
}


function view_sent_email(id){
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-detail-view').style.display = 'block';



  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
      // Print email
      
      document.querySelector('#email-detail-view').innerHTML = `<div><strong>From:</strong> ${email.sender}</div>
      <div><strong>To:</strong> ${email.recipients}</div>
      <div><strong>Subject:</strong> ${email.subject}</div>
      <div><strong>Time:</strong> ${email.timestamp}</div>      
      <hr>
      <div style="font-size: 40px">${email.body}</div>`;
      console.log(email);

      // ... do something else with email ...
  });
}