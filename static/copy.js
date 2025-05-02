/**
 * 图片复制功能，兼容 Chrome/Edge，Firefox 仅提示不支持
 * 依赖 toast.js
 */
document.addEventListener('DOMContentLoaded', function () {
  function isClipboardImageSupported() {
    // Chrome/Edge 支持 ClipboardItem 和 write
    return !!(navigator.clipboard && window.ClipboardItem);
  }

  async function copyImageFromUrl(imgUrl, btn) {
    try {
      // 获取图片 blob
      const resp = await fetch(imgUrl, { mode: 'cors' });
      const blob = await resp.blob();
      // 仅 image/png 可直接写入 clipboard，image/jpeg 需转为 png
      if (blob.type === 'image/png') {
        try {
          const item = new ClipboardItem({ [blob.type]: blob });
          await navigator.clipboard.write([item]);
          showToast('✅ 已复制', 'success');
        } catch (err) {
          console.error('ClipboardItem 写入失败:', err);
          showToast('❌ 复制失败', 'error');
        }
      } else if (blob.type === 'image/jpeg') {
        // 用 canvas 转为 png
        const img = new Image();
        img.crossOrigin = 'anonymous';
        img.onload = async function () {
          try {
            const canvas = document.createElement('canvas');
            canvas.width = img.width;
            canvas.height = img.height;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0);
            canvas.toBlob(async function (pngBlob) {
              if (pngBlob) {
                try {
                  const item = new ClipboardItem({ 'image/png': pngBlob });
                  await navigator.clipboard.write([item]);
                  showToast('✅ 已复制', 'success');
                } catch (err) {
                  console.error('ClipboardItem 写入失败:', err);
                  showToast('❌ 复制失败', 'error');
                }
              } else {
                showToast('❌ PNG 转换失败', 'error');
              }
            }, 'image/png');
          } catch (err) {
            console.error('canvas 转换失败:', err);
            showToast('❌ 复制失败', 'error');
          }
        };
        img.onerror = function () {
          showToast('❌ 图片加载失败', 'error');
        };
        img.src = URL.createObjectURL(blob);
      } else {
        showToast('❌ 不支持的图片格式: ' + blob.type, 'error');
      }
    } catch (e) {
      console.error('fetch 或 blob 处理失败:', e);
      showToast('❌ 复制失败', 'error');
    }
  }

  // 事件委托，支持懒加载后新插入的按钮
  document.body.addEventListener('click', function (e) {
    if (e.target && e.target.classList.contains('copy-btn')) {
      e.preventDefault();
      const imgUrl = e.target.getAttribute('data-img');
      if (!isClipboardImageSupported()) {
        showToast('❌ 当前浏览器不支持复制图片', 'error');
        return;
      }
      copyImageFromUrl(imgUrl, e.target);
    }
  });
});
