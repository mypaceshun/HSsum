function loading() {
  const loading = document.getElementById("loading");
  const img = document.createElement('img');
  img.setAttribute('src', "/HSsum/static/img/loading.gif");
  loading.append(img);
  return true;
}
