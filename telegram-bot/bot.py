import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = "8941840968:AAF3HRPIdXdWP54oZZg7hagh2eUCMj9W2EM"

logging.basicConfig(level=logging.INFO)

# ══════════════════════════════════════════
# بيانات الباقات (نفس الموقع)
# ══════════════════════════════════════════
PACKAGES = {
    "pkg_65": {
        "name": "الباقة الاقتصادية", "icon": "🏠", "price": 65,
        "desc": "مثالية للغرف والشقق الصغيرة",
        "features": [
            "💧 السباكة: PPR السعد، 10 برميل المسعود، سخان إيطالي 17 كيلو",
            "⚡ الكهرباء: أسلاك لينا، مفاتيح برايز، قواطع كاملة",
            "🎨 التشطيبات: بلاط حسواني 30×30، سيراميك زنوبيا 50×50، أبواب ألمنيوم مسالكو"
        ]
    },
    "pkg_120": {
        "name": "الباقة المتوسطة", "icon": "🏢", "price": 120,
        "desc": "للشقق والمنازل المتوسطة — الأكثر طلباً ⭐",
        "features": [
            "💧 السباكة: كل الاقتصادية + PPR ساخن 32mm، خلاطات برنس",
            "⚡ الكهرباء: كل الاقتصادية + إضاءة LED متكاملة، تأريض وحماية",
            "🎨 التشطيبات: كل الاقتصادية + خشب سويد، صيني برنس فاخر"
        ]
    },
    "pkg_200": {
        "name": "الباقة الفاخرة", "icon": "👑", "price": 200,
        "desc": "للفلل والمشاريع الكبيرة",
        "features": [
            "💧 السباكة: PPR كالدا، خلاطات ومغاسل برنس فاخرة، نظام مياه مستقل",
            "⚡ الكهرباء: لوحة قواطع ذكية، طاقة شمسية 4 ألواح + بطارية 200A",
            "🎨 التشطيبات: واجهة ألمنيوم فاخرة، كومبوزيت، زجاج مزدوج، ديكور كامل"
        ]
    },
    "pkg_85": {
        "name": "باقة التقسيط الدرجة الثانية", "icon": "💳", "price": 85,
        "desc": "تقسيط مريح للشقق الصغيرة",
        "features": [
            "💧 PPR السعد 20 بار، 10 برميل المسعود",
            "⚡ أسلاك لينا، مفاتيح برايز",
            "🎨 بلاط حسواني 30×30، أبواب خشب سويد + ألمنيوم مسالكو"
        ]
    },
    "pkg_180": {
        "name": "الباقة الممتازة", "icon": "⭐", "price": 180,
        "desc": "للشقق والمنازل المتوسطة",
        "features": [
            "💧 PPR كالدا، برميل 3 طبقات حديد",
            "⚡ VIMAR كوري، تكييف صالون 2 طن، طاقة شمسية 4 ألواح",
            "🎨 سعودي 60×120 جدران، سويد ملبس قشر سنديان"
        ]
    },
    "pkg_300": {
        "name": "الباقة السوبر فاخرة", "icon": "💎", "price": 300,
        "desc": "للفلل والمشاريع الكبيرة VIP",
        "features": [
            "💧 كالدا، غندور 10×2، حنفية كولار",
            "⚡ 8 ألواح طاقة شمسية + بطارية 300A، تدفئة أرضية",
            "🎨 هندي 120×60 أرضية، كومبوزيت، ديكور كامل فاخر"
        ]
    }
}

