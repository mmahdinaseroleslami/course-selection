const AppState = { currentView: 'dashboard', students: [], professors: [], courses: [], activeStudentId: null, theme: localStorage.getItem('theme') || 'dark', confirmCallback: null };

document.addEventListener('DOMContentLoaded', () => {
  initTheme(); initNavigation(); initModals(); initSearch(); initForms(); initConfirmModal(); initMobileMenu(); initPersianValidation(); loadAllData();
});

const escapeHtml = s => !s ? '' : String(s).replace(/[&<>"']/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m]));
const jsStr = s => escapeHtml(s).replace(/\\/g, '\\\\').replace(/&#039;/g, "\\'");
const debounce = (fn, delay = 80) => { let t; return (...a) => { clearTimeout(t); t = setTimeout(() => fn(...a), delay); }; };

async function apiCall(url, method = 'GET', body = null) {
  try {
    const opts = { method, headers: body ? { 'Content-Type': 'application/json' } : {} };
    if (body) opts.body = JSON.stringify(body);
    const res = await fetch(url, opts);
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.detail || data.message || 'خطا در انجام عملیات');
    return { ok: true, data };
  } catch (err) {
    showToast(err.message, 'danger');
    return { ok: false, err: err.message };
  }
}

function showToast(message, type = 'info') {
  const container = document.getElementById('toastContainer');
  if (!container) return;
  const msg = typeof message === 'string' ? message : Array.isArray(message) ? message.map(m => m.msg || m).join(' | ') : (message.detail || message.message || String(message));
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = msg;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    setTimeout(() => toast.remove(), 200);
  }, 3200);
}

const emptyTableHtml = (cols, title, desc) => `<tr><td colspan="${cols}"><div class="empty-state">
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
  <h4>${title}</h4><p>${desc}</p></div></td></tr>`;

function initTheme() {
  document.documentElement.setAttribute('data-theme', AppState.theme);
  updateThemeIcon();
  document.getElementById('themeToggleBtn')?.addEventListener('click', () => {
    AppState.theme = AppState.theme === 'light' ? 'dark' : 'light';
    localStorage.setItem('theme', AppState.theme);
    document.documentElement.setAttribute('data-theme', AppState.theme);
    updateThemeIcon();
    showToast(AppState.theme === 'dark' ? 'حالت شب (تاریک) فعال شد' : 'حالت روز (روشن) فعال شد', 'info');
  });
}

function updateThemeIcon() {
  const icon = document.getElementById('themeIcon');
  if (icon) icon.innerHTML = AppState.theme === 'dark'
    ? `<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>`
    : `<circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>`;
}

function initMobileMenu() {
  document.getElementById('mobileMenuBtn')?.addEventListener('click', () => document.body.classList.toggle('sidebar-open'));
  document.getElementById('sidebarBackdrop')?.addEventListener('click', () => document.body.classList.remove('sidebar-open'));
}

function initPersianValidation() {
  document.querySelectorAll('input, select, textarea').forEach(el => {
    el.addEventListener('invalid', e => {
      const v = e.target.validity;
      let msg = 'مقدار وارد شده معتبر نیست.';
      if (v.valueMissing) msg = 'لطفاً این فیلد را تکمیل کنید.';
      else if (v.patternMismatch) msg = el.getAttribute('title') || 'لطفاً بدون فاصله وارد کنید.';
      else if (v.tooShort) msg = `تعداد کاراکترها باید حداقل ${el.minLength} کاراکتر باشد.`;
      else if (v.tooLong) msg = `تعداد کاراکترها نباید بیشتر از ${el.maxLength} کاراکتر باشد.`;
      else if (v.rangeUnderflow) msg = `مقدار وارد شده باید حداقل ${el.min} باشد.`;
      else if (v.rangeOverflow) msg = `مقدار وارد شده باید حداکثر ${el.max} باشد.`;
      e.target.setCustomValidity(msg);
    });
    el.addEventListener('input', e => e.target.setCustomValidity(''));
  });
}

function initNavigation() {
  document.querySelectorAll('.nav-item').forEach(item => {
    const fn = () => { navigateToView(item.getAttribute('data-view')); document.body.classList.remove('sidebar-open'); };
    item.addEventListener('click', fn);
    item.addEventListener('keydown', e => (e.key === 'Enter' || e.key === ' ') && (e.preventDefault(), fn()));
  });
  document.getElementById('btnGoHomeFrom404')?.addEventListener('click', () => navigateToView('dashboard'));
}

