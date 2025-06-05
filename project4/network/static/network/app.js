let form;
document.addEventListener('DOMContentLoaded', () => {
  if (document.querySelector("#user"))
  {
    form = document.querySelector("#new-post__form");
    const userId = document.querySelector("#user").dataset.userId; 
    document.querySelector("#user").addEventListener("click", () => load_page(`profile-${userId}`));
    document.querySelector("#following").addEventListener("click", () => load_page("following"));
    form.addEventListener("submit", (e) => {
      send_post(e);
    })
  }
    
  document.querySelector("#all-posts").addEventListener("click", () => load_page("all"));
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
  document.querySelector("#profile-view").style.display = "none";
  document.querySelector("#posts-view").style.display = "block";

  if (pageType == "all") {
    document.querySelector("#new-post").style.display = "block";
  }

  if (pageType.startsWith("profile"))
  {
    const profileView = document.querySelector("#profile-view");
    const userId = pageType.split("-")[1];
    /** datas we need to fetch are :
     * - number of followers
     * - number of following
     * - username for displaying follow/unfollow button
    */
    try {
      //I need to get user id to make a good fetching
      const res = await fetch(`profile/${userId}`)
      const data = await res.json()
      pageType = `profile-${data.profile_id}`;
      console.log("fetching success:",data);
      
      profileView.style.display = "block";
      profileView.innerHTML = `
      <h1>${data.profile_name}</h1>
      Followers : ${data.followers_count}
      Following : ${data.following_count}
      ${data.following_button == true ? `<button>Follow</button>` : data.following_button == false ? "<button>Unfollow</button>" : ""}
      <p>Your posts: </p>`;
    }
    catch (err)
    {
      console.error(err);
    }
  }

  /* query for all posts */
  try {
    console.log("searching for posts... pageType=",pageType);
    
    const res = await fetch(`load_posts/${pageType}`)
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
  view.innerHTML = "";
  console.log("posts:",posts);
  
  for (const post of posts) {
    const postElement = document.createElement("div");
    const userElement = document.createElement("div");
    const textElement = document.createElement("p");
    const timeElement = document.createElement("div");
    const likeCounterElement = document.createElement("div");
    
    postElement.classList.add("post");
    postElement.id = `post-${post.id}`
    postElement.setAttribute("data-user-id", post.user_id);
    
    userElement.classList.add("post-user");
    userElement.textContent = post.user;
    userElement.addEventListener("click", () => load_page(`profile-${post.user_id}`));

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