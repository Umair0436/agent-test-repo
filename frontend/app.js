const API_BASE = "http://localhost:5000/api";

const taskList = document.getElementById("task-list");
const addForm = document.getElementById("add-form");
const titleInput = document.getElementById("new-task-title");

async function loadTasks() {
  const response = await fetch(`${API_BASE}/tasks`);
  const tasks = await response.json();
  taskList.innerHTML = "";
  for (const task of tasks) {
    const li = document.createElement("li");
    li.className = task.done ? "done" : "";
    li.innerHTML = `
      <span>${task.title}</span>
      <button data-action="toggle" data-id="${task.id}">${task.done ? "Undo" : "Done"}</button>
      <button data-action="delete" data-id="${task.id}">Delete</button>
    `;
    taskList.appendChild(li);
  }
}

addForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const title = titleInput.value.trim();
  if (!title) return;
  await fetch(`${API_BASE}/tasks`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title }),
  });
});

taskList.addEventListener("click", async (event) => {
  const button = event.target.closest("button");
  if (!button) return;
  const { action, id } = button.dataset;
  if (action === "toggle") {
    await fetch(`${API_BASE}/tasks/${id}/toggle`, { method: "PATCH" });
  } else if (action === "delete") {
    await fetch(`${API_BASE}/tasks/${id}`, { method: "DELETE" });
  }
  loadTasks();
});

loadTasks();
