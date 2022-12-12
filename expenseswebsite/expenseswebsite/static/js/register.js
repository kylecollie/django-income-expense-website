const usernameField = document.querySelector("#usernameField");
const usernameFeedbackArea = document.querySelector(".usernameFeedbackArea");
const emailField = document.querySelector("#emailField");
const emailFeedbackArea = document.querySelector(".emailFeedbackArea");
const usernameSuccessOutput = document.querySelector(".usernameSuccessOutput");
const emailSuccessOutput = document.querySelector(".emailSuccessOutput");

emailField.addEventListener("keyup", (e) => {
  const emailValue = e.target.value;

  emailSuccessOutput.style.display = "block";
  emailSuccessOutput.textContent = `Checking ${emailValue}`;

  emailField.classList.remove("is-invalid");
  emailFeedbackArea.style.display = "none";

  if (emailValue.length > 0) {
    fetch("/authentication/validate-email", {
      body: JSON.stringify({ email: emailValue }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        emailSuccessOutput.style.display = "none";
        if (data.email_error) {
          emailField.classList.add("is-invalid");
          emailFeedbackArea.style.display = "block";
          emailFeedbackArea.innerHTML = `<p>${data.email_error}</p>`;
        }
      });
  }
});

usernameField.addEventListener("keyup", (e) => {
  const usernameValue = e.target.value;

  usernameSuccessOutput.style.display = "block";
  usernameSuccessOutput.textContent = `Checking ${usernameValue}`;

  usernameField.classList.remove("is-invalid");
  usernameFeedbackArea.style.display = "none";

  if (usernameValue.length > 0) {
    fetch("/authentication/validate-username", {
      body: JSON.stringify({ username: usernameValue }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        usernameSuccessOutput.style.display = "none";
        if (data.username_error) {
          usernameField.classList.add("is-invalid");
          usernameFeedbackArea.style.display = "block";
          usernameFeedbackArea.innerHTML = `<p>${data.username_error}</p>`;
        }
      });
  }
});
