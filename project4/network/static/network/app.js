document.addEventListener('DOMContentLoaded', () => {
  const submitPost = document.querySelector("#new-post__form");

  submitPost.addEventListener("submit", (e) => {
    send_post(e);
  })
})

async function send_post(datas) {
    datas.preventDefault();
  const datas = datas;
  try {
    const res = await fetch("new_post/", {
      method:"POST",
    });
    console.log(datas);
  }
  catch (err) {}
}