let form;
document.addEventListener('DOMContentLoaded', () => {
  form = document.querySelector("#new-post__form");

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    send_post(e);
  })
})

async function send_post(e) {
  const url = form.dataset.url;
  const content = e.target[1].value;
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

  const data = new FormData();
  data.append('content', content);

  try {
    const res = await fetch(url, {
      method:"POST",
      headers: { "X-CSRFToken": csrfToken },
      body: data,
    });
    
    const json = await res.json();
    const message = document.querySelector("#message")
    message.textContent = json.message;
    if (res.ok) {
      message.classList.add("alert");
      message.classList.add("alert-success");
    }
    else {
      message.classList.add("alert");
      message.classList.add("alert-danger");

    }
  }
  catch (err) {
    console.error("unexpected error when sending post:",err);
  }
}