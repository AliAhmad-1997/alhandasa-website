/* ═══════════════════════════════════════════
   Package Builder — نظام تبديل البنود
   الهندسية التقدمية
═══════════════════════════════════════════ */

let activePackageId = null;
let userSelections   = {};   // { itemKey: { label, priceDelta } }

/* ── فتح/إغلاق مودال الباقة ── */
function openPackageBuilder(pkgId) {
  activePackageId = pkgId;
  userSelections  = {};
  const pkg = PACKAGES_DATA[pkgId];
  if (!pkg) return;

  document.getElementById('pbTitle').textContent    = pkg.name;
  document.getElementById('pbBasePrice').textContent = pkg.price + ' $';
  document.getElementById('pbTotalPrice').textContent = pkg.price + ' $';
  document.getElementById('pbDelta').textContent    = '';
  document.getElementById('pbDelta').className      = 'pb-delta';

  renderSections(pkg);
  document.getElementById('packageBuilderModal').classList.add('active');
  document.body.style.overflow = 'hidden';
}

function closePackageBuilder() {
  document.getElementById('packageBuilderModal').classList.remove('active');
  document.body.style.overflow = '';
}

/* ── رسم الأقسام والبنود ── */
function renderSections(pkg) {
  const container = document.getElementById('pbSections');
  container.innerHTML = '';

  pkg.sections.forEach(section => {
    const secEl = document.createElement('div');
    secEl.className = 'pb-section';
    secEl.innerHTML = `<div class="pb-section-title">${section.icon} ${section.title}</div>`;

    section.items.forEach(item => {
      const itemEl = document.createElement('div');
      itemEl.className = 'pb-item';

      const sel = userSelections[item.key];
      const currentLabel = sel ? sel.label : item.value;
      const hasAlts = item.alts && item.alts.length > 0;

      itemEl.innerHTML = `
        <div class="pb-item-info">
          <div class="pb-item-label">${item.label}</div>
          <div class="pb-item-value" id="val_${item.key}">${currentLabel}</div>
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
}

/* ── فتح قائمة البدائل ── */
function openSwapMenu(pkgId, itemKey, btn) {
  // أغلق أي قائمة مفتوحة
  document.querySelectorAll('.pb-dropdown').forEach(d => d.remove());

  const pkg  = PACKAGES_DATA[pkgId];
  const item = findItem(pkg, itemKey);
  if (!item || !item.alts || !item.alts.length) return;

  const dropdown = document.createElement('div');
  dropdown.className = 'pb-dropdown';

  // الخيار الأصلي دائماً موجود
  const allAlts = [
    { label: item.value, price: 0, isDefault: true },
    ...item.alts.filter(a => a.label !== item.value)
  ];

  const currentSel = userSelections[itemKey];

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

  // موضع القائمة
  const rect = btn.getBoundingClientRect();
  dropdown.style.position = 'fixed';
  dropdown.style.top  = (rect.bottom + 6) + 'px';
  dropdown.style.right = (window.innerWidth - rect.right) + 'px';
  dropdown.style.zIndex = '10000';

  document.body.appendChild(dropdown);

  // إغلاق عند الضغط خارجها
  setTimeout(() => {
    document.addEventListener('click', function handler(e) {
      if (!dropdown.contains(e.target)) {
        dropdown.remove();
        document.removeEventListener('click', handler);
      }
    });
  }, 10);
}

/* ── اختيار بديل ── */
function selectAlt(pkgId, itemKey, alt) {
  const pkg  = PACKAGES_DATA[pkgId];
  const item = findItem(pkg, itemKey);

  if (alt.isDefault || alt.price === 0 && alt.label === item.value) {
    delete userSelections[itemKey];
  } else {
    userSelections[itemKey] = { label: alt.label, priceDelta: alt.price };
  }

  // حدّث النص
  const valEl = document.getElementById('val_' + itemKey);
  if (valEl) {
    valEl.textContent = alt.isDefault ? item.value : alt.label;
    valEl.classList.toggle('modified', !alt.isDefault && alt.price !== 0);
  }

  updateTotalPrice(pkg);
}

/* ── حساب السعر الإجمالي ── */
function updateTotalPrice(pkg) {
  const base  = pkg.price;
  const delta = Object.values(userSelections)
    .reduce((sum, s) => sum + (s.priceDelta || 0), 0);
  const total = base + delta;

  document.getElementById('pbTotalPrice').textContent = total + ' $';

  const deltaEl = document.getElementById('pbDelta');
  if (delta > 0) {
    deltaEl.textContent = '(+' + delta + '$ إضافات)';
    deltaEl.className   = 'pb-delta plus';
  } else if (delta < 0) {
    deltaEl.textContent = '(' + delta + '$ توفير)';
    deltaEl.className   = 'pb-delta minus';
  } else {
    deltaEl.textContent = '';
    deltaEl.className   = 'pb-delta';
  }
}

/* ── إرسال عبر واتساب ── */
function sendPackageToWhatsapp() {
  const pkg = PACKAGES_DATA[activePackageId];
  if (!pkg) return;

  const base  = pkg.price;
  const delta = Object.values(userSelections)
    .reduce((sum, s) => sum + (s.priceDelta || 0), 0);
  const total = base + delta;

  let msg = `مرحباً، أريد الاستفسار عن:\n`;
  msg += `*${pkg.name}*\n`;
  msg += `السعر الأساسي: ${base} $\n`;

  if (Object.keys(userSelections).length > 0) {
    msg += `\nالتعديلات المطلوبة:\n`;
    Object.entries(userSelections).forEach(([key, sel]) => {
      const item = findItemByKey(pkg, key);
      const sign = sel.priceDelta > 0 ? '+' : '';
      msg += `• ${item ? item.label : key}: ${sel.label} (${sign}${sel.priceDelta}$)\n`;
    });
  }

  msg += `\n*السعر الإجمالي: ${total} $*\n`;
  msg += `أرجو التواصل معي للمزيد من التفاصيل.`;

  window.open('https://wa.me/00963986555105?text=' + encodeURIComponent(msg), '_blank');
}

/* ── مساعدات ── */
function findItem(pkg, key) {
  for (const sec of pkg.sections) {
    const found = sec.items.find(i => i.key === key);
    if (found) return found;
  }
  return null;
}
function findItemByKey(pkg, key) { return findItem(pkg, key); }

/* ── إغلاق بالضغط خارج المودال ── */
document.addEventListener('DOMContentLoaded', () => {
  const modal = document.getElementById('packageBuilderModal');
  if (modal) {
    modal.addEventListener('click', e => {
      if (e.target === modal) closePackageBuilder();
    });
  }
});
