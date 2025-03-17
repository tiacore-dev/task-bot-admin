document.addEventListener("DOMContentLoaded", () => {
    if (window.location.pathname !== "/login") {
        checkToken();
    }

    const loginForm = document.getElementById("login-form");
    if (loginForm) {
        loginForm.addEventListener("submit", async (event) => {
            event.preventDefault();
            await login();
        });
    }
});

async function login() {
    const username = document.querySelector("input[name='username']").value;
    const password = document.querySelector("input[name='password']").value;

    console.log("📤 Отправляем JSON на /auth/token:", { username, password });

    try {
        const response = await fetch("/auth/token", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();
        console.log("📥 Ответ от сервера:", data);

        if (response.ok) {
            localStorage.setItem("access_token", data.access_token);
            localStorage.setItem("refresh_token", data.refresh_token);
            window.location.href = "/";

        } else {
            alert("Ошибка входа: " + data.detail);
        }
    } catch (error) {
        console.error("❌ Ошибка запроса:", error);
    }
}


