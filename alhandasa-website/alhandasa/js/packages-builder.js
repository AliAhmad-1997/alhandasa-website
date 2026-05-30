/* ═══════════════════════════════════════════
   Package Builder — نظام تبديل البنود
   الهندسية التقدمية
   v2 — حفظ التخصيصات دائم per-package
═══════════════════════════════════════════ */

let activePackageId = null;

/*
  allSelections يحفظ تخصيصات كل باقة بشكل مستقل
  { pkg_65: { itemKey: { label, priceDelta } }, pkg_120: {...}, ... }
*/
const allSelections = {};

/* مساعد: تجيب تخصيصات الباقة الحالية */
function getSelections(pkgId) {
  if (!allSelections[pkgId]) allSelections[pkgId] = {};
  return allSelections[pkgId];
}

/* ─── حساب السعر المعدّل لباقة معينة ─── */
function getAdjustedPrice(pkgId) {
  const pkg = PACKAGES_DATA[pkgId];
  if (!pkg) return 0;
  const sels = getSelections(pkgId);
  const delta = Object.values(sels).reduce((sum, s) => sum + (s.priceDelta || 0), 0);
  return pkg.price + delta;
}

/* ─── فتح/إغلاق مودال الباقة ─── */
function openPackageBuilder(pkgId) {
  activePackageId = pkgId;
  const pkg = PACKAGES_DATA[pkgId];
  if (!pkg) return;

  const sels  = getSelections(pkgId);
  const delta = Object.values(sels).reduce((sum, s) => sum + (s.priceDelta || 0), 0);
  const total = pkg.price + delta;

  document.getElementById('pbTitle').textContent     = pkg.name;
  document.getElementById('pbBasePrice').textContent = pkg.price + ' $';
  document.getElementById('pbTotalPrice').textContent = total + ' $';

  const deltaEl = document.getElementById('pbDelta');
  if (delta > 0)      { deltaEl.textContent = '(+' + delta + '$ إضافات)'; deltaEl.className = 'pb-delta plus'; }
  else if (delta < 0) { deltaEl.textContent = '(' + delta + '$ توفير)';   deltaEl.className = 'pb-delta minus'; }
  else                { deltaEl.textContent = '';                           deltaEl.className = 'pb-delta'; }

  renderSections(pkg);
  document.getElementById('packageBuilderModal').classList.add('active');
  document.body.style.overflow = 'hidden';
}

function closePackageBuilder() {
  document.getElementById('packageBuilderModal').classList.remove('active');
  document.body.style.overflow = '';
  /* بعد الإغلاق: حدّث الحاسبة إذا كانت تعرض نفس الباقة */
  syncCalculatorIfNeeded(activePackageId);
}

/* ─── مزامنة الحاسبة بعد تغيير الباقة ─── */
function syncCalculatorIfNeeded(pkgId) {
  const typeEl = document.getElementById('calcType');
  const areaEl = document.getElementById('calcArea');
  if (!typeEl || !areaEl) return;

  /* ابحث عن قيمة الـ select المقابلة للباقة */
  const CALC_TO_PKG = {
    taqsit2: 'pkg_85', taqsit1: 'pkg_110',
    basic: 'pkg_65',   standard: 'pkg_120',
    momtaza: 'pkg_180', premium: 'pkg_200',
    super: 'pkg_300'
  };
  const currentCalcVal = typeEl.value;
  if (!currentCalcVal) return;
  if (CALC_TO_PKG[currentCalcVal] !== pkgId) return;

  /* نفس الباقة محددة بالحاسبة → أعد الحساب */
  if (areaEl.value && parseFloat(areaEl.value) > 0) {
    calcCost();
  }
}

/* ─── رسم الأقسام والبنود ─── */
function renderSections(pkg) {
  const container = document.getElementById('pbSections');
  container.innerHTML = '';
  const sels = getSelections(pkg.id);

  pkg.sections.forEach(section => {
    const secEl = document.createElement('div');
    secEl.className = 'pb-section';
    secEl.innerHTML = `<div class="pb-section-title">${section.icon} ${section.title}</div>`;

    section.items.forEach(item => {
      const itemEl = document.createElement('div');
      itemEl.className = 'pb-item';

      const sel = sels[item.key];
      const currentLabel = sel ? sel.label : item.value;
      const isModified   = !!sel;
      const hasAlts = item.alts && item.alts.length > 0;

      itemEl.innerHTML = `
        <div class="pb-item-info">
          <div class="pb-item-label">${item.label}</div>
          <div class="pb-item-value${isModified ? ' modified' : ''}" id="val_${item.key}">${currentLabel}</div>
        </div>
        ${hasAlts ? `
        <div class="pb-item-actions">
          <button class="pb-swap-btn" onclick="openSwapMenu('${pkg.id}', '${item.key}', this)">
            🔄 تبديل
          </button>
        </div>
        ` : `<div class="pb-item-actions"><span class="pb-fixed-badge">ثابت</span></div>`}
      `;
      secEl.appendChild(itemEl);
    });

    container.appendChild(secEl);
  });

  updateTotalPrice(pkg);
}

