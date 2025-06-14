document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("post-form");
    const message = document.getElementById("post-message");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const data = {
            title: document.getElementById("title").value,
            content: document.getElementById("content").value,
            secret_info: document.getElementById("secret_info").value
        };

        try {
            const response = await fetch("/create-post", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (!response.ok) {
                message.style.color = "red";
                message.textContent = result.detail || "Failed to create post.";
            } else {
                message.style.color = "green";
                message.textContent = "Post created successfully!";
                form.reset();
            }
        } catch (err) {
            message.style.color = "red";
            message.textContent = "An error occurred.";
        }
    });
});
