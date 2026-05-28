/* ═══════════════════════════════════════════
   بيانات الباقات الكاملة — الهندسية التقدمية
   7 باقات مع نظام تبديل البنود والتسعير
═══════════════════════════════════════════ */

const PACKAGES_DATA = {

  // ─── باقة التقسيط الأولى ───────────────────
  pkg_110: {
    id: 'pkg_110',
    name: 'باقة التقسيط الدرجة الأولى',
    icon: '💳',
    price: 110,
    badge: '',
    desc: 'مثالية للميزانيات المحدودة مع جودة مضمونة',
    sections: [
      {
        title: 'الصحية', icon: '💧',
        items: [
          { key: 'miah_malha',   label: 'مياه مالحة (سواد)',  value: 'إنش 4 — سماكة 3.2 / إنش 3 — سماكة 3.6 / إنش 2', price: 0,
            alts: [
              { label: 'إنش 4 سماكة 3.2 (اقتصادي)', price: 0 },
              { label: 'إنش 4 سماكة 4 (ممتاز)', price: 5 },
            ]
          },
          { key: 'miah_helwa',  label: 'مياه حلوة (سواد)',   value: '20 بار PPR بارد 25mm — ساخن 32mm (السعد)', price: 0,
            alts: [
              { label: 'PPR السعد 20 بار (قياسي)', price: 0 },
              { label: 'PPR السعد 25 بار (ممتاز)', price: 8 },
            ]
          },
          { key: 'khazzan',     label: 'خزان',               value: '10 برميل أزرق بلاستيك كفالة 5 سنوات (المسعود)', price: 0,
            alts: [
              { label: '10 برميل أزرق (المسعود)', price: 0 },
              { label: '10 برميل ستانليس', price: 25 },
            ]
          },
          { key: 'hanafiyat',   label: 'حنفيات (سواد)',       value: 'نحاس صيني (زاهية)', price: 0,
            alts: [
              { label: 'نحاس صيني زاهية', price: 0 },
              { label: 'نحاس إيطالي برنس', price: 12 },
            ]
          },
          { key: 'khallatat',   label: 'خلاطات (سواد)',       value: 'صيني (برنس)', price: 0,
            alts: [
              { label: 'صيني برنس', price: 0 },
              { label: 'تركي ريمكس', price: 10 },
            ]
          },
          { key: 'deenamo',     label: 'دينمو (بياض)',        value: 'كانديلا', price: 0,
            alts: [
              { label: 'كانديلا', price: 0 },
              { label: 'إيطالي أسطوانة', price: 15 },
            ]
          },
          { key: 'doush',       label: 'دوش (بياض)',          value: 'كرت كامل بلور', price: 0,
            alts: [
              { label: 'كرت كامل بلور', price: 0 },
              { label: 'كرت شطاف نوع 1', price: 5 },
            ]
          },
          { key: 'maghasil',    label: 'مغاسل (بياض)',        value: 'مغسلة نصف عامود أو معلق', price: 0,
            alts: [
              { label: 'نصف عامود معلق', price: 0 },
              { label: 'بورسلان فاخر برنس', price: 18 },
            ]
          },
          { key: 'jakdoush',    label: 'جاكدوش',              value: 'عادي + غرفة بلور', price: 0,
            alts: [
              { label: 'عادي + غرفة بلور', price: 0 },
              { label: 'تركي ريمكس 3 مآخذ', price: 12 },
            ]
          },
          { key: 'teb',         label: 'تيب (سواد)',          value: '23 ضغط عالي — 16 للجدران', price: 0,
            alts: [
              { label: '23 ضغط عالي / 16 جدران', price: 0 },
              { label: 'ماجيك 23 ضغط عالي', price: 6 },
            ]
          },
          { key: 'olab',        label: 'علب (سواد)',          value: 'ماجيك', price: 0, alts: [] },
        ]
      },
      {
        title: 'الكهرباء', icon: '⚡',
        items: [
          { key: 'aslak',       label: 'أسلاك',               value: '3mm مفرد برايز — 1.5mm مفتاح — 1mm مزدوج ليد — 6mm الرئيسي (لينا)', price: 0,
            alts: [
              { label: 'لينا (قياسي)', price: 0 },
              { label: 'نيو باور (ممتاز)', price: 10 },
            ]
          },
          { key: 'accessories', label: 'اكسسوارات',           value: 'لينا', price: 0, alts: [] },
          { key: 'qawate3',     label: 'قواطع',               value: '16 مفرد لكل غرفة — 32 مزدوج رئيسي — 20 قازان', price: 0,
            alts: [
              { label: 'قياسي 16+32+20', price: 0 },
              { label: 'كوري حماية كاملة', price: 20 },
            ]
          },
          { key: 'enareh',      label: 'إنارة + ليد',         value: 'نيولات — لمبات', price: 0,
            alts: [
              { label: 'نيولات + لمبات', price: 0 },
              { label: 'سبوتات + إضاءة خفية', price: 15 },
            ]
          },
        ]
      },
      {
        title: 'رخام شبابيك', icon: '🪟',
        items: [
          { key: 'rkhm_shbabik', label: 'رخام شبابيك', value: 'مصيافي سماكة 3cm لكل الشبابيك', price: 0,
            alts: [
              { label: 'مصيافي 3cm', price: 0 },
              { label: 'تركي غامق/فاتح', price: 10 },
            ]
          },
        ]
      },
      {
        title: 'رخام أبواب', icon: '🚪',
        items: [
          { key: 'rkhm_abwab', label: 'رخام أبواب', value: 'مصيافي للحمام والتواليت', price: 0,
            alts: [
              { label: 'مصيافي', price: 0 },
              { label: 'تركي غامق/فاتح', price: 8 },
            ]
          },
        ]
      },
      {
        title: 'تلييس', icon: '🏗️',
        items: [
          { key: 'tlees', label: 'تلييس', value: '3 أوجه (قدة)', price: 0,
            alts: [
              { label: '3 أوجه قدة', price: 0 },
              { label: '3 أوجه ودع كامل', price: 12 },
            ]
          },
        ]
      },
      {
        title: 'سيراميك', icon: '🟦',
        items: [
          { key: 'ceramic_jdran', label: 'جدران',   value: 'حمام ومطبخ زنوبيا 4 (30×60)', price: 0,
            alts: [
              { label: 'زنوبيا 4 (30×60)', price: 0 },
              { label: 'سعودي (60×120)', price: 20 },
            ]
          },
          { key: 'ceramic_n3leh', label: 'نعلة',    value: 'زنوبيا', price: 0,
            alts: [
              { label: 'زنوبيا', price: 0 },
              { label: '8cm من غرانيت الأرضيات', price: 8 },
            ]
          },
          { key: 'ceramic_ard',   label: 'أرضية',   value: 'بلاط حسواني (30×30) / سيراميك زنوبيا 3 (50×50)', price: 0,
            alts: [
              { label: 'بلاط حسواني 30×30', price: 0 },
              { label: 'سيراميك زنوبيا 3 (50×50)', price: 5 },
              { label: 'هندي (60×60)', price: 15 },
              { label: 'سعودي (60×60)', price: 20 },
            ]
          },
        ]
      },
      {
        title: 'المجلى', icon: '🍽️',
        items: [
          { key: 'mujla', label: 'المجلى', value: 'غرانيت تركي 3cm — جرن حجر 60cm', price: 0,
            alts: [
              { label: 'غرانيت تركي 3cm + جرن حجر 60cm', price: 0 },
              { label: 'جالكسي 3cm + جرن حجر 7cm + ستانليس ستيل', price: 20 },
            ]
          },
        ]
      },
      {
        title: 'أبواب', icon: '🚪',
        items: [
          { key: 'bab_dakhli',  label: 'داخلي',       value: 'فرنسي سويد مع بلور (عادي أو محجر)', price: 0,
            alts: [
              { label: 'فرنسي سويد + بلور', price: 0 },
              { label: 'سنديان ملبس قشر', price: 15 },
            ]
          },
          { key: 'bab_kharji',  label: 'خارجي',       value: 'خشب سويد سد كامل', price: 0,
            alts: [
              { label: 'خشب سويد سد كامل', price: 0 },
              { label: 'سنديان ملبس قشر', price: 20 },
            ]
          },
          { key: 'bab_hmam',    label: 'حمام+تواليت', value: 'ألمنيوم مسالكو فضي', price: 0,
            alts: [
              { label: 'ألمنيوم مسالكو فضي', price: 0 },
              { label: 'ألمنيوم مدار أسود/خشبي', price: 10 },
            ]
          },
        ]
      },
      {
        title: 'نوافذ', icon: '🪟',
        items: [
          { key: 'nawafidh', label: 'نوافذ', value: 'ألمنيوم مسالكو فضي', price: 0,
            alts: [
              { label: 'ألمنيوم مسالكو فضي', price: 0 },
              { label: 'ألمنيوم مدار أسود/خشبي — أبجور كهربا حركة', price: 15 },
            ]
          },
        ]
      },
      {
        title: 'دهان', icon: '🎨',
        items: [
          { key: 'dahan', label: 'دهان', value: '3 أوجه / طرش', price: 0,
            alts: [
              { label: '3 أوجه طرش', price: 0 },
              { label: '3 معجونة أكرليك', price: 10 },
            ]
          },
        ]
      },
    ]
  },

  // ─── باقة التقسيط الثانية ──────────────────
  pkg_85: {
    id: 'pkg_85',
    name: 'باقة التقسيط الدرجة الثانية',
    icon: '🏠',
    price: 85,
    badge: '',
    desc: 'للشقق الاقتصادية بمواصفات جيدة',
    sections: [
      {
        title: 'الصحية', icon: '💧',
        items: [
          { key: 'miah_malha',  label: 'مياه مالحة (سواد)', value: '4 إنش سماكة 3.2 — 3 إنش سماكة 3.6 — 2 إنش (ماركة السعد)', price: 0, alts: [
            { label: 'ماركة السعد (قياسي)', price: 0 },
            { label: 'ماركة كالدا (ممتاز)', price: 8 },
          ]},
          { key: 'miah_helwa',  label: 'مياه حلوة (سواد)', value: '20 بار PPR بارد 25mm — ساخن 32mm (ماركة السعد)', price: 0, alts: [
            { label: 'السعد 20 بار', price: 0 },
            { label: 'السعد 25 بار', price: 6 },
          ]},
          { key: 'khazzan',     label: 'خزان',              value: '10 برميل أبيض — أزرق بلاستيك (كفالة 5 سنوات — المسعود)', price: 0, alts: [
            { label: 'برميل بلاستيك المسعود', price: 0 },
            { label: 'ستانليس ستيل', price: 20 },
          ]},
          { key: 'hanafiyat',   label: 'حنفيات (سواد)',     value: 'نحاس صيني (زاهية)', price: 0, alts: [
            { label: 'زاهية', price: 0 }, { label: 'برنس', price: 10 },
          ]},
          { key: 'khallatat',   label: 'خلاطات (سواد)',     value: 'صيني (برنس)', price: 0, alts: [
            { label: 'برنس', price: 0 }, { label: 'تركي ريمكس', price: 8 },
          ]},
          { key: 'deenamo',     label: 'دينمو (بياض)',      value: '17 كيلو (البهاء) سخان إيطالي', price: 0, alts: [
            { label: 'البهاء 17 كيلو', price: 0 },
            { label: 'أسطوانة مازوت أو كهرباء', price: 20 },
          ]},
          { key: 'doush',       label: 'دوش (بياض)',        value: 'قصبة (زاهية)', price: 0, alts: [
            { label: 'قصبة زاهية', price: 0 }, { label: 'كرت كامل بلور', price: 5 },
          ]},
          { key: 'maghasil',    label: 'مغاسل (بياض)',      value: 'زاهية', price: 0, alts: [
            { label: 'زاهية', price: 0 }, { label: 'برنس فاخر', price: 12 },
          ]},
          { key: 'teb',         label: 'تيب (سواد)',        value: '23 ضغط عالي — 16 للجدران', price: 0, alts: [
            { label: '23/16 قياسي', price: 0 }, { label: 'ماجيك 23', price: 5 },
          ]},
          { key: 'olab',        label: 'علب (سواد)',        value: 'ماجيك', price: 0, alts: [] },
        ]
      },
      {
        title: 'الكهرباء', icon: '⚡',
        items: [
          { key: 'aslak',       label: 'أسلاك',             value: '3mm مفرد برايز — 1.5mm مفتاح — 1mm مزدوج ليد — 6mm الرئيسي (لينا)', price: 0, alts: [
            { label: 'لينا', price: 0 }, { label: 'نيو باور', price: 10 },
          ]},
          { key: 'accessories', label: 'اكسسوارات',         value: 'لينا', price: 0, alts: [] },
          { key: 'qawate3',     label: 'قواطع',             value: '16 مفرد لكل غرفة — 32 مزدوج رئيسي — 20 قازان', price: 0, alts: [
            { label: 'قياسي', price: 0 }, { label: 'كوري', price: 18 },
          ]},
          { key: 'enareh',      label: 'إنارة + ليد',       value: 'نيولات — لمبات', price: 0, alts: [
            { label: 'نيولات + لمبات', price: 0 }, { label: 'سبوتات مخفية', price: 12 },
          ]},
        ]
      },
      {
        title: 'رخام شبابيك', icon: '🪟',
        items: [{ key: 'rkhm_shbabik', label: 'رخام شبابيك', value: 'مصيافي سماكة 3cm لكل الشبابيك', price: 0, alts: [
          { label: 'مصيافي 3cm', price: 0 }, { label: 'تركي', price: 8 },
        ]}]
      },
      {
        title: 'رخام أبواب', icon: '🚪',
        items: [{ key: 'rkhm_abwab', label: 'رخام أبواب', value: 'مصيافي للحمام والتواليت', price: 0, alts: [
          { label: 'مصيافي', price: 0 }, { label: 'تركي', price: 6 },
        ]}]
      },
      {
        title: 'تلييس', icon: '🏗️',
        items: [{ key: 'tlees', label: 'تلييس', value: '3 أوجه (قدة)', price: 0, alts: [
          { label: '3 أوجه قدة', price: 0 }, { label: '3 أوجه ودع كامل', price: 10 },
        ]}]
      },
      {
        title: 'سيراميك', icon: '🟦',
        items: [
          { key: 'ceramic_jdran', label: 'جدران', value: 'حمام ومطبخ زنوبيا 4 (30×60)', price: 0, alts: [
            { label: 'زنوبيا 4 (30×60)', price: 0 }, { label: 'سعودي (60×120)', price: 18 },
          ]},
          { key: 'ceramic_n3leh', label: 'نعلة',  value: 'زنوبيا', price: 0, alts: [
            { label: 'زنوبيا', price: 0 }, { label: '8cm غرانيت', price: 6 },
          ]},
          { key: 'ceramic_ard',   label: 'أرضية', value: 'بلاط حسواني (30×30) / سيراميك زنوبيا 3 (50×50)', price: 0, alts: [
            { label: 'بلاط حسواني 30×30', price: 0 },
            { label: 'زنوبيا 3 (50×50)', price: 5 },
            { label: 'هندي (60×60)', price: 12 },
          ]},
        ]
      },
      {
        title: 'المجلى', icon: '🍽️',
        items: [{ key: 'mujla', label: 'المجلى', value: 'غرانيت تركي 3cm — جرن حجر 60cm', price: 0, alts: [
          { label: 'غرانيت تركي 3cm', price: 0 }, { label: 'جالكسي ستانليس', price: 15 },
        ]}]
      },
      {
        title: 'أبواب', icon: '🚪',
        items: [
          { key: 'bab_dakhli', label: 'داخلي',       value: 'فرنسي سويد مع بلور', price: 0, alts: [
            { label: 'فرنسي سويد', price: 0 }, { label: 'سنديان ملبس قشر', price: 15 },
          ]},
          { key: 'bab_kharji', label: 'خارجي',       value: 'خشب سويد سد كامل', price: 0, alts: [
            { label: 'خشب سويد', price: 0 }, { label: 'سنديان', price: 18 },
          ]},
          { key: 'bab_hmam',   label: 'حمام+تواليت', value: 'ألمنيوم مسالكو فضي', price: 0, alts: [
            { label: 'مسالكو فضي', price: 0 }, { label: 'مدار أسود/خشبي', price: 8 },
          ]},
        ]
      },
      {
        title: 'نوافذ', icon: '🪟',
        items: [{ key: 'nawafidh', label: 'نوافذ', value: 'ألمنيوم مسالكو فضي', price: 0, alts: [
          { label: 'مسالكو فضي', price: 0 }, { label: 'مدار أسود + أبجور كهربا', price: 12 },
        ]}]
      },
      {
        title: 'دهان', icon: '🎨',
        items: [{ key: 'dahan', label: 'دهان', value: '3 أوجه / طرش', price: 0, alts: [
          { label: '3 أوجه طرش', price: 0 }, { label: '3 معجونة أكرليك', price: 8 },
        ]}]
      },
    ]
  },

  // ─── الباقة الممتازة ───────────────────────
  pkg_180: {
    id: 'pkg_180',
    name: 'الباقة الممتازة',
    icon: '⭐',
    price: 180,
    badge: 'الأكثر طلباً',
    desc: 'للشقق والمنازل المتوسطة بمواصفات ممتازة',
    sections: [
      {
        title: 'الصحية', icon: '💧',
        items: [
          { key: 'miah_malha',  label: 'مياه مالحة (سواد)', value: '4 إنش سماكة 3.7 — 3 إنش سماكة 3.6 — 2 إنش (السعد)', price: 0, alts: [
            { label: 'السعد', price: 0 }, { label: 'كالدا', price: 10 },
          ]},
          { key: 'miah_helwa',  label: 'مياه حلوة (سواد)', value: '20 بار PPR بارد 25mm — ساخن 32mm (السعد)', price: 0, alts: [
            { label: 'السعد', price: 0 }, { label: 'كالدا', price: 8 },
          ]},
          { key: 'khazzan',     label: 'خزان',              value: '10 برميل أحمر بلاستيك 3 طبقات حديد (السعد)', price: 0, alts: [
            { label: 'برميل 3 طبقات السعد', price: 0 }, { label: 'غندور 10×2', price: 12 },
          ]},
          { key: 'hanafiyat',   label: 'حنفيات (سواد)',     value: 'نحاس صيني (زاهية)', price: 0, alts: [
            { label: 'زاهية', price: 0 }, { label: 'تركي ريمكس', price: 12 },
          ]},
          { key: 'khallatat',   label: 'خلاطات (سواد)',     value: 'تركي ريمكس', price: 0, alts: [
            { label: 'تركي ريمكس', price: 0 }, { label: 'إيطالي فاخر', price: 20 },
          ]},
          { key: 'deenamo',     label: 'دينمو (بياض)',      value: 'أسطوانة/طاقة شمسية', price: 0, alts: [
            { label: 'أسطوانة/طاقة شمسية', price: 0 }, { label: 'كانديلا 4 ألواح 200A', price: 35 },
          ]},
          { key: 'doush',       label: 'دوش (بياض)',        value: 'كرت كامل (زاهية)', price: 0, alts: [
            { label: 'كرت كامل زاهية', price: 0 }, { label: 'كرت شطاف ستانليس', price: 8 },
          ]},
          { key: 'maghasil',    label: 'مغاسل (بياض)',      value: 'مغسلة نصف عامود أو معلق', price: 0, alts: [
            { label: 'نصف عامود معلق', price: 0 }, { label: 'بورسلان فاخر', price: 15 },
          ]},
          { key: 'jakdoush',    label: 'جاكدوش',            value: 'عادي + غرفة بلور', price: 0, alts: [
            { label: 'عادي + غرفة بلور', price: 0 }, { label: 'تركي ريمكس 3 مآخذ', price: 15 },
          ]},
          { key: 'teb',         label: 'تيب (سواد)',        value: '23 ضغط عالي — 16 للجدران', price: 0, alts: [
            { label: '23/16 قياسي', price: 0 }, { label: 'ماجيك 23', price: 6 },
          ]},
          { key: 'olab',        label: 'علب (سواد)',        value: 'ماجيك', price: 0, alts: [] },
        ]
      },
      {
        title: 'الكهرباء', icon: '⚡',
        items: [
          { key: 'aslak',       label: 'أسلاك',             value: '3mm مفرد برايز — 1.5mm مفتاح — 1mm مزدوج ليد — 6mm الرئيسي (نيو باور)', price: 0, alts: [
            { label: 'نيو باور', price: 0 }, { label: 'فيمار VIMAR', price: 15 },
          ]},
          { key: 'accessories', label: 'اكسسوارات',         value: 'VIMAR', price: 0, alts: [
            { label: 'VIMAR', price: 0 }, { label: 'كومو', price: -5 },
          ]},
          { key: 'qawate3',     label: 'قواطع',             value: '16 مفرد لكل غرفة — 32 مزدوج رئيسي — 20 قازان — 16 لكل مكيف (كوري)', price: 0, alts: [
            { label: 'كوري', price: 0 }, { label: 'دارات حماية فاخرة', price: 20 },
          ]},
          { key: 'enareh',      label: 'إنارة + ليد',       value: 'سبوتات — إضاءة حبال مخفية — سترب لايت', price: 0, alts: [
            { label: 'سبوتات + حبال مخفية + سترب', price: 0 }, { label: 'نيولات بسيطة', price: -10 },
          ]},
          { key: 'solar',       label: 'طاقة شمسية',        value: '4 ألواح — بطارية 200A ليثيوم — انفتر 4.2', price: 0, alts: [
            { label: '4 ألواح + بطارية 200A', price: 0 }, { label: '8 ألواح + 300A + انفتر 6200 (سوبر)', price: 60 },
          ]},
        ]
      },
      {
        title: 'تكييف', icon: '❄️',
        items: [
          { key: 'takif_sawad', label: 'تكييف سواد',  value: 'مواسير نحاس (بحريني)', price: 0, alts: [
            { label: 'نحاس بحريني', price: 0 }, { label: 'نحاس إيطالي', price: 10 },
          ]},
          { key: 'takif_byad',  label: 'تكييف بياض',  value: 'مكيف صالون 2طن لكل غرفة — تدفئة سلم لكل حمام', price: 0, alts: [
            { label: 'صالون 2طن + تدفئة سلم', price: 0 }, { label: 'مكيفات انفرتر', price: 25 },
          ]},
        ]
      },
      {
        title: 'رخام شبابيك', icon: '🪟',
        items: [{ key: 'rkhm_shbabik', label: 'رخام شبابيك', value: 'تركي غامق/فاتح', price: 0, alts: [
          { label: 'تركي غامق/فاتح', price: 0 }, { label: 'إيطالي', price: 15 },
        ]}]
      },
      {
        title: 'رخام أبواب', icon: '🚪',
        items: [{ key: 'rkhm_abwab', label: 'رخام أبواب', value: 'تركي غامق/فاتح', price: 0, alts: [
          { label: 'تركي غامق/فاتح', price: 0 }, { label: 'إيطالي', price: 12 },
        ]}]
      },
      {
        title: 'تلييس', icon: '🏗️',
        items: [{ key: 'tlees', label: 'تلييس', value: '3 أوجه (قدة) ودع فقط لجدران السيراميك', price: 0, alts: [
          { label: '3 أوجه قدة', price: 0 }, { label: '3 أوجه ودع كامل', price: 15 },
        ]}]
      },
      {
        title: 'سيراميك', icon: '🟦',
        items: [
          { key: 'ceramic_jdran', label: 'جدران', value: 'سعودي 1 (60×120)', price: 0, alts: [
            { label: 'سعودي (60×120)', price: 0 }, { label: 'إيطالي فاخر', price: 30 },
          ]},
          { key: 'ceramic_n3leh', label: 'نعلة',  value: '8cm من غرانيت الأرضيات', price: 0, alts: [
            { label: '8cm غرانيت', price: 0 }, { label: 'رخام', price: 10 },
          ]},
          { key: 'ceramic_ard',   label: 'أرضية', value: 'سعودي (60×60)', price: 0, alts: [
            { label: 'سعودي (60×60)', price: 0 }, { label: 'هندي (60×60)', price: -5 },
            { label: 'إيطالي فاخر', price: 25 },
          ]},
        ]
      },
      {
        title: 'المجلى', icon: '🍽️',
        items: [{ key: 'mujla', label: 'المجلى', value: 'تركي جالكسي', price: 0, alts: [
          { label: 'تركي جالكسي', price: 0 }, { label: 'جالكسي 3cm + جرن 7cm + ستانليس', price: 15 },
        ]}]
      },
      {
        title: 'خزن المجلى', icon: '🗄️',
        items: [{ key: 'khazn_mujla', label: 'خزن المجلى', value: 'هاي غلوس ضد الرطوبة — اكسسوار ثقيل', price: 0, alts: [
          { label: 'هاي غلوس', price: 0 }, { label: 'كومبوزيت', price: 10 },
        ]}]
      },
      {
        title: 'أبواب', icon: '🚪',
        items: [
          { key: 'bab_dakhli', label: 'داخلي',       value: 'سويد ملبس قشر سنديان / سنديان ملبس قشر', price: 0, alts: [
            { label: 'سويد ملبس قشر سنديان', price: 0 }, { label: 'كومبوزيت', price: -8 },
          ]},
          { key: 'bab_kharji', label: 'خارجي',       value: 'سويد ملبس قشر', price: 0, alts: [
            { label: 'سويد ملبس قشر', price: 0 }, { label: 'كومبوزيت', price: -5 },
          ]},
          { key: 'bab_hmam',   label: 'حمام+تواليت', value: 'ألمنيوم (مدار) أسود / خشبي', price: 0, alts: [
            { label: 'مدار أسود/خشبي', price: 0 }, { label: 'مسالكو فضي', price: -5 },
          ]},
        ]
      },
      {
        title: 'نوافذ', icon: '🪟',
        items: [{ key: 'nawafidh', label: 'نوافذ', value: 'ألمنيوم (مدار) أسود/خشبي — أبجور كهربا حركة وحدة', price: 0, alts: [
          { label: 'مدار أسود + أبجور كهربا', price: 0 }, { label: 'مدار خشبي بلور دبل + أبجور', price: 10 },
        ]}]
      },
      {
        title: 'دهان', icon: '🎨',
        items: [{ key: 'dahan', label: 'دهان', value: '3 معجونة أكرليك', price: 0, alts: [
          { label: '3 معجونة أكرليك', price: 0 }, { label: 'ديكور سقف كامل + سترب لايت', price: 20 },
        ]}]
      },
    ]
  },

  // ─── الباقة السوبر فاخرة ──────────────────
  pkg_300: {
    id: 'pkg_300',
    name: 'الباقة السوبر فاخرة',
    icon: '👑',
    price: 300,
    badge: 'VIP',
    desc: 'للفلل والمشاريع الكبيرة — أعلى مستوى',
    sections: [
      {
        title: 'الصحية', icon: '💧',
        items: [
          { key: 'miah_malha',  label: 'مياه مالحة (سواد)', value: '4 إنش سماكة 3.7 — 3 إنش سماكة 3.6 — 2 إنش (كالدا)', price: 0, alts: [
            { label: 'كالدا', price: 0 }, { label: 'ألماني فاخر', price: 20 },
          ]},
          { key: 'miah_helwa',  label: 'مياه حلوة (سواد)', value: '20 بار PPR بارد 25mm — ساخن 32mm (كالدا)', price: 0, alts: [
            { label: 'كالدا', price: 0 }, { label: 'ألماني', price: 15 },
          ]},
          { key: 'khazzan',     label: 'خزان',              value: 'غندور 10×2 بلكون — حنفية كولار — 3 طبقات حديد', price: 0, alts: [
            { label: 'غندور 10×2', price: 0 }, { label: 'ستانليس ستيل', price: 30 },
          ]},
          { key: 'hanafiyat',   label: 'حنفيات (سواد)',     value: 'مازوت — 2 بلكون — حنفية كولار', price: 0, alts: [
            { label: 'قياسي', price: 0 }, { label: 'إيطالي فاخر', price: 25 },
          ]},
          { key: 'khallatat',   label: 'خلاطات (سواد)',     value: 'صيني فاخر', price: 0, alts: [
            { label: 'صيني فاخر', price: 0 }, { label: 'إيطالي فاخر', price: 30 },
          ]},
          { key: 'deenamo',     label: 'دينمو (بياض)',      value: 'كانديلا — 200L — حراق مازوت/كهرباء — طاقة شمسية', price: 0, alts: [
            { label: 'كانديلا 200L', price: 0 }, { label: 'كانديلا 300L', price: 20 },
          ]},
          { key: 'doush',       label: 'دوش (بياض)',        value: 'كرت كامل بلور', price: 0, alts: [
            { label: 'كرت كامل بلور', price: 0 }, { label: 'كرت شطاف ستانليس مصافي', price: 10 },
          ]},
          { key: 'maghasil',    label: 'مغاسل (بياض)',      value: 'مغسلة جرن / معلق (حسب الطلب)', price: 0, alts: [
            { label: 'جرن/معلق حسب الطلب', price: 0 }, { label: 'بورسلان إيطالي', price: 25 },
          ]},
          { key: 'jakdoush',    label: 'جاكدوش',            value: '3 مآخذ / متحرك', price: 0, alts: [
            { label: '3 مآخذ متحرك', price: 0 }, { label: 'إيطالي 5 مآخذ', price: 20 },
          ]},
          { key: 'teb',         label: 'تيب (سواد)',        value: '23 ضغط عالي — 16 للجدران', price: 0, alts: [] },
          { key: 'olab',        label: 'علب (سواد)',        value: 'ماجيك', price: 0, alts: [] },
        ]
      },
      {
        title: 'الكهرباء', icon: '⚡',
        items: [
          { key: 'aslak',       label: 'أسلاك',             value: '3mm مفرد برايز — 1.5mm مفتاح — 1mm مزدوج ليد — 6mm الرئيسي (نيو باور)', price: 0, alts: [
            { label: 'نيو باور', price: 0 }, { label: 'VIMAR إيطالي', price: 20 },
          ]},
          { key: 'accessories', label: 'اكسسوارات',         value: 'كومو/VIMAR', price: 0, alts: [] },
          { key: 'qawate3',     label: 'قواطع',             value: '(كوري) قاطع لكل غرفة مكيف براد غسالة — دارات حماية — طاقة شمسية', price: 0, alts: [
            { label: 'كوري دارات حماية', price: 0 }, { label: 'ABB أوروبي', price: 35 },
          ]},
          { key: 'enareh',      label: 'إنارة + ليد',       value: 'سبوتات — إضاءة حبال مخفية — سترب لايت', price: 0, alts: [
            { label: 'سبوتات + حبال + سترب', price: 0 }, { label: 'LED ذكي', price: 20 },
          ]},
          { key: 'solar',       label: 'طاقة شمسية',        value: '8 ألواح — بطارية 300A ليثيوم — انفتر 6200', price: 0, alts: [
            { label: '8 ألواح + 300A', price: 0 }, { label: '12 لوح + 400A', price: 50 },
          ]},
        ]
      },
      {
        title: 'تكييف', icon: '❄️',
        items: [
          { key: 'takif_sawad', label: 'تكييف سواد', value: 'مواسير نحاس (بحريني)', price: 0, alts: [
            { label: 'نحاس بحريني', price: 0 }, { label: 'نحاس إيطالي', price: 15 },
          ]},
          { key: 'takif_byad',  label: 'تكييف بياض', value: 'مكيفات انفرتر', price: 0, alts: [
            { label: 'انفرتر', price: 0 }, { label: 'مركزي', price: 40 },
          ]},
        ]
      },
      {
        title: 'تدفئة', icon: '🔥',
        items: [{ key: 'tadfeh', label: 'تدفئة', value: 'تدفئة أرضية أنانيب — أسطوانة — مجمع — حراق', price: 0, alts: [
          { label: 'تدفئة أرضية', price: 0 }, { label: 'راديتور ألمنيوم', price: 20 },
        ]}]
      },
      {
        title: 'رخام شبابيك', icon: '🪟',
        items: [{ key: 'rkhm_shbabik', label: 'رخام شبابيك', value: 'تركي غامق/فاتح', price: 0, alts: [
          { label: 'تركي', price: 0 }, { label: 'إيطالي', price: 20 },
        ]}]
      },
      {
        title: 'رخام أبواب', icon: '🚪',
        items: [{ key: 'rkhm_abwab', label: 'رخام أبواب', value: 'تركي غامق/فاتح — أبواب خارجية/داخلية', price: 0, alts: [
          { label: 'تركي', price: 0 }, { label: 'إيطالي', price: 18 },
        ]}]
      },
      {
        title: 'تلييس', icon: '🏗️',
        items: [{ key: 'tlees', label: 'تلييس', value: '3 أوجه ودع لكل الحيطان', price: 0, alts: [
          { label: '3 أوجه ودع كامل', price: 0 }, { label: 'ودع + بياض جاهز', price: 10 },
        ]}]
      },
      {
        title: 'سيراميك', icon: '🟦',
        items: [
          { key: 'ceramic_jdran', label: 'جدران', value: 'سعودي (120×60)', price: 0, alts: [
            { label: 'سعودي (120×60)', price: 0 }, { label: 'إيطالي فاخر', price: 35 },
          ]},
          { key: 'ceramic_n3leh', label: 'نعلة',  value: '8cm من غرانيت الأرضيات', price: 0, alts: [] },
          { key: 'ceramic_ard',   label: 'أرضية', value: 'هندي (120×60)', price: 0, alts: [
            { label: 'هندي (120×60)', price: 0 }, { label: 'إيطالي فاخر', price: 40 },
          ]},
        ]
      },
      {
        title: 'المجلى', icon: '🍽️',
        items: [{ key: 'mujla', label: 'المجلى', value: 'جالكسي 3cm — جرن حجر 7cm — ستانليس ستيل', price: 0, alts: [
          { label: 'جالكسي + ستانليس', price: 0 }, { label: 'كوارتز إيطالي', price: 30 },
        ]}]
      },
      {
        title: 'خزن المجلى', icon: '🗄️',
        items: [{ key: 'khazn_mujla', label: 'خزن المجلى', value: 'هاي غلوس ضد الرطوبة — اكسسوار ثقيل', price: 0, alts: [
          { label: 'هاي غلوس', price: 0 }, { label: 'لاكيه فاخر', price: 20 },
        ]}]
      },
      {
        title: 'أبواب', icon: '🚪',
        items: [
          { key: 'bab_dakhli', label: 'داخلي',       value: 'كومبوزيت', price: 0, alts: [
            { label: 'كومبوزيت', price: 0 }, { label: 'خشب ماليزي فاخر', price: 25 },
          ]},
          { key: 'bab_kharji', label: 'خارجي',       value: 'كومبوزيت', price: 0, alts: [
            { label: 'كومبوزيت', price: 0 }, { label: 'خشب ماليزي', price: 20 },
          ]},
          { key: 'bab_hmam',   label: 'حمام+تواليت', value: 'مدار خشبي — اكسسوارات ثقيلة', price: 0, alts: [
            { label: 'مدار خشبي ثقيل', price: 0 }, { label: 'زجاج مزدوج', price: 15 },
          ]},
        ]
      },
      {
        title: 'نوافذ', icon: '🪟',
        items: [{ key: 'nawafidh', label: 'نوافذ', value: 'مدار خشبي/بلور دبل — اكسسوارات ثقيلة — أبجور كهربا حركة وحدة', price: 0, alts: [
          { label: 'مدار خشبي + أبجور كهربا', price: 0 }, { label: 'زجاج ثلاثي عازل', price: 25 },
        ]}]
      },
      {
        title: 'دهان', icon: '🎨',
        items: [{ key: 'dahan', label: 'دهان', value: '3 معجونة أكرليك', price: 0, alts: [
          { label: '3 معجونة أكرليك', price: 0 }, { label: 'طلاء فلوري إيطالي', price: 20 },
        ]}]
      },
      {
        title: 'ديكور', icon: '✨',
        items: [{ key: 'dekor', label: 'ديكور', value: 'سقف كامل — سترب لايت — ديكور جدران — شقر بلاستيك (المستقبل) بلكون', price: 0, alts: [
          { label: 'سقف + سترب + ديكور', price: 0 }, { label: 'ديكور فاخر كامل', price: 30 },
        ]}]
      },
      {
        title: 'حجر للجدران', icon: '🪨',
        items: [{ key: 'hajar', label: 'حجر للجدران', value: 'وطني / تركي', price: 0, alts: [
          { label: 'وطني', price: 0 }, { label: 'تركي', price: 10 },
        ]}]
      },
    ]
  }
};

