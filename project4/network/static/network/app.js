let form;
document.addEventListener('DOMContentLoaded', () => {
  form = document.querySelector("#new-post__form");
  document.querySelector("#user").addEventListener("click", () => load_page("profile"));
  document.querySelector("#all-posts").addEventListener("click", () => load_page("all"));
  document.querySelector("#following").addEventListener("click", () => load_page("following"));

  form.addEventListener("submit", (e) => {
    send_post(e);
  })

  load_page("all");
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
  }
  catch (err) {
    console.error("unexpected error when sending post:",err);
  }
}

async function load_page(pageType) {
  document.querySelector("#new-post").style.display = "none";
  document.querySelector("#profile").style.display = "none";
  document.querySelector("#posts-view").style.display = "block";

  if (pageType == "all") {
    document.querySelector("#new-post").style.display = "block";
  }

  if (pageType === "profile") 
  {
    const profile = document.querySelector("#profile");
    const username = profile.dataset.username;
    /** datas we need to fetch are :
     * - number of followers
     * - number of following
     * - is_user (?) for displaying follow/unfollow button
    */
    fetch(`profile/${username}`)
    .then(res => res.json())
    .then(() => {
      console.log(res);
    });


    profile.style.display = "block";
    profile.innerHTML = `
    <h1>${username}</h1>
    Followers :
    Following :
    <p>Your posts: </p>`;
  }

  try {
    //query for all posts
    // const res = await fetch(`load_posts/${pageType}`)
    const res = await fetch(`load_posts/all`)
    if (!res.ok) {
      throw new Error(`Response status: ${res.status}`)
    }
    const posts = await res.json();
    
    display_posts(posts);
  }
  catch (err) {
    console.error("Unexpected error when fetching posts:",err);
  }
}

function display_posts(posts) {
  const view = document.querySelector("#posts-view");
  for (const post of posts) {
    const postElement = document.createElement("div");
    const userElement = document.createElement("div");
    const textElement = document.createElement("p");
    const timeElement = document.createElement("div");
    const likeCounterElement = document.createElement("div");
    
    postElement.classList.add("post");
    postElement.id = `post-${post.id}`
    
    userElement.classList.add("post-user");
    userElement.textContent = post.user;

    textElement.classList.add("post-text");
    textElement.textContent = post.content;

    timeElement.classList.add("post-time");
    timeElement.textContent = post.timestamp;

    likeCounterElement.classList.add("post-likes");
    likeCounterElement.textContent = post.likes + " likes";

    postElement.appendChild(userElement);
    postElement.appendChild(textElement);
    postElement.appendChild(timeElement);
    postElement.appendChild(likeCounterElement);
    view.appendChild(postElement);
  }
}