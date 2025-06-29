const itemList = document.querySelector('ul');

getItems().then(showItems);

itemList.onchange = handleCheck;

function handleCheck(e) {
  if (e.target.name !== 'done') return;
  
  const box = e.target;
  const li = box.closest('li');
  const id = Number(li.dataset.id);
  const done = e.target.checked;

  updateStatus(id, done).then(showItems);
}

function updateStatus(id, done) {
  return fetch(`/api/task`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ id, done })
  }).then(response => response.json());
}

function getItems() {
  return fetch('/api/items')
    .then(response => response.json());
}

function showItems(items) {
  itemList.replaceChildren(...items.map(buildItem));
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
