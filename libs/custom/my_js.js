document.addEventListener('DOMContentLoaded', function () {
  // Native anchors, sticky navigation and details work without JavaScript.
  document.querySelectorAll('.code-example-body').forEach(function (snippet) {
    snippet.textContent = snippet.innerHTML;
  });
  var tools = document.querySelector('.publication-tools');
  if (!tools) return;
  var search = document.getElementById('publication-search');
  var count = document.getElementById('publication-count');
  var buttons = Array.from(tools.querySelectorAll('[data-cat]'));
  var papers = Array.from(document.querySelectorAll('#publication-list .paper'));
  var category = 'all';
  var normalize = function (value) { return value.normalize('NFC').toLocaleLowerCase().trim(); };
  var searchable = papers.map(function (paper) { return normalize(paper.textContent); });
  function update() {
    var terms = normalize(search.value).split(/\s+/).filter(Boolean);
    var visible = 0;
    papers.forEach(function (paper, index) {
      var matches = (category === 'all' || paper.dataset.cat === category) &&
        terms.every(function (term) { return searchable[index].includes(term); });
      paper.hidden = !matches;
      if (matches) visible += 1;
    });
    count.textContent = visible ? visible + ' / ' + papers.length + ' publications · 논문' :
      'No matches · 검색 결과가 없습니다. 검색어나 주제 필터를 바꿔 주세요.';
  }
  buttons.forEach(function (button) {
    button.addEventListener('click', function () {
      category = button.dataset.cat;
      buttons.forEach(function (item) {
        var active = item === button;
        item.classList.toggle('active', active);
        item.setAttribute('aria-pressed', String(active));
      });
      update();
    });
  });
  search.addEventListener('input', update);
  tools.hidden = false;
  update();
});
