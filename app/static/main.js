document.addEventListener("DOMContentLoaded", function () {
    console.log("📢 DOM загружен!");

    const token = localStorage.getItem("access_token");
    const navbar = document.getElementById("admin-navbar");

    console.log("🔍 Токен в localStorage:", token);
    
    if (!token) {
        console.warn("⚠️ Токен отсутствует. Навбар скрыт.");
        document.body.classList.remove("authenticated");
    } else {
        console.log("✅ Токен найден. Показываем навбар.");
        document.body.classList.add("authenticated");
    }
});



function logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token")
    window.location.href = "/login";
}


function fetchWithAuth(url, options = {}) {
    let token = localStorage.getItem("access_token");
    if (!token) {
        window.location.href = "/login";
        return;
    }

    options.headers = {
        ...options.headers,
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
    };

    return fetch(url, options).then(async response => {
        if (response.status === 401) {
            console.warn("⚠️ Токен истёк, пытаемся обновить...");

            const refreshToken = localStorage.getItem("refresh_token");
            if (!refreshToken) {
                console.error("❌ Нет refresh_token! Перенаправляем на логин...");
                localStorage.removeItem("access_token");
                window.location.href = "/login";
                return;
            }

            const refreshResponse = await fetch("/auth/refresh", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ refresh_token: refreshToken })
            });

            if (refreshResponse.ok) {
                const data = await refreshResponse.json();
                localStorage.setItem("access_token", data.access_token);
                localStorage.setItem("refresh_token", data.refresh_token);

                options.headers["Authorization"] = `Bearer ${data.access_token}`;
                return fetch(url, options);
            } else {
                console.error("❌ Ошибка обновления токена! Перенаправляем на логин...");
                localStorage.removeItem("access_token");
                localStorage.removeItem("refresh_token");
                window.location.href = "/login";
            }
        }

        return response;
    });
}

// Делаем функцию глобальной
window.fetchWithAuth = fetchWithAuth;
