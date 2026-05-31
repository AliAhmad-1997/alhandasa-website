import logging
import os
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup,
    InputMediaPhoto
)
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes, ConversationHandler
)
from telegram.constants import ChatAction

# ══════════════════════════════════════════════════════════════
# ⚙️  الإعدادات — كل القيم من متغيرات البيئة فقط
# ══════════════════════════════════════════════════════════════
TOKEN    = os.environ["BOT_TOKEN"]          # مطلوب — لا توكن = لا تشغيل
ADMIN_ID = int(os.environ.get("ADMIN_ID", "0"))   # Chat ID للمشرف
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "")

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ══════════════════════════════════════════════════════════════
# 📦  بيانات الباقات
# ══════════════════════════════════════════════════════════════
PACKAGES = {
    "pkg_65": {
        "name": "الباقة الاقتصادية", "icon": "🏠", "price": 65,
        "desc": "مثالية للغرف والشقق الصغيرة",
        "features": [
            "💧 السباكة: PPR السعد، 10 برميل المسعود، سخان إيطالي 17 كيلو",
            "⚡ الكهرباء: أسلاك لينا، مفاتيح برايز، قواطع كاملة",
            "🎨 التشطيبات: بلاط حسواني 30×30، سيراميك زنوبيا 50×50، أبواب ألمنيوم مسالكو",
        ],
    },
    "pkg_120": {
        "name": "الباقة المتوسطة", "icon": "🏢", "price": 120,
        "desc": "للشقق والمنازل المتوسطة — الأكثر طلباً ⭐",
        "features": [
            "💧 السباكة: كل الاقتصادية + PPR ساخن 32mm، خلاطات برنس",
            "⚡ الكهرباء: كل الاقتصادية + إضاءة LED متكاملة، تأريض وحماية",
            "🎨 التشطيبات: كل الاقتصادية + خشب سويد، صيني برنس فاخر",
        ],
    },
    "pkg_200": {
        "name": "الباقة الفاخرة", "icon": "👑", "price": 200,
        "desc": "للفلل والمشاريع الكبيرة",
        "features": [
            "💧 السباكة: PPR كالدا، خلاطات ومغاسل برنس فاخرة، نظام مياه مستقل",
            "⚡ الكهرباء: لوحة قواطع ذكية، طاقة شمسية 4 ألواح + بطارية 200A",
            "🎨 التشطيبات: واجهة ألمنيوم فاخرة، كومبوزيت، زجاج مزدوج، ديكور كامل",
        ],
    },
    "pkg_85": {
        "name": "باقة التقسيط الدرجة الثانية", "icon": "💳", "price": 85,
        "desc": "تقسيط مريح للشقق الصغيرة",
        "features": [
            "💧 PPR السعد 20 بار، 10 برميل المسعود",
            "⚡ أسلاك لينا، مفاتيح برايز",
            "🎨 بلاط حسواني 30×30، أبواب خشب سويد + ألمنيوم مسالكو",
        ],
    },
    "pkg_180": {
        "name": "الباقة الممتازة", "icon": "⭐", "price": 180,
        "desc": "للشقق والمنازل المتوسطة",
        "features": [
            "💧 PPR كالدا، برميل 3 طبقات حديد",
            "⚡ VIMAR كوري، تكييف صالون 2 طن، طاقة شمسية 4 ألواح",
            "🎨 سعودي 60×120 جدران، سويد ملبس قشر سنديان",
        ],
    },
    "pkg_300": {
        "name": "الباقة السوبر فاخرة", "icon": "💎", "price": 300,
        "desc": "للفلل والمشاريع الكبيرة VIP",
        "features": [
            "💧 كالدا، غندور 10×2، حنفية كولار",
            "⚡ 8 ألواح طاقة شمسية + بطارية 300A، تدفئة أرضية",
            "🎨 هندي 120×60 أرضية، كومبوزيت، ديكور كامل فاخر",
        ],
    },
}

SHOP_ITEMS = [
    {"name": "سخان إيطالي 17 كيلو (البهاء)", "icon": "🔥"},
    {"name": "خلاطات برنس فاخرة",             "icon": "🚿"},
    {"name": "ألواح طاقة شمسية 400W",          "icon": "☀️"},
    {"name": "بطارية 200A",                    "icon": "🔋"},
    {"name": "مفاتيح VIMAR كوري",              "icon": "💡"},
    {"name": "سيراميك زنوبيا 60×60",           "icon": "🏠"},
    {"name": "أسلاك لينا 6mm",                 "icon": "⚡"},
    {"name": "PPR السعد 20 بار",               "icon": "💧"},
]

WHATSAPP = "https://wa.me/00963986555105"
WEBSITE  = "https://aliahmad-1997.github.io/Advance-Engineering-Company/"
PHONE    = "0986555105"