function navigateToView(view) {
  const titleMap = { dashboard: 'داشبورد اصلی', students: 'مدیریت دانشجویان', professors: 'مدیریت اساتید', courses: 'مدیریت دروس', selection: 'انتخاب واحد' };
  document.querySelectorAll('.nav-item').forEach(i => i.classList.toggle('active', i.getAttribute('data-view') === view));
  document.querySelectorAll('.view-section').forEach(s => s.classList.remove('active'));
  
  const sec = document.getElementById(`view-${view}`) || document.getElementById('view-404');
  const titleText = document.getElementById('pageTitleText');
  if (titleText) titleText.textContent = titleMap[view] || 'صفحه ۴۰۴ یافت نشد';
  sec?.classList.add('active');
  
  AppState.currentView = view;
  if (view === 'dashboard') fetchSummary();
  if (view === 'students') renderStudentsTable();
  if (view === 'professors') renderProfessorsTable();
  if (view === 'courses') renderCoursesTable();
  if (view === 'selection') prepareSelectionWorkspace();
}

async function loadAllData() { await Promise.all([fetchSummary(), fetchStudents(), fetchProfessors(), fetchCourses()]); }

async function fetchSummary() {
  const { ok, data } = await apiCall('/summary');
  if (!ok) return;
  document.getElementById('stat-students-count').textContent = data.total_students || 0;
  document.getElementById('stat-professors-count').textContent = data.total_professors || 0;
  document.getElementById('stat-courses-count').textContent = data.total_courses || 0;
  document.getElementById('stat-enrollments-count').textContent = data.total_enrollments || 0;
}

async function fetchStudents() {
  const { ok, data } = await apiCall('/students/');
  if (ok) { AppState.students = data; if (AppState.currentView === 'students') renderStudentsTable(); populateStudentDropdown(); }
}

async function fetchProfessors() {
  const { ok, data } = await apiCall('/professors/');
  if (ok) { AppState.professors = data; if (AppState.currentView === 'professors') renderProfessorsTable(); }
}

async function fetchCourses() {
  const { ok, data } = await apiCall('/courses/');
  if (ok) { AppState.courses = data; if (AppState.currentView === 'courses') renderCoursesTable(); }
}

function renderStudentsTable(q = '') {
  const tbody = document.getElementById('studentsTableBody');
  if (!tbody) return;
  const kw = q.toLowerCase();
  const list = AppState.students.filter(s => s.full_name.toLowerCase().includes(kw) || String(s.student_number).toLowerCase().includes(kw) || s.major.toLowerCase().includes(kw));
  if (!list.length) return tbody.innerHTML = emptyTableHtml(5, 'هیچ دانشجویی یافت نشد', 'می‌توانید دانشجو جدید ثبت کنید.');
  
  tbody.innerHTML = list.map(s => `<tr>
    <td><strong>${escapeHtml(s.full_name)}</strong></td>
    <td><span class="badge badge-primary">${escapeHtml(s.student_number)}</span></td>
    <td>${escapeHtml(s.major)}</td>
    <td><span class="badge badge-success">${(s.selected_courses || []).length} درس</span></td>
    <td>
      <button class="btn btn-secondary btn-sm" onclick="showStudentDetails(${s.ID})">جزئیات</button>
      <button class="btn btn-secondary btn-sm" onclick="editStudent(${s.ID})">ویرایش</button>
      <button class="btn btn-danger btn-sm" onclick="deleteStudent(${s.ID})">حذف</button>
    </td>
  </tr>`).join('');
}

function renderProfessorsTable(q = '') {
  const tbody = document.getElementById('professorsTableBody');
  if (!tbody) return;
  const kw = q.toLowerCase();
  const list = AppState.professors.filter(p => p.full_name.toLowerCase().includes(kw) || p.personnel_code.toLowerCase().includes(kw) || p.department.toLowerCase().includes(kw));
  if (!list.length) return tbody.innerHTML = emptyTableHtml(5, 'هیچ استادی یافت نشد', 'می‌توانید استاد جدید ثبت کنید.');

  tbody.innerHTML = list.map(p => `<tr>
    <td><strong>${escapeHtml(p.full_name)}</strong></td>
    <td><span class="badge badge-primary">${escapeHtml(p.personnel_code)}</span></td>
    <td>${escapeHtml(p.department)}</td>
    <td><span class="badge badge-warning">${(p.courses || []).length} درس</span></td>
    <td>
      <button class="btn btn-secondary btn-sm" onclick="showProfDetails(${p.ID})">جزئیات</button>
      <button class="btn btn-secondary btn-sm" onclick="editProfessor(${p.ID})">ویرایش</button>
      <button class="btn btn-danger btn-sm" onclick="deleteProfessor(${p.ID})">حذف</button>
    </td>
  </tr>`).join('');
}

