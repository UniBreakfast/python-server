const userSelect = document.getElementById('users');
const taskList = document.getElementById('tasks');

getUsers().then(fillUserSelect);

const userId = userSelect.selectedOptions[0].value

getTasks(userId).then(showItems);

taskList.onchange = handleCheck;

function handleCheck(e) {
  if (e.target.name !== 'done') return;
  
  const box = e.target;
  const li = box.closest('li');
  const id = Number(li.dataset.id);
  const done = e.target.checked;

  updateStatus(id, done).then(showItems);
}

function fillUserSelect(users) {
  for (const {id, name} of users) {
    userSelect.append(new Option(name, id))
  }
}

function updateStatus(id, done) {
  return fetch(`/api/task`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ id, done })
  }).then(response => response.json());
}

function getUsers() {
  return fetch('/api/users')
    .then(response => response.json());
}

function getTasks(id) {

  return fetch('/api/tasks/${id}')
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

  label.append(box, ' ', item.task);
  box.type = 'checkbox';
  box.name = 'done';
  box.checked = item.done;
  btn.textContent = 'Delete';

  li.dataset.id = item.id;
  li.append(label, ' ', btn);

  return li;
}