# ══════════════════════════════════════════════════════════════
# 🧠  FAQ — أسئلة شائعة مع ردود تلقائية
# ══════════════════════════════════════════════════════════════
FAQ = [
    {
        "keywords": ["سعر", "كم", "تكلفة", "تكلف", "بكم", "أسعار"],
        "answer": (
            "💰 *أسعارنا تبدأ من 65$ للمتر المربع*\n\n"
            "لدينا 6 باقات تناسب كل الميزانيات:\n"
            "• 🏠 الاقتصادية — 65$/م²\n"
            "• 💳 التقسيط — 85$/م²\n"
            "• 🏢 المتوسطة — 120$/م²\n"
            "• ⭐ الممتازة — 180$/م²\n"
            "• 👑 الفاخرة — 200$/م²\n"
            "• 💎 السوبر فاخرة — 300$/م²\n\n"
            "اضغط /start للاستعراض الكامل أو استخدم الحاسبة لمعرفة تكلفة مشروعك تحديداً 🧮"
        ),
    },
    {
        "keywords": ["وين", "فين", "موقع", "عنوان", "حمص", "سوريا"],
        "answer": (
            "📍 *موقعنا*\n\n"
            "الشركة الهندسية التقدمية\n"
            "📌 حمص — سوريا\n\n"
            f"📱 للتواصل: *{PHONE}*\n"
            f"🌐 [زيارة الموقع]({WEBSITE})"
        ),
    },
    {
        "keywords": ["ضمان", "كفالة", "ضمانة"],
        "answer": (
            "✅ *الضمان*\n\n"
            "نقدم ضماناً على جميع أعمالنا:\n"
            "• ضمان سنة كاملة على أعمال السباكة\n"
            "• ضمان سنتين على أعمال الكهرباء\n"
            "• ضمان على جودة مواد التشطيب\n\n"
            "للاستفسار أكثر تواصل معنا مباشرة 📞"
        ),
    },
    {
        "keywords": ["تقسيط", "دفع", "قسط", "أقساط"],
        "answer": (
            "💳 *نظام التقسيط*\n\n"
            "نعم! نوفر خيارات تقسيط مريحة:\n"
            "• تقسيط 12 شهر\n"
            "• تقسيط 24 شهر\n\n"
            "استخدم الحاسبة لمعرفة قيمة القسط الشهري لمشروعك 🧮\n"
            "أو تواصل معنا مباشرة للتفاصيل 📱"
        ),
    },
    {
        "keywords": ["كم وقت", "مدة", "متى", "ينتهي", "تنتهي"],
        "answer": (
            "⏱️ *مدة التنفيذ*\n\n"
            "تعتمد على حجم المشروع:\n"
            "• شقة صغيرة (80-100م²): 3-4 أسابيع\n"
            "• شقة متوسطة (100-150م²): 4-6 أسابيع\n"
            "• فيلا أو مشروع كبير: حسب الاتفاق\n\n"
            "نلتزم بالمواعيد المتفق عليها ✅"
        ),
    },
    {
        "keywords": ["خبرة", "منذ", "سنة", "سنوات", "تجربة"],
        "answer": (
            "🏆 *خبرتنا*\n\n"
            "• منذ عام *2005* في المجال\n"
            "• أكثر من *500 مشروع منجز*\n"
            "• أكثر من *200 عميل راضٍ*\n"
            "• *20 سنة* خبرة متراكمة\n"
            "• *15 قسم* متخصص\n\n"
            "جودتنا تتحدث عن نفسها 💪"
        ),
    },
    {
        "keywords": ["طاقة شمسية", "سولار", "كهرباء شمسية", "ألواح"],
        "answer": (
            "☀️ *الطاقة الشمسية*\n\n"
            "نوفر حلول طاقة شمسية متكاملة:\n"
            "• 4 ألواح 400W (متضمنة في الباقة الفاخرة)\n"
            "• 8 ألواح 400W (متضمنة في السوبر فاخرة)\n"
            "• بطاريات 200A و 300A\n"
            "• تركيب وصيانة كاملة\n\n"
            "للاستفسار تواصل معنا 📱"
        ),
    },
]

# ══════════════════════════════════════════════════════════════
# 🔄  حالات المحادثة (ConversationHandler)
# ══════════════════════════════════════════════════════════════
# حاسبة التكاليف
CALC_CHOOSE_PKG, CALC_AREA, CALC_RATE = range(3)

# نموذج الطلب
ORDER_NAME, ORDER_AREA_TEXT, ORDER_REGION, ORDER_PROJECT_TYPE, ORDER_NOTES = range(5, 10)

# تقييم
RATING_WAIT = 20