// ─── الباقة الاقتصادية (65$) ──────────────
PACKAGES_DATA['pkg_65'] = {
  id: 'pkg_65',
  name: 'الباقة الاقتصادية',
  icon: '🏠',
  price: 65,
  badge: '',
  desc: 'مثالية للغرف والشقق الصغيرة',
  sections: [
    {
      title: 'السباكة', icon: '💧',
      items: [
        { key: 'ppr_barid',  label: 'أنابيب بارد',    value: 'PPR بارد 20mm (السعد)', price: 0,
          alts: [{ label: 'PPR بارد 20mm (السعد)', price: 0 }, { label: 'PPR بارد 25mm (السعد)', price: 5 }, { label: 'PPR بارد 25mm (كالدا)', price: 10 }] },
        { key: 'ppr_sakhin', label: 'أنابيب ساخن',    value: 'PPR ساخن 25mm (السعد)', price: 0,
          alts: [{ label: 'PPR ساخن 25mm (السعد)', price: 0 }, { label: 'PPR ساخن 32mm (السعد)', price: 6 }, { label: 'PPR ساخن 32mm (كالدا)', price: 12 }] },
        { key: 'mawaseer',   label: 'مواسير صرف',     value: '1 إنش (31.2) و 2 إنش (36)', price: 0, alts: [] },
        { key: 'barmeel',    label: 'براميل مياه',    value: '10 برميل أبيض/أزرق بلاستيك (المسعود) كفالة 5 سنوات', price: 0,
          alts: [{ label: '10 برميل بلاستيك المسعود', price: 0 }, { label: '10 برميل ستانليس', price: 25 }] },
        { key: 'znobia',     label: 'زنوبيا',         value: 'زنوبيا + زنوبيا دعسة', price: 0,
          alts: [{ label: 'زنوبيا + دعسة', price: 0 }, { label: 'زنوبيا دعسة فاخرة', price: 8 }] },
        { key: 'sakhkhan',   label: 'سخان',           value: 'سخان إيطالي 17 كيلو (البهاء)', price: 0,
          alts: [{ label: 'البهاء 17 كيلو', price: 0 }, { label: 'أسطوانة مازوت 100L', price: 15 }, { label: 'طاقة شمسية', price: 35 }] },
        { key: 'rasoor',     label: 'راصور + فرنجي',  value: 'راصور + فرنجي + قازان', price: 0, alts: [] },
        { key: 'twaleet',    label: 'تواليت',         value: 'تواليت شرق + خرطوم تواليت', price: 0,
          alts: [{ label: 'تواليت شرق', price: 0 }, { label: 'تواليت صيني برنس', price: 15 }] },
        { key: 'masafi',     label: 'مصافي',          value: 'مصافي + مياه مالحة وحلوة', price: 0, alts: [] },
        { key: 'hanafiyat',  label: 'حنفيات',         value: 'حنفيات نحاس صيني (زاهية) + خلاطات', price: 0,
          alts: [{ label: 'زاهية (صيني)', price: 0 }, { label: 'برنس (صيني فاخر)', price: 10 }, { label: 'تركي ريمكس', price: 18 }] },
        { key: 'doush',      label: 'دوش + مغاسل',   value: 'دوش + مغاسل + قصبة (زاهية)', price: 0,
          alts: [{ label: 'زاهية', price: 0 }, { label: 'برنس فاخر', price: 12 }] },
      ]
    },
    {
      title: 'الكهرباء', icon: '⚡',
      items: [
        { key: 'aslak',      label: 'أسلاك',          value: '6mm رئيسي — 1.5mm مفرد — 1mm مزدوج (لينا)', price: 0,
          alts: [{ label: 'لينا', price: 0 }, { label: 'نيو باور', price: 10 }] },
        { key: 'mafateeh',   label: 'مفاتيح',         value: 'مفاتيح برايز 3mm + ليد', price: 0,
          alts: [{ label: 'برايز 3mm', price: 0 }, { label: 'VIMAR إيطالي', price: 12 }] },
        { key: 'qawate3',    label: 'قواطع',          value: '16 مفرد لكل غرفة — 32 مزدوج رئيسي', price: 0,
          alts: [{ label: 'قياسي 16+32', price: 0 }, { label: 'كوري مع حماية', price: 15 }] },
        { key: 'qawazin',    label: 'قوازين',         value: 'قواطع + علب + اكسسوارات', price: 0, alts: [] },
        { key: 'enareh',     label: 'إنارة',          value: 'إنارة + ليد + نيولات', price: 0,
          alts: [{ label: 'نيولات + ليد', price: 0 }, { label: 'سبوتات مخفية', price: 12 }] },
        { key: 'deenamo',    label: 'دينمو',          value: 'دينمو كانديلا', price: 0,
          alts: [{ label: 'كانديلا', price: 0 }, { label: 'كانديلا احتياطي كامل', price: 20 }] },
      ]
    },
    {
      title: 'التشطيبات', icon: '🎨',
      items: [
        { key: 'shibabik',   label: 'شبابيك وأبواب',  value: 'شبابيك + أبواب ألمنيوم مسالكو فضي', price: 0,
          alts: [{ label: 'مسالكو فضي', price: 0 }, { label: 'مسالكو أسود', price: 8 }, { label: 'مدار خشبي', price: 20 }] },
        { key: 'masayafi',   label: 'مصيافي',         value: 'مصيافي سماكة 3cm لجميع الشبابيك', price: 0,
          alts: [{ label: 'مصيافي 3cm', price: 0 }, { label: 'تركي غامق/فاتح', price: 8 }] },
        { key: 'blat',       label: 'بلاط/سيراميك',   value: 'بلاط حسواني 30×30 / سيراميك زنوبيا 50×50', price: 0,
          alts: [{ label: 'بلاط حسواني 30×30', price: 0 }, { label: 'زنوبيا 50×50', price: 5 }, { label: 'هندي 60×60', price: 15 }, { label: 'سعودي 60×60', price: 20 }] },
        { key: 'ceramic_hmam', label: 'سيراميك حمام/مطبخ', value: 'زنوبيا 4 (60×30)', price: 0,
          alts: [{ label: 'زنوبيا 4 (60×30)', price: 0 }, { label: 'سعودي (60×120)', price: 18 }] },
        { key: 'graneet',    label: 'غرانيت مجلى',   value: 'غرانيت تركي 3cm — جرن حجر 60cm', price: 0,
          alts: [{ label: 'غرانيت تركي 3cm', price: 0 }, { label: 'جالكسي + ستانليس', price: 20 }] },
        { key: 'mdf',        label: 'MDF خزن',       value: 'MDF صيني جاهز', price: 0,
          alts: [{ label: 'MDF صيني', price: 0 }, { label: 'هاي غلوس', price: 12 }] },
        { key: 'tarsh',      label: 'طرش وبياض',     value: 'طرش 3 أوجه (جدران + نعلة + أرضية) + بياض داخلي وخارجي', price: 0,
          alts: [{ label: '3 أوجه طرش + بياض', price: 0 }, { label: '3 معجونة أكرليك', price: 10 }] },
        { key: 'bab_dakhli', label: 'أبواب داخلية',  value: 'فرنسي سويد MDF صيني جاهز', price: 0,
          alts: [{ label: 'MDF صيني', price: 0 }, { label: 'فرنسي سويد + بلور', price: 8 }, { label: 'سنديان ملبس قشر', price: 18 }] },
      ]
    },
  ]
};

