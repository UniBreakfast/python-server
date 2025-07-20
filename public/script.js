const userSelect = document.getElementById('users');
const taskList = document.getElementById('tasks');

const users = await getUsers();
const userId = users[0].id;
const tasks = await getTasks(userId);

fillUserSelect(users);
showTasks(tasks);

userSelect.onchange = handleSelect;
taskList.onchange = handleCheck;
taskList.onclick = handleDelete;

function handleSelect(e) {
  const id = Number(e.target.value);
  getTasks(id).then(showTasks);
}

function handleCheck(e) {
  if (e.target.name !== 'done') return;

  const box = e.target;
  const li = box.closest('li');
  const userId = Number(userSelect.value);
  const taskId = Number(li.dataset.id);
  const done = e.target.checked;

  updateStatus(userId, taskId, done).then(showTasks);
}

function handleDelete(e) {
  if (e.target.tagName !== 'BUTTON') return;

  const li = e.target.closest('li');
  const userId = Number(userSelect.value);
  const taskId = Number(li.dataset.id);

  deleteTask(userId, taskId).then(showTasks);
}

function fillUserSelect(users) {
  for (const { id, name } of users) {
    userSelect.append(new Option(name, id))
  }
}

function updateStatus(userId, taskId, done) {
  return fetch(`/api/task`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ userId, taskId, done })
  }).then(response => response.json());
}

function getUsers() {
  return fetch('/api/users')
    .then(response => response.json());
}

function getTasks(userId) {
  return fetch(`/api/tasks/${userId}`)
    .then(response => response.json());
}

function deleteTask(userId, taskId) {
  return fetch(`/api/task`, {
    method: 'DELETE',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ userId, taskId })
  }).then(response => response.json());
}

function showTasks(tasks) {
  taskList.replaceChildren(...tasks.map(buildTask));
}

function buildTask(task) {
  const li = document.createElement('li');
  const label = document.createElement('label');
  const box = document.createElement('input');
  const btn = document.createElement('button');

  label.append(box, ' ', task.text);
  box.type = 'checkbox';
  box.name = 'done';
  box.checked = task.done;
  btn.textContent = 'Delete';

  li.dataset.id = task.id;
  li.append(label, ' ', btn);

  return li;
}
