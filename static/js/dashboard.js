/**
 * MANAGER DASHBOARD JS
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Media Type Selector Toggle in Settings Form
  const mediaTypeSelect = document.getElementById('hero_media_type_select');
  const imageFieldGroup = document.querySelector('.hero-image-field-group');
  const videoFieldGroup = document.querySelector('.hero-video-field-group');

  function updateMediaFields() {
    if (!mediaTypeSelect) return;
    const val = mediaTypeSelect.value;
    if (val === 'image') {
      if (imageFieldGroup) imageFieldGroup.style.display = 'block';
      if (videoFieldGroup) videoFieldGroup.style.display = 'none';
    } else {
      if (imageFieldGroup) imageFieldGroup.style.display = 'none';
      if (videoFieldGroup) videoFieldGroup.style.display = 'block';
    }
  }

  if (mediaTypeSelect) {
    updateMediaFields();
    mediaTypeSelect.addEventListener('change', updateMediaFields);
  }

  // 2. Auto-hide Alerts after 5 seconds
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(alert => {
    setTimeout(() => {
      alert.style.transition = 'opacity 0.5s ease';
      alert.style.opacity = '0';
      setTimeout(() => alert.remove(), 500);
    }, 4500);
  });
});
