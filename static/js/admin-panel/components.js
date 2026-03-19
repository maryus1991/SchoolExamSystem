/* =========================================
   ADMIN PANEL - COMPONENTS
   Sidebar, Navbar, Footer Templates
   ========================================= */

'use strict';

// ================================================
// SIDEBAR HTML
// ================================================
const SIDEBAR_HTML = `

`;

// ================================================
// TOPBAR HTML
// ================================================
function getTopbarHTML(title, breadcrumbs) {
  const bc = breadcrumbs || [{ label: 'داشبورد', href: '/admin-panel/pages/index.html' }, { label: title }];
  const bcHTML = bc.map(function (b, i) {
    if (i === bc.length - 1) return '<li class="breadcrumb-item active">' + b.label + '</li>';
    return '<li class="breadcrumb-item"><a href="/admin-panel/pages/' + (b.href || '#') + '">' + b.label + '</a></li>';
  }).join('');

  return `
`;
}

// ================================================
// FOOTER HTML
// ================================================
const FOOTER_HTML = `
`;

// ================================================
// DELETE MODAL HTML
// ================================================
const DELETE_MODAL_HTML = `
<div class="modal fade" id="deleteModal" tabindex="-1">
  <div class="modal-dialog modal-dialog-centered modal-sm">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">تأیید حذف</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <div class="modal-body text-center py-4">
        <div style="width:56px;height:56px;background:rgba(248,81,73,.12);border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 16px">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--accent-danger)" stroke-width="2">
            <polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14H6L5 6"/>
            <path d="M10 11v6"/><path d="M14 11v6"/>
            <path d="M9 6V4h6v2"/>
          </svg>
        </div>
        <h6 style="color:var(--text-primary);font-weight:700;margin-bottom:8px">آیا مطمئن هستید؟</h6>
        <p style="font-size:.82rem;color:var(--text-muted)">
          رکورد <strong id="deleteTargetName" style="color:var(--text-primary)"></strong> حذف خواهد شد. این عملیات قابل بازگشت نیست.
        </p>
      </div>
      <div class="modal-footer justify-content-center">
        <button type="button" class="btn btn-outline-secondary btn-sm" data-bs-dismiss="modal">انصراف</button>
        <button type="button" class="btn btn-danger btn-sm" id="deleteConfirmBtn">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14H6L5 6"/></svg>
          بله، حذف کن
        </button>
      </div>
    </div>
  </div>
</div>`;

// ================================================
// INJECT COMPONENTS
// ================================================
function injectComponents(pageTitle, breadcrumbs) {
  // Sidebar
  const sidebarContainer = document.getElementById('sidebarContainer');
  if (sidebarContainer) sidebarContainer.innerHTML = SIDEBAR_HTML;

  // Topbar
  const topbarContainer = document.getElementById('topbarContainer');
  if (topbarContainer) topbarContainer.innerHTML = getTopbarHTML(pageTitle || 'داشبورد', breadcrumbs);

  // Footer
  const footerContainer = document.getElementById('footerContainer');
  if (footerContainer) footerContainer.innerHTML = FOOTER_HTML;

  // Delete modal
  document.body.insertAdjacentHTML('beforeend', DELETE_MODAL_HTML);
}