/* ─── فتح قائمة البدائل ─── */
function openSwapMenu(pkgId, itemKey, btn) {
  document.querySelectorAll('.pb-dropdown').forEach(d => d.remove());

  const pkg  = PACKAGES_DATA[pkgId];
  const item = findItem(pkg, itemKey);
  if (!item || !item.alts || !item.alts.length) return;

  const sels = getSelections(pkgId);
  const dropdown = document.createElement('div');
  dropdown.className = 'pb-dropdown';

  const allAlts = [
    { label: item.value, price: 0, isDefault: true },
    ...item.alts.filter(a => a.label !== item.value)
  ];

  const currentSel = sels[itemKey];

  allAlts.forEach(alt => {
    const isActive = currentSel
      ? currentSel.label === alt.label
      : alt.isDefault;

    const opt = document.createElement('div');
    opt.className = 'pb-opt' + (isActive ? ' active' : '');

    let priceTag = '';
    if (alt.price > 0)  priceTag = `<span class="pb-opt-price plus">+${alt.price}$</span>`;
    if (alt.price < 0)  priceTag = `<span class="pb-opt-price minus">${alt.price}$</span>`;
    if (alt.price === 0 && !alt.isDefault) priceTag = `<span class="pb-opt-price zero">±0$</span>`;

    opt.innerHTML = `
      <span class="pb-opt-check">${isActive ? '✓' : ''}</span>
      <span class="pb-opt-label">${alt.label}</span>
      ${priceTag}
    `;

    opt.addEventListener('click', () => {
      selectAlt(pkgId, itemKey, alt);
      dropdown.remove();
    });

    dropdown.appendChild(opt);
  });

  const rect = btn.getBoundingClientRect();
  dropdown.style.position = 'fixed';
  dropdown.style.top  = (rect.bottom + 6) + 'px';
  dropdown.style.right = (window.innerWidth - rect.right) + 'px';
  dropdown.style.zIndex = '10000';

  document.body.appendChild(dropdown);

  setTimeout(() => {
    document.addEventListener('click', function handler(e) {
      if (!dropdown.contains(e.target)) {
        dropdown.remove();
        document.removeEventListener('click', handler);
      }
    });
  }, 10);
}

/* ─── اختيار بديل ─── */
function selectAlt(pkgId, itemKey, alt) {
  const pkg  = PACKAGES_DATA[pkgId];
  const item = findItem(pkg, itemKey);
  const sels = getSelections(pkgId);

  if (alt.isDefault || (alt.price === 0 && alt.label === item.value)) {
    delete sels[itemKey];
  } else {
    sels[itemKey] = { label: alt.label, priceDelta: alt.price };
  }

  const valEl = document.getElementById('val_' + itemKey);
  if (valEl) {
    valEl.textContent = alt.isDefault ? item.value : alt.label;
    valEl.classList.toggle('modified', !alt.isDefault);
  }

  updateTotalPrice(pkg);
}

/* ─── حساب وعرض السعر الإجمالي ─── */
function updateTotalPrice(pkg) {
  const sels  = getSelections(pkg.id);
  const base  = pkg.price;
  const delta = Object.values(sels).reduce((sum, s) => sum + (s.priceDelta || 0), 0);
  const total = base + delta;

  document.getElementById('pbTotalPrice').textContent = total + ' $';
  document.getElementById('pbFooterTotal').textContent = total + ' $';

  const deltaEl = document.getElementById('pbDelta');
  if (delta > 0)      { deltaEl.textContent = '(+' + delta + '$ إضافات)'; deltaEl.className = 'pb-delta plus'; }
  else if (delta < 0) { deltaEl.textContent = '(' + delta + '$ توفير)';   deltaEl.className = 'pb-delta minus'; }
  else                { deltaEl.textContent = '';                           deltaEl.className = 'pb-delta'; }
}

/* ─── إرسال عبر واتساب ─── */
function sendPackageToWhatsapp() {
  const pkg = PACKAGES_DATA[activePackageId];
  if (!pkg) return;

  const sels  = getSelections(activePackageId);
  const base  = pkg.price;
  const delta = Object.values(sels).reduce((sum, s) => sum + (s.priceDelta || 0), 0);
  const total = base + delta;

  let msg = `مرحباً، أريد الاستفسار عن:\n`;
  msg += `*${pkg.name}*\n`;
  msg += `السعر الأساسي: ${base} $\n`;

  if (Object.keys(sels).length > 0) {
    msg += `\nالتعديلات المطلوبة:\n`;
    Object.entries(sels).forEach(([key, sel]) => {
      const item = findItemByKey(pkg, key);
      const sign = sel.priceDelta > 0 ? '+' : '';
      msg += `• ${item ? item.label : key}: ${sel.label} (${sign}${sel.priceDelta}$)\n`;
    });
  }

  msg += `\n*السعر الإجمالي: ${total} $*\n`;
  msg += `أرجو التواصل معي للمزيد من التفاصيل.`;

  window.open('https://wa.me/00963986555105?text=' + encodeURIComponent(msg), '_blank');
}

/* ─── مساعدات ─── */
function findItem(pkg, key) {
  for (const sec of pkg.sections) {
    const found = sec.items.find(i => i.key === key);
    if (found) return found;
  }
  return null;
}
function findItemByKey(pkg, key) { return findItem(pkg, key); }

/* ─── إغلاق بالضغط خارج المودال ─── */
document.addEventListener('DOMContentLoaded', () => {
  const modal = document.getElementById('packageBuilderModal');
  if (modal) {
    modal.addEventListener('click', e => {
      if (e.target === modal) closePackageBuilder();
    });
  }
});
