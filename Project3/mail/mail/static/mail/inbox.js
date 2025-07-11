let formElement, emailView, infoElement;
document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  formElement = document.querySelector("#compose-form");
  emailView = document.querySelector("#emails-view");
  infoElement = document.querySelector("#user-info");
  
  formElement.addEventListener("submit", (e) => {
    e.preventDefault();
    send_mail();
  });
});

function compose_email(e,mailData = null) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = `${mailData ? mailData.sender : ""}`;
  document.querySelector('#compose-subject').value = `${mailData ? displaySubject(mailData.subject) : ""}`;
  document.querySelector('#compose-body').value = `${mailData ? displayBody(mailData) : ""}`;
  infoElement.textContent = "";

}

async function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  //Make a get request for the current mailbox
  try {
    const response = await fetch(`emails/${mailbox}`);
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }
    const mails = await response.json();
    display_mails(mails,mailbox);
  }
  catch (error) {
    console.error("unexpected error:",error);
  }
}

async function send_mail() {

  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;
  console.log("body:",body);
  

  try 
  {
    const response = await fetch("/emails", {
      method: "POST",
      headers:{
        "Content-Type":"application/json"
      },
      body: JSON.stringify({recipients,subject,body}),
    });

    const data = await response.json();
    
    if (response.ok)
    {
      compose_email();
      infoElement.textContent = data.message;
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

function display_mails(mails, mailbox) {
  const archivingBtn = mailbox != "sent";
  let displaying = "";
  for (let i = 0, len = mails.length; i < len; i++)
  {
    let color;
    if (mails[i].read) color = "grey";
    displaying += `
    <div class="mail-envelope" style="color:${color}">
      <div class="mail-envelope-container" id=mail-${mails[i].id}>
        ${mailbox === "sent" ? `<h4>to: ${displayRecipients(mails[i].recipients)}</h4>` : `<h4>from: ${mails[i].sender}</h4>`}
        <h3><b>subject:</b> ${mails[i].subject}</h3>
        <p>${mails[i].body.slice(0,40)}(...)</p>
        <em>${mails[i].timestamp}</em>
      </div>
    <div class="mail-envelope-buttons">
      ${archivingBtn ? generateArchiveBtn(mails[i].archived) : ""}
    </div>
    </div>`
  }

  emailView.innerHTML = displaying;
  /* create event handlers */
  //attach event handler to view mails
  emailView.querySelectorAll(".mail-envelope-container").forEach(mail => {
    mail.addEventListener("click", () => view_email(mail))
  });
  //to archive
  emailView.querySelectorAll(".archive-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const emailId = btn.parentNode.previousElementSibling.id.slice(5);
      const mailData = mails.find(m => m.id === +emailId);
      archive(emailId, mailData);
    })
  })
}

async function view_email(mailElement) {
  console.log(mailElement.id.slice(5));
  const id = mailElement.id.slice(5);
  try {
    const response = await fetch(`emails/${id}`)
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }
    const mailData = await response.json();
    console.log("mail view:",mailData);
    emailView.innerHTML = `
      <div class="single-mail">
        <div class="sm-time">received ${displayTime(mailData.timestamp)}</div>
        <div class="sm-sender"><em>from:</em> <b>${mailData.sender}</b></div>
        <div class="sm-recipients"><em>to:</em> <b>${displayRecipients(mailData.recipients)}</b></div>
        <div class="sm-subject"><em>subject:</em> <b>${mailData.subject}</b></div>
        <button class="sm-reply">Reply</button>
        <div class="sm-body">${displayHTMLBody(mailData.body)}</div>
      </div>
    `
    document.querySelector(".sm-reply").addEventListener("click", (e) => compose_email(e,mailData))
  }
  catch (error) {
    console.error("Unexpected error when fetch mail: ",error);
  }

  //mark the mail as read
  try {
    const res = await fetch(`emails/${id}`, {
      method:"PUT",
      body: JSON.stringify({
        read:true,
      })
    })
  }
  catch (err) {
    console.error("unexpected error when trying to mark mail as read:",err);
    
  }
}

async function archive(emailId, mail) {
      console.log("mail archived:", mail);
      if (mail.archived) {
        console.log("unarchived");
      }
      
      try {
        const res = await fetch(`emails/${emailId}`, {
          method:"PUT",
          body:JSON.stringify({
            archived:!mail.archived,
          })
        });
        load_mailbox(mail.archived ? "archive" : "inbox");
    }
    catch (err) {
      console.error("unexpected error when trying to trigger archive button:", err);
      
    }
}

/* Helpers functions */

function displayRecipients(rec) {
  return rec.length > 1 ? rec.split(", ") : rec[0];
}

function displaySubject(subject) {
  console.log(subject.slice(0,4));
  
  return subject.slice(0,4) == "Re: " ? subject : `Re: ${subject}`;
}

function displayTime(timestamp) {
  /**
   * This function is used to timestamp to local UTC datetime
   * BUT it needs to be implemented
   */

  return timestamp;
}

function displayBody(mail) {
  return `\n
  ----------
  On ${mail.timestamp}, ${mail.sender} wrote: \n
  ${mail.body}`
}

function displayHTMLBody(body) {
  return body.split("\n").join("<br />");
  
}

function generateArchiveBtn(isArchived) {
  const text = isArchived ? "unarchive" : "archive";
  return `<button class="archive-btn">${text}</button>`;
  
}