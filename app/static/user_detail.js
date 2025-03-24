document.addEventListener("DOMContentLoaded", async () => {
    const userId = window.location.pathname.split("/").pop(); // Берём ID из URL

    const response = await fetchWithAuth(`/api/users/${userId}`);

    if (response.ok) {
        const user = await response.json();
        document.getElementById("user-info").innerHTML = `
            <p><strong>ID:</strong> ${user.user_id}</p>
            <p><strong>Логин:</strong> ${user.username}</p>
            <p><strong>Дата регистрации:</strong> ${new Date(user.created_at).toLocaleDateString()}</p>
        `;

        const taskList = document.getElementById("task-list");
        taskList.innerHTML = user.tasks.map(task => `
            <tr>
                <td>${task.task_name}</td>
                <td>${task.status}</td>
                <td>${task.submitted_at ? new Date(task.submitted_at).toLocaleDateString() : "—"}</td>
                <td>
                    ${task.status === "pending_review" ? `
                        <button class="btn btn-success btn-sm" onclick="approveTask('${task.task_id}')">✅ Подтвердить</button>
                        <button class="btn btn-danger btn-sm" onclick="rejectTask('${task.task_id}')">❌ Отклонить</button>
                    ` : ""}
                </td>
            </tr>
        `).join("");

    } else {
        alert("Ошибка загрузки профиля пользователя");
    }
});

async function approveTask(taskId) {
    const response = await fetchWithAuth(`/api/tasks/${taskId}/approve`, {
        method: "POST",
    });

    if (response.ok) {
        alert("Задание подтверждено, деньги начислены!");
        location.reload();
    } else {
        alert("Ошибка при подтверждении задания");
    }
}

async function rejectTask(taskId) {
    const response = await fetchWithAuth(`/api/tasks/${taskId}/reject`, {
        method: "POST",
    });

    if (response.ok) {
        alert("Задание отклонено");
        location.reload();
    } else {
        alert("Ошибка при отклонении задания");
    }
}
