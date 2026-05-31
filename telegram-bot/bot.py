import logging
import os
import json
import urllib.request
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes, ConversationHandler
)
from telegram.constants import ChatAction

# ══════════════════════════════════════════════════════════════
# ⚙️  الإعدادات
# ══════════════════════════════════════════════════════════════
TOKEN    = os.environ["BOT_TOKEN"]
ADMIN_ID = int(os.environ.get("ADMIN_ID", "0"))

logging.basicConfig(format="%(asctime)s | %(levelname)s | %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

WHATSAPP    = "https://wa.me/00963986555105"
WEBSITE     = "https://aliahmad-1997.github.io/Advance-Engineering-Company/"
PHONE       = "0986555105"
EMAIL       = "aliahmad@gmail.com"
ADDRESS     = "حمص — شارع الأهرام، مقابل مدرسة جميل سرحان"
BOT_USERNAME = "AdvanceEngineeringBot"
PRICES_URL  = "https://raw.githubusercontent.com/AliAhmad-1997/Advance-Engineering-Company/main/prices.json"

# ══════════════════════════════════════════════════════════════
# 📥  تحميل الأسعار من prices.json (مصدر الحقيقة الوحيد)
# ══════════════════════════════════════════════════════════════
def load_prices():
    """يحمّل prices.json من GitHub — fallback للبيانات المحلية"""
    try:
        with urllib.request.urlopen(PRICES_URL, timeout=5) as r:
            return json.loads(r.read())
    except Exception as e:
        logger.warning(f"تعذّر تحميل prices.json: {e} — استخدام البيانات المحلية")
        return None

def build_packages_from_json(data):
    """يحوّل بيانات JSON لـ PACKAGES dict"""
    pkgs = {}
    for p in data["packages"]:
        pkgs[p["id"]] = {
            "name": p["name"], "icon": p["icon"],
            "price": p["price"], "unit": p["unit"],
            "desc": p["desc"],
            "features": {
                f"💧 السباكة": p["features"].get("السباكة", []),
                f"⚡ الكهرباء": p["features"].get("الكهرباء", []),
                f"🎨 التشطيبات": p["features"].get("التشطيبات", []),
            }
        }
    return pkgs

def build_shop_from_json(data):
    """يحوّل بيانات JSON لـ SHOP dict"""
    shop = {}
    icons = {"سيراميك وبلاط":"🏺","صحيات وسباكة":"💧","كهربائيات":"⚡","أبواب وشبابيك":"🚪","تشطيبات وديكور":"🎨"}
    for cat, items in data["shop"].items():
        icon = icons.get(cat, "📦")
        shop[f"{icon} {cat}"] = [{"id":i["id"],"name":i["name"],"price":"حسب الطلب"} for i in items]
    return shop

# تحميل البيانات عند بدء التشغيل
_prices_data = load_prices()
if _prices_data:
    PACKAGES = build_packages_from_json(_prices_data)
    _shop_raw = _prices_data["shop"]
    logger.info(f"✅ تم تحميل prices.json — {len(PACKAGES)} باقة")
else:
    _prices_data = None

# ══════════════════════════════════════════════════════════════
# 📦  7 باقات كاملة
# ══════════════════════════════════════════════════════════════
PACKAGES = {
    "pkg_65": {
        "name": "الباقة الاقتصادية", "icon": "🏠", "price": 65,
        "unit": "للغرفة الواحدة",
        "desc": "مثالية للغرف والشقق الصغيرة",
        "features": {
            "💧 السباكة": [
                "أنابيب PPR بارد 20mm — ساخن 25mm (السعد)",
                "10 برميل أبيض/أزرق (المسعود) — كفالة 5 سنوات",
                "سخان إيطالي 17 كيلو (البهاء)",
                "زنوبيا + دعسة + راصور + فرنجي",
                "حنفيات نحاس صيني (زاهية) + خلاطات + دوش",
            ],
            "⚡ الكهرباء": [
                "أسلاك: 6mm رئيسي — 1.5mm مفرد — 1mm مزدوج (لينا)",
                "مفاتيح برايز 3mm + ليد",
                "16 مفرد لكل غرفة — 32 مزدوج رئيسي",
                "قواطع + علب + اكسسوارات + إنارة LED",
            ],
            "🎨 التشطيبات": [
                "بلاط حسواني 30×30 أرضية",
                "سيراميك زنوبيا 50×50 حمام",
                "أبواب ألمنيوم مسالكو",
                "شبابيك ألمنيوم عادي",
            ],
        },
    },
    "pkg_85": {
        "name": "التقسيط الدرجة الثانية", "icon": "💳", "price": 85,
        "unit": "للمتر المربع",
        "desc": "تقسيط مريح للشقق الصغيرة",
        "features": {
            "💧 السباكة": [
                "PPR السعد 20 بار — برميل المسعود",
                "سخان إيطالي + صحيات زاهية",
            ],
            "⚡ الكهرباء": [
                "أسلاك لينا — مفاتيح برايز",
                "قواطع كاملة + إنارة",
            ],
            "🎨 التشطيبات": [
                "بلاط حسواني 30×30",
                "أبواب خشب سويد + ألمنيوم مسالكو",
            ],
        },
    },
    "pkg_110": {
        "name": "التقسيط الدرجة الأولى", "icon": "💳", "price": 110,
        "unit": "للمتر المربع",
        "desc": "تقسيط ممتاز للشقق المتوسطة",
        "features": {
            "💧 السباكة": [
                "PPR ساخن وبارد (السعد) — برميل 3 طبقات",
                "خلاطات برنس + سخان إيطالي",
            ],
            "⚡ الكهرباء": [
                "أسلاك لينا — مفاتيح برايز مع ليد",
                "تأريض + حماية كاملة",
            ],
            "🎨 التشطيبات": [
                "سيراميك زنوبيا 60×60",
                "خشب سويد — أبواب ألمنيوم",
            ],
        },
    },
    "pkg_120": {
        "name": "الباقة المتوسطة", "icon": "🏢", "price": 120,
        "unit": "للمتر المربع",
        "desc": "للشقق والمنازل المتوسطة — الأكثر طلباً ⭐",
        "features": {
            "💧 السباكة": [
                "PPR ساخن 32mm + بارد (السعد)",
                "خلاطات برنس فاخرة + سخان إيطالي",
                "برميل 3 طبقات حديد",
            ],
            "⚡ الكهرباء": [
                "أسلاك لينا كاملة + إضاءة LED متكاملة",
                "تأريض وحماية + قواطع احترافية",
            ],
            "🎨 التشطيبات": [
                "سيراميك زنوبيا 60×60 أرضية",
                "خشب سويد داخلي — صيني برنس فاخر",
                "أبواب ألمنيوم مسالكو",
            ],
        },
    },
    "pkg_180": {
        "name": "الباقة الممتازة", "icon": "⭐", "price": 180,
        "unit": "للمتر المربع",
        "desc": "للشقق والمنازل المتوسطة الراقية",
        "features": {
            "💧 السباكة": [
                "PPR كالدا — برميل 3 طبقات حديد",
                "خلاطات وصحيات برنس فاخرة",
            ],
            "⚡ الكهرباء": [
                "مفاتيح VIMAR كوري — أسلاك لينا",
                "تكييف صالون 2 طن",
                "طاقة شمسية 4 ألواح 400W",
            ],
            "🎨 التشطيبات": [
                "سعودي 60×120 جدران",
                "خشب سويد ملبس قشر سنديان",
                "واجهة ألمنيوم مطور",
            ],
        },
    },
    "pkg_200": {
        "name": "الباقة الفاخرة", "icon": "👑", "price": 200,
        "unit": "للمتر المربع",
        "desc": "للفلل والمشاريع الكبيرة",
        "features": {
            "💧 السباكة": [
                "PPR كالدا كامل — نظام مياه مستقل",
                "خلاطات ومغاسل برنس فاخرة",
                "حنفية كولار + غندور",
            ],
            "⚡ الكهرباء": [
                "لوحة قواطع ذكية — VIMAR كوري",
                "طاقة شمسية 4 ألواح + بطارية 200A",
                "تكييف مركزي",
            ],
            "🎨 التشطيبات": [
                "واجهة ألمنيوم فاخرة + كومبوزيت",
                "زجاج مزدوج — ديكور داخلي كامل",
                "سيراميك إيطالي 80×80",
            ],
        },
    },
    "pkg_300": {
        "name": "الباقة السوبر فاخرة", "icon": "💎", "price": 300,
        "unit": "للمتر المربع",
        "desc": "للفلل والمشاريع الكبيرة VIP",
        "features": {
            "💧 السباكة": [
                "PPR كالدا + غندور 10×2",
                "حنفية كولار + نظام مياه ذكي",
            ],
            "⚡ الكهرباء": [
                "8 ألواح طاقة شمسية 400W + بطارية 300A",
                "تدفئة أرضية — لوحة ذكية كاملة",
                "VIMAR كوري + تكييف مركزي",
            ],
            "🎨 التشطيبات": [
                "هندي 120×60 أرضية فاخرة",
                "كومبوزيت + ديكور كامل VIP",
                "واجهة زجاج مزدوج + ألمنيوم",
            ],
        },
    },
}

# ══════════════════════════════════════════════════════════════
# 🛒  المتجر — 28 منتج بـ 6 فئات
# ══════════════════════════════════════════════════════════════
SHOP = {
    "🏺 سيراميك وبلاط": [
        {"id": "s01", "name": "بلاط حسواني 30×30",        "price": "حسب الطلب"},
        {"id": "s02", "name": "سيراميك زنوبيا 50×50",      "price": "حسب الطلب"},
        {"id": "s03", "name": "سيراميك زنوبيا 60×60",      "price": "حسب الطلب"},
        {"id": "s04", "name": "سعودي 60×120",              "price": "حسب الطلب"},
        {"id": "s05", "name": "هندي 120×60 فاخر",          "price": "حسب الطلب"},
        {"id": "s06", "name": "سيراميك إيطالي 80×80",      "price": "حسب الطلب"},
    ],
    "💧 صحيات وسباكة": [
        {"id": "s07", "name": "سخان إيطالي 17 كيلو (البهاء)", "price": "حسب الطلب"},
        {"id": "s08", "name": "خلاطات برنس فاخرة",            "price": "حسب الطلب"},
        {"id": "s09", "name": "PPR السعد 20 بار",             "price": "حسب الطلب"},
        {"id": "s10", "name": "PPR كالدا",                    "price": "حسب الطلب"},
        {"id": "s11", "name": "برميل 3 طبقات حديد",           "price": "حسب الطلب"},
        {"id": "s12", "name": "حنفية كولار",                  "price": "حسب الطلب"},
        {"id": "s13", "name": "مغاسل برنس فاخرة",             "price": "حسب الطلب"},
        {"id": "s14", "name": "دوش + قصبة زاهية",             "price": "حسب الطلب"},
    ],
    "⚡ كهربائيات": [
        {"id": "s15", "name": "أسلاك لينا 6mm",              "price": "حسب الطلب"},
        {"id": "s16", "name": "مفاتيح برايز",                 "price": "حسب الطلب"},
        {"id": "s17", "name": "مفاتيح VIMAR كوري",            "price": "حسب الطلب"},
        {"id": "s18", "name": "ألواح طاقة شمسية 400W",        "price": "حسب الطلب"},
        {"id": "s19", "name": "بطارية 200A",                  "price": "حسب الطلب"},
        {"id": "s20", "name": "بطارية 300A",                  "price": "حسب الطلب"},
        {"id": "s21", "name": "إنارة LED متكاملة",            "price": "حسب الطلب"},
    ],
    "🚪 أبواب وشبابيك": [
        {"id": "s22", "name": "أبواب ألمنيوم مسالكو",         "price": "حسب الطلب"},
        {"id": "s23", "name": "أبواب خشب سويد",               "price": "حسب الطلب"},
        {"id": "s24", "name": "شبابيك ألمنيوم مزدوج",         "price": "حسب الطلب"},
        {"id": "s25", "name": "واجهة كومبوزيت",               "price": "حسب الطلب"},
    ],
    "🎨 تشطيبات وديكور": [
        {"id": "s26", "name": "خشب سويد ملبس قشر سنديان",     "price": "حسب الطلب"},
        {"id": "s27", "name": "جبس بورد + أسقف مستعارة",      "price": "حسب الطلب"},
        {"id": "s28", "name": "دهانات فاخرة",                  "price": "حسب الطلب"},
    ],
}

# ══════════════════════════════════════════════════════════════
# 🏗️  6 أقسام الخدمات
# ══════════════════════════════════════════════════════════════
SECTIONS = [
    {
        "name": "المقاولات العامة", "icon": "🏗️",
        "desc": "تنفيذ المشاريع الإنشائية الكبرى والصغرى بكفاءة عالية من الصفر حتى التسليم",
        "items": ["بناء المباني السكنية والتجارية", "إدارة المشاريع الكاملة", "توريد مواد البناء", "الإشراف الهندسي"],
    },
    {
        "name": "التصميم الهندسي", "icon": "📐",
        "desc": "تصميم معماري وإنشائي احترافي بأحدث البرامج والأساليب العالمية",
        "items": ["التصميم المعماري ثلاثي الأبعاد", "الرسومات الهندسية التنفيذية", "دراسات الجدوى الإنشائية", "استخراج التراخيص"],
    },
    {
        "name": "الكهرباء والميكانيك", "icon": "⚡",
        "desc": "تركيب وصيانة جميع الأنظمة الكهربائية والميكانيكية وفق أعلى معايير السلامة",
        "items": ["تمديدات كهربائية كاملة", "أنظمة التكييف المركزي", "أنظمة الإنذار والحريق", "الطاقة الشمسية"],
    },
    {
        "name": "السباكة والصرف", "icon": "💧",
        "desc": "تمديد شبكات المياه والصرف الصحي بمواد عالية الجودة وضمانات طويلة الأمد",
        "items": ["شبكات المياه الباردة والساخنة", "شبكات الصرف الصحي", "أنظمة معالجة المياه", "صيانة وإصلاح الشبكات"],
    },
    {
        "name": "الديكور والتشطيب", "icon": "🎨",
        "desc": "تشطيبات داخلية وخارجية فاخرة تجمع بين الجماليات والوظيفية",
        "items": ["أعمال الجبس والدهان", "تركيب السيراميك والرخام", "الأسقف المستعارة والجبسية", "الواجهات الزجاجية"],
    },
    {
        "name": "تنسيق الحدائق", "icon": "🌿",
        "desc": "تصميم وتنفيذ الحدائق والمساحات الخضراء بأسلوب فني راقٍ",
        "items": ["تصميم الحدائق الخارجية", "أنظمة الري الأوتوماتيكي", "زراعة الأشجار والنباتات", "الصيانة الدورية"],
    },
]

# ══════════════════════════════════════════════════════════════
# 🧠  FAQ ذكي
# ══════════════════════════════════════════════════════════════
FAQ = [
    {
        "keywords": ["سعر", "كم", "تكلفة", "بكم", "أسعار", "تكلف"],
        "answer": (
            "💰 *أسعارنا تبدأ من 65$ للغرفة*\n\n"
            "• 🏠 الاقتصادية — 65$/غرفة\n"
            "• 💳 التقسيط الثانية — 85$/م²\n"
            "• 💳 التقسيط الأولى — 110$/م²\n"
            "• 🏢 المتوسطة — 120$/م²\n"
            "• ⭐ الممتازة — 180$/م²\n"
            "• 👑 الفاخرة — 200$/م²\n"
            "• 💎 السوبر فاخرة — 300$/م²\n\n"
            "استخدم الحاسبة لمعرفة تكلفة مشروعك تحديداً 🧮"
        ),
    },
    {
        "keywords": ["ضمان", "كفالة", "ضمانة"],
        "answer": (
            "✅ *الضمان*\n\n"
            "• ضمان سنة على السباكة\n"
            "• ضمان سنتين على الكهرباء\n"
            "• ضمان على جودة مواد التشطيب\n"
            "• برميل المسعود كفالة 5 سنوات\n\n"
            "نلتزم بجودة عملنا 💪"
        ),
    },
    {
        "keywords": ["تقسيط", "قسط", "أقساط", "دفع"],
        "answer": (
            "💳 *نظام التقسيط*\n\n"
            "نوفر تقسيطاً مريحاً:\n"
            "• قسط 12 شهر\n"
            "• قسط 24 شهر\n\n"
            "استخدم الحاسبة لمعرفة قيمة القسط الشهري 🧮"
        ),
    },
    {
        "keywords": ["وين", "فين", "عنوان", "موقع", "حمص"],
        "answer": (
            f"📍 *موقعنا*\n\n{ADDRESS}\n\n"
            f"📱 {PHONE}\n"
            f"🌐 [الموقع]({WEBSITE})"
        ),
    },
    {
        "keywords": ["مدة", "وقت", "متى", "ينتهي"],
        "answer": (
            "⏱️ *مدة التنفيذ*\n\n"
            "• شقة صغيرة (80-100م²): 3-4 أسابيع\n"
            "• شقة متوسطة (100-150م²): 4-6 أسابيع\n"
            "• فيلا أو مشروع كبير: حسب الاتفاق\n\n"
            "نلتزم بالمواعيد ✅"
        ),
    },
    {
        "keywords": ["طاقة شمسية", "سولار", "ألواح", "بطارية"],
        "answer": (
            "☀️ *الطاقة الشمسية*\n\n"
            "• 4 ألواح 400W (الباقة الفاخرة)\n"
            "• 8 ألواح 400W + بطارية 300A (السوبر فاخرة)\n"
            "• تركيب وصيانة كاملة\n\n"
            "متوفرة أيضاً في المتجر الاختياري ☀️"
        ),
    },
]

# ══════════════════════════════════════════════════════════════
# 🔄  حالات المحادثة
# ══════════════════════════════════════════════════════════════
CALC_PKG, CALC_AREA, CALC_RATE = range(3)
ORD_NAME, ORD_AREA, ORD_REGION, ORD_TYPE, ORD_NOTES = range(5, 10)

# ══════════════════════════════════════════════════════════════
# 🛠️  دوال مساعدة
# ══════════════════════════════════════════════════════════════
def btn(text, cb): return InlineKeyboardButton(text, callback_data=cb)
def url_btn(text, url): return InlineKeyboardButton(text, url=url)
def home_btn(): return btn("🏠 الرئيسية", "back")

def main_kb():
    return InlineKeyboardMarkup([
        [btn("📦 الباقات والأسعار", "packages")],
        [btn("🧮 حاسبة التكاليف", "calc_start"),
         btn("📋 اطلب عرض سعر", "order_start")],
        [btn("🛒 المتجر الاختياري", "shop_home"),
         btn("🏗️ أقسام الخدمات", "sections")],
        [btn("❓ الأسئلة الشائعة", "faq"),
         btn("ℹ️ من نحن", "about")],
        [btn("📞 تواصل معنا", "contact")],
        [url_btn("🌐 زيارة الموقع", WEBSITE)],
    ])

async def typing(update, ctx):
    try:
        cid = update.message.chat_id if hasattr(update, "message") and update.message else update.effective_chat.id
        await ctx.bot.send_chat_action(chat_id=cid, action=ChatAction.TYPING)
    except: pass

async def notify_admin(ctx, text, kb=None):
    if ADMIN_ID:
        try:
            await ctx.bot.send_message(chat_id=ADMIN_ID, text=text, parse_mode="Markdown", reply_markup=kb)
        except Exception as e:
            logger.warning(f"Admin notify failed: {e}")

WELCOME = """🏗️ *أهلاً بك في الشركة الهندسية التقدمية* 👋

سباكة • كهرباء • تشطيبات

🏆 رائدون في المقاولات منذ *2005*
✅ أكثر من *500 مشروع منجز* في حمص وسوريا
👨‍💼 المدير: الأستاذ عبدالله الشيخ

━━━━━━━━━━━━━━━━━━
كيف يمكنني مساعدتك؟ 👇"""

# ══════════════════════════════════════════════════════════════
# 🏠  /start
# ══════════════════════════════════════════════════════════════
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await typing(update, ctx)
    try:
        await update.message.reply_photo(
            photo="https://raw.githubusercontent.com/AliAhmad-1997/Advance-Engineering-Company/main/construction-site.png",
            caption=WELCOME, parse_mode="Markdown", reply_markup=main_kb()
        )
    except:
        await update.message.reply_text(WELCOME, parse_mode="Markdown", reply_markup=main_kb())

async def contact_support(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await typing(update, ctx)
    kb = InlineKeyboardMarkup([
        [url_btn("💬 واتساب", WHATSAPP)],
        [url_btn("🌐 الموقع", WEBSITE)],
        [home_btn()],
    ])
    await update.message.reply_text(
        f"📞 *تواصل معنا*\n\n📱 {PHONE}\n📧 {EMAIL}\n📍 {ADDRESS}\n\n⏰ الأحد-الخميس: 8ص-6م",
        parse_mode="Markdown", reply_markup=kb
    )

async def language_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌐 *اللغة / Language*\n\nالبوت يعمل باللغة العربية حالياً\n_Arabic only for now_",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[home_btn()]])
    )

# ══════════════════════════════════════════════════════════════
# 📦  الباقات
# ══════════════════════════════════════════════════════════════
async def show_packages(q):
    kb = [
        [btn(f"{p['icon']} {p['name']} — {p['price']}$ ({p['unit']})", f"pkg_{k}")]
        for k, p in PACKAGES.items()
    ]
    kb.append([home_btn()])
    await q.edit_message_caption(
        caption="📦 *الباقات والأسعار*\n\n_اختر باقة لترى تفاصيلها الكاملة_\n\n⚠️ الأسعار شاملة المواد والعمالة",
        parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb)
    )

