const itemList = document.querySelector('ul');

getItems().then(showItems);

function getItems() {
  return fetch('/api/items')
    .then(response => response.json());
}

function showItems(items) {
  itemList.replaceChildren(...items.map(buildItem));
}

function buildItem(item) {
  const li = document.createElement('li');
  
  li.textContent = item.name;
  
  return li;
}
