document.addEventListener('DOMContentLoaded', () => {
  const submitPost = document.querySelector("#new-post__form");

  submitPost.addEventListener("submit", (e) => {
    e.preventDefault();
    send_post(e);
  })
})

async function send_post(datas) {
  const content = datas.target[1].value;
  try {
    const res = await fetch("new_post/", {
      method:"POST",
      body: JSON.stringify({content})
    });

    console.log(await res.json());
    
  }
  catch (err) {}
}