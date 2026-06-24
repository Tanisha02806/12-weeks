/* =========================
   STUDY SPROUT - PART 7
   FINAL POLISHED VERSION
   - add task
   - delete task
   - mark complete
   - filters
   - localStorage
   - progress bar
   - clear completed
   - created date
   - toast messages
========================== */

/* =========================
   1. DOM SELECTIONS
========================== */
const taskForm = document.getElementById("taskForm");
const taskInput = document.getElementById("taskInput");
const taskList = document.getElementById("taskList");
const emptyState = document.getElementById("emptyState");
const gardenBadge = document.getElementById("gardenBadge");
const toast = document.getElementById("toast");

const totalTasksEl = document.getElementById("totalTasks");
const pendingTasksEl = document.getElementById("pendingTasks");
const completedTasksEl = document.getElementById("completedTasks");

const progressText = document.getElementById("progressText");
const progressPercentage = document.getElementById("progressPercentage");
const progressBarFill = document.getElementById("progressBarFill");

const clearCompletedBtn = document.getElementById("clearCompletedBtn");
const filterButtons = document.querySelectorAll(".filter-btn");

/* =========================
   2. APP STATE
========================== */
let tasks = [];
let currentFilter = "all";

const STORAGE_KEY = "studySproutTasks";
let toastTimeout;

/* =========================
   3. EVENT LISTENERS
========================== */
taskForm.addEventListener("submit", function (event) {
  event.preventDefault();
  addTask();
});

filterButtons.forEach((button) => {
  button.addEventListener("click", function () {
    currentFilter = button.dataset.filter;

    filterButtons.forEach((btn) => btn.classList.remove("active"));
    button.classList.add("active");

    renderTasks();
  });
});

clearCompletedBtn.addEventListener("click", clearCompletedTasks);

taskList.addEventListener("click", function (event) {
  const clickedButton = event.target.closest("button");
  if (!clickedButton) return;

  const action = clickedButton.dataset.action;
  const taskId = Number(clickedButton.dataset.id);

  if (!action || !taskId) return;

  if (action === "delete") {
    deleteTask(taskId);
  }

  if (action === "complete") {
    markTaskComplete(taskId);
  }
});

/* =========================
   4. TASK ACTIONS
========================== */
function addTask() {
  const taskText = taskInput.value.trim();

  if (taskText === "") {
    showToast("Please enter a task before adding it 🌱");
    return;
  }

  const newTask = {
    id: Date.now(),
    text: taskText,
    completed: false,
    createdAt: new Date().toISOString()
  };

  tasks.push(newTask);

  saveTasksToLocalStorage();
  renderTasks();
  updateStats();
  updateProgress();

  taskInput.value = "";
  taskInput.focus();

  showToast("Task added to your garden 🌱");
}

function deleteTask(taskId) {
  tasks = tasks.filter((task) => task.id !== taskId);

  saveTasksToLocalStorage();
  renderTasks();
  updateStats();
  updateProgress();

  showToast("Task deleted 🗑️");
}

function markTaskComplete(taskId) {
  const taskToUpdate = tasks.find((task) => task.id === taskId);

  if (!taskToUpdate || taskToUpdate.completed) return;

  taskToUpdate.completed = true;

  saveTasksToLocalStorage();
  renderTasks();
  updateStats();
  updateProgress();

  showToast("Task bloomed successfully 🌸");
}

function clearCompletedTasks() {
  const completedCount = tasks.filter((task) => task.completed).length;

  if (completedCount === 0) {
    showToast("No completed tasks to clear yet 🌿");
    return;
  }

  tasks = tasks.filter((task) => !task.completed);

  saveTasksToLocalStorage();
  renderTasks();
  updateStats();
  updateProgress();

  showToast("Completed tasks cleared 🧹");
}

/* =========================
   5. FILTER LOGIC
========================== */
function getFilteredTasks() {
  if (currentFilter === "pending") {
    return tasks.filter((task) => task.completed === false);
  }

  if (currentFilter === "completed") {
    return tasks.filter((task) => task.completed === true);
  }

  return tasks;
}

