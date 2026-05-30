/* ═══════════════════════════════════════════
   ENHANCEMENTS JS — الهندسية التقدمية
   1. Before/After Slider
   2. Cost Calculator (مرتبطة مع PACKAGES_DATA + تخصيصات الزبون)
═══════════════════════════════════════════ */

/* ── 1. Before/After Slider ── */
function initBASlider() {
  const wrap = document.querySelector('.ba-slider-wrap');
  if (!wrap) return;
  const before = wrap.querySelector('.ba-before');
  const handle = wrap.querySelector('.ba-handle');
  let dragging = false;

  function setPos(x) {
    const rect = wrap.getBoundingClientRect();
    let pct = ((x - rect.left) / rect.width) * 100;
    pct = Math.max(5, Math.min(95, pct));
    before.style.width = pct + '%';
    handle.style.left  = pct + '%';
  }

  wrap.addEventListener('mousedown',  e => { dragging = true; setPos(e.clientX); });
  wrap.addEventListener('touchstart', e => { dragging = true; setPos(e.touches[0].clientX); }, { passive: true });
  document.addEventListener('mousemove',  e => { if (dragging) setPos(e.clientX); });
  document.addEventListener('touchmove',  e => { if (dragging) setPos(e.touches[0].clientX); }, { passive: true });
  document.addEventListener('mouseup',  () => dragging = false);
  document.addEventListener('touchend', () => dragging = false);
}

/* ── 2. Cost Calculator ── */

/* خريطة: قيمة الـ select → مفتاح PACKAGES_DATA */
const CALC_TO_PKG = {
  taqsit2:  'pkg_85',
  taqsit1:  'pkg_110',
  basic:    'pkg_65',
  standard: 'pkg_120',
  momtaza:  'pkg_180',
  premium:  'pkg_200',
  super:    'pkg_300'
};

function calcCost() {
  const typeEl = document.getElementById('calcType');
  const areaEl = document.getElementById('calcArea');
  const result = document.getElementById('calcResult');
  const btnWA  = document.getElementById('btnWhatsapp');

  if (!typeEl || !areaEl) return;

  const type = typeEl.value;
  const area = parseFloat(areaEl.value);

  if (!type) { areaEl.focus(); return; }
  if (!area || area <= 0 || area > 10000) {
    areaEl.style.borderColor = '#ef4444';
    setTimeout(() => areaEl.style.borderColor = '', 1500);
    return;
  }

  const pkgKey = CALC_TO_PKG[type];

  /*
    السعر = السعر الأساسي + تعديلات الزبون المحفوظة في packages-builder.js
    getAdjustedPrice() موجودة في packages-builder.js وتجيب السعر بعد التخصيص
  */
  let pricePerM2;
  let pkgName;
  let pkgIcon = '';
  let hasCustomizations = false;
  let customizationDelta = 0;

  if (typeof PACKAGES_DATA !== 'undefined' && pkgKey && PACKAGES_DATA[pkgKey]) {
    const pkg = PACKAGES_DATA[pkgKey];
    pkgName = pkg.name;
    pkgIcon = pkg.icon || '';

    if (typeof getAdjustedPrice === 'function') {
      pricePerM2 = getAdjustedPrice(pkgKey);
      customizationDelta = pricePerM2 - pkg.price;
      hasCustomizations = customizationDelta !== 0;
    } else {
      pricePerM2 = pkg.price;
    }
  } else {
    /* fallback */
    const fallback = { basic:65, standard:120, premium:200, taqsit2:85, taqsit1:110, momtaza:180, super:300 };
    const fallbackNames = {
      basic:'الباقة الاقتصادية', standard:'الباقة المتوسطة', premium:'الباقة الفاخرة',
      taqsit2:'باقة التقسيط الدرجة الثانية', taqsit1:'باقة التقسيط الدرجة الأولى',
      momtaza:'الباقة الممتازة', super:'الباقة السوبر فاخرة'
    };
    pricePerM2 = fallback[type] || 0;
    pkgName    = fallbackNames[type] || type;
  }

  const total     = Math.round(area * pricePerM2);
  const monthly12 = Math.round(total / 12);
  const monthly24 = Math.round(total / 24);

  /* عرض السعر مع إشارة التعديل إن وجدت */
  const priceLabel = hasCustomizations
    ? `${pricePerM2} $ <span style="font-size:.75em;color:${customizationDelta>0?'#e74c3c':'#27ae60'}">(${customizationDelta>0?'+':''}${customizationDelta}$ تخصيص)</span>`
    : `${pricePerM2} $`;

  document.getElementById('calcTotal').textContent     = total.toLocaleString('ar') + ' $';
  document.getElementById('calcMonthly12').textContent = monthly12.toLocaleString('ar') + ' $';
  document.getElementById('calcMonthly24').textContent = monthly24.toLocaleString('ar') + ' $';
  document.getElementById('calcPriceM2').innerHTML     = priceLabel;

  result.classList.add('show');

  /* ── زر "خصّص الباقة" ── */
  let customizeBtn = document.getElementById('calcCustomizeBtn');
  if (pkgKey && typeof openPackageBuilder === 'function') {
    if (!customizeBtn) {
      customizeBtn = document.createElement('button');
      customizeBtn.id = 'calcCustomizeBtn';
      customizeBtn.className = 'btn-calc';
      customizeBtn.style.cssText = 'background:#1a3a5c;margin-top:10px;width:100%;';
      const calcBtn = document.querySelector('.btn-calc');
      if (calcBtn && calcBtn.parentNode) {
        calcBtn.parentNode.insertBefore(customizeBtn, calcBtn.nextSibling);
      }
    }
    const badge = hasCustomizations ? ' ✏️' : '';
    customizeBtn.textContent = pkgIcon + ' خصّص ' + pkgName + badge;
    customizeBtn.onclick = () => openPackageBuilder(pkgKey);
    customizeBtn.style.display = 'block';
  }

  /* ── زر الواتساب ── */
  let waMsg = `مرحباً، أريد مقايسة لـ ${pkgName}\n`;
  waMsg += `المساحة: ${area} م²\n`;
  waMsg += `سعر المتر: ${pricePerM2} $`;
  if (hasCustomizations) waMsg += ` (بعد التخصيص)`;
  waMsg += `\nالتكلفة التقريبية: ${total.toLocaleString('ar')} $\n`;
  waMsg += `أرجو التواصل معي للمزيد من التفاصيل.`;

  btnWA.href = `https://wa.me/00963986555105?text=${encodeURIComponent(waMsg)}`;
  btnWA.classList.add('show');

  result.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/* ── Init ── */
document.addEventListener('DOMContentLoaded', () => {
  initBASlider();
  if (typeof AOS !== 'undefined') {
    AOS.init({ duration: 700, once: true, offset: 80 });
  }
});
