document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("post-form");
    const message = document.getElementById("post-message");

    // Get cookie value by name
    function getCookie(cname) {
        const name = cname + "=";
        const decodedCookie = decodeURIComponent(document.cookie);
        const cookieArray = decodedCookie.split(';');

        for (let i = 0; i < cookieArray.length; i++) {
            let cookie = cookieArray[i];
            while (cookie.charAt(0) === ' ') {
                cookie = cookie.substring(1);
            }
            if (cookie.indexOf(name) === 0) {
                return cookie.substring(name.length, cookie.length);
            }
        }
        return "";
    }

    // Get CSRF token from cookie
    function getCSRFCookie() {
        return getCookie("csrf_access_token");
    }

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const data = {
            title: document.getElementById("title").value,
            content: document.getElementById("content").value,
            secret_info: document.getElementById("secret_info").value
        };

        const csrfToken = getCSRFCookie();

        try {
            const response = await fetch("/article", {
                method: "POST",
                credentials: "include", // Required to send access_token cookie
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRF-TOKEN": csrfToken // Required by backend
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
