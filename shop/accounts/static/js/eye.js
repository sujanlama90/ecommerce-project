function togglePassword(inputId, buttonElement) {
    const input = document.getElementById(inputId);
    const icon = buttonElement.querySelector("i");

    if (!input || !icon) return;

    if (input.type === "password") {
        input.type = "text";
        icon.classList.remove("fa-eye");
        icon.classList.add("fa-eye-slash");
        buttonElement.setAttribute("aria-label", "Hide password");
    } else {
        input.type = "password";
        icon.classList.remove("fa-eye-slash");
        icon.classList.add("fa-eye");
        buttonElement.setAttribute("aria-label", "Show password");
    }
}