const userSelect = document.getElementById('users');
const taskList = document.getElementById('tasks');

const users = await getUsers();
const userId = users[0].id;
const tasks = await getTasks(userId);

fillUserSelect(users);
showItems(tasks);

userSelect.onchange = handleSelect;
taskList.onchange = handleCheck;

function handleSelect(e) {
  const id = Number(e.target.value);
  getTasks(id).then(showItems);
}

function handleCheck(e) {
  if (e.target.name !== 'done') return;

  const box = e.target;
  const li = box.closest('li');
  const userId = Number(userSelect.value);
  const taskId = Number(li.dataset.id);
  const done = e.target.checked;

  updateStatus(userId, taskId, done).then(showItems);
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

function getTasks(id) {

  return fetch(`/api/tasks/${id}`)
    .then(response => response.json());
}

function showItems(items) {
  taskList.replaceChildren(...items.map(buildItem));
}

function buildItem(item) {
  const li = document.createElement('li');
  const label = document.createElement('label');
  const box = document.createElement('input');
  const btn = document.createElement('button');

  label.append(box, ' ', item.text);
  box.type = 'checkbox';
  box.name = 'done';
  box.checked = item.done;
  btn.textContent = 'Delete';

  li.dataset.id = item.id;
  li.append(label, ' ', btn);

  return li;
}
