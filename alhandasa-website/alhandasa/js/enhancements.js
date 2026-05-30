/* ═══════════════════════════════════════════
   ENHANCEMENTS JS — الهندسية التقدمية
   1. Before/After Slider
   2. Cost Calculator v3 — اختيار العملة + PACKAGES_DATA
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

const CALC_TO_PKG = {
  taqsit2:'pkg_85', taqsit1:'pkg_110', basic:'pkg_65',
  standard:'pkg_120', momtaza:'pkg_180', premium:'pkg_200', super:'pkg_300'
};

/* العملة المختارة: 'usd' | 'syp' | 'both' */
let activeCurrency = 'usd';

/* تنسيق الليرة */
function formatSYP(num) {
  if (num >= 1000000000) return (num/1000000000).toFixed(2).replace(/\.?0+$/,'') + ' مليار ل.س';
  if (num >= 1000000)    return (num/1000000).toFixed(2).replace(/\.?0+$/,'') + ' مليون ل.س';
  return num.toLocaleString('ar') + ' ل.س';
}

/* ── اختيار العملة ── */
function setCurrency(mode) {
  activeCurrency = mode;

  /* تحديث الأزرار */
  document.getElementById('btnUSD').className  = 'calc-currency-btn' + (mode === 'usd'  ? ' active-usd'  : '');
  document.getElementById('btnSYP').className  = 'calc-currency-btn' + (mode === 'syp'  ? ' active-syp'  : '');
  document.getElementById('btnBOTH').className = 'calc-currency-btn' + (mode === 'both' ? ' active-both' : '');

  /* إظهار/إخفاء حقل سعر الصرف */
  const rateRow = document.getElementById('calcRateRow');
  if (rateRow) {
    if (mode === 'syp' || mode === 'both') {
      rateRow.classList.add('visible');
    } else {
      rateRow.classList.remove('visible');
    }
  }

  /* أعد الحساب إذا في نتائج مسبقة */
  const result = document.getElementById('calcResult');
  if (result && result.classList.contains('show')) calcCost();
}

/* ── إظهار/إخفاء خانات الدولار والليرة ── */
function updateResultVisibility(hasRate) {
  const showUSD = activeCurrency === 'usd' || activeCurrency === 'both';
  const showSYP = (activeCurrency === 'syp' || activeCurrency === 'both') && hasRate;

  const usdIds = ['r-total-usd','r-m2-usd','r-m12-usd','r-m24-usd'];
  const sypIds = ['r-total-syp','r-m2-syp','r-m12-syp','r-m24-syp'];

  usdIds.forEach(id => {
    const el = document.getElementById(id);
    if (el) el.style.display = showUSD ? '' : 'none';
  });
  sypIds.forEach(id => {
    const el = document.getElementById(id);
    if (el) el.style.display = showSYP ? '' : 'none';
  });
}