# ══════════════════════════════════════════════════════════════
# 🛠️  دوال مساعدة
# ══════════════════════════════════════════════════════════════
def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📦 الباقات والأسعار",       callback_data="packages")],
        [InlineKeyboardButton("🧮 احسب تكلفة مشروعك",     callback_data="calc_start"),
         InlineKeyboardButton("📋 اطلب عرض سعر",          callback_data="order_start")],
        [InlineKeyboardButton("🛒 المتجر الاختياري",       callback_data="shop"),
         InlineKeyboardButton("🏗️ أعمالنا السابقة",       callback_data="portfolio")],
        [InlineKeyboardButton("❓ الأسئلة الشائعة",        callback_data="faq"),
         InlineKeyboardButton("ℹ️ من نحن",                callback_data="about")],
        [InlineKeyboardButton("📞 تواصل معنا",             callback_data="contact")],
        [InlineKeyboardButton("🌐 زيارة الموقع",           url=WEBSITE)],
    ])

def back_to_main_btn():
    """زر ثابت للرجوع للقائمة الرئيسية"""
    return InlineKeyboardButton("🏠 الرئيسية", callback_data="back")

async def typing(update_or_query, ctx):
    """يُظهر مؤشر الكتابة قبل الرد — يجعل البوت يبدو أكثر حيوية"""
    try:
        chat_id = (
            update_or_query.message.chat_id
            if hasattr(update_or_query, "message") and update_or_query.message
            else update_or_query.effective_chat.id
        )
        await ctx.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    except Exception:
        pass

async def notify_admin(ctx: ContextTypes.DEFAULT_TYPE, message: str, reply_markup=None):
    """إرسال إشعار للمشرف"""
    if ADMIN_ID:
        try:
            await ctx.bot.send_message(
                chat_id=ADMIN_ID,
                text=message,
                parse_mode="Markdown",
                reply_markup=reply_markup,
            )
        except Exception as e:
            logger.warning(f"تعذّر إرسال إشعار للمشرف: {e}")

# ══════════════════════════════════════════════════════════════
# 🏠  /start — رسالة الترحيب
# ══════════════════════════════════════════════════════════════
WELCOME = """🏗️ *أهلاً وسهلاً في الشركة الهندسية التقدمية* 👋

سباكة • كهرباء • تشطيبات

نحن رائدون في مجال المقاولات والإنشاءات منذ *2005* 🏆
أكثر من *500 مشروع منجز* في حمص وسوريا

━━━━━━━━━━━━━━━━━━
كيف يمكنني مساعدتك اليوم؟ 👇"""

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await typing(update, ctx)
    # إرسال صورة الشركة مع رسالة الترحيب
    try:
        await update.message.reply_photo(
            photo="https://raw.githubusercontent.com/AliAhmad-1997/Advance-Engineering-Company/main/construction-site.png",
            caption=WELCOME,
            parse_mode="Markdown",
            reply_markup=main_menu_keyboard(),
        )
    except Exception:
        # fallback بدون صورة إذا فشل التحميل
        await update.message.reply_text(
            WELCOME, parse_mode="Markdown", reply_markup=main_menu_keyboard()
        )

# ══════════════════════════════════════════════════════════════
# 📞  /contact_support
# ══════════════════════════════════════════════════════════════
async def contact_support(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await typing(update, ctx)
    txt = (
        "📞 *تواصل مع الدعم*\n\n"
        f"📱 واتساب: *{PHONE}*\n"
        f"🌐 الموقع: [اضغط هنا]({WEBSITE})\n\n"
        "⏰ نرد على جميع الاستفسارات خلال ساعات العمل"
    )
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("💬 واتساب", url=WHATSAPP)],
        [InlineKeyboardButton("🌐 الموقع", url=WEBSITE)],
        [back_to_main_btn()],
    ])
    await update.message.reply_text(txt, parse_mode="Markdown", reply_markup=kb)

# ══════════════════════════════════════════════════════════════
# 🌐  /language
# ══════════════════════════════════════════════════════════════
async def language_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await typing(update, ctx)
    await update.message.reply_text(
        "🌐 *اللغة / Language*\n\n"
        "البوت يعمل باللغة العربية حالياً\n"
        "_The bot currently operates in Arabic_",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[back_to_main_btn()]]),
    )

# ══════════════════════════════════════════════════════════════
# 📦  الباقات
# ══════════════════════════════════════════════════════════════
async def show_packages(query):
    kb = [
        [InlineKeyboardButton(f"{p['icon']} {p['name']} — {p['price']}$/م²", callback_data=f"pkg_{k.split('_')[1]}")]
        for k, p in PACKAGES.items()
    ]
    kb.append([back_to_main_btn()])
    await query.edit_message_caption(
        caption="📦 *اختر الباقة لتعرف تفاصيلها:*\n\n_الأسعار شاملة المواد والعمالة_",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(kb),
    )