// ─── الباقة المتوسطة (120$) ────────────────
PACKAGES_DATA['pkg_120'] = {
  id: 'pkg_120',
  name: 'الباقة المتوسطة',
  icon: '🏢',
  price: 120,
  badge: 'الأكثر طلباً',
  desc: 'للشقق والمنازل المتوسطة',
  sections: [
    {
      title: 'السباكة المحسّنة', icon: '💧',
      items: [
        { key: 'ppr_barid',  label: 'أنابيب بارد',    value: 'PPR بارد 20mm (السعد)', price: 0,
          alts: [{ label: 'PPR 20mm السعد', price: 0 }, { label: 'PPR 25mm كالدا', price: 8 }] },
        { key: 'ppr_sakhin', label: 'أنابيب ساخن',    value: 'PPR ساخن 32mm (السعد)', price: 0,
          alts: [{ label: 'PPR 32mm السعد', price: 0 }, { label: 'PPR 32mm كالدا', price: 10 }] },
        { key: 'barmeel',    label: 'براميل مياه',    value: '10 برميل أبيض/أزرق بلاستيك (المسعود)', price: 0,
          alts: [{ label: 'بلاستيك المسعود', price: 0 }, { label: 'ستانليس ستيل', price: 20 }] },
        { key: 'znobia',     label: 'زاهية/ليلك/تيب', value: 'زاهية — ليلك — تيب فاخر', price: 0,
          alts: [{ label: 'زاهية + ليلك + تيب', price: 0 }, { label: 'برنس فاخر', price: 10 }] },
        { key: 'khazzan',    label: 'خزان مياه',      value: 'خزان مياه + صحية متكاملة', price: 0,
          alts: [{ label: 'خزان صحية متكاملة', price: 0 }, { label: 'خزان ستانليس', price: 18 }] },
        { key: 'masayafi',   label: 'مصيافي',         value: 'مصيافي حمام وتواليت مستقل', price: 0, alts: [] },
        { key: 'khallatat',  label: 'خلاطات',         value: 'خلاطات صيني (برنس)', price: 0,
          alts: [{ label: 'برنس صيني', price: 0 }, { label: 'تركي ريمكس', price: 12 }] },
        { key: 'sakhkhan',   label: 'سخان',           value: 'سخان إيطالي 17 كيلو (البهاء)', price: 0,
          alts: [{ label: 'البهاء 17 كيلو', price: 0 }, { label: 'أسطوانة 100L مازوت', price: 12 }, { label: 'طاقة شمسية 4 ألواح', price: 40 }] },
      ]
    },
    {
      title: 'الكهرباء المحسّنة', icon: '⚡',
      items: [
        { key: 'aslak',      label: 'أسلاك',          value: '6mm رئيسي — 1.5mm مفرد — 1mm مزدوج (لينا)', price: 0,
          alts: [{ label: 'لينا', price: 0 }, { label: 'نيو باور', price: 8 }] },
        { key: 'qawazin',    label: 'قوازين',         value: '20 قازان كهربائي', price: 0,
          alts: [{ label: '20 قازان', price: 0 }, { label: '32 قازان', price: 8 }] },
        { key: 'enareh',     label: 'إضاءة LED',      value: 'إضاءة LED متكاملة', price: 0,
          alts: [{ label: 'LED متكاملة', price: 0 }, { label: 'سبوتات + سترب لايت', price: 15 }] },
        { key: 'qawate3',    label: 'لوحة قواطع',     value: 'لوحة قواطع رئيسية متكاملة + تأريض + حماية', price: 0,
          alts: [{ label: 'لوحة قياسية', price: 0 }, { label: 'كوري دارات حماية', price: 15 }, { label: 'VIMAR إيطالي', price: 25 }] },
      ]
    },
    {
      title: 'التشطيبات المحسّنة', icon: '🎨',
      items: [
        { key: 'shibabik',   label: 'شبابيك وأبواب',  value: 'شبابيك + أبواب ألمنيوم مسالكو فضي', price: 0,
          alts: [{ label: 'مسالكو فضي', price: 0 }, { label: 'مدار أسود', price: 10 }, { label: 'مدار خشبي', price: 22 }] },
        { key: 'blat',       label: 'بلاط/سيراميك',   value: 'بلاط حسواني 30×30 / سيراميك زنوبيا 50×50', price: 0,
          alts: [{ label: 'بلاط حسواني 30×30', price: 0 }, { label: 'زنوبيا 50×50', price: 5 }, { label: 'هندي 60×60', price: 15 }, { label: 'سعودي 60×60', price: 20 }] },
        { key: 'ceramic_hmam', label: 'سيراميك حمام',  value: 'زنوبيا 4 (60×30)', price: 0,
          alts: [{ label: 'زنوبيا 4 (60×30)', price: 0 }, { label: 'سعودي (60×120)', price: 18 }] },
        { key: 'khashab',    label: 'خشب سويد',       value: 'خشب سويد سد كامل', price: 0,
          alts: [{ label: 'خشب سويد سد كامل', price: 0 }, { label: 'سنديان ملبس قشر', price: 15 }, { label: 'كومبوزيت', price: 10 }] },
        { key: 'borslaan',   label: 'مغاسل برنس',     value: 'صيني برنس (مغاسل فاخرة)', price: 0,
          alts: [{ label: 'برنس صيني', price: 0 }, { label: 'بورسلان إيطالي', price: 20 }] },
        { key: 'majeek',     label: 'دهان ماجيك',     value: 'ضغط عالي 23 — 16 للجدران (ماجيك)', price: 0,
          alts: [{ label: 'ماجيك 23/16', price: 0 }, { label: '3 معجونة أكرليك', price: 8 }] },
        { key: 'sawad',      label: 'سواد',           value: 'سواد داخلي وخارجي', price: 0, alts: [] },
        { key: 'graneet',    label: 'غرانيت مجلى',   value: 'غرانيت تركي 3cm — جرن حجر 60cm', price: 0,
          alts: [{ label: 'غرانيت تركي', price: 0 }, { label: 'جالكسي + ستانليس', price: 18 }] },
      ]
    },
  ]
};

