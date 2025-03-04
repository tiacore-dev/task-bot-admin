document.addEventListener("DOMContentLoaded", loadTasks);

async function loadTasks() {
    const token = localStorage.getItem("jwt_token");
    if (!token) {
        window.location.href = "/login";
        return;
    }

    const response = await fetch("/admin/tasks", {
        headers: { "Authorization": `Bearer ${token}` }
    });

    if (response.ok) {
        const tasks = await response.json();
        const taskList = document.getElementById("task-list");
        taskList.innerHTML = "";
        tasks.forEach(task => {
            const li = document.createElement("li");
            li.textContent = task.description;
            taskList.appendChild(li);
        });
    } else {
        alert("Ошибка загрузки заданий");
    }
}

async function createTask() {
    const token = localStorage.getItem("jwt_token");
    if (!token) {
        window.location.href = "/login";
        return;
    }

    const description = prompt("Введите описание задания:");
    if (!description) return;
    
    const response = await fetch("/admin/tasks", {
        method: "POST",
        headers: { 
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ description })
    });

    if (response.ok) {
        alert("Задание создано!");
        loadTasks();
    } else {
        alert("Ошибка при создании задания");
    }
}