function renderCoursesTable(q = '') {
  const tbody = document.getElementById('coursesTableBody');
  if (!tbody) return;
  const kw = q.toLowerCase();
  const list = AppState.courses.filter(c => c.title.toLowerCase().includes(kw) || c.code.toLowerCase().includes(kw) || c.major.toLowerCase().includes(kw));
  if (!list.length) return tbody.innerHTML = emptyTableHtml(7, 'هیچ درسی یافت نشد', 'می‌توانید درس جدید اضافه کنید.');

  tbody.innerHTML = list.map(c => {
    const enrolled = c.enrolled_count || (c.students || []).length;
    const isFull = enrolled >= c.capacity;
    const badgeCls = isFull ? 'badge-danger' : (enrolled > c.capacity * 0.8 ? 'badge-warning' : 'badge-success');
    const profName = AppState.professors.find(p => p.personnel_code === c.professor)?.full_name || 'تخصیص نیافته';

    return `<tr>
      <td><span class="badge badge-primary">${escapeHtml(c.code)}</span></td>
      <td><strong>${escapeHtml(c.title)}</strong></td>
      <td>${c.unit} واحد</td>
      <td><span class="badge ${badgeCls}">${enrolled} / ${c.capacity}</span></td>
      <td>${escapeHtml(c.major)}</td>
      <td>${escapeHtml(profName)}</td>
      <td>
        <button class="btn btn-secondary btn-sm" onclick="showCourseDetails('${jsStr(c.code)}')">جزئیات</button>
        ${c.professor
          ? `<button class="btn btn-secondary btn-sm" style="background:#f59e0b; color:#fff; border:none;" onclick="openReplaceProfModal('${jsStr(c.code)}')">تعویض استاد</button>`
          : `<button class="btn btn-secondary btn-sm" onclick="openAssignProfModal('${jsStr(c.code)}')">تخصیص استاد</button>`
        }
        <button class="btn btn-secondary btn-sm" onclick="editCourse('${jsStr(c.code)}')">ویرایش</button>
        <button class="btn btn-danger btn-sm" onclick="deleteCourse('${jsStr(c.code)}')">حذف</button>
      </td>
    </tr>`;
  }).join('');
}

function initSearch() {
  const searchMap = { studentSearchInput: renderStudentsTable, profSearchInput: renderProfessorsTable, courseSearchInput: renderCoursesTable };
  Object.entries(searchMap).forEach(([id, fn]) => {
    document.getElementById(id)?.addEventListener('input', debounce(e => fn(e.target.value), 80));
  });
}

function populateStudentDropdown() {
  const select = document.getElementById('selectStudentForCourse');
  if (!select) return;
  const val = select.value;
  select.innerHTML = `<option value="">-- لطفاً یک دانشجو انتخاب کنید --</option>` +
    AppState.students.map(s => `<option value="${s.ID}">${escapeHtml(s.full_name)} (${escapeHtml(s.student_number)} - ${escapeHtml(s.major)})</option>`).join('');
  if (val && AppState.students.some(s => String(s.ID) === val)) select.value = val;
}

function prepareSelectionWorkspace() {
  populateStudentDropdown();
  const select = document.getElementById('selectStudentForCourse');
  if (!select) return;
  select.onchange = e => {
    const id = e.target.value;
    if (!id) { document.getElementById('selectionWorkspaceContainer').style.display = 'none'; AppState.activeStudentId = null; return; }
    AppState.activeStudentId = parseInt(id);
    renderStudentSelectionWorkspace(AppState.activeStudentId);
  };
  if (AppState.activeStudentId && !AppState.students.some(s => s.ID === AppState.activeStudentId)) {
    AppState.activeStudentId = null;
    document.getElementById('selectionWorkspaceContainer').style.display = 'none';
  }
  if (AppState.activeStudentId) { select.value = AppState.activeStudentId; renderStudentSelectionWorkspace(AppState.activeStudentId); }
}