async def show_pkg_detail(q, key):
    p = PACKAGES.get(key)
    if not p: return
    txt = f"{p['icon']} *{p['name']}*\n_{p['desc']}_\n\n💰 *{p['price']}$ {p['unit']}*\n\n"
    for section, items in p["features"].items():
        txt += f"*{section}:*\n"
        txt += "\n".join(f"  ✓ {i}" for i in items) + "\n\n"
    txt += f"📐 مثال: 100م² = *{p['price']*100:,}$*"
    kb = [
        [btn("🧮 احسب تكلفة مشروعي", f"calc_from_{key}")],
        [btn("📋 اطلب عرض سعر رسمي", f"order_from_{key}")],
        [url_btn("💬 استفسر واتساب", f"{WHATSAPP}?text=أريد الاستفسار عن {p['name']}")],
        [btn("🔙 رجوع للباقات", "packages"), home_btn()],
    ]
    await q.edit_message_caption(caption=txt, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))

# ══════════════════════════════════════════════════════════════
# 🧮  حاسبة التكاليف
# ══════════════════════════════════════════════════════════════
async def calc_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if q.data.startswith("calc_from_"):
        key = q.data.replace("calc_from_", "")
        p = PACKAGES.get(key)
        if p:
            ctx.user_data["calc_pkg"] = key
            await q.edit_message_caption(
                caption=f"🧮 *حاسبة التكاليف*\n\nالباقة: {p['icon']} *{p['name']}* ({p['price']}$ {p['unit']})\n\n📐 أرسل المساحة بالمتر المربع:\n_مثال: 120_",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([[btn("❌ إلغاء", "back")]])
            )
            return CALC_AREA
    kb = [[btn(f"{p['icon']} {p['name']} ({p['price']}$)", f"cpkg_{k}")] for k, p in PACKAGES.items()]
    kb.append([btn("❌ إلغاء", "back")])
    await q.edit_message_caption(
        caption="🧮 *حاسبة التكاليف*\n\nاختر الباقة أولاً:",
        parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb)
    )
    return CALC_PKG