/* =========================
   6. RENDER TASKS
========================== */
function renderTasks() {
  taskList.innerHTML = "";

  const filteredTasks = getFilteredTasks();
  gardenBadge.textContent = `${tasks.length} task${tasks.length !== 1 ? "s" : ""}`;

  if (filteredTasks.length === 0) {
    emptyState.classList.remove("hidden");

    const emptyTitle = emptyState.querySelector(".empty-title");
    const emptyText = emptyState.querySelector(".empty-text");

    if (tasks.length === 0) {
      emptyTitle.textContent = "Your garden is empty";
      emptyText.textContent =
        "Add your first task and start growing your study garden.";
    } else if (currentFilter === "pending") {
      emptyTitle.textContent = "No pending tasks 🌿";
      emptyText.textContent =
        "You're all caught up for now. Add more tasks whenever you're ready.";
    } else if (currentFilter === "completed") {
      emptyTitle.textContent = "No completed blooms yet 🌸";
      emptyText.textContent =
        "Complete a task to see your finished blooms here.";
    } else {
      emptyTitle.textContent = "No tasks found";
      emptyText.textContent = "Try adding a new task to your garden.";
    }

    return;
  }

  emptyState.classList.add("hidden");

  filteredTasks.forEach((task) => {
    const taskCard = document.createElement("article");
    taskCard.classList.add("task-card");

    if (task.completed) {
      taskCard.classList.add("completed-task");
    }

    taskCard.innerHTML = `
      <div class="task-main">
        <div class="task-icon">${task.completed ? "🌸" : "🌱"}</div>

        <div class="task-content">
          <h3 class="task-title ${task.completed ? "completed-text" : ""}">
            ${escapeHTML(task.text)}
          </h3>

          <p class="task-status ${task.completed ? "completed-status" : "pending-status"}">
            Status: ${task.completed ? "Completed" : "Pending"}
          </p>

          <p class="task-date">Added: ${formatDate(task.createdAt)}</p>
        </div>
      </div>

      <div class="task-actions">
        ${
          task.completed
            ? `<button class="task-btn completed-btn" disabled>Completed</button>`
            : `<button class="task-btn complete-btn" data-action="complete" data-id="${task.id}">Mark Complete</button>`
        }
        <button class="task-btn delete-btn" data-action="delete" data-id="${task.id}">Delete</button>
      </div>
    `;

    taskList.appendChild(taskCard);
  });
}

/* =========================
   7. STATS + PROGRESS
========================== */
function updateStats() {
  const total = tasks.length;
  const completed = tasks.filter((task) => task.completed).length;
  const pending = total - completed;

  totalTasksEl.textContent = total;
  pendingTasksEl.textContent = pending;
  completedTasksEl.textContent = completed;
}

function updateProgress() {
  const total = tasks.length;
  const completed = tasks.filter((task) => task.completed).length;

  const percentage = total === 0 ? 0 : Math.round((completed / total) * 100);

  progressText.textContent = `${completed} of ${total} task${total !== 1 ? "s" : ""} completed`;
  progressPercentage.textContent = `${percentage}%`;
  progressBarFill.style.width = `${percentage}%`;
}

/* =========================
   8. LOCAL STORAGE
========================== */
function saveTasksToLocalStorage() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(tasks));
}

function loadTasksFromLocalStorage() {
  const savedTasks = localStorage.getItem(STORAGE_KEY);
  if (!savedTasks) return;

  try {
    const parsedTasks = JSON.parse(savedTasks);

    if (Array.isArray(parsedTasks)) {
      tasks = parsedTasks.map((task) => ({
        id: task.id,
        text: task.text,
        completed: task.completed,
        createdAt: task.createdAt || new Date().toISOString()
      }));
    }
  } catch (error) {
    console.error("Failed to load tasks from localStorage:", error);
  }
}

/* =========================
   9. HELPERS
========================== */
function formatDate(dateString) {
  const date = new Date(dateString);

  return date.toLocaleDateString("en-GB", {
    day: "numeric",
    month: "short",
    year: "numeric"
  });
}

function showToast(message) {
  clearTimeout(toastTimeout);

  toast.textContent = message;
  toast.classList.add("show");

  toastTimeout = setTimeout(() => {
    toast.classList.remove("show");
  }, 2200);
}

function escapeHTML(text) {
  return text
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

/* =========================
   10. INITIAL LOAD
========================== */
loadTasksFromLocalStorage();
renderTasks();
updateStats();
updateProgress();