async function renderStudentSelectionWorkspace(studentId) {
  const container = document.getElementById('selectionWorkspaceContainer');
  const student = AppState.students.find(s => s.ID === studentId);
  if (!container) return;
  if (!student) { container.style.display = 'none'; AppState.activeStudentId = null; return; }

  container.style.display = 'block';
  document.getElementById('activeStudentName').textContent = `دانشجو: ${student.full_name}`;
  document.getElementById('activeStudentInfo').textContent = `شماره دانشجویی: ${student.student_number} | رشته: ${student.major}`;

  const { ok, data } = await apiCall(`/students/${studentId}/courses`);
  const selected = ok ? data : [];
  const totalUnits = selected.reduce((s, c) => s + (c.unit || 0), 0);
  document.getElementById('activeStudentTotalUnits').textContent = `مجموع واحدهای اخذ شده: ${totalUnits} واحد`;

  document.getElementById('studentSelectedCoursesBody').innerHTML = !selected.length ? `<tr><td colspan="4" style="text-align:center; color:var(--text-muted); padding:16px;">هنوز درسی اخذ نشده است.</td></tr>` :
    selected.map(c => `<tr>
      <td><span class="badge badge-primary">${escapeHtml(c.code)}</span></td>
      <td><strong>${escapeHtml(c.title)}</strong></td>
      <td>${c.unit} واحد</td>
      <td><button class="btn btn-danger btn-sm" onclick="dropCourseForStudent(${studentId}, '${jsStr(c.code)}')">حذف درس</button></td>
    </tr>`).join('');

  const selCodes = selected.map(c => c.code);
  const available = AppState.courses.filter(c => !selCodes.includes(c.code));

  document.getElementById('availableCoursesBody').innerHTML = !available.length ? `<tr><td colspan="4" style="text-align:center; color:var(--text-muted); padding:16px;">تمام دروس ارائه شده اخذ شده‌اند یا درسی ارائه نشده است.</td></tr>` :
    available.map(c => {
      const enrolled = c.enrolled_count || (c.students || []).length;
      const isFull = enrolled >= c.capacity;
      return `<tr>
        <td><span class="badge badge-primary">${escapeHtml(c.code)}</span></td>
        <td><strong>${escapeHtml(c.title)}</strong> (${c.unit} واحد)</td>
        <td><span class="badge ${isFull ? 'badge-danger' : 'badge-success'}">${enrolled} / ${c.capacity}</span></td>
        <td>
          <button class="btn btn-primary btn-sm" ${isFull ? 'disabled style="opacity:0.5; cursor:not-allowed;"' : ''} onclick="selectCourseForStudent(${studentId}, '${jsStr(c.code)}')">
            ${isFull ? 'تکمیل ظرفیت' : 'اخذ درس'}
          </button>
        </td>
      </tr>`;
    }).join('');
}

async function selectCourseForStudent(studentId, courseCode) {
  const { ok, data } = await apiCall(`/students/${studentId}/select-course/${courseCode}`, 'POST');
  if (ok) { showToast(data.message || 'درس با موفقیت اخذ شد.', 'success'); await loadAllData(); renderStudentSelectionWorkspace(studentId); }
}

async function dropCourseForStudent(studentId, courseCode) {
  const { ok, data } = await apiCall(`/students/${studentId}/drop-course/${courseCode}`, 'DELETE');
  if (ok) { showToast(data.message || 'درس با موفقیت حذف شد.', 'success'); await loadAllData(); renderStudentSelectionWorkspace(studentId); }
}

function renderDetailBox(fields, title, items, empty) {
  return `<div class="detail-grid">${fields.map(f => `<div class="detail-item"><div class="detail-label">${f.label}</div><div class="detail-value">${escapeHtml(f.val)}</div></div>`).join('')}</div>
    <div style="margin-top:16px;"><h4 style="font-size:0.95rem; font-weight:700; margin-bottom:10px; color:var(--text-primary);">${title} (${items.length}):</h4>
    ${!items.length ? `<p style="font-size:0.88rem; color:var(--text-muted);">${empty}</p>` :
      `<ul style="list-style:none; padding:0;">${items.map(it => `<li style="padding:8px 12px; background:var(--glass-bg); margin-bottom:6px; border-radius:8px; border:1px solid var(--border-color); font-size:0.88rem;">${escapeHtml(it)}</li>`).join('')}</ul>`}</div>`;
}

