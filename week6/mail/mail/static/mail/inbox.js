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
}

function load_mailbox(mailbox) {
  // get the div
  let email_view = document.querySelector("#emails-view");
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
        let li = document.createElement("li");
        // create anchor
        let a = document.createElement("a");
        a.className = "email-item";
        a.id = `${email.id}`;
        // add sender mail,subject and timestamp in the anchor tag
        if(mailbox=="sent"){
          a.innerHTML = `${email.recipients} ${email.subject} ${email.timestamp}`;
        }
        else{
          a.innerHTML = `${email.sender} ${email.subject} ${email.timestamp}`;
        }
        
        li.append(a);
        console.log(a);
        ul.append(li);
        email_view.append(ul);
        // append anchor to li
        // append li to ul
      })
    })
    .catch(exception => {
      console.log("Error", exception);
    });


  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}

function send_mail() {
  // get the data fields from the 
  // this.preventDefault();
  let peoples = document.querySelector("#compose-recipients").value;
  let sub = document.querySelector("#compose-subject").value;
  let msg = document.querySelector("#compose-body").value;

  console.log(peoples);
  console.log(sub);
  console.log(msg);
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