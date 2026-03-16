const API_BASE = '/api';

async function apiRequest(method, path, body = null) {
  const token = localStorage.getItem('token');
  const headers = { 'Content-Type': 'application/json' };
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const opts = { method, headers };
  if (body) opts.body = JSON.stringify(body);

  const res = await fetch(API_BASE + path, opts);
  if (res.status === 401) {
    localStorage.clear();
    window.location.href = '/login.html';
    return;
  }
  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.detail || 'Request failed');
  }
  return data;
}

const api = {
  get: (path) => apiRequest('GET', path),
  post: (path, body) => apiRequest('POST', path, body),
  put: (path, body) => apiRequest('PUT', path, body),
  delete: (path) => apiRequest('DELETE', path),
};

// Toast notifications
function showToast(msg, type = 'success') {
  const container = document.getElementById('toast-container') || createToastContainer();
  const toast = document.createElement('div');
  const icons = { success: '✅', error: '❌', info: 'ℹ️' };
  toast.className = `toast ${type}`;
  toast.innerHTML = `<span>${icons[type]}</span><span>${msg}</span>`;
  container.appendChild(toast);
  setTimeout(() => toast.remove(), 3500);
}

function createToastContainer() {
  const el = document.createElement('div');
  el.id = 'toast-container';
  document.body.appendChild(el);
  return el;
}

// Auth helpers
function requireAuth() {
  const token = localStorage.getItem('token');
  if (!token) {
    window.location.href = '/login.html';
    return false;
  }
  return true;
}

function getCurrentUser() {
  try {
    const token = localStorage.getItem('token');
    if (!token) return null;
    const payload = JSON.parse(atob(token.split('.')[1]));
    return { username: payload.sub };
  } catch (e) { return null; }
}

function logout() {
  localStorage.clear();
  window.location.href = '/login.html';
}

function renderSidebarUser() {
  const user = getCurrentUser();
  if (!user) return;
  const role = localStorage.getItem('role') || 'librarian';
  const nameEl = document.getElementById('sidebar-username');
  const roleEl = document.getElementById('sidebar-role');
  const avatarEl = document.getElementById('sidebar-avatar');
  if (nameEl) nameEl.textContent = user.username;
  if (roleEl) roleEl.textContent = role === 'admin' ? '🔑 Admin' : '📚 Thủ thư';
  if (avatarEl) avatarEl.textContent = user.username.charAt(0).toUpperCase();
}

// Modal helpers
function openModal(id) {
  document.getElementById(id).classList.add('open');
}

function closeModal(id) {
  document.getElementById(id).classList.remove('open');
}

// Format date
function fmtDate(d) {
  if (!d) return '—';
  return new Date(d).toLocaleDateString('vi-VN');
}

// Status badge
function statusBadge(status) {
  const map = {
    available: ['✅ Có sẵn', 'badge-success'],
    borrowed: ['📖 Đã mượn', 'badge-warning'],
    lost: ['❌ Mất', 'badge-danger'],
    repair: ['🔧 Sửa chữa', 'badge-secondary'],
    active: ['📗 Đang mượn', 'badge-warning'],
    returned: ['✅ Đã trả', 'badge-success'],
    overdue: ['⚠️ Quá hạn', 'badge-danger'],
    admin: ['🔑 Admin', 'badge-primary'],
    librarian: ['📚 Thủ thư', 'badge-info'],
  };
  const [label, cls] = map[status] || [status, 'badge-secondary'];
  return `<span class="badge ${cls}">${label}</span>`;
}
