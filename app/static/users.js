document.addEventListener("DOMContentLoaded", async () => {
    const response = await fetchWithAuth("/api/users");
    
    if (response.ok) {
        const users = await response.json();
        const userList = document.getElementById("user-list");
        userList.innerHTML = "";

        users.forEach(user => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${user.username}</td>
                <td>${new Date(user.created_at).toLocaleDateString()}</td>
                <td>
                    <button class="btn btn-info btn-sm" onclick="viewUser('${user.user_id}')">👁️ Открыть</button>
                </td>
            `;
            row.style.cursor = "pointer";
            row.onclick = () => viewUser(user.user_id);
            userList.appendChild(row);
        });
    } else {
        alert("Ошибка загрузки пользователей");
    }
});

function viewUser(userId) {
    window.location.href = `/users/${userId}`;
}