async def calc_choose_pkg(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    key = q.data.replace("cpkg_", "")
    p = PACKAGES.get(key)
    if not p: return CALC_PKG
    ctx.user_data["calc_pkg"] = key
    await q.edit_message_caption(
        caption=f"🧮 *حاسبة التكاليف*\n\nالباقة: {p['icon']} *{p['name']}* ({p['price']}$ {p['unit']})\n\n📐 أرسل المساحة بالمتر المربع:\n_مثال: 120_",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[btn("❌ إلغاء", "back")]])
    )
    return CALC_AREA

async def calc_area(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await typing(update, ctx)
    text = update.message.text.strip().replace(",", "").replace("م²","").replace("م2","")
    try:
        area = float(text)
        if area <= 0 or area > 50000: raise ValueError
    except:
        await update.message.reply_text("⚠️ أرسل رقماً صحيحاً فقط، مثال: *120*", parse_mode="Markdown")
        return CALC_AREA
    ctx.user_data["calc_area"] = area
    kb = InlineKeyboardMarkup([
        [btn("💵 دولار فقط (تخطى)", "skip_rate")],
        [btn("❌ إلغاء", "back")],
    ])
    await update.message.reply_text(
        f"✅ المساحة: *{area:g} م²*\n\n💱 أرسل سعر صرف الدولار بالليرة للحساب بالعملتين\n_مثال: 13000_\n\nأو اضغط *تخطى* للدولار فقط",
        parse_mode="Markdown", reply_markup=kb
    )
    return CALC_RATE

async def calc_rate(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await typing(update, ctx)
    try:
        rate = float(update.message.text.strip().replace(",",""))
        if rate <= 0: raise ValueError
    except:
        await update.message.reply_text("⚠️ أرسل رقماً صحيحاً، مثال: *13000*", parse_mode="Markdown")
        return CALC_RATE
    await _calc_result(update.message, ctx, rate)
    return ConversationHandler.END

async def calc_skip(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await _calc_result(q.message, ctx, None)
    return ConversationHandler.END

async def _calc_result(msg, ctx, rate=None):
    key   = ctx.user_data.get("calc_pkg", "pkg_120")
    area  = ctx.user_data.get("calc_area", 100)
    p     = PACKAGES.get(key, PACKAGES["pkg_120"])
    price = p["price"]
    total = round(area * price)
    m12   = round(total / 12)
    m24   = round(total / 24)

    txt = (
        f"🧮 *نتيجة الحساب*\n\n"
        f"{p['icon']} *{p['name']}*\n"
        f"📐 المساحة: *{area:g} م²*\n"
        f"💰 السعر: *{price}$ {p['unit']}*\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"💵 *الإجمالي: {total:,} $*\n"
        f"📅 قسط 12 شهر: *{m12:,} $*\n"
        f"📅 قسط 24 شهر: *{m24:,} $*\n"
        "━━━━━━━━━━━━━━━━━━"
    )
    if rate:
        txt += (
            f"\n\n🇸🇾 *بالليرة* (1$={rate:,.0f} ل.س)\n"
            "━━━━━━━━━━━━━━━━━━\n"
            f"💴 *{round(total*rate):,} ل.س*\n"
            f"📅 قسط 12: *{round(m12*rate):,} ل.س*\n"
            f"📅 قسط 24: *{round(m24*rate):,} ل.س*\n"
            "━━━━━━━━━━━━━━━━━━"
        )
    txt += "\n_* تقديرية شاملة المواد والعمالة_"

    wa = f"مرحباً، أريد مقايسة\nالباقة: {p['name']}\nالمساحة: {area:g}م²\nالإجمالي: {total:,}$"
    kb = InlineKeyboardMarkup([
        [btn("📋 اطلب عرض سعر رسمي", "order_start")],
        [url_btn("💬 أرسل المقايسة واتساب", f"{WHATSAPP}?text={wa}")],
        [btn("🔄 احسب باقة أخرى", "calc_start"), home_btn()],
    ])
    await msg.reply_text(txt, parse_mode="Markdown", reply_markup=kb)
    await _ask_rating(msg, ctx)

# ══════════════════════════════════════════════════════════════
# 🛒  المتجر
# ══════════════════════════════════════════════════════════════
async def show_shop_home(q):
    cats = list(SHOP.keys())
    kb = [[btn(f"{c} ({len(SHOP[c])} منتج)", f"shop_cat_{i}")] for i, c in enumerate(cats)]
    kb.append([btn("🛒 سلتي", "cart_view"), home_btn()])
    total = sum(len(v) for v in SHOP.values())
    await q.edit_message_caption(
        caption=f"🛒 *المتجر الاختياري*\n\n{total} منتج في {len(cats)} فئات\nاختر الفئة التي تريدها 👇",
        parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb)
    )

async def show_shop_cat(q, cat_idx):
    cats = list(SHOP.keys())
    cat  = cats[cat_idx]
    items = SHOP[cat]
    kb = [[btn(f"➕ {item['name']}", f"cart_add_{item['id']}")] for item in items]
    kb.append([btn("🛒 سلتي", "cart_view"), btn("🔙 رجوع", "shop_home")])
    await q.edit_message_caption(
        caption=f"{cat}\n\nاضغط ➕ لإضافة منتج للسلة:",
        parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb)
    )

async def cart_add(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    item_id = q.data.replace("cart_add_", "")
    cart = ctx.user_data.setdefault("cart", [])
    # إيجاد المنتج
    for items in SHOP.values():
        for item in items:
            if item["id"] == item_id:
                cart.append(item["name"])
                await q.answer(f"✅ تمت إضافة: {item['name']}", show_alert=False)
                return
    await q.answer("❌ لم يتم العثور على المنتج", show_alert=True)

async def show_cart(q, ctx):
    cart = ctx.user_data.get("cart", [])
    if not cart:
        await q.edit_message_caption(
            caption="🛒 *سلتك فارغة*\n\nأضف منتجات من المتجر أولاً",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[btn("🛒 تصفح المتجر", "shop_home"), home_btn()]])
        )
        return
    txt = "🛒 *سلتك*\n\n"
    for i, item in enumerate(cart, 1):
        txt += f"{i}. {item}\n"
    txt += f"\n_إجمالي: {len(cart)} منتج_\n\nللاستفسار عن الأسعار تواصل معنا مباشرة"
    wa_list = "%0a".join(f"{i}. {item}" for i, item in enumerate(cart, 1))
    kb = InlineKeyboardMarkup([
        [url_btn("💬 اطلب عبر واتساب", f"{WHATSAPP}?text=أريد الاستفسار عن:%0a{wa_list}")],
        [btn("🗑️ تفريغ السلة", "cart_clear"), btn("🛒 تصفح أكثر", "shop_home")],
        [home_btn()],
    ])
    await q.edit_message_caption(caption=txt, parse_mode="Markdown", reply_markup=kb)

# ══════════════════════════════════════════════════════════════
# 🏗️  الأقسام
# ══════════════════════════════════════════════════════════════
async def show_sections(q):
    kb = [[btn(f"{s['icon']} {s['name']}", f"sec_{i}")] for i, s in enumerate(SECTIONS)]
    kb.append([home_btn()])
    await q.edit_message_caption(
        caption="🏗️ *أقسام خدماتنا*\n\nنغطي جميع احتياجاتك الإنشائية تحت سقف واحد 👇",
        parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb)
    )

async def show_section_detail(q, idx):
    s = SECTIONS[idx]
    txt = f"{s['icon']} *{s['name']}*\n\n_{s['desc']}_\n\n*ما نقدمه:*\n"
    txt += "\n".join(f"✓ {item}" for item in s["items"])
    kb = InlineKeyboardMarkup([
        [url_btn("📋 اطلب الخدمة واتساب", f"{WHATSAPP}?text=أريد الاستفسار عن خدمة {s['name']}")],
        [btn("🔙 رجوع للأقسام", "sections"), home_btn()],
    ])
    await q.edit_message_caption(caption=txt, parse_mode="Markdown", reply_markup=kb)

# ══════════════════════════════════════════════════════════════
# 📋  نظام الطلبات
# ══════════════════════════════════════════════════════════════
async def order_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if q.data.startswith("order_from_"):
        ctx.user_data["order_pkg"] = q.data.replace("order_from_", "")
    else:
        ctx.user_data.pop("order_pkg", None)
    await q.edit_message_caption(
        caption="📋 *طلب عرض سعر رسمي*\n\nسأحتاج بعض المعلومات لإعداد عرض مخصص 📝\n\n*الخطوة 1/5 — ما اسمك الكريم؟*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[btn("❌ إلغاء", "back")]])
    )
    return ORD_NAME

async def ord_name(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await typing(update, ctx)
    ctx.user_data["ord_name"] = update.message.text.strip()
    await update.message.reply_text(
        f"👋 أهلاً *{ctx.user_data['ord_name']}*!\n\n*الخطوة 2/5 — مساحة المشروع بالمتر المربع؟*\n_مثال: 150_",
        parse_mode="Markdown"
    )
    return ORD_AREA

async def ord_area(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await typing(update, ctx)
    try:
        area = float(update.message.text.strip().replace(",","").replace("م²",""))
        if area <= 0 or area > 50000: raise ValueError
        ctx.user_data["ord_area"] = area
    except:
        await update.message.reply_text("⚠️ أرسل رقماً صحيحاً، مثال: *150*", parse_mode="Markdown")
        return ORD_AREA
    await update.message.reply_text(
        "*الخطوة 3/5 — في أي منطقة المشروع؟*\n_مثال: حمص — الزهراء_",
        parse_mode="Markdown"
    )
    return ORD_REGION

async def ord_region(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await typing(update, ctx)
    ctx.user_data["ord_region"] = update.message.text.strip()
    kb = InlineKeyboardMarkup([
        [btn("🏠 شقة سكنية", "ot_شقة سكنية"), btn("🏢 مكتب تجاري", "ot_مكتب تجاري")],
        [btn("🏗️ فيلا", "ot_فيلا"),           btn("🏭 مشروع تجاري", "ot_مشروع تجاري")],
        [btn("🔧 ترميم", "ot_ترميم"),          btn("📝 أخرى", "ot_أخرى")],
    ])
    await update.message.reply_text("*الخطوة 4/5 — نوع المشروع؟*", parse_mode="Markdown", reply_markup=kb)
    return ORD_TYPE

async def ord_type(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    ctx.user_data["ord_type"] = q.data.replace("ot_", "")
    await q.edit_message_text(
        "*الخطوة 5/5 — أي ملاحظات إضافية؟*\n_مثال: أريد طاقة شمسية، عندي تصميم خاص..._\n\nأو أرسل *تخطى*",
        parse_mode="Markdown"
    )
    return ORD_NOTES

async def ord_notes(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await typing(update, ctx)
    notes = update.message.text.strip()
    if notes.lower() in ["تخطى", "skip", "-", "لا"]: notes = "لا توجد ملاحظات"
    ctx.user_data["ord_notes"] = notes
    await _finalize_order(update.message, ctx)
    return ConversationHandler.END

def generate_invoice_text(d, pkg_info_str=""):
    """يولّد فاتورة نصية احترافية"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    inv_num = f"ITE-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    lines = [
        "━━━━━━━━━━━━━━━━━━━━━━",
        "🏗️ *الشركة الهندسية التقدمية*",
        f"📍 {ADDRESS}",
        f"📱 {PHONE}",
        "━━━━━━━━━━━━━━━━━━━━━━",
        f"📋 *فاتورة طلب عرض سعر*",
        f"🔢 رقم الطلب: `{inv_num}`",
        f"📅 التاريخ: {now}",
        "━━━━━━━━━━━━━━━━━━━━━━",
        f"👤 الاسم: *{d.get('ord_name','-')}*",
        f"📐 المساحة: *{d.get('ord_area','-')} م²*",
        f"📍 المنطقة: *{d.get('ord_region','-')}*",
        f"🏗️ النوع: *{d.get('ord_type','-')}*",
    ]
    if pkg_info_str:
        lines.append(f"📦 {pkg_info_str}")
    
    # حساب تقديري إذا عندنا الباقة والمساحة
    pkg_key = d.get("order_pkg")
    area = d.get("ord_area")
    if pkg_key and area and pkg_key in PACKAGES:
        p = PACKAGES[pkg_key]
        total = round(float(area) * p["price"])
        m12 = round(total / 12)
        m24 = round(total / 24)
        lines += [
            "━━━━━━━━━━━━━━━━━━━━━━",
            f"💰 *التكلفة التقديرية*",
            f"💵 الإجمالي: *{total:,} $*",
            f"📅 قسط 12 شهر: *{m12:,} $*",
            f"📅 قسط 24 شهر: *{m24:,} $*",
        ]
    
    lines += [
        "━━━━━━━━━━━━━━━━━━━━━━",
        f"📝 ملاحظات: {d.get('ord_notes','-')}",
        "━━━━━━━━━━━━━━━━━━━━━━",
        "_* الأسعار تقديرية وتشمل المواد والعمالة_",
        f"_سيتواصل معك فريقنا خلال 24 ساعة_",
    ]
    return "\n".join(lines)

async def _finalize_order(msg, ctx):
    d = ctx.user_data
    pkg_info = ""
    if d.get("order_pkg"):
        p = PACKAGES.get(d["order_pkg"])
        if p: pkg_info = f"\n📦 الباقة: *{p['name']}* ({p['price']}$)"

    # فاتورة للمستخدم
    invoice_text = generate_invoice_text(d, pkg_info.replace("\n📦 الباقة: ","") if pkg_info else "")
    full_invoice = "✅ *تم استلام طلبك بنجاح!*\n\n" + invoice_text
    
    kb = InlineKeyboardMarkup([
        [url_btn("💬 واتساب مباشر", WHATSAPP)],
        [InlineKeyboardButton("🤖 فتح البوت", url=f"https://t.me/{BOT_USERNAME}")],
        [home_btn()],
    ])
    await msg.reply_text(full_invoice, parse_mode="Markdown", reply_markup=kb)

    # إشعار المشرف
    user = msg.from_user
    admin_msg = (
        "🔔 *طلب عرض سعر جديد!*\n\n"
        f"👤 {d.get('ord_name','-')}\n"
        f"📱 @{user.username or 'لا يوجد'} (ID: `{user.id}`)\n"
        f"📐 {d.get('ord_area','-')} م²\n"
        f"📍 {d.get('ord_region','-')}\n"
        f"🏗️ {d.get('ord_type','-')}\n"
        f"📝 {d.get('ord_notes','-')}"
        + pkg_info
    )
    admin_kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("💬 رد عبر تيليغرام", url=f"tg://user?id={user.id}")],
        [url_btn("📱 واتساب", WHATSAPP)],
    ])
    await notify_admin(ctx, admin_msg, admin_kb)

# ══════════════════════════════════════════════════════════════
# ⭐  التقييم
# ══════════════════════════════════════════════════════════════
async def _ask_rating(msg, ctx):
    kb = InlineKeyboardMarkup([[
        btn("⭐", "rate_1"), btn("⭐⭐", "rate_2"), btn("⭐⭐⭐", "rate_3"),
        btn("⭐⭐⭐⭐", "rate_4"), btn("⭐⭐⭐⭐⭐", "rate_5"),
    ]])
    await msg.reply_text("كيف تقيّم تجربتك؟ 😊", reply_markup=kb)

async def handle_rating(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    stars = int(q.data.split("_")[1])
    s = "⭐" * stars
    msgs = {1:"شكراً! سنتحسن 🙏", 2:"شكراً! نسعى للأفضل 💪", 3:"شكراً! 😊", 4:"شكراً! سعداء بخدمتك 🌟", 5:"شكراً! تقييمك يشجعنا 🏆"}
    await q.edit_message_text(f"{s}\n\n{msgs[stars]}\n\n/start للقائمة الرئيسية", parse_mode="Markdown")
    user = q.from_user
    await notify_admin(ctx, f"📊 *تقييم جديد*\n@{user.username or user.first_name}: {s} ({stars}/5)")

# ══════════════════════════════════════════════════════════════
# 🎛️  الـ Callback الرئيسي
# ══════════════════════════════════════════════════════════════
async def handle_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    d = q.data

    if d == "packages":       await show_packages(q)
    elif d.startswith("pkg_"): await show_pkg_detail(q, d.replace("pkg_",""))
    elif d == "shop_home":     await show_shop_home(q)
    elif d.startswith("shop_cat_"): await show_shop_cat(q, int(d.replace("shop_cat_","")))
    elif d.startswith("cart_add_"): await cart_add(update, ctx)
    elif d == "cart_view":     await show_cart(q, ctx)
    elif d == "cart_clear":
        ctx.user_data["cart"] = []
        await q.edit_message_caption(caption="🗑️ تم تفريغ السلة", parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[btn("🛒 تصفح المتجر","shop_home"), home_btn()]]))
    elif d == "sections":      await show_sections(q)
    elif d.startswith("sec_"): await show_section_detail(q, int(d.replace("sec_","")))
    elif d == "faq":
        topics = [("💰 الأسعار","fq_0"),("✅ الضمان","fq_1"),("💳 التقسيط","fq_2"),
                  ("📍 الموقع","fq_3"),("⏱️ المدة","fq_4"),("☀️ الطاقة الشمسية","fq_5")]
        kb = [[btn(t, cb)] for t, cb in topics]
        kb.append([home_btn()])
        await q.edit_message_caption(caption="❓ *الأسئلة الشائعة*\n\nاختر الموضوع:",
            parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))
    elif d.startswith("fq_"):
        idx = int(d.replace("fq_",""))
        if idx < len(FAQ):
            await q.edit_message_caption(caption=FAQ[idx]["answer"], parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([[btn("🔙 رجوع","faq"), home_btn()]]))
    elif d == "about":
        txt = ("ℹ️ *الشركة الهندسية التقدمية*\n\n"
               "🏗️ مقاولات معتمدة منذ *2005*\n"
               f"📍 {ADDRESS}\n\n"
               "✅ +500 مشروع منجز\n✅ +200 عميل راضٍ\n✅ 20 سنة خبرة\n✅ 15 قسم متخصص\n\n"
               "👨‍💼 *المدير:* الأستاذ عبدالله الشيخ\n\n"
               "*خدماتنا:* مقاولات، تصميم، كهرباء، سباكة، ديكور، حدائق")
        await q.edit_message_caption(caption=txt, parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[home_btn()]]))
    elif d == "contact":
        kb = InlineKeyboardMarkup([
            [url_btn("💬 واتساب", WHATSAPP)],
            [url_btn("🌐 الموقع", WEBSITE)],
            [home_btn()],
        ])
        await q.edit_message_caption(
            caption=f"📞 *تواصل معنا*\n\n📱 {PHONE}\n📧 {EMAIL}\n📍 {ADDRESS}\n\n⏰ الأحد-الخميس: 8ص-6م",
            parse_mode="Markdown", reply_markup=kb)
    elif d == "back":
        await q.edit_message_caption(caption=WELCOME, parse_mode="Markdown", reply_markup=main_kb())
    elif d.startswith("rate_"):
        await handle_rating(update, ctx)

# ══════════════════════════════════════════════════════════════
# 💬  الرسائل النصية — FAQ تلقائي
# ══════════════════════════════════════════════════════════════
async def handle_message(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().lower()
    for item in FAQ:
        if any(kw in text for kw in item["keywords"]):
            await typing(update, ctx)
            await update.message.reply_text(item["answer"], parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([[home_btn()]]))
            return
    await typing(update, ctx)
    await update.message.reply_text(
        "لم أفهم رسالتك 😅\n\nاضغط /start للقائمة الرئيسية",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[home_btn()], [url_btn("💬 واتساب", WHATSAPP)]])
    )

# ══════════════════════════════════════════════════════════════
# 🚀  post_init + التشغيل
# ══════════════════════════════════════════════════════════════
async def post_init(app):
    await app.bot.set_my_commands([
        ("start",           "🏠 ابدأ — القائمة الرئيسية"),
        ("contact_support", "📞 تواصل معنا"),
        ("language",        "🌐 اللغة"),
    ])

def main():
    app = Application.builder().token(TOKEN).post_init(post_init).build()

    calc_conv = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(calc_start, pattern="^calc_start$"),
            CallbackQueryHandler(calc_start, pattern="^calc_from_"),
        ],
        states={
            CALC_PKG:  [CallbackQueryHandler(calc_choose_pkg, pattern="^cpkg_")],
            CALC_AREA: [MessageHandler(filters.TEXT & ~filters.COMMAND, calc_area)],
            CALC_RATE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, calc_rate),
                CallbackQueryHandler(calc_skip, pattern="^skip_rate$"),
            ],
        },
        fallbacks=[CallbackQueryHandler(handle_callback, pattern="^back$")],
        allow_reentry=True,
    )

    order_conv = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(order_start, pattern="^order_start$"),
            CallbackQueryHandler(order_start, pattern="^order_from_"),
        ],
        states={
            ORD_NAME:   [MessageHandler(filters.TEXT & ~filters.COMMAND, ord_name)],
            ORD_AREA:   [MessageHandler(filters.TEXT & ~filters.COMMAND, ord_area)],
            ORD_REGION: [MessageHandler(filters.TEXT & ~filters.COMMAND, ord_region)],
            ORD_TYPE:   [CallbackQueryHandler(ord_type, pattern="^ot_")],
            ORD_NOTES:  [MessageHandler(filters.TEXT & ~filters.COMMAND, ord_notes)],
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

    logger.info("✅ البوت v2.0 شغّال — الهندسية التقدمية")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