async def show_package_detail(query, key):
    p = PACKAGES.get(key)
    if not p:
        return
    txt = (
        f"{p['icon']} *{p['name']}*\n"
        f"_{p['desc']}_\n\n"
        f"💰 *السعر: {p['price']}$ للمتر المربع*\n\n"
        + "\n".join(f"• {f}" for f in p["features"])
        + f"\n\n📐 *مثال:* شقة 100م² = *{p['price'] * 100:,}$*"
    )
    kb = [
        [InlineKeyboardButton("🧮 احسب تكلفة مشروعي بهذه الباقة", callback_data=f"calc_from_{key}")],
        [InlineKeyboardButton("📋 اطلب عرض سعر رسمي",             callback_data=f"order_from_{key}")],
        [InlineKeyboardButton("💬 استفسر عبر واتساب",
                              url=f"{WHATSAPP}?text=مرحباً، أريد الاستفسار عن {p['name']} ({p['price']}$/م²)")],
        [InlineKeyboardButton("🔙 رجوع للباقات", callback_data="packages")],
    ]
    await query.edit_message_caption(
        caption=txt, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb)
    )

# ══════════════════════════════════════════════════════════════
# 🧮  حاسبة التكاليف — ConversationHandler
# ══════════════════════════════════════════════════════════════
async def calc_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    # إذا جاء من باقة محددة مباشرة
    if query.data.startswith("calc_from_"):
        key = query.data.replace("calc_from_", "")
        p   = PACKAGES.get(key)
        if p:
            ctx.user_data["calc_pkg"] = key
            await query.edit_message_caption(
                caption=(
                    f"🧮 *حاسبة التكاليف*\n\n"
                    f"الباقة: {p['icon']} *{p['name']}* ({p['price']}$/م²)\n\n"
                    "📐 أرسل لي *المساحة بالمتر المربع:*\n"
                    "_مثال: 120_"
                ),
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ إلغاء", callback_data="back")]]),
            )
            return CALC_AREA
    # اختيار الباقة أولاً
    kb = [
        [InlineKeyboardButton(f"{p['icon']} {p['name']} ({p['price']}$/م²)", callback_data=f"cpkg_{k}")]
        for k, p in PACKAGES.items()
    ]
    kb.append([InlineKeyboardButton("❌ إلغاء", callback_data="back")])
    await query.edit_message_caption(
        caption="🧮 *حاسبة التكاليف*\n\nاختر الباقة أولاً:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(kb),
    )
    return CALC_CHOOSE_PKG