function showStudentDetails(id) {
  const s = AppState.students.find(st => st.ID === id);
  if (!s) return;
  const taken = (s.selected_courses || []).map(code => {
    const c = AppState.courses.find(course => course.code === code);
    return c ? `${c.title} (${code}) - ${c.unit} واحد` : code;
  });
  document.getElementById('studentDetailsContent').innerHTML = renderDetailBox([
    { label: 'نام و نام خانوادگی', val: s.full_name }, { label: 'شماره دانشجویی', val: s.student_number },
    { label: 'رشته تحصیلی', val: s.major }
  ], 'لیست دروس اخذ شده', taken, 'درسی اخذ نشده است.');
  openModal('studentDetailsModal');
}

function showProfDetails(id) {
  const p = AppState.professors.find(pr => pr.ID === id);
  if (!p) return;
  const assigned = (p.courses || []).map(cCode => {
    const c = AppState.courses.find(course => course.code === cCode);
    return c ? `${c.title} (${cCode})` : cCode;
  });
  document.getElementById('profDetailsContent').innerHTML = renderDetailBox([
    { label: 'نام و نام خانوادگی', val: p.full_name }, { label: 'کد پرسنلی', val: p.personnel_code },
    { label: 'دانشکده / گروه آموزشی', val: p.department }
  ], 'دروس ارائه شده توسط استاد', assigned, 'درسی تخصیص داده نشده است.');
  openModal('profDetailsModal');
}

function showCourseDetails(code) {
  const c = AppState.courses.find(co => co.code === code);
  if (!c) return;
  const profName = AppState.professors.find(p => p.personnel_code === c.professor)?.full_name || 'تخصیص نیافته';
  const studentsList = (c.students || []).map(num => {
    const s = AppState.students.find(st => st.student_number === num);
    return s ? `${s.full_name} (${num})` : num;
  });
  document.getElementById('courseDetailsContent').innerHTML = renderDetailBox([
    { label: 'عنوان درس', val: c.title }, { label: 'کد درس', val: c.code },
    { label: 'تعداد واحد', val: `${c.unit} واحد` }, { label: 'ظرفیت ثبت‌نام', val: `${(c.students || []).length} از ${c.capacity}` },
    { label: 'رشته ارائه دهنده', val: c.major }, { label: 'استاد مدرس', val: profName }
  ], 'دانشجویان ثبت‌نام شده', studentsList, 'هیچ دانشجویی در این درس ثبت‌نام نکرده است.');
  openModal('courseDetailsModal');
}

const openModal = id => document.getElementById(id)?.classList.add('active');
const closeModal = id => document.getElementById(id)?.classList.remove('active');

function initModals() {
  document.querySelectorAll('[data-close-modal]').forEach(b => b.addEventListener('click', () => closeModal(b.getAttribute('data-close-modal'))));
  document.querySelectorAll('.modal-backdrop').forEach(b => b.addEventListener('click', e => e.target === b && closeModal(b.id)));
  document.addEventListener('keydown', e => e.key === 'Escape' && closeModal(document.querySelector('.modal-backdrop.active')?.id));

  document.getElementById('btnOpenAddStudentModal')?.addEventListener('click', () => openStudentModal());
  document.getElementById('btnOpenAddProfModal')?.addEventListener('click', () => openProfessorModal());
  document.getElementById('btnOpenAddCourseModal')?.addEventListener('click', () => openCourseModal());
}

function initConfirmModal() {
  const close = () => closeModal('confirmModal');
  document.getElementById('btnCancelConfirm')?.addEventListener('click', close);
  document.getElementById('btnCancelConfirmAction')?.addEventListener('click', close);
  document.getElementById('btnOkConfirmAction')?.addEventListener('click', () => {
    close();
    if (typeof AppState.confirmCallback === 'function') { AppState.confirmCallback(); AppState.confirmCallback = null; }
  });
}

function showConfirmModal(title, message, onConfirm) {
  document.getElementById('confirmModalTitle').textContent = title || 'تایید عملیات';
  document.getElementById('confirmModalBody').textContent = message || 'آیا از انجام این عملیات اطمینان دارید؟';
  AppState.confirmCallback = onConfirm;
  openModal('confirmModal');
}

