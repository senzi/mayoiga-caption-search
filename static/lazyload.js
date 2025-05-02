/**
 * lazyload.js
 * 滚动懒加载截图卡片，IntersectionObserver 方案
 * 依赖 window.allResults, 以及 daisyUI/card 结构
 */
document.addEventListener('DOMContentLoaded', function () {
  const grid = document.getElementById('result-grid');
  const sentinel = document.getElementById('lazyload-sentinel');
  const allResults = window.allResults || [];
  const BATCH_SIZE = 40;
  let loaded = grid ? grid.children.length : 0;

  if (!grid || !sentinel || allResults.length <= BATCH_SIZE) return;

  function createCard(item) {
    // 构造卡片 DOM
    const card = document.createElement('div');
    card.className = 'card shadow bg-base-100';
    card.setAttribute('data-key', item.episode + '-' + item.file);
    card.innerHTML = `
      <figure class="px-2 pt-2">
        <img src="${item.img}" alt="截图" class="rounded" loading="lazy">
      </figure>
      <div class="card-body p-4">
        <p class="mb-2">${item.text}</p>
        <p class="text-xs text-gray-400 mb-2">${item.episode}</p>
        <button class="btn btn-sm btn-outline copy-btn" data-img="${item.img}">📋 复制</button>
      </div>
    `;
    return card;
  }

  function loadNextBatch() {
    const next = allResults.slice(loaded, loaded + BATCH_SIZE);
    next.forEach(item => {
      grid.appendChild(createCard(item));
    });
    loaded += next.length;
    // 全部加载完毕，移除 sentinel
    if (loaded >= allResults.length && sentinel.parentNode) {
      sentinel.parentNode.removeChild(sentinel);
      observer.disconnect();
    }
  }

  // IntersectionObserver 监听 sentinel
  const observer = new IntersectionObserver(entries => {
    if (entries[0].isIntersecting) {
      loadNextBatch();
    }
  }, {
    root: null,
    rootMargin: '0px',
    threshold: 0.1
  });

  observer.observe(sentinel);
});