/* ── الحساب الرئيسي ── */
function calcCost() {
  const typeEl    = document.getElementById('calcType');
  const areaEl    = document.getElementById('calcArea');
  const rateEl    = document.getElementById('calcRate');
  const result    = document.getElementById('calcResult');
  const btnWA     = document.getElementById('btnWhatsapp');
  const rateBadge = document.getElementById('calcRateBadge');

  if (!typeEl || !areaEl) return;

  const type = typeEl.value;
  const area = parseFloat(areaEl.value);
  const rate = rateEl ? parseFloat(rateEl.value) : NaN;
  const hasRate = !isNaN(rate) && rate > 0;

  if (!type) { areaEl.focus(); return; }
  if (!area || area <= 0 || area > 10000) {
    areaEl.style.borderColor = '#ef4444';
    setTimeout(() => areaEl.style.borderColor = '', 1500);
    return;
  }

  /* badge سعر الصرف */
  if (rateBadge) {
    if (hasRate) {
      rateBadge.textContent = '1$ = ' + rate.toLocaleString('ar') + ' ل.س';
      rateBadge.style.display = 'inline-block';
    } else {
      rateBadge.style.display = 'none';
    }
  }

  /* جيب السعر */
  const pkgKey = CALC_TO_PKG[type];
  let pricePerM2, pkgName, pkgIcon = '', hasCustom = false, customDelta = 0;

  if (typeof PACKAGES_DATA !== 'undefined' && pkgKey && PACKAGES_DATA[pkgKey]) {
    const pkg = PACKAGES_DATA[pkgKey];
    pkgName = pkg.name; pkgIcon = pkg.icon || '';
    if (typeof getAdjustedPrice === 'function') {
      pricePerM2 = getAdjustedPrice(pkgKey);
      customDelta = pricePerM2 - pkg.price;
      hasCustom   = customDelta !== 0;
    } else { pricePerM2 = pkg.price; }
  } else {
    const fb = {basic:65,standard:120,premium:200,taqsit2:85,taqsit1:110,momtaza:180,super:300};
    const fn = {basic:'الباقة الاقتصادية',standard:'الباقة المتوسطة',premium:'الباقة الفاخرة',
                taqsit2:'باقة التقسيط الدرجة الثانية',taqsit1:'باقة التقسيط الدرجة الأولى',
                momtaza:'الباقة الممتازة',super:'الباقة السوبر فاخرة'};
    pricePerM2 = fb[type]||0; pkgName = fn[type]||type;
  }

  const total     = Math.round(area * pricePerM2);
  const monthly12 = Math.round(total / 12);
  const monthly24 = Math.round(total / 24);

  /* ── قيم الدولار ── */
  const priceLabel = hasCustom
    ? pricePerM2 + ' $&nbsp;<small style="color:' + (customDelta>0?'#e74c3c':'#27ae60') + '">(' + (customDelta>0?'+':'') + customDelta + '$)</small>'
    : pricePerM2 + ' $';

  document.getElementById('calcTotal').textContent     = total.toLocaleString('ar') + ' $';
  document.getElementById('calcMonthly12').textContent = monthly12.toLocaleString('ar') + ' $';
  document.getElementById('calcMonthly24').textContent = monthly24.toLocaleString('ar') + ' $';
  document.getElementById('calcPriceM2').innerHTML     = priceLabel;

  /* ── قيم الليرة ── */
  if (hasRate) {
    const tSYP   = Math.round(total * rate);
    const m2SYP  = Math.round(pricePerM2 * rate);
    const m12SYP = Math.round(monthly12 * rate);
    const m24SYP = Math.round(monthly24 * rate);
    document.getElementById('calcSypTotal').textContent     = formatSYP(tSYP);
    document.getElementById('calcSypM2').textContent        = formatSYP(m2SYP);
    document.getElementById('calcSypMonthly12').textContent = formatSYP(m12SYP);
    document.getElementById('calcSypMonthly24').textContent = formatSYP(m24SYP);
  }

  /* إظهار الخانات حسب العملة المختارة */
  updateResultVisibility(hasRate);

  result.classList.add('show');

  /* ── زر خصّص الباقة ── */
  let customizeBtn = document.getElementById('calcCustomizeBtn');
  if (pkgKey && typeof openPackageBuilder === 'function') {
    if (!customizeBtn) {
      customizeBtn = document.createElement('button');
      customizeBtn.id = 'calcCustomizeBtn';
      customizeBtn.className = 'btn-calc customize';
      const actions = document.querySelector('.calc-actions');
      if (actions) actions.insertBefore(customizeBtn, actions.firstChild);
    }
    customizeBtn.textContent = pkgIcon + ' خصّص ' + pkgName + (hasCustom ? ' ✏️' : '');
    customizeBtn.onclick = () => openPackageBuilder(pkgKey);
    customizeBtn.style.display = 'block';
  }

  /* ── واتساب ── */
  let waMsg = 'مرحباً، أريد مقايسة لـ ' + pkgName + '\n';
  waMsg += 'المساحة: ' + area + ' م²\n';
  waMsg += 'سعر المتر: ' + pricePerM2 + ' $' + (hasCustom ? ' (بعد التخصيص)' : '') + '\n';
  waMsg += 'التكلفة: ' + total.toLocaleString('ar') + ' $\n';
  if (hasRate) {
    waMsg += 'سعر الصرف: 1$ = ' + rate.toLocaleString('ar') + ' ل.س\n';
    waMsg += 'التكلفة بالليرة: ' + formatSYP(Math.round(total*rate)) + '\n';
  }
  waMsg += 'أرجو التواصل معي للمزيد من التفاصيل.';
  btnWA.href = 'https://wa.me/00963986555105?text=' + encodeURIComponent(waMsg);
  btnWA.classList.add('show');

  result.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/* ── Init ── */
document.addEventListener('DOMContentLoaded', () => {
  initBASlider();
  if (typeof AOS !== 'undefined') AOS.init({ duration:700, once:true, offset:80 });
});
