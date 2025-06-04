let form;
document.addEventListener('DOMContentLoaded', () => {
  form = document.querySelector("#new-post__form");

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    send_post(e);
  })
})

async function send_post(datas) {
  const url = form.dataset.url;
  const content = datas.target[1].value;
  try {
    const res = await fetch(url, {
      method:"POST",
      headers:{
        "Content-Type":"application/json"
      },
      body: JSON.stringify({content}),
      credentials: 'same-origin',
    });
    // console.log(await res.json());
  }
  catch (err) {
    console.error("unexpected error when sending post:",err);
  }
}