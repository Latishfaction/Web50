document.addEventListener('DOMContentLoaded', function () {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector("#compose-form").onsubmit = send_mail;
  
  
  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
  document.querySelector('#view-email').innerHTML = '';
}

function load_mailbox(mailbox) {
  // create a ul
  let ul = document.createElement("ul");
  ul.className = "emails";
  
  // fetch the email inbox
  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(data => {
      // for each of the mail entry
      data.forEach(email => {
        // create li
        const element = document.createElement('div');

        if(mailbox=="sent"){
          element.innerHTML = `${email.recipients} ${email.subject} ${email.timestamp}`;
        }
        else{
          element.innerHTML = `${email.sender} ${email.subject} ${email.timestamp}`;
        }
        element.addEventListener('click', function() {
            view_mail(email.id);
        });
        // document.querySelector('#container').append(element);
        document.querySelector("#emails-view").append(element);
        document.querySelector('#view-email').innerHTML = '';
      })
    })
    .catch(exception => {
      console.log("Error", exception);
    });


  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#view-email').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}

function send_mail() {
  // get the data fields from the 

  // fetch POST requests and put the data fields in the 
  fetch("/emails", {
    method: 'POST',
    body: JSON.stringify({
      recipients: document.querySelector("#compose-recipients").value,
      subject: document.querySelector("#compose-subject").value,
      body: document.querySelector("#compose-body").value,
    })
  }).then(response => response.json())
    .then(result => {
      console.log(result);
    }).catch(error => {
      alert("Error : ", error);
    })
  // redirect to the 'sent' page
  load_mailbox('sent');

  alert("done");
  return false;
}

function view_mail(email_id){
    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector("#view-email").style.display='block';

  // fetch the request by giving email_id
  fetch(`/emails/${email_id}`)
  .then(response=>response.json())
  .then(email=>{
    let div = document.createElement('div');
    div.className="email_content_container";
    let elem_sender = document.createElement('h5');
    let elem_recipients = document.createElement('h6');
    let elem_subject = document.createElement('p');
    let elem_timestamp = document.createElement('span');
    let elem_body = document.createElement('p');

    elem_sender.innerHTML = email.sender;
    email.recipients.forEach(emails=>{
      elem_recipients.append(emails);
    })
    document.querySelector("#view-email").append(div);

    elem_subject.innerHTML = email.subject;
    elem_timestamp.innerHTML = email.timestamp;
    elem_body.innerHTML = email.body;

    //get the div
    document.querySelector(".email_content_container").appendChild(elem_sender);
    document.querySelector(".email_content_container").appendChild(elem_recipients);
    document.querySelector(".email_content_container").appendChild(elem_subject);
    document.querySelector(".email_content_container").appendChild(elem_timestamp);
    document.querySelector(".email_content_container").appendChild(elem_body);
  })
  .catch(error=>{
    // alert("Error : ",error);
    console.log(error);
  });
}