async def calc_choose_pkg(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    key = query.data.replace("cpkg_", "")
    p   = PACKAGES.get(key)
    if not p:
        return CALC_CHOOSE_PKG
    ctx.user_data["calc_pkg"] = key
    await query.edit_message_caption(
        caption=(
            f"🧮 *حاسبة التكاليف*\n\n"
            f"الباقة: {p['icon']} *{p['name']}* ({p['price']}$/م²)\n\n"
            "📐 أرسل لي *المساحة بالمتر المربع:*\n"
            "_مثال: 120_"
        ),
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ إلغاء", callback_data="back")]]),
    )
    return CALC_AREA

async def calc_area(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await typing(update, ctx)
    text = update.message.text.strip().replace(",", "").replace("م²", "").replace("م2", "")
    try:
        area = float(text)
        if area <= 0 or area > 50000:
            raise ValueError
    except ValueError:
        await update.message.reply_text(
            "⚠️ أرسل رقماً صحيحاً فقط، مثال: *120*\n_لا حروف ولا رموز_",
            parse_mode="Markdown",
        )
        return CALC_AREA
    ctx.user_data["calc_area"] = area
    kb = [
        [InlineKeyboardButton("⏭️ بالدولار فقط (تخطى)", callback_data="skip_rate")],
        [InlineKeyboardButton("❌ إلغاء", callback_data="back")],
    ]
    await update.message.reply_text(
        f"✅ المساحة: *{area:g} م²*\n\n"
        "💱 أرسل *سعر صرف الدولار* بالليرة السورية للحساب بالعملتين\n"
        "_مثال: 13000_\n\n"
        "أو اضغط *تخطى* للحساب بالدولار فقط",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(kb),
    )
    return CALC_RATE

async def calc_rate(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await typing(update, ctx)
    text = update.message.text.strip().replace(",", "")
    try:
        rate = float(text)
        if rate <= 0:
            raise ValueError
    except ValueError:
        await update.message.reply_text(
            "⚠️ أرسل رقماً صحيحاً، مثال: *13000*",
            parse_mode="Markdown",
        )
        return CALC_RATE
    await _send_calc_result(update.message, ctx, rate=rate)
    return ConversationHandler.END

async def calc_skip_rate(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await _send_calc_result(query.message, ctx, rate=None)
    return ConversationHandler.END

async def _send_calc_result(message, ctx, rate=None):
    """إرسال نتيجة الحساب — داخلية"""
    pkg_key = ctx.user_data.get("calc_pkg", "pkg_120")
    area    = ctx.user_data.get("calc_area", 100)
    p       = PACKAGES.get(pkg_key, PACKAGES["pkg_120"])
    price   = p["price"]
    total   = round(area * price)
    m12     = round(total / 12)
    m24     = round(total / 24)

    txt = (
        f"🧮 *نتيجة الحساب*\n\n"
        f"{p['icon']} *{p['name']}*\n"
        f"📐 المساحة: *{area:g} م²*\n"
        f"💰 سعر المتر: *{price} $*\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"💵 *الإجمالي: {total:,} $*\n"
        f"📅 قسط 12 شهر: *{m12:,} $*\n"
        f"📅 قسط 24 شهر: *{m24:,} $*\n"
        "━━━━━━━━━━━━━━━━━━"
    )
    if rate:
        total_syp = round(total * rate)
        m12_syp   = round(m12   * rate)
        m24_syp   = round(m24   * rate)
        txt += (
            f"\n\n🇸🇾 *بالليرة السورية* (1$={rate:,.0f} ل.س)\n"
            "━━━━━━━━━━━━━━━━━━\n"
            f"💴 *الإجمالي: {total_syp:,} ل.س*\n"
            f"📅 قسط 12 شهر: *{m12_syp:,} ل.س*\n"
            f"📅 قسط 24 شهر: *{m24_syp:,} ل.س*\n"
            "━━━━━━━━━━━━━━━━━━"
        )
    txt += "\n_* الأسعار تقديرية وتشمل المواد والعمالة_"

    wa_text = f"مرحباً، أريد مقايسة لـ {p['name']}%0aالمساحة: {area:g} م²%0aالإجمالي: {total:,}$"
    if rate:
        wa_text += f"%0aبالليرة: {round(total * rate):,} ل.س"

    kb = [
        [InlineKeyboardButton("📋 اطلب عرض سعر رسمي",        callback_data="order_start")],
        [InlineKeyboardButton("💬 أرسل المقايسة عبر واتساب", url=f"{WHATSAPP}?text={wa_text}")],
        [InlineKeyboardButton("🔄 احسب باقة أخرى",            callback_data="calc_start")],
        [InlineKeyboardButton("🔙 القائمة الرئيسية",          callback_data="back")],
    ]
    await message.reply_text(txt, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))
    # طلب التقييم بعد الحساب
    await _ask_rating(message, ctx)

# ══════════════════════════════════════════════════════════════
# 📋  نظام الطلبات الرسمي — ConversationHandler
# ══════════════════════════════════════════════════════════════
async def order_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    # إذا جاء من باقة محددة
    if query.data.startswith("order_from_"):
        key = query.data.replace("order_from_", "")
        ctx.user_data["order_pkg"] = key
    else:
        ctx.user_data.pop("order_pkg", None)

    await query.edit_message_caption(
        caption=(
            "📋 *طلب عرض سعر رسمي*\n\n"
            "سأحتاج منك بعض المعلومات لإعداد عرض مخصص لك 📝\n\n"
            "*الخطوة 1/5 — ما اسمك الكريم؟*"
        ),
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ إلغاء", callback_data="back")]]),
    )
    return ORDER_NAME

async def order_name(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await typing(update, ctx)
    ctx.user_data["order_name"] = update.message.text.strip()
    await update.message.reply_text(
        f"👋 أهلاً *{ctx.user_data['order_name']}*!\n\n"
        "*الخطوة 2/5 — ما مساحة المشروع بالمتر المربع؟*\n"
        "_مثال: 150_",
        parse_mode="Markdown",
    )
    return ORDER_AREA_TEXT

async def order_area(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await typing(update, ctx)
    text = update.message.text.strip().replace(",", "").replace("م²", "").replace("م2", "")
    try:
        area = float(text)
        if area <= 0 or area > 50000:
            raise ValueError
        ctx.user_data["order_area"] = area
    except ValueError:
        await update.message.reply_text(
            "⚠️ أرسل رقماً صحيحاً فقط، مثال: *150*", parse_mode="Markdown"
        )
        return ORDER_AREA_TEXT
    await update.message.reply_text(
        "*الخطوة 3/5 — في أي منطقة المشروع؟*\n"
        "_مثال: حمص — الزهراء_",
        parse_mode="Markdown",
    )
    return ORDER_REGION

async def order_region(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await typing(update, ctx)
    ctx.user_data["order_region"] = update.message.text.strip()
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🏠 شقة سكنية",   callback_data="otype_شقة سكنية"),
         InlineKeyboardButton("🏢 مكتب تجاري",  callback_data="otype_مكتب تجاري")],
        [InlineKeyboardButton("🏗️ فيلا",        callback_data="otype_فيلا"),
         InlineKeyboardButton("🏭 مشروع تجاري", callback_data="otype_مشروع تجاري")],
        [InlineKeyboardButton("🔧 ترميم",        callback_data="otype_ترميم"),
         InlineKeyboardButton("📝 أخرى",         callback_data="otype_أخرى")],
    ])
    await update.message.reply_text(
        "*الخطوة 4/5 — ما نوع المشروع؟*",
        parse_mode="Markdown",
        reply_markup=kb,
    )
    return ORDER_PROJECT_TYPE

async def order_project_type(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    ctx.user_data["order_type"] = query.data.replace("otype_", "")
    await query.edit_message_text(
        "*الخطوة 5/5 — أي ملاحظات أو تفاصيل إضافية؟*\n\n"
        "_مثال: أريد إضافة طاقة شمسية، أو لدي تصميم خاص..._\n\n"
        "أو أرسل *تخطى* إذا لا يوجد",
        parse_mode="Markdown",
    )
    return ORDER_NOTES

async def order_notes(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await typing(update, ctx)
    notes = update.message.text.strip()
    if notes.lower() in ["تخطى", "لا", "skip", "-"]:
        notes = "لا توجد ملاحظات"
    ctx.user_data["order_notes"] = notes
    await _finalize_order(update.message, ctx)
    return ConversationHandler.END

async def _finalize_order(message, ctx):
    """إتمام الطلب وإرسال إشعار للمشرف"""
    d = ctx.user_data
    pkg_info = ""
    if d.get("order_pkg"):
        p = PACKAGES.get(d["order_pkg"])
        if p:
            pkg_info = f"\n📦 الباقة المهتم بها: *{p['name']}* ({p['price']}$/م²)"

    # رسالة التأكيد للمستخدم
    confirm_txt = (
        "✅ *تم استلام طلبك بنجاح!*\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"👤 الاسم: *{d.get('order_name', '-')}*\n"
        f"📐 المساحة: *{d.get('order_area', '-')} م²*\n"
        f"📍 المنطقة: *{d.get('order_region', '-')}*\n"
        f"🏗️ نوع المشروع: *{d.get('order_type', '-')}*\n"
        f"📝 الملاحظات: {d.get('order_notes', '-')}"
        + pkg_info +
        "\n━━━━━━━━━━━━━━━━━━\n\n"
        "سيتواصل معك فريقنا *خلال 24 ساعة* 📞\n\n"
        "أو يمكنك التواصل المباشر:"
    )
    kb = [
        [InlineKeyboardButton("💬 واتساب مباشر", url=WHATSAPP)],
        [back_to_main_btn()],
    ]
    await message.reply_text(confirm_txt, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))

    # إشعار المشرف
    user = message.from_user
    admin_txt = (
        "🔔 *طلب عرض سعر جديد!*\n\n"
        f"👤 الاسم: *{d.get('order_name', '-')}*\n"
        f"📱 تيليغرام: @{user.username or 'لا يوجد'} (ID: `{user.id}`)\n"
        f"📐 المساحة: *{d.get('order_area', '-')} م²*\n"
        f"📍 المنطقة: *{d.get('order_region', '-')}*\n"
        f"🏗️ نوع المشروع: *{d.get('order_type', '-')}*\n"
        f"📝 الملاحظات: {d.get('order_notes', '-')}"
        + pkg_info
    )
    admin_kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("💬 رد مباشر عبر تيليغرام", url=f"tg://user?id={user.id}")],
        [InlineKeyboardButton("📱 واتساب", url=WHATSAPP)],
    ])
    await notify_admin(ctx, admin_txt, reply_markup=admin_kb)

# ══════════════════════════════════════════════════════════════
# ⭐  نظام التقييم
# ══════════════════════════════════════════════════════════════
async def _ask_rating(message, ctx):
    """يطلب تقييم بعد إتمام عملية"""
    kb = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⭐",     callback_data="rate_1"),
            InlineKeyboardButton("⭐⭐",   callback_data="rate_2"),
            InlineKeyboardButton("⭐⭐⭐", callback_data="rate_3"),
            InlineKeyboardButton("⭐⭐⭐⭐", callback_data="rate_4"),
            InlineKeyboardButton("⭐⭐⭐⭐⭐", callback_data="rate_5"),
        ]
    ])
    await message.reply_text(
        "كيف تقيّم تجربتك مع البوت؟ 😊",
        reply_markup=kb,
    )

async def handle_rating(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    stars = int(query.data.split("_")[1])
    star_str = "⭐" * stars
    responses = {
        1: "شكراً على تقييمك! سنعمل على التحسين 🙏",
        2: "شكراً! نسعى دائماً لتقديم الأفضل 💪",
        3: "شكراً على تقييمك! 😊",
        4: "شكراً جزيلاً! سعداء بخدمتك 🌟",
        5: "شكراً جزيلاً! تقييمك يشجعنا على التميز 🏆",
    }
    await query.edit_message_text(
        f"{star_str}\n\n{responses[stars]}\n\nاضغط /start للعودة للقائمة",
        parse_mode="Markdown",
    )
    # إشعار المشرف بالتقييم
    user = query.from_user
    await notify_admin(
        ctx,
        f"📊 *تقييم جديد*\n"
        f"👤 @{user.username or user.first_name} (ID: `{user.id}`)\n"
        f"التقييم: {star_str} ({stars}/5)",
    )

# ══════════════════════════════════════════════════════════════
# 🏗️  أعمالنا السابقة
# ══════════════════════════════════════════════════════════════
PORTFOLIO = [
    {
        "title": "فيلا فاخرة — حمص",
        "desc": "تشطيب كامل، طاقة شمسية 8 ألواح، ديكور فاخر\nالمساحة: 350م² | الباقة: السوبر فاخرة",
        "url": "https://raw.githubusercontent.com/AliAhmad-1997/Advance-Engineering-Company/main/luxury-interior.png",
    },
    {
        "title": "حمام فاخر — حمص",
        "desc": "سيراميك إيطالي، خلاطات برنس، إضاءة LED\nتشطيب درجة أولى",
        "url": "https://raw.githubusercontent.com/AliAhmad-1997/Advance-Engineering-Company/main/luxury-bathroom.png",
    },
    {
        "title": "موقع إنشاء — مشروع تجاري",
        "desc": "مقاولات عامة، هيكل خرساني، إشراف هندسي كامل",
        "url": "https://raw.githubusercontent.com/AliAhmad-1997/Advance-Engineering-Company/main/construction-site.png",
    },
]

async def show_portfolio(query):
    await query.edit_message_caption(
        caption=(
            "🏗️ *أعمالنا السابقة*\n\n"
            "اختر مشروعاً لترى تفاصيله 👇"
        ),
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(f"🖼️ {p['title']}", callback_data=f"port_{i}")] for i, p in enumerate(PORTFOLIO)]
            + [[back_to_main_btn()]]
        ),
    )

async def show_portfolio_item(query, idx):
    p = PORTFOLIO[idx]
    try:
        await query.message.reply_photo(
            photo=p["url"],
            caption=f"🏗️ *{p['title']}*\n\n_{p['desc']}_",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📋 اطلب مشروعاً مشابهاً", callback_data="order_start")],
                [InlineKeyboardButton("🔙 رجوع للأعمال", callback_data="portfolio")],
            ]),
        )
    except Exception:
        await query.answer("تعذّر تحميل الصورة، حاول لاحقاً", show_alert=True)

# ══════════════════════════════════════════════════════════════
# ❓  الأسئلة الشائعة
# ══════════════════════════════════════════════════════════════
async def show_faq(query):
    faq_topics = [
        ("💰 الأسعار والباقات",  "faq_0"),
        ("📍 الموقع والعنوان",    "faq_1"),
        ("✅ الضمان",             "faq_2"),
        ("💳 التقسيط",           "faq_3"),
        ("⏱️ مدة التنفيذ",       "faq_4"),
        ("🏆 خبرتنا",            "faq_5"),
        ("☀️ الطاقة الشمسية",    "faq_6"),
    ]
    kb = [[InlineKeyboardButton(label, callback_data=cb)] for label, cb in faq_topics]
    kb.append([back_to_main_btn()])
    await query.edit_message_caption(
        caption="❓ *الأسئلة الشائعة*\n\nاختر الموضوع الذي تريد معرفة المزيد عنه:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(kb),
    )

# ══════════════════════════════════════════════════════════════
# 🎛️  الـ Callback الرئيسي
# ══════════════════════════════════════════════════════════════
async def handle_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data

    # ── الباقات ──
    if data == "packages":
        await show_packages(q)

    elif data.startswith("pkg_"):
        key = "pkg_" + data.split("_")[1]
        await show_package_detail(q, key)

    # ── المتجر ──
    elif data == "shop":
        txt = "🛒 *المتجر الاختياري*\n_مواد وتجهيزات بأفضل الأسعار_\n\n"
        for item in SHOP_ITEMS:
            txt += f"{item['icon']} {item['name']}\n"
        txt += "\n💬 للاستفسار عن الأسعار تواصل معنا مباشرة"
        kb = [
            [InlineKeyboardButton("💬 استفسر عبر واتساب",
                                  url=f"{WHATSAPP}?text=مرحباً، أريد الاستفسار عن المتجر الاختياري")],
            [back_to_main_btn()],
        ]
        await q.edit_message_caption(caption=txt, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))

    # ── أعمالنا السابقة ──
    elif data == "portfolio":
        await show_portfolio(q)

    elif data.startswith("port_"):
        await show_portfolio_item(q, int(data.split("_")[1]))

    # ── الأسئلة الشائعة (أزرار) ──
    elif data == "faq":
        await show_faq(q)

    elif data.startswith("faq_"):
        idx = int(data.split("_")[1])
        if idx < len(FAQ):
            await q.edit_message_caption(
                caption=FAQ[idx]["answer"],
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔙 رجوع للأسئلة", callback_data="faq")],
                    [back_to_main_btn()],
                ]),
            )

    # ── من نحن ──
    elif data == "about":
        txt = (
            "ℹ️ *الشركة الهندسية التقدمية*\n\n"
            "🏗️ شركة مقاولات معتمدة منذ *2005*\n"
            "📍 حمص — سوريا\n\n"
            "✅ أكثر من *500 مشروع منجز*\n"
            "✅ أكثر من *200 عميل راضٍ*\n"
            "✅ *20 سنة* خبرة في المجال\n"
            "✅ *15 قسم* متخصص\n\n"
            "*خدماتنا:*\n"
            "• المقاولات العامة\n"
            "• التصميم الهندسي\n"
            "• الكهرباء والميكانيك\n"
            "• السباكة والصرف\n"
            "• الديكور والتشطيب\n"
            "• تنسيق الحدائق"
        )
        await q.edit_message_caption(
            caption=txt, parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[back_to_main_btn()]]),
        )

    # ── تواصل ──
    elif data == "contact":
        txt = (
            "📞 *تواصل معنا*\n\n"
            f"📱 واتساب: *{PHONE}*\n"
            f"🌐 الموقع: [اضغط هنا]({WEBSITE})\n\n"
            "⏰ نرد على جميع الاستفسارات خلال ساعات العمل"
        )
        kb = [
            [InlineKeyboardButton("💬 واتساب",  url=WHATSAPP)],
            [InlineKeyboardButton("🌐 الموقع",  url=WEBSITE)],
            [back_to_main_btn()],
        ]
        await q.edit_message_caption(caption=txt, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))

    # ── رجوع للقائمة الرئيسية ──
    elif data == "back":
        await q.edit_message_caption(
            caption=WELCOME, parse_mode="Markdown", reply_markup=main_menu_keyboard()
        )

    # ── التقييم ──
    elif data.startswith("rate_"):
        await handle_rating(update, ctx)

# ══════════════════════════════════════════════════════════════
# 💬  استقبال الرسائل النصية — FAQ تلقائي
# ══════════════════════════════════════════════════════════════
async def handle_message(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().lower()

    # بحث في الـ FAQ
    for item in FAQ:
        if any(kw in text for kw in item["keywords"]):
            await typing(update, ctx)
            await update.message.reply_text(
                item["answer"],
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([
                    [back_to_main_btn()]
                ]),
            )
            return

    # رد افتراضي
    await typing(update, ctx)
    await update.message.reply_text(
        "لم أفهم رسالتك 😅\n\nاضغط /start للعودة للقائمة الرئيسية\nأو تواصل معنا مباشرة 📞",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [back_to_main_btn()],
            [InlineKeyboardButton("💬 واتساب", url=WHATSAPP)],
        ]),
    )

# ══════════════════════════════════════════════════════════════
# 🚀  التشغيل
# ══════════════════════════════════════════════════════════════
async def set_commands(app):
    await app.bot.set_my_commands([
        ("start",           "🏠 ابدأ — القائمة الرئيسية"),
        ("contact_support", "📞 تواصل معنا"),
        ("language",        "🌐 اللغة"),
    ])

def main():
    app = Application.builder().token(TOKEN).post_init(set_commands).build()

    # ── ConversationHandler للحاسبة ──
    calc_conv = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(calc_start, pattern="^calc_start$"),
            CallbackQueryHandler(calc_start, pattern="^calc_from_"),
        ],
        states={
            CALC_CHOOSE_PKG: [CallbackQueryHandler(calc_choose_pkg, pattern="^cpkg_")],
            CALC_AREA:       [MessageHandler(filters.TEXT & ~filters.COMMAND, calc_area)],
            CALC_RATE:       [
                MessageHandler(filters.TEXT & ~filters.COMMAND, calc_rate),
                CallbackQueryHandler(calc_skip_rate, pattern="^skip_rate$"),
            ],
        },
        fallbacks=[CallbackQueryHandler(handle_callback, pattern="^back$")],
        allow_reentry=True,
    )

    # ── ConversationHandler للطلبات ──
    order_conv = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(order_start, pattern="^order_start$"),
            CallbackQueryHandler(order_start, pattern="^order_from_"),
        ],
        states={
            ORDER_NAME:         [MessageHandler(filters.TEXT & ~filters.COMMAND, order_name)],
            ORDER_AREA_TEXT:    [MessageHandler(filters.TEXT & ~filters.COMMAND, order_area)],
            ORDER_REGION:       [MessageHandler(filters.TEXT & ~filters.COMMAND, order_region)],
            ORDER_PROJECT_TYPE: [CallbackQueryHandler(order_project_type, pattern="^otype_")],
            ORDER_NOTES:        [MessageHandler(filters.TEXT & ~filters.COMMAND, order_notes)],
        },
        fallbacks=[CallbackQueryHandler(handle_callback, pattern="^back$")],
        allow_reentry=True,
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("contact_support", contact_support))
    app.add_handler(CommandHandler("language", language_cmd))
    app.add_handler(calc_conv)
    app.add_handler(order_conv)
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("✅ البوت شغّال — الهندسية التقدمية")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