function openStudentModal(student = null) {
  document.getElementById('studentForm').reset();
  document.getElementById('studentModalTitle').textContent = student ? 'ویرایش اطلاعات دانشجو' : 'افزودن دانشجوی جدید';
  document.getElementById('studentEditOriginalId').value = student ? student.ID : '';
  if (student) {
    document.getElementById('student_first_name').value = student.first_name;
    document.getElementById('student_last_name').value = student.last_name;
    document.getElementById('student_number').value = student.student_number;
    document.getElementById('student_major').value = student.major;
  }
  openModal('studentModal');
}

function editStudent(id) { const s = AppState.students.find(st => st.ID === id); if (s) openStudentModal(s); }
function deleteStudent(id) {
  const s = AppState.students.find(st => st.ID === id);
  const label = s ? s.student_number : id;
  showConfirmModal('حذف دانشجو', `آیا از حذف دانشجوی شماره ${label} اطمینان دارید؟`, async () => {
    const { ok, data } = await apiCall(`/students/${id}`, 'DELETE');
    if (ok) {
      showToast(data.message || 'دانشجو با موفقیت حذف شد.', 'success');
      if (AppState.activeStudentId === id) {
        AppState.activeStudentId = null;
        const ws = document.getElementById('selectionWorkspaceContainer');
        if (ws) ws.style.display = 'none';
      }
      loadAllData();
    }
  });
}

function openProfessorModal(prof = null) {
  document.getElementById('professorForm').reset();
  document.getElementById('profModalTitle').textContent = prof ? 'ویرایش اطلاعات استاد' : 'افزودن استاد جدید';
  document.getElementById('profEditOriginalCode').value = prof ? prof.ID : '';
  if (prof) {
    document.getElementById('prof_first_name').value = prof.first_name;
    document.getElementById('prof_last_name').value = prof.last_name;
    document.getElementById('prof_personnel_code').value = prof.personnel_code;
    document.getElementById('prof_department').value = prof.department;
  }
  openModal('professorModal');
}

function editProfessor(id) { const p = AppState.professors.find(pr => pr.ID === id); if (p) openProfessorModal(p); }
function deleteProfessor(id) {
  const p = AppState.professors.find(pr => pr.ID === id);
  const label = p ? p.personnel_code : id;
  showConfirmModal('حذف استاد', `آیا از حذف استاد با کد پرسنلی ${label} اطمینان دارید؟`, async () => {
    const { ok, data } = await apiCall(`/professors/${id}`, 'DELETE');
    if (ok) { showToast(data.message || 'استاد با موفقیت حذف شد.', 'success'); loadAllData(); }
  });
}

function openCourseModal(course = null) {
  document.getElementById('courseForm').reset();
  document.getElementById('courseModalTitle').textContent = course ? 'ویرایش اطلاعات درس' : 'افزودن درس جدید';
  document.getElementById('courseEditOriginalCode').value = course ? course.code : '';
  if (course) {
    document.getElementById('course_code').value = course.code;
    document.getElementById('course_title').value = course.title;
    document.getElementById('course_unit').value = course.unit;
    document.getElementById('course_capacity').value = course.capacity;
    document.getElementById('course_major').value = course.major;
  }
  openModal('courseModal');
}

function editCourse(code) { const c = AppState.courses.find(co => co.code === code); if (c) openCourseModal(c); }
function deleteCourse(code) {
  showConfirmModal('حذف درس', `آیا از حذف درس با کد ${code} اطمینان دارید؟`, async () => {
    const { ok, data } = await apiCall(`/courses/${code}`, 'DELETE');
    if (ok) { showToast(data.message || 'درس با موفقیت حذف شد.', 'success'); loadAllData(); }
  });
}

function openAssignProfModal(courseCode) {
  const course = AppState.courses.find(c => c.code === courseCode);
  if (!course) return;
  document.getElementById('assignCourseCode').value = course.code;
  document.getElementById('assignCourseTitle').textContent = `${course.title} (${course.code})`;
  document.getElementById('selectProfForAssign').innerHTML = `<option value="">-- لطفاً یک استاد انتخاب کنید --</option>` +
    AppState.professors.map(p => `<option value="${p.ID}">${escapeHtml(p.full_name)} (${escapeHtml(p.personnel_code)} - ${escapeHtml(p.department)})</option>`).join('');
  openModal('assignProfModal');
}

