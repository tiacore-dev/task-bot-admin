document.addEventListener("DOMContentLoaded", async () => {
    console.log("🚀 Страница загружена, вызываем loadMetaData()");
    await loadMetaData();

    console.log("🚀 Вызываем loadTasks()");
    await loadTasks();
});

console.log(typeof fetchWithAuth);

let taskStatuses = [];
let taskTypes = [];
let taskPlatforms = [];

const token = localStorage.getItem("access_token");
if (!token) {
    window.location.href = "/login";
}




async function loadMetaData() {
    
    try {
        // Загружаем статусы заданий
        let response = await fetchWithAuth("/admin/meta/task_statuses", { headers: { "Authorization": `Bearer ${token}` } });
        if (response.ok) taskStatuses = await response.json();

        // Загружаем типы заданий
        response = await fetchWithAuth("/admin/meta/task_types", { headers: { "Authorization": `Bearer ${token}` } });
        if (response.ok) taskTypes = await response.json();

        // Загружаем платформы
        response = await fetchWithAuth("/admin/meta/platforms", { headers: { "Authorization": `Bearer ${token}` } });
        if (response.ok) taskPlatforms = await response.json();

    } catch (error) {
        console.error("❌ Ошибка загрузки метаданных:", error);
    }
}

async function loadTasks() {
    const token = localStorage.getItem("access_token");
    if (!token) {
        window.location.href = "/login";
        return;
    }

    const response = await fetchWithAuth("/admin/tasks", {
        headers: { "Authorization": `Bearer ${token}` }
    });

    if (response.ok) {
        const tasks = await response.json();
        const taskList = document.getElementById("task-list");
        taskList.innerHTML = "";

        tasks.forEach(task => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${task.task_name}</td> <!-- 🔥 Добавили имя -->
                <td>${task.description}</td>
                <td>${task.reward}</td>
                <td>${task.verification_type}</td>
                <td>
                    <button class="btn btn-info btn-sm" onclick="openTaskModal('${task.task_id}', '${task.task_name}', '${task.description}', '${task.reward}', '${task.verification_type}', '${task.status_id}')">✏️ Редактировать</button>
                    <button class="btn btn-danger btn-sm" onclick="deleteTask('${task.task_id}')">🗑️ Удалить</button>
                </td>
            `;
            taskList.appendChild(row);
        });
    } else {
        alert("Ошибка загрузки заданий");
    }
}


// Форма создания и редактирования задания
function openTaskModal(task_id = null, task_name = "", description = "", reward = "", verificationType = "", platform_id = "", task_type_id = "", status_id = "") {
    console.log("🛠 Открытие модального окна для:", { task_id, task_name });
    const modal = document.getElementById("taskModal");
    // Проверяем стили
    console.log(getComputedStyle(document.querySelector(".modal")).display);
    console.log(getComputedStyle(document.querySelector(".modal")).position);
    console.log(getComputedStyle(document.querySelector(".modal")).justifyContent);
    console.log(getComputedStyle(document.querySelector(".modal")).alignItems);
    
    document.getElementById("modal-title").innerText = task_id ? "Редактировать задание" : "Создать задание";
    document.getElementById("task-id").value = task_id || "";
    document.getElementById("task-name").value = task_name;
    document.getElementById("task-description").value = description;
    document.getElementById("task-reward").value = reward;

    const verificationSelect = document.getElementById("task-verification");
    verificationSelect.innerHTML = ["auto", "manual", "screenshot"].map(v => 
        `<option value="${v}" ${v === verificationType ? "selected" : ""}>${v}</option>`
    ).join("");

    const statusSelect = document.getElementById("task-status");
    statusSelect.innerHTML = taskStatuses.map(s => 
        `<option value="${s.status_id}" ${s.status_id === status_id ? "selected" : ""}>${s.name}</option>`
    ).join("");

    const platformSelect = document.getElementById("task-platform");
    platformSelect.innerHTML = taskPlatforms.map(p => 
        `<option value="${p.platform_id}" ${p.platform_id === platform_id ? "selected" : ""}>${p.name}</option>`
    ).join("");

    const typeSelect = document.getElementById("task-type");
    typeSelect.innerHTML = taskTypes.map(t => 
        `<option value="${t.task_type_id}" ${t.task_type_id === task_type_id ? "selected" : ""}>${t.name}</option>`
    ).join("");

    document.getElementById("taskModal").style.display = "block";
}





// Закрытие модального окна
function closeModal() {
    document.getElementById("taskModal").style.display = "none";
}


// Отправка формы (создание или обновление)
document.getElementById("task-form").addEventListener("submit", async function (event) {
    event.preventDefault();
    const token = localStorage.getItem("access_token");
    if (!token) {
        window.location.href = "/login";
        return;
    }

    const task_id = document.getElementById("task-id").value;
    const task_name = document.getElementById("task-name").value;
    const description = document.getElementById("task-description").value;
    const reward = parseFloat(document.getElementById("task-reward").value);
    const verificationType = document.getElementById("task-verification").value;
    const status_id = document.getElementById("task-status").value;
    const platform_id = document.getElementById("task-platform").value;
    const task_type_id = document.getElementById("task-type").value;

    if (!task_name || !description || isNaN(reward)) {
        alert("Все поля обязательны!");
        return;
    }

    const taskData = {
        task_name,
        description,
        reward,
        verification_type: verificationType,
        status_id,
        platform_id,
        task_type_id
    };

    console.log("📤 Отправляем на сервер:", JSON.stringify(taskData, null, 2)); // 🔥 Логируем данные

    const url = task_id ? `/admin/tasks/${task_id}` : "/admin/tasks";
    const method = task_id ? "PATCH" : "POST";

    const response = await fetchWithAuth(url, {
        method: method,
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(taskData)
    });

    if (response.ok) {
        alert(`Задание ${task_id ? "обновлено" : "создано"}!`);
        closeModal();
        loadTasks();
    } else {
        const errorData = await response.json(); // Получаем текст ошибки
        console.error("❌ Ошибка при сохранении задания:", errorData);
        alert("Ошибка при сохранении задания: " + JSON.stringify(errorData, null, 2));
    }
});





// Удаление задания
async function deleteTask(task_id) {
    const token = localStorage.getItem("access_token");
    if (!token) {
        window.location.href = "/login";
        return;
    }

    if (!confirm("Вы уверены, что хотите удалить это задание?")) return;

    const response = await fetchWithAuth(`/admin/tasks/${task_id}`, {
        method: "DELETE",
        headers: { "Authorization": `Bearer ${token}` }
    });

    if (response.ok) {
        alert("Задание удалено!");
        loadTasks();
    } else {
        alert("Ошибка при удалении задания");
    }
}
