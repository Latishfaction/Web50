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

function compose_email(email_details=undefined) {
  // console.log(email_details.isTrusted);
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  if(email_details.isTrusted){
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
    document.querySelector('#view-email').innerHTML = '';
  }
  else{
    fetch(`/emails/${email_details}`)
.then(response => response.json())
.then(email => {
    // Print email
    document.querySelector('#compose-recipients').value = `${email.sender}`;
    document.querySelector('#compose-subject').value = `Re : ${email.subject}`;
    document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote : `+email.body + `<br>------------------------<br>`;
})
.catch((exception)=>{
  console.log("Error",exception);
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
  document.querySelector('#view-email').innerHTML = '';
});
  }
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
        element.className = "mail-entry";
        element.id = email.id;

        if(mailbox=="sent"){
          element.innerHTML = `${email.recipients} ${email.subject} ${email.timestamp}`;
        }
        else{
          element.innerHTML = `${email.sender} ${email.subject} ${email.timestamp}`;
        }
        element.addEventListener('click', function() {
            view_mail(email.id);
        });
        
        // higlighting read and unread mails
        if(email.read){
          // already read
          element.className = "mail-entry-read";
        }
        else{
          // unread
          element.className = "mail-entry";
        }

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
}

function view_mail(email_id){
    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector("#view-email").style.display='block';

  // fetch the request by giving email_id
const read_status={
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  };
  // marking email as read
  fetch(`/emails/${email_id}`,read_status);
  fetch(`/emails/${email_id}`)
  .then(response=>response.json())
  .then(email=>{
    console.log(email);
    // create elements for message storage
    let div = document.createElement('div');
    div.className="email_content_container";

    let elem_sender = document.createElement('h5');
    elem_sender.className = "email_sender";
    
    let elem_recipients = document.createElement('h6');
    elem_recipients.className = "email_receipients";

    let elem_subject = document.createElement('p');
    elem_subject.className = "email_subject";
    
    let elem_timestamp = document.createElement('span');
    elem_timestamp.className ="email_timestap";
    
    let elem_body = document.createElement('p');
    elem_body.className ="email_body";


    // archive btn
    let archive_status_btn = document.createElement("button");
    archive_status_btn.className = "archive_btn";
    if(email.archived){
      archive_status_btn.innerText = "Unarchive";
      archive_status_btn.addEventListener("click",function(){
        archive_status(email.id,false);
      })
    }
    else{
      archive_status_btn.innerText = "Archive";
      archive_status_btn.addEventListener("click",function(){
        archive_status(email.id,true);
      })
    }
    // reply btn
    let reply_btn = document.createElement("button");
    reply_btn.className = "reply_btn";

    reply_btn.innerText = "Reply";
    reply_btn.addEventListener("click",function(){
      // trigger reply 
      reply_mail(email.id);
    })

    // appending list of recipients
    elem_sender.innerHTML = email.sender;
    email.recipients.forEach(emails=>{
      elem_recipients.append(emails);
    })
    // appending div conatiner to view-email
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
    document.querySelector(".email_content_container").appendChild(reply_btn);
    document.querySelector(".email_content_container").appendChild(archive_status_btn);
    
  })
  .catch(error=>{
    // alert("Error : ",error);
    console.log(error);
  });
}

function archive_status(id,isArchived){
  
  if(isArchived){
    fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
          archived: true
      })
    })
  }
  else{
    fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
          archived: false
      })
    })
  }

  load_mailbox('archive');
  document.location.reload();
  
}

function reply_mail(id){
  compose_email(id);
}