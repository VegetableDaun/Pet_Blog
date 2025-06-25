document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("signin-form");
    const message = document.getElementById("signin-message");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const data = {
            username: document.getElementById("username").value,
            password: document.getElementById("password").value
        };

        try {
            const response = await fetch("/signin", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                credentials: "include" // Important to allow cookies
            , body: JSON.stringify(data) });

            // If redirect is handled by the browser, no need to parse JSON
            if (response.redirected) {
                window.location.href = response.url; // Follow redirect manually
                return;
            }

            const result = await response.json();

            if (!response.ok) {
                message.style.color = "red";
                message.textContent = result.detail || "Login failed.";
            } else {
                message.style.color = "green";
                message.textContent = "Logged in successfully!";
                form.reset();
            }
        } catch (err) {
            message.style.color = "red";
            message.textContent = "Error submitting form.";
        }
    });
});