SHOP_ITEMS = [
    {"name": "سخان إيطالي 17 كيلو (البهاء)", "icon": "🔥", "price": "حسب الطلب"},
    {"name": "خلاطات برنس فاخرة", "icon": "🚿", "price": "حسب الطلب"},
    {"name": "ألواح طاقة شمسية 400W", "icon": "☀️", "price": "حسب الطلب"},
    {"name": "بطارية 200A", "icon": "🔋", "price": "حسب الطلب"},
    {"name": "مفاتيح VIMAR كوري", "icon": "💡", "price": "حسب الطلب"},
    {"name": "سيراميك زنوبيا 60×60", "icon": "🏠", "price": "حسب الطلب"},
    {"name": "أسلاك لينا 6mm", "icon": "⚡", "price": "حسب الطلب"},
    {"name": "PPR السعد 20 بار", "icon": "💧", "price": "حسب الطلب"},
]

WHATSAPP = "https://wa.me/00963986555105"
WEBSITE  = "https://aliahmad-1997.github.io/Advance-Engineering-Company/"

# ══════════════════════════════════════════
# القائمة الرئيسية
# ══════════════════════════════════════════
def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📦 الباقات والأسعار", callback_data="packages")],
        [InlineKeyboardButton("🧮 احسب تكلفة مشروعك", callback_data="calc")],
        [InlineKeyboardButton("🛒 المتجر الاختياري", callback_data="shop")],
        [InlineKeyboardButton("ℹ️ من نحن", callback_data="about")],
        [InlineKeyboardButton("📞 تواصل معنا", callback_data="contact")],
        [InlineKeyboardButton("🌐 زيارة الموقع", url=WEBSITE)],
    ])

WELCOME = """🏗️ *أهلاً بك في الشركة الهندسية التقدمية*

سباكة • كهرباء • تشطيبات

نحن رائدون في مجال المقاولات والإنشاءات منذ 2005 🏆
أكثر من *500 مشروع منجز* وأكثر من *200 عميل راضٍ*

اختر ما تريد من القائمة أدناه 👇"""

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME, parse_mode="Markdown", reply_markup=main_menu_keyboard())

async def handle_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data

    # ── الباقات ──
    if data == "packages":
        kb = [[InlineKeyboardButton(f"{p['icon']} {p['name']} — {p['price']}$/م²", callback_data=f"pkg_{k.split('_')[1]}")]
              for k, p in PACKAGES.items()]
        kb.append([InlineKeyboardButton("🔙 رجوع", callback_data="back")])
        await q.edit_message_text("📦 *اختر الباقة لتعرف تفاصيلها:*", parse_mode="Markdown",
                                   reply_markup=InlineKeyboardMarkup(kb))

    # ── تفاصيل باقة ──
    elif data.startswith("pkg_"):
        key = "pkg_" + data.split("_")[1]
        p   = PACKAGES.get(key)
        if p:
            txt = f"{p['icon']} *{p['name']}*\n_{p['desc']}_\n\n💰 *السعر: {p['price']}$ للمتر المربع*\n\n"
            txt += "\n".join(f"• {f}" for f in p["features"])
            txt += f"\n\n📐 *مثال:* شقة 100م² = *{p['price']*100:,}$*"
            kb = [
                [InlineKeyboardButton("🧮 احسب مشروعي بهذه الباقة", callback_data=f"calc_{key}")],
                [InlineKeyboardButton("💬 اطلب عبر واتساب", url=f"{WHATSAPP}?text=مرحباً، أريد الاستفسار عن {p['name']} {p['price']}$/م²")],
                [InlineKeyboardButton("🔙 رجوع للباقات", callback_data="packages")],
            ]
            await q.edit_message_text(txt, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))

    # ── الحاسبة ──
    elif data == "calc" or data.startswith("calc_"):
        pkg_key = data.split("_", 1)[1] if "_" in data and data != "calc" else None
        if pkg_key and pkg_key in PACKAGES:
            ctx.user_data["calc_pkg"] = pkg_key
            p = PACKAGES[pkg_key]
            await q.edit_message_text(
                f"🧮 *حاسبة التكاليف*\n\nالباقة المختارة: {p['icon']} *{p['name']}* ({p['price']}$/م²)\n\n📐 أرسل لي *المساحة بالمتر المربع* وأنا أحسبلك التكلفة:",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="packages")]]))
            ctx.user_data["waiting_area"] = True
        else:
            kb = [[InlineKeyboardButton(f"{p['icon']} {p['name']}", callback_data=f"calc_pkg_{k}")]
                  for k, p in PACKAGES.items()]
            kb.append([InlineKeyboardButton("🔙 رجوع", callback_data="back")])
            await q.edit_message_text("🧮 *اختر الباقة أولاً:*", parse_mode="Markdown",
                                       reply_markup=InlineKeyboardMarkup(kb))

    elif data.startswith("calc_pkg_"):
        key = data.replace("calc_pkg_", "pkg_")
        p   = PACKAGES.get(key)
        if p:
            ctx.user_data["calc_pkg"]    = key
            ctx.user_data["waiting_area"] = True
            await q.edit_message_text(
                f"🧮 *حاسبة التكاليف*\n\nالباقة: {p['icon']} *{p['name']}* ({p['price']}$/م²)\n\n📐 أرسل لي *المساحة بالمتر المربع:*",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="packages")]]))

    # ── المتجر ──
    elif data == "shop":
        txt = "🛒 *المتجر الاختياري*\n_مواد وتجهيزات بأفضل الأسعار_\n\n"
        for item in SHOP_ITEMS:
            txt += f"{item['icon']} {item['name']}\n"
        txt += f"\n💬 للاستفسار عن الأسعار تواصل معنا مباشرة"
        kb = [
            [InlineKeyboardButton("💬 استفسر عبر واتساب", url=f"{WHATSAPP}?text=مرحباً، أريد الاستفسار عن المتجر الاختياري")],
            [InlineKeyboardButton("🔙 رجوع", callback_data="back")],
        ]
        await q.edit_message_text(txt, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))

    # ── من نحن ──
    elif data == "about":
        txt = """ℹ️ *الشركة الهندسية التقدمية*

🏗️ شركة مقاولات معتمدة منذ *2005*
📍 حمص — سوريا

✅ أكثر من *500 مشروع منجز*
✅ أكثر من *200 عميل راضٍ*
✅ *20 سنة* خبرة في المجال
✅ *15 قسم* متخصص

*خدماتنا:*
• المقاولات العامة
• التصميم الهندسي
• الكهرباء والميكانيك
• السباكة والصرف
• الديكور والتشطيب
• تنسيق الحدائق"""
        kb = [[InlineKeyboardButton("🔙 رجوع", callback_data="back")]]
        await q.edit_message_text(txt, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))

    # ── تواصل ──
    elif data == "contact":
        txt = """📞 *تواصل معنا*

📱 واتساب: *0986555105*
🌐 الموقع الإلكتروني: [اضغط هنا]({})

⏰ نرد على جميع الاستفسارات خلال ساعات العمل""".format(WEBSITE)
        kb = [
            [InlineKeyboardButton("💬 واتساب", url=WHATSAPP)],
            [InlineKeyboardButton("🌐 الموقع", url=WEBSITE)],
            [InlineKeyboardButton("🔙 رجوع", callback_data="back")],
        ]
        await q.edit_message_text(txt, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))

    # ── تخطى سعر الصرف ──
    elif data == "skip_rate":
        ctx.user_data["waiting_rate"] = False
        await send_calc_result(q, ctx, rate=None)

    # ── رجوع ──
    elif data == "back":
        await q.edit_message_text(WELCOME, parse_mode="Markdown", reply_markup=main_menu_keyboard())

# ── استقبال المساحة وسعر الصرف للحاسبة ──
async def handle_message(update: Update, ctx: ContextTypes.DEFAULT_TYPE):

    # الخطوة 1: استقبال المساحة
    if ctx.user_data.get("waiting_area"):
        try:
            area = float(update.message.text.strip().replace(",", "").replace("م²","").replace("م2",""))
            if area <= 0 or area > 50000:
                raise ValueError
            ctx.user_data["calc_area"]    = area
            ctx.user_data["waiting_area"] = False
            ctx.user_data["waiting_rate"] = True

            pkg_key = ctx.user_data.get("calc_pkg", "pkg_120")
            p       = PACKAGES.get(pkg_key, PACKAGES["pkg_120"])

            kb = [
                [InlineKeyboardButton("⏭️ بالدولار فقط (تخطى)", callback_data="skip_rate")],
                [InlineKeyboardButton("🔙 رجوع", callback_data="calc")],
            ]
            await update.message.reply_text(
                f"✅ المساحة: *{area:g} م²*\n\n💱 أرسل *سعر صرف الدولار* بالليرة السورية للحساب بالعملتين\n_مثال: 13000_\n\nأو اضغط *تخطى* للحساب بالدولار فقط",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(kb)
            )
        except ValueError:
            await update.message.reply_text("⚠️ أرسل رقماً صحيحاً فقط، مثال: *120*", parse_mode="Markdown")

    # الخطوة 2: استقبال سعر الصرف
    elif ctx.user_data.get("waiting_rate"):
        try:
            rate = float(update.message.text.strip().replace(",", ""))
            if rate <= 0:
                raise ValueError
            ctx.user_data["waiting_rate"] = False
            await send_calc_result(update, ctx, rate=rate)
        except ValueError:
            await update.message.reply_text("⚠️ أرسل رقماً صحيحاً، مثال: *13000*", parse_mode="Markdown")

    else:
        await update.message.reply_text(WELCOME, parse_mode="Markdown", reply_markup=main_menu_keyboard())


async def send_calc_result(update_or_query, ctx, rate=None):
    """يرسل نتيجة الحساب — يُستدعى من handle_message أو skip_rate callback"""
    pkg_key = ctx.user_data.get("calc_pkg", "pkg_120")
    area    = ctx.user_data.get("calc_area", 100)
    p       = PACKAGES.get(pkg_key, PACKAGES["pkg_120"])
    price   = p["price"]
    total   = round(area * price)
    m12     = round(total / 12)
    m24     = round(total / 24)

    # بناء النص
    txt = f"""🧮 *نتيجة الحساب*

{p['icon']} *{p['name']}*
📐 المساحة: *{area:g} م²*
💰 سعر المتر: *{price} $*

━━━━━━━━━━━━━━━━━━
💵 *الإجمالي: {total:,} $*
📅 قسط 12 شهر: *{m12:,} $*
📅 قسط 24 شهر: *{m24:,} $*
━━━━━━━━━━━━━━━━━━"""

    if rate:
        total_syp = round(total * rate)
        m12_syp   = round(m12   * rate)
        m24_syp   = round(m24   * rate)
        txt += f"""
🇸🇾 *بالليرة السورية* (1$={rate:,.0f} ل.س)
━━━━━━━━━━━━━━━━━━
💴 *الإجمالي: {total_syp:,} ل.س*
📅 قسط 12 شهر: *{m12_syp:,} ل.س*
📅 قسط 24 شهر: *{m24_syp:,} ل.س*
━━━━━━━━━━━━━━━━━━"""

    txt += "\n_* الأسعار تقديرية وتشمل المواد والعمالة_"

    wa_text = f"مرحباً، أريد مقايسة لـ {p['name']}%0aالمساحة: {area:g} م²%0aالإجمالي: {total:,}$"
    if rate:
        wa_text += f"%0aبالليرة: {total_syp:,} ل.س"

    kb = [
        [InlineKeyboardButton("💬 أرسل المقايسة عبر واتساب", url=f"{WHATSAPP}?text={wa_text}")],
        [InlineKeyboardButton("🔄 احسب باقة أخرى", callback_data="calc")],
        [InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="back")],
    ]

    if hasattr(update_or_query, 'message'):
        await update_or_query.message.reply_text(txt, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))
    else:
        await update_or_query.edit_message_text(txt, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))

# ══════════════════════════════════════════
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ البوت شغّال!")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
