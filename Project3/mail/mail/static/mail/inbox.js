let formElement;
document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  formElement = document.querySelector("#compose-form");
  
  formElement.addEventListener("submit", (e) => {
    e.preventDefault();
    send_mail();
  });
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

async function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  //Make a get request for the current mailbox
  try {
    const response = await fetch(`email/${mailbox}`);
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }
    console.log(response.json());
    
  }
  catch (error) {
    console.error("unexpected error:",error);
    
  }
}

async function send_mail() {

  const infoElement = document.querySelector("#user-info");
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  try 
  {
    const response = await fetch("/emails", {
      method: "POST",
      headers:{
        "Content-Type":"application/json"
      },
      body: JSON.stringify({recipients,subject,body}),
    });

    console.log("response status:", response.status);
    const data = await response.json();
    console.log("try works! data:",data);
    
    if (response.ok)
    {
      infoElement.textContent = data.message;
      compose_email();
      infoElement.style.color = "green";
    }
    else
    {
      infoElement.textContent = data.error;
      infoElement.style.color = "red";
    }
  }
  catch (err)
  {
    console.error("Unexpected error:",err);
    infoElement.textContent = "Sorry, an unknown error happened. Please try again.";
    infoElement.style.color = "red";
  }
}