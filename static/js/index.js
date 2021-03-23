let add_icon = document.getElementById("add-todo");
let modal = document.getElementById("modal");
let form = document.getElementById("modal-form");
let close_btn = document.getElementById("close-btn");

function show_form() {
  if(form.className == "closed") {
    form.style.top = "15%";
    form.className = "opened";
    modal.classList.add('bg-dark');
  }
}

function hide_form() {
  form.style.top = "-800%";
  form.className = "closed";
  modal.classList.remove('bg-dark');
}

add_icon.addEventListener('click', show_form);

close_btn.addEventListener('click', hide_form);

window.addEventListener('click', function(event){
  if(form.className == "opened" && event.target == modal)
    hide_form();
});