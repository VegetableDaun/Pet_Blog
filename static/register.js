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
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                const error = await response.json();
                message.style.color = "red";
                message.textContent = error.detail || "Registration failed.";
            } else {
                const result = await response.json();
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