// ─── الباقة الفاخرة (200$) ─────────────────
PACKAGES_DATA['pkg_200'] = {
  id: 'pkg_200',
  name: 'الباقة الفاخرة',
  icon: '👑',
  price: 200,
  badge: '',
  desc: 'للفلل والمشاريع الكبيرة',
  sections: [
    {
      title: 'سباكة فاخرة كاملة', icon: '💧',
      items: [
        { key: 'ppr_barid',  label: 'أنابيب بارد',    value: 'PPR بارد 25mm (السعد)', price: 0,
          alts: [{ label: 'PPR 25mm السعد', price: 0 }, { label: 'PPR 25mm كالدا', price: 8 }, { label: 'PPR 32mm كالدا', price: 15 }] },
        { key: 'ppr_sakhin', label: 'أنابيب ساخن',    value: 'PPR ساخن 32mm (السعد)', price: 0,
          alts: [{ label: 'PPR 32mm السعد', price: 0 }, { label: 'PPR 32mm كالدا', price: 10 }] },
        { key: 'znobia',     label: 'زنوبيا دعسة',    value: 'زنوبيا دعسة فاخرة', price: 0,
          alts: [{ label: 'زنوبيا دعسة فاخرة', price: 0 }, { label: 'تيب فاخر إيطالي', price: 15 }] },
        { key: 'khallatat',  label: 'خلاطات ومغاسل',  value: 'خلاطات ومغاسل برنس فاخرة', price: 0,
          alts: [{ label: 'برنس فاخر', price: 0 }, { label: 'تركي ريمكس', price: -5 }, { label: 'إيطالي فاخر', price: 20 }] },
        { key: 'miah_sys',   label: 'نظام مياه',      value: 'نظام مياه مالحة وحلوة مستقل', price: 0, alts: [] },
        { key: 'khazzan',    label: 'خزانات',         value: 'خزان علوي وسفلي + دينمو', price: 0,
          alts: [{ label: 'علوي + سفلي + دينمو', price: 0 }, { label: 'ستانليس ستيل', price: 25 }] },
        { key: 'qasba',      label: 'قصبة وليلك',     value: 'قصبة وليلك وتيب فاخر', price: 0, alts: [] },
      ]
    },
    {
      title: 'كهرباء فاخرة كاملة', icon: '⚡',
      items: [
        { key: 'aslak',      label: 'أسلاك رئيسية',   value: 'أسلاك لينا 6mm رئيسي كامل', price: 0,
          alts: [{ label: 'لينا 6mm', price: 0 }, { label: 'نيو باور 6mm', price: 8 }, { label: 'VIMAR إيطالي', price: 20 }] },
        { key: 'qawate3',    label: 'لوحة قواطع',     value: 'لوحة قواطع ذكية', price: 0,
          alts: [{ label: 'قواطع ذكية', price: 0 }, { label: 'ABB أوروبي', price: 30 }] },
        { key: 'enareh',     label: 'إنارة LED فاخرة', value: 'إنارة LED + نيولات فاخرة', price: 0,
          alts: [{ label: 'LED + نيولات فاخرة', price: 0 }, { label: 'سبوتات + سترب + حبال مخفية', price: 15 }] },
        { key: 'qawazin',    label: 'قوازين',         value: '32 مزدوج + 20 قازان', price: 0,
          alts: [{ label: '32 مزدوج + 20 قازان', price: 0 }, { label: '32 + 32 + 20 (موسّع)', price: 12 }] },
        { key: 'deenamo',    label: 'دينمو احتياطي',  value: 'دينمو كانديلا احتياطي', price: 0,
          alts: [{ label: 'كانديلا احتياطي', price: 0 }, { label: 'طاقة شمسية 8 ألواح', price: 50 }] },
        { key: 'ta2reed',    label: 'تأريض',          value: 'تأريض كامل + حماية فائقة', price: 0, alts: [] },
      ]
    },
    {
      title: 'تشطيبات فاخرة كاملة', icon: '🎨',
      items: [
        { key: 'wajha',      label: 'واجهة ألمنيوم',  value: 'واجهة ألمنيوم مسالكو فضي فاخر', price: 0,
          alts: [{ label: 'مسالكو فضي فاخر', price: 0 }, { label: 'مدار أسود فاخر', price: 15 }, { label: 'كومبوزيت', price: 10 }] },
        { key: 'khashab',    label: 'خشب سويد',       value: 'خشب سويد سد كامل فاخر', price: 0,
          alts: [{ label: 'خشب سويد فاخر', price: 0 }, { label: 'سنديان ملبس قشر', price: 12 }, { label: 'كومبوزيت', price: -5 }] },
        { key: 'graneet',    label: 'غرانيت',         value: 'غرانيت تركي 3cm كامل', price: 0,
          alts: [{ label: 'غرانيت تركي 3cm', price: 0 }, { label: 'جالكسي + ستانليس', price: 15 }, { label: 'كوارتز إيطالي', price: 30 }] },
        { key: 'ceramic_ard', label: 'سيراميك أرضية', value: 'سيراميك زنوبيا 3 (50×50)', price: 0,
          alts: [{ label: 'زنوبيا 3 (50×50)', price: 0 }, { label: 'هندي (60×60)', price: 10 }, { label: 'سعودي (60×60)', price: 15 }, { label: 'هندي (120×60)', price: 25 }] },
        { key: 'tarsh',      label: 'طرش وبياض',     value: 'طرش 3 أوجه + بياض داخلي/خارجي', price: 0,
          alts: [{ label: '3 أوجه طرش + بياض', price: 0 }, { label: '3 معجونة أكرليك', price: 10 }] },
        { key: 'majeek',     label: 'دهان ماجيك',     value: 'ماجيك ضغط عالي 23 للجدران', price: 0,
          alts: [{ label: 'ماجيك 23', price: 0 }, { label: 'دهان إيطالي فلوري', price: 20 }] },
        { key: 'borslaan',   label: 'صيني برنس',      value: 'صيني برنس فاخر كامل', price: 0,
          alts: [{ label: 'برنس فاخر', price: 0 }, { label: 'إيطالي فاخر', price: 25 }] },
        { key: 'dhaman',     label: 'ضمان',           value: 'ضمان شامل على جميع الأعمال ✅', price: 0, alts: [] },
      ]
    },
  ]
};
