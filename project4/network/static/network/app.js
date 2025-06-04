let form;
document.addEventListener('DOMContentLoaded', () => {
  form = document.querySelector("#new-post__form");
  document.querySelector("#user").addEventListener("click", () => load_posts("user"));
  document.querySelector("#all-posts").addEventListener("click", () => load_posts("all"));
  document.querySelector("#following").addEventListener("click", () => load_posts("following"));

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    send_post(e);
  })

  load_posts("all");
})

async function send_post(e) {
  const url = form.dataset.url;
  let content = e.target[1].value;
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
    //remove text written by user
    document.querySelector("#id_content").value = "";
  }
  catch (err) {
    console.error("unexpected error when sending post:",err);
  }
}

async function load_posts(postsType) {
  document.querySelector("#new-post").style.display = "none";
  document.querySelector("#posts-view").style.display = "block";
  if (postsType == "all") {
    document.querySelector("#new-post").style.display = "block";
    try {
      //query for all posts
      const res = await fetch(`load_posts/${postsType}`)
      if (!res.ok) {
        throw new Error(`Response status: ${res.status}`)
      }
      const posts = await res.json();
      console.log("fetching posts success");
      
      display_posts(posts);
    }
    catch (err) {
      console.error("Unexpected error when fetching posts:",err);
    }
  }
}

function display_posts(posts) {
  const view = document.querySelector("#posts-view");
  for (const post of posts) {
    console.log(post);
    const newPost = document.createElement("div");
    newPost.classList.add("post");
    newPost.id = `post-${post.id}`
    newPost.textContent = post.content;
    view.appendChild(newPost);
  }
}