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
    const formData = new FormData(document.getElementById("login-form"));
    const response = await fetch("/auth/token", {
        method: "POST",
        body: formData
    });

    const data = await response.json();
    if (response.ok) {
        localStorage.setItem("jwt_token", data.access_token);
        window.location.href = "/admin";
    } else {
        alert("Ошибка входа: " + data.detail);
    }
}

async function checkToken() {
    const token = localStorage.getItem("jwt_token");
    if (!token) {
        window.location.href = "/login";
        return;
    }

    const response = await fetch("/protected", {
        headers: { "Authorization": `Bearer ${token}` }
    });

    if (!response.ok) {
        localStorage.removeItem("jwt_token");
        window.location.href = "/login";
    }
}

function logout() {
    localStorage.removeItem("jwt_token");
    window.location.href = "/login";
}