function openReplaceProfModal(courseCode) {
  const course = AppState.courses.find(c => c.code === courseCode);
  if (!course) return;
  const profName = AppState.professors.find(p => p.personnel_code === course.professor)?.full_name || 'تخصیص نیافته';
  document.getElementById('replaceCourseCode').value = course.code;
  document.getElementById('replaceCourseTitle').textContent = `${course.title} (${course.code})`;
  document.getElementById('replaceCurrentProf').textContent = profName;
  document.getElementById('selectProfForReplace').innerHTML = `<option value="">-- لطفاً یک استاد انتخاب کنید --</option>` +
    AppState.professors.map(p => `<option value="${p.ID}">${escapeHtml(p.full_name)} (${escapeHtml(p.personnel_code)} - ${escapeHtml(p.department)})</option>`).join('');
  openModal('replaceProfModal');
}

function initForms() {
  document.getElementById('studentForm')?.addEventListener('submit', async e => {
    e.preventDefault();
    const orig = document.getElementById('studentEditOriginalId').value;
    const payload = {
      first_name: document.getElementById('student_first_name').value.trim(),
      last_name: document.getElementById('student_last_name').value.trim(),
      student_number: document.getElementById('student_number').value.trim(),
      major: document.getElementById('student_major').value.trim()
    };
    const { ok } = await apiCall(orig ? `/students/${orig}` : '/students/', orig ? 'PUT' : 'POST', payload);
    if (ok) { showToast(orig ? 'اطلاعات دانشجو به روز شد.' : 'دانشجوی جدید با موفقیت اضافه شد.', 'success'); closeModal('studentModal'); loadAllData(); }
  });

  document.getElementById('professorForm')?.addEventListener('submit', async e => {
    e.preventDefault();
    const orig = document.getElementById('profEditOriginalCode').value;
    const payload = {
      first_name: document.getElementById('prof_first_name').value.trim(),
      last_name: document.getElementById('prof_last_name').value.trim(),
      personnel_code: document.getElementById('prof_personnel_code').value.trim(),
      department: document.getElementById('prof_department').value.trim()
    };
    const { ok } = await apiCall(orig ? `/professors/${orig}` : '/professors/', orig ? 'PUT' : 'POST', payload);
    if (ok) { showToast(orig ? 'اطلاعات استاد به روز شد.' : 'استاد جدید با موفقیت اضافه شد.', 'success'); closeModal('professorModal'); loadAllData(); }
  });

  document.getElementById('courseForm')?.addEventListener('submit', async e => {
    e.preventDefault();
    const orig = document.getElementById('courseEditOriginalCode').value;
    const payload = {
      code: document.getElementById('course_code').value.trim(),
      title: document.getElementById('course_title').value.trim(),
      unit: parseInt(document.getElementById('course_unit').value, 10),
      capacity: parseInt(document.getElementById('course_capacity').value, 10),
      major: document.getElementById('course_major').value.trim()
    };
    const { ok } = await apiCall(orig ? `/courses/${orig}` : '/courses/', orig ? 'PUT' : 'POST', payload);
    if (ok) { showToast(orig ? 'اطلاعات درس به روز شد.' : 'درس جدید با موفقیت اضافه شد.', 'success'); closeModal('courseModal'); loadAllData(); }
  });

  document.getElementById('assignProfForm')?.addEventListener('submit', async e => {
    e.preventDefault();
    const courseCode = document.getElementById('assignCourseCode').value;
    const professorId = document.getElementById('selectProfForAssign').value;
    if (!professorId) return showToast('لطفاً یک استاد را انتخاب کنید.', 'warning');
    const { ok, data } = await apiCall(`/professors/${professorId}/assign-course/${courseCode}`, 'POST');
    if (ok) { showToast(data.message || 'درس با موفقیت به استاد تخصیص داده شد.', 'success'); closeModal('assignProfModal'); loadAllData(); }
  });

  document.getElementById('replaceProfForm')?.addEventListener('submit', async e => {
    e.preventDefault();
    const courseCode = document.getElementById('replaceCourseCode').value;
    const professorId = document.getElementById('selectProfForReplace').value;
    if (!professorId) return showToast('لطفاً یک استاد جدید را انتخاب کنید.', 'warning');
    const { ok, data } = await apiCall(`/professors/${professorId}/replace-course/${courseCode}`, 'POST');
    if (ok) { showToast(data.message || 'استاد درس با موفقیت تعویض شد.', 'success'); closeModal('replaceProfModal'); loadAllData(); }
  });
}
