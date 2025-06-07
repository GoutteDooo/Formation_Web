let form,user_connected,userId;
document.addEventListener('DOMContentLoaded', () => {
  if (document.querySelector("#user")) user_connected = true;
  if (user_connected)
  {
    form = document.querySelector("#new-post__form");
    userId = document.querySelector("#user").dataset.userId; 
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
  if (user_connected) {
    document.querySelector("#new-post").style.display = "none";
    document.querySelector("#profile-view").style.display = "none";
  }
  document.querySelector("#posts-view").style.display = "flex";

  if (pageType.startsWith("all") && user_connected) {
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
      
      profileView.innerHTML = `
      <h1>${data.profile_name}</h1>
      Followers : ${data.followers_count}
      Following : ${data.following_count}
      ${data.following_button == true ? `<button id="follow-btn">Unfollow</button>` : data.following_button == false ? `<button id="follow-btn">Follow</button>` : ""}
      <p>Your posts: </p>`;

      profileView.style.display = "block";
      profileView.setAttribute("data-profile-id",data.profile_id);

      if (document.querySelector("#follow-btn")) {
        document.querySelector("#follow-btn").addEventListener("click", follow);
      }
    }
    catch (err)
    {
      console.error(err);
    }
  }

  /* query for all posts */
  load_posts(pageType)
}

const load_posts = async (pageType, page = 1) => {
  try {
    const res = await fetch(`load_posts/${pageType}?page=${page}`)
    if (!res.ok) {
      throw new Error(`Response status: ${res.status}`)
    }
    const data = await res.json();
    generate_posts(pageType, data);
  }
  catch (err) {
    console.error("Unexpected error when fetching posts:",err);
  }
}

function generate_posts(pageType, posts_data) {
  const view = document.querySelector("#posts-view");
  view.innerHTML = "";
  console.log("posts:",posts_data);
  
  for (const post of posts_data.posts) {
    const postElement = document.createElement("div");
    const topElements = document.createElement("div");
    const userElement = document.createElement("div");
    const textElement = document.createElement("p");
    const bottomElements = document.createElement("div");
    const timeElement = document.createElement("div");
    const likeCounterElement = document.createElement("div");
    
    postElement.classList.add("post");
    postElement.id = `post-${post.id}`
    postElement.setAttribute("data-user-id", post.user_id);
    
    
    userElement.classList.add("post-user");
    userElement.textContent = post.user;
    userElement.addEventListener("click", () => load_page(`profile-${post.user_id}`));
    
    topElements.classList.add("post-top");
    topElements.appendChild(userElement);
    topElements.appendChild(userElement);

    if (post.user_id == userId) {
      const editButton = document.createElement("button");
      editButton.classList.add("post-edit");
      editButton.textContent = "Editer";
      editButton.onclick = () => edit_post(postElement);
      topElements.appendChild(editButton);
    }

    textElement.classList.add("post-text");
    textElement.textContent = post.content;

    bottomElements.classList.add("post-bottom");
    timeElement.classList.add("post-time");
    timeElement.textContent = post.timestamp;
    
    likeCounterElement.classList.add("post-likes");
    likeCounterElement.textContent = post.likes + " likes";
    bottomElements.appendChild(timeElement);
    if (user_connected) {
      const likeButton = document.createElement("button");
      likeButton.textContent = `TODO`;
      likeButton.classList.add("post-like__button");
      likeButton.onclick = () => like_post(post);
      bottomElements.appendChild(likeButton);
    }
    bottomElements.appendChild(likeCounterElement);

    postElement.appendChild(topElements);
    postElement.appendChild(textElement);
    postElement.appendChild(bottomElements);
    view.appendChild(postElement);
  }

    // Add buttons or links for navigation
    if (posts_data.has_next) {
      const next = document.createElement("button");
      next.textContent = "next";
      next.onclick = () => load_posts(pageType, posts_data.current_page + 1)
      document.querySelector("#posts-view").append(next);
    }

    if (posts_data.has_previous) {
      const prev = document.createElement("button");
      prev.textContent = "previous";
      prev.onclick = () => load_posts(pageType, posts_data.current_page - 1)
      document.querySelector("#posts-view").append(prev);
    }

    window.scrollTo(0,0)
}

const edit_post = (post, edit=true) => {
  const editButton = post.querySelector(".post-edit"),
  editBtnClone = editButton.cloneNode(true);
  editButton.parentNode.replaceChild(editBtnClone, editButton);
  if (edit) {
    editBtnClone.textContent = "Save";
    editBtnClone.onclick = () => edit_post(post, false);
    
    //replace content by textarea while editing
    const content = post.querySelector(".post-text");
    content.style.display = "none";
    const textArea = document.createElement("textarea");
    textArea.value = content.textContent; 
    textArea.classList.add("post-edit__text");
    post.appendChild(textArea);

  } else {
    editBtnClone.textContent = "Editer";
    editBtnClone.onclick = () => edit_post(post);
    const textArea = document.querySelector(".post-edit__text");
    const registeredText = textArea.value;
    textArea.remove();
    const content = post.querySelector(".post-text");
    content.style.display = "block";

    const postId = post.id.split("-")[1];
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(`edit_post/${postId}`, {
      method:"PATCH",
      headers: { "X-CSRFToken": csrfToken },
      body: JSON.stringify({
        registeredText
      })
    })
    .then((r) => r.json())
    .then((data) => {
      content.textContent = data.edited_text;
    })
    .catch((err) => {
      console.error("error when editing post: ", err);
    })
  }

}

const follow = async () => {
  const profileId = document.querySelector("#profile-view").getAttribute("data-profile-id");

  const csrftoken = getCookie("csrftoken");

  await fetch(`follow/${profileId}`, {
    method:"POST",
    headers: {
      "Content-Type":"applications/json",
      "X-CSRFToken":csrftoken,
    },
    body:{
      profile_id: profileId,
    },
    credentials: "same-origin"
  })
  .then((r) => r.json())
  .then((data) => {
    console.log(data);
    const followBtn = document.querySelector("#follow-btn")
    followBtn.textContent = data.toggle ? "Follow": "Unfollow";
    load_page(`profile-${profileId}`)

  })
  .catch(err => {
    console.error("erreur lors de la requête follow:",err);
  })
}

const like_post = (post) => {
  console.log("post:",post);
  const csrftoken = getCookie("csrftoken");
  fetch(`like_post/${post.id}`, {
    method:"POST",
    headers: {
      "Content-Type":"applications/json",
      "X-CSRFToken":csrftoken,
    },
    body:{
      post_id:post.id
    }
  })
  .then(r => r.json())
  .then((data) => {
    console.log(data);
    document.querySelector(`#post-${post.id}`).style.color = "blue";
    
  })
  .catch(err => {
    console.error("error when like:", err);
  })
}


/* Helpers */
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");

    for (let cookie of cookies) {
      cookie = cookie.trim();
      // Vérifie si le cookie commence par le bon nom
      if (cookie.substring(0, name.length + 1) === `${name}=`) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}