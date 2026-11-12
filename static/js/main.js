/**
 * NAFTALAN ACCORDION & MOBILE-FIRST INTERACTION JS
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Accordion Toggle Logic
  const accordionHeaders = document.querySelectorAll('.accordion-header');

  accordionHeaders.forEach(header => {
    header.addEventListener('click', () => {
      const parentItem = header.closest('.accordion-item');
      const isAlreadyActive = parentItem.classList.contains('active');

      // Boshqa barcha akkordeon elementlarini yopish
      document.querySelectorAll('.accordion-item').forEach(item => {
        item.classList.remove('active');
        const h = item.querySelector('.accordion-header');
        if (h) h.setAttribute('aria-expanded', 'false');
      });

      // Agar bosilgan element avval ochilmagan bo'lsa, uni ochish
      if (!isAlreadyActive) {
        parentItem.classList.add('active');
        header.setAttribute('aria-expanded', 'true');

        // Ochilgan joyga silliq scroll qilish
        setTimeout(() => {
          parentItem.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }, 150);
      }
    });
  });

  // 6-punktni (Operator bilan bog'lanish) default ochiq qilib qo'yish
  const defaultOpen = document.getElementById('acc-item-6') || document.querySelector('.accordion-item.active-default');
  if (defaultOpen) {
    defaultOpen.classList.add('active');
  }

  // 2. Image Lightbox Modal Handler
  const lightbox = document.getElementById('imageLightbox');
  const lightboxImg = document.getElementById('lightboxImg');
  const lightboxCaption = document.getElementById('lightboxCaption');
  const lightboxClose = document.getElementById('lightboxClose');

  document.querySelectorAll('.gallery-lightbox-trigger').forEach(img => {
    img.addEventListener('click', (e) => {
      e.stopPropagation();
      if (lightbox && lightboxImg) {
        lightboxImg.src = img.src;
        if (lightboxCaption) {
          lightboxCaption.textContent = img.dataset.title || img.alt || '';
        }
        lightbox.classList.add('active');
      }
    });
  });

  if (lightboxClose) {
    lightboxClose.addEventListener('click', () => {
      lightbox.classList.remove('active');
    });
  }

  if (lightbox) {
    lightbox.addEventListener('click', (e) => {
      if (e.target === lightbox) {
        lightbox.classList.remove('active');
      }
    });
  }

  // 3. Phone Number Mask (+998 __ ___-__-__)
  const phoneInputs = document.querySelectorAll('input[name="phone"], #acc_lead_phone');
  phoneInputs.forEach(input => {
    input.addEventListener('focus', (e) => {
      if (!e.target.value) {
        e.target.value = '+998 ';
      }
    });

    input.addEventListener('input', (e) => {
      let val = e.target.value.replace(/\D/g, '');
      if (val.startsWith('998')) {
        val = val.substring(3);
      }
      let formatted = '+998 ';
      if (val.length > 0) formatted += '(' + val.substring(0, 2);
      if (val.length >= 2) formatted += ') ' + val.substring(2, 5);
      if (val.length >= 5) formatted += '-' + val.substring(5, 7);
      if (val.length >= 7) formatted += '-' + val.substring(7, 9);
      
      e.target.value = formatted.trim();
    });
  });

  // 4. AJAX Lead Form Submission
  const leadForms = document.querySelectorAll('.ajax-lead-form');
  leadForms.forEach(form => {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const submitBtn = form.querySelector('button[type="submit"]');
      const originalText = submitBtn.innerHTML;
      
      submitBtn.disabled = true;
      submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Yuborilmoqda...';

      const formData = new FormData(form);

      try {
        const response = await fetch(form.action, {
          method: 'POST',
          headers: {
            'X-Requested-With': 'XMLHttpRequest'
          },
          body: formData
        });

        const data = await response.json();

        if (response.ok && data.success) {
          showToast(data.message, 'success');
          form.reset();
        } else {
          showToast(data.message || 'Xatolik yuz berdi. Qaytadan urinib ko\'ring.', 'error');
        }
      } catch (err) {
        console.error(err);
        showToast('Server bilan aloqa uzildi. Qayta urinib ko\'ring.', 'error');
      } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
      }
    });
  });

  // 5. Toast Notification
  function showToast(message, type = 'success') {
    const existing = document.querySelector('.custom-toast');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.className = 'custom-toast';
    if (type === 'error') {
      toast.style.borderLeftColor = '#ef4444';
      toast.innerHTML = `<i class="fas fa-exclamation-circle" style="color: #ef4444; font-size: 18px;"></i> <div>${message}</div>`;
    } else {
      toast.innerHTML = `<i class="fas fa-check-circle" style="color: #10b981; font-size: 18px;"></i> <div><strong>Muvaffaqiyatli!</strong><br>${message}</div>`;
    }

    document.body.appendChild(toast);

    setTimeout(() => {
      toast.remove();
    }, 4500);
  }
});
