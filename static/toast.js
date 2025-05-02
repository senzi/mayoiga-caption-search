/**
 * toast.js
 * 简单 toast 提示，支持 success/error 类型
 * 依赖 daisyUI 样式
 */
window.showToast = function (msg, type = 'success', duration = 2000) {
  const container = document.getElementById('toast-container');
  if (!container) return;
  // 清空已有 toast
  container.innerHTML = '';
  // 选择样式
  let colorClass = 'alert-success';
  if (type === 'error') colorClass = 'alert-error';
  // 构造 toast 元素
  const toast = document.createElement('div');
  toast.className = `alert ${colorClass} shadow-lg`;
  toast.style.minWidth = '160px';
  toast.innerHTML = `<span>${msg}</span>`;
  container.appendChild(toast);
  // 自动消失
  setTimeout(() => {
    toast.classList.add('opacity-0');
    setTimeout(() => container.innerHTML = '', 300);
  }, duration);
};
