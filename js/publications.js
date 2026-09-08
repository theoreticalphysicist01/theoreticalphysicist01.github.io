document.querySelectorAll(".nav-toggle").forEach(button => {
  button.addEventListener("click", () => {
    const menu = document.getElementById(button.getAttribute("aria-controls"));
    const open = button.getAttribute("aria-expanded") === "true";
    button.setAttribute("aria-expanded", String(!open));
    menu.classList.toggle("open", !open);
  });
});

document.getElementById("year").textContent = new Date().getFullYear();
