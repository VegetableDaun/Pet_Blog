document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("signup-form");
    const message = document.getElementById("signup-message");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const data = {
            username: document.getElementById("username").value,
            email: document.getElementById("email").value,
            password: document.getElementById("password").value
        };

        try {
            const response = await fetch("/signup", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                credentials: "include", // Allow cookies to be set
                body: JSON.stringify(data)
            });

            if (response.redirected) {
                window.location.href = response.url; // Follow server-side redirect
                return;
            }

            const result = await response.json();

            if (!response.ok) {
                message.style.color = "red";
                message.textContent = result.detail || "Registration failed.";
            } else {
                message.style.color = "green";
                message.textContent = "Signed up successfully!";
                form.reset();
            }
        } catch (err) {
            message.style.color = "red";
            message.textContent = "Error submitting form.";
        }
    });
});
