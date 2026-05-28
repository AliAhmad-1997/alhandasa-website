/* ═══════════════════════════════════════════
   ENHANCEMENTS JS — الهندسية التقدمية
   1. Before/After Slider
   2. Cost Calculator
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
// أسعار لكل متر مربع بالدولار
const PRICES = {
  basic:    65,   // اقتصادية
  standard: 120,  // متوسطة
  premium:  200,  // فاخرة
  taqsit2:  85,   // تقسيط الدرجة الثانية
  taqsit1:  110,  // تقسيط الدرجة الأولى
  momtaza:  180,  // الممتازة
  super:    300   // السوبر فاخرة
};

const PACKAGE_NAMES = {
  basic:    'الباقة الاقتصادية',
  standard: 'الباقة المتوسطة',
  premium:  'الباقة الفاخرة',
  taqsit2:  'باقة التقسيط الدرجة الثانية',
  taqsit1:  'باقة التقسيط الدرجة الأولى',
  momtaza:  'الباقة الممتازة',
  super:    'الباقة السوبر فاخرة'
};

function calcCost() {
  const typeEl  = document.getElementById('calcType');
  const areaEl  = document.getElementById('calcArea');
  const result  = document.getElementById('calcResult');
  const btnWA   = document.getElementById('btnWhatsapp');

  if (!typeEl || !areaEl) return;

  const type = typeEl.value;
  const area = parseFloat(areaEl.value);

  if (!type) { areaEl.focus(); return; }
  if (!area || area <= 0 || area > 10000) {
    areaEl.style.borderColor = '#ef4444';
    setTimeout(() => areaEl.style.borderColor = '', 1500);
    return;
  }

  const pricePerM2 = PRICES[type];
  const total      = Math.round(area * pricePerM2);
  const monthly12  = Math.round(total / 12);
  const monthly24  = Math.round(total / 24);

  document.getElementById('calcTotal').textContent    = total.toLocaleString('ar') + ' $';
  document.getElementById('calcMonthly12').textContent = monthly12.toLocaleString('ar') + ' $';
  document.getElementById('calcMonthly24').textContent = monthly24.toLocaleString('ar') + ' $';
  document.getElementById('calcPriceM2').textContent   = pricePerM2 + ' $';

  result.classList.add('show');

  // زر الواتساب
  const msg = encodeURIComponent(
    `مرحباً، أريد مقايسة لـ ${PACKAGE_NAMES[type]}\n` +
    `المساحة: ${area} م²\n` +
    `التكلفة التقريبية: ${total.toLocaleString('ar')} $\n` +
    `أرجو التواصل معي للمزيد من التفاصيل.`
  );
  btnWA.href = `https://wa.me/00963986555105?text=${msg}`;
  btnWA.classList.add('show');

  // scroll للنتيجة
  result.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/* ── Init ── */
document.addEventListener('DOMContentLoaded', () => {
  initBASlider();

  // AOS init (إذا كانت المكتبة محمّلة)
  if (typeof AOS !== 'undefined') {
    AOS.init({ duration: 700, once: true, offset: 80 });
  }
});
