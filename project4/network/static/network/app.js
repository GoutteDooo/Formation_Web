document.addEventListener('DOMContentLoaded', () => {
  const submitPost = document.querySelector("#new-post__form");


  submitPost.addEventListener("submit", (e) => {
    e.preventDefault();
    fetch("new_post/", () => {
      
    }
  })
})