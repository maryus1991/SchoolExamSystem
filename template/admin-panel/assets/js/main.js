/* =========================================
   ADMIN PANEL - MAIN JAVASCRIPT
   ========================================= */

'use strict';

// ---- DOM Ready ----
document.addEventListener('DOMContentLoaded', function () {
  initSidebar();
  initTooltips();
  initCheckboxes();
  initFormValidation();
  initDemoCharts();
  highlightCurrentPage();
});

// ================================================
// SIDEBAR
// ================================================
function initSidebar() {
  const sidebar  = document.getElementById('sidebar');
  const overlay  = document.getElementById('sidebarOverlay');
  const toggleBtn = document.getElementById('sidebarToggle');

  if (!sidebar) return;

  if (toggleBtn) {
    toggleBtn.addEventListener('click', function () {
      sidebar.classList.toggle('open');
      overlay && overlay.classList.toggle('show');
    });
  }

  if (overlay) {
    overlay.addEventListener('click', function () {
      sidebar.classList.remove('open');
      overlay.classList.remove('show');
    });
  }

  // Collapse submenu persistence
  const collapseEls = document.querySelectorAll('.nav-collapse-toggle');
  collapseEls.forEach(function (el) {
    el.addEventListener('click', function () {
      const expanded = this.getAttribute('aria-expanded') === 'true';
      this.setAttribute('aria-expanded', !expanded);
    });
  });
}

// ================================================
// HIGHLIGHT ACTIVE PAGE IN SIDEBAR
// ================================================
function highlightCurrentPage() {
  const path = window.location.pathname.split('/').pop();
  const links = document.querySelectorAll('.nav-link-item[href]');

  links.forEach(function (link) {
    const href = link.getAttribute('href').split('/').pop();
    if (href && href === path) {
      link.classList.add('active');
      // Expand parent collapse
      const parentCollapse = link.closest('.collapse');
      if (parentCollapse) {
        parentCollapse.classList.add('show');
        const toggle = document.querySelector('[data-bs-target="#' + parentCollapse.id + '"]');
        if (toggle) toggle.setAttribute('aria-expanded', 'true');
      }
    }
  });
}

// ================================================
// BOOTSTRAP TOOLTIPS
// ================================================
function initTooltips() {
  const tooltipEls = document.querySelectorAll('[data-bs-toggle="tooltip"]');
  tooltipEls.forEach(function (el) {
    new bootstrap.Tooltip(el);
  });
}

// ================================================
// SELECT ALL CHECKBOXES
// ================================================
function initCheckboxes() {
  const selectAll = document.getElementById('selectAll');
  if (!selectAll) return;

  selectAll.addEventListener('change', function () {
    const checkboxes = document.querySelectorAll('.row-checkbox');
    checkboxes.forEach(function (cb) {
      cb.checked = selectAll.checked;
    });
    updateBulkActions();
  });

  document.querySelectorAll('.row-checkbox').forEach(function (cb) {
    cb.addEventListener('change', updateBulkActions);
  });
}

function updateBulkActions() {
  const checked = document.querySelectorAll('.row-checkbox:checked');
  const bulkBar = document.getElementById('bulkActionsBar');
  const countEl = document.getElementById('selectedCount');

  if (bulkBar) {
    bulkBar.style.display = checked.length > 0 ? 'flex' : 'none';
  }

  if (countEl) {
    countEl.textContent = checked.length;
  }
}

// ================================================
// FORM VALIDATION
// ================================================
function initFormValidation() {
  const forms = document.querySelectorAll('.needs-validation');
  forms.forEach(function (form) {
    form.addEventListener('submit', function (event) {
      if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
      }
      form.classList.add('was-validated');
    }, false);
  });
}

// ================================================
// DEMO CHARTS (Pure CSS/JS, no library)
// ================================================
function initDemoCharts() {
  renderBarChart('barChart', [65, 80, 55, 90, 75, 88, 70, 95, 60, 85, 78, 92]);
  renderBarChart('barChart2', [40, 60, 80, 55, 70, 85, 65, 90, 45, 75, 88, 60], true);
}

function renderBarChart(id, data, alternate) {
  const container = document.getElementById(id);
  if (!container) return;

  const max = Math.max(...data);
  container.innerHTML = '';

  data.forEach(function (val, i) {
    const bar = document.createElement('div');
    const pct = (val / max) * 100;
    bar.className = 'chart-bar' + (alternate && i % 3 === 0 ? ' accent' : '');
    bar.style.height = pct + '%';
    bar.title = val;
    container.appendChild(bar);
  });
}

// ================================================
// TOAST NOTIFICATION
// ================================================
function showToast(message, type) {
  type = type || 'success';

  const toastColors = {
    success: '#2ea043',
    danger:  '#f85149',
    warning: '#d29922',
    info:    '#58a6ff',
  };

  const toastEl = document.createElement('div');
  toastEl.className = 'toast align-items-center border-0 show';
  toastEl.setAttribute('role', 'alert');
  toastEl.style.cssText = [
    'background:var(--bg-secondary)',
    'border:1px solid var(--border-color) !important',
    'border-right:3px solid ' + (toastColors[type] || toastColors.info) + ' !important',
    'color:var(--text-primary)',
    'font-family:Vazirmatn,sans-serif',
    'font-size:.85rem',
    'min-width:280px',
  ].join(';');

  toastEl.innerHTML = [
    '<div class="d-flex align-items-center p-3 gap-2">',
    '<span style="color:' + (toastColors[type] || toastColors.info) + '">' + getToastIcon(type) + '</span>',
    '<div class="flex-grow-1">' + message + '</div>',
    '<button type="button" class="btn-close btn-close-white ms-2" style="filter:invert(1);opacity:.5" onclick="this.closest(\'.toast\').remove()"></button>',
    '</div>',
  ].join('');

  let container = document.getElementById('toastContainer');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toastContainer';
    container.style.cssText = 'position:fixed;top:80px;left:24px;z-index:9999;display:flex;flex-direction:column;gap:8px;';
    document.body.appendChild(container);
  }

  container.appendChild(toastEl);

  setTimeout(function () {
    toastEl.style.opacity = '0';
    toastEl.style.transition = 'opacity .3s';
    setTimeout(function () { toastEl.remove(); }, 300);
  }, 3500);
}

function getToastIcon(type) {
  const icons = {
    success: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>',
    danger:  '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>',
    warning: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
    info:    '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>',
  };
  return icons[type] || icons.info;
}

// ================================================
// DELETE CONFIRM
// ================================================
function confirmDelete(id, name) {
  const modal = document.getElementById('deleteModal');
  if (!modal) return;

  const nameEl = modal.querySelector('#deleteTargetName');
  if (nameEl && name) nameEl.textContent = name;

  const confirmBtn = modal.querySelector('#deleteConfirmBtn');
  if (confirmBtn) {
    confirmBtn.onclick = function () {
      bootstrap.Modal.getInstance(modal).hide();
      showToast('رکورد با موفقیت حذف شد.', 'success');
    };
  }

  new bootstrap.Modal(modal).show();
}

// ================================================
// LOADING STATE
// ================================================
function showLoading(btn) {
  if (!btn) return;
  btn.dataset.originalText = btn.innerHTML;
  btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status"></span>در حال پردازش...';
  btn.disabled = true;
}

function hideLoading(btn) {
  if (!btn || !btn.dataset.originalText) return;
  btn.innerHTML = btn.dataset.originalText;
  btn.disabled = false;
}

// ================================================
// FILE UPLOAD PREVIEW
// ================================================
function initFileUpload() {
  const fileInputs = document.querySelectorAll('.file-upload-input');
  fileInputs.forEach(function (input) {
    input.addEventListener('change', function () {
      const preview = document.getElementById(this.dataset.preview);
      const label   = document.getElementById(this.dataset.label);
      const file    = this.files[0];

      if (!file) return;

      if (label) label.textContent = file.name;

      if (preview && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = function (e) {
          preview.src = e.target.result;
          preview.style.display = 'block';
        };
        reader.readAsDataURL(file);
      }
    });
  });
}

// ================================================
// TABLE SEARCH
// ================================================
function initTableSearch(inputId, tableId) {
  const input = document.getElementById(inputId);
  const table = document.getElementById(tableId);
  if (!input || !table) return;

  input.addEventListener('input', function () {
    const q = this.value.toLowerCase();
    const rows = table.querySelectorAll('tbody tr');
    rows.forEach(function (row) {
      const text = row.textContent.toLowerCase();
      row.style.display = text.includes(q) ? '' : 'none';
    });
  });
}
