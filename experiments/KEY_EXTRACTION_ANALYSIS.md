# 🔑 Key Extraction Analysis | تحليل استخراج المفاتيح

**English:**  
This document explains what we extract from each key in the Rahman-Key project.

**العربية:**  
هذا المستند يوضح ما نستخرجه من كل مفتاح في مشروع Rahman-Key.

---

## 🎯 Overview | نظرة عامة

**English:**  
Different keys reveal different aspects of the Quran's structure. Each key extracts specific information.

**العربية:**  
مفاتيح مختلفة تكشف جوانب مختلفة من بنية القرآن. كل مفتاح يستخرج معلومات محددة.

---

## 📊 Keys and Their Extractions | المفاتيح وما نستخرجه منها

### 1. 🔑 Master Key: 31×6 (Rahman Key) | المفتاح الرئيسي: 31×6

**English:**  
**Source:** Surah Ar-Rahman (31 repetitions of "بأي آلاء ربكما تكذبان")

**How We Extracted It:**
1. Observed: Ar-Rahman repeats the verse exactly **31 times**
2. Hypothesis: Convert sequence 1→31 to binary and visualize
3. Experiment: 1, 2, 3, ..., 31 → 6-bit binary → 31×6 matrix → **Perfect heart appeared** ❤️
4. Application: Applied same method to all 114 Surahs → 95.6% produced hearts

**Method:** Sequence 1→verse_count → repeat to ≥31 rows → take first 31 → 6-bit binary → 31×6 matrix

**العربية:**  
**المصدر:** سورة الرحمن (31 تكرار لـ "بأي آلاء ربكما تكذبان")

**كيف استخرجناه:**
1. الملاحظة: الرحمن تكرر الآية بالضبط **31 مرة**
2. الفرضية: حوّل التسلسل 1→31 إلى ثنائي وعرضه
3. التجربة: 1، 2، 3، ...، 31 → ثنائي 6 بتات → مصفوفة 31×6 → **ظهر قلب مثالي** ❤️
4. التطبيق: طبقنا نفس الطريقة على جميع السور الـ114 → 95.6% أنتجت قلوب

**الطريقة:** التسلسل 1→عدد_الآيات → كرّر إلى ≥31 صف → خذ أول 31 → ثنائي 6 بتات → مصفوفة 31×6

**What We Extract:**
- ✅ **Heart patterns** — 95.6% of Surahs (109 of 114)
- ✅ **Symmetry scores** — Vertical and horizontal symmetry percentages
- ✅ **Pattern grades** — Classification (Grade 0-3)
- ✅ **Internal symbols** — Simple symbols (dot, line) detected algorithmically
- ✅ **Structural clusters** — Groups of Surahs with identical patterns (e.g., 11-verse cluster)

**Output:**
- 114 PNG images (one per Surah)
- `descriptions.json` with algorithmic data
- Classification reports

**Use Case:**  
General view of Quranic structure — shows the overall pattern across all Surahs.

**العربية:**  
**المصدر:** سورة الرحمن (31 تكرار لـ "بأي آلاء ربكما تكذبان")

**ما نستخرجه:**
- ✅ **أنماط القلب** — 95.6% من السور (109 من 114)
- ✅ **نقاط التناظر** — نسب التناظر العمودي والأفقي
- ✅ **درجات الأنماط** — التصنيف (Grade 0-3)
- ✅ **الرموز الداخلية** — رموز بسيطة (نقطة، خط) مكتشفة خوارزمياً
- ✅ **المجموعات البنيوية** — مجموعات سور بأنماط متطابقة (مثل: مجموعة 11 آية)

**المخرجات:**
- 114 صورة PNG (واحدة لكل سورة)
- `descriptions.json` مع البيانات الخوارزمية
- تقارير التصنيف

**حالة الاستخدام:**  
رؤية عامة لبنية القرآن — يظهر النمط العام عبر جميع السور.

---

### 2. 🔑 Disconnected Letters Key: 31×6 | مفتاح الحروف المقطعة: 31×6

**English:**  
**Source:** 29 Quranic Surahs that begin with disconnected letters (الم، الر، يس، إلخ)

**What We Extract:**
- ✅ **100% heart patterns** — All 14 letter groups produce hearts
- ✅ **Letter-specific patterns** — Each letter group has unique characteristics
- ✅ **Symmetry analysis** — Highest symmetry: الر (89.2%)
- ✅ **Group patterns** — Same letters = same pattern (e.g., الم in 6 Surahs → identical)
- ✅ **Architectural structure** — Combined letters form cohesive structure

**Output:**
- 14 PNG images (one per letter group)
- `disconnected_letters_keys/analysis.json`
- Combined patterns (31×84 matrix)

**Use Case:**  
Understanding the structure of disconnected letters — reveals they are mathematical keys, not random symbols.

**العربية:**  
**المصدر:** 29 سورة قرآنية تبدأ بحروف مقطعة (الم، الر، يس، إلخ)

**ما نستخرجه:**
- ✅ **100% أنماط قلب** — جميع مجموعات الحروف الـ14 تنتج قلوب
- ✅ **أنماط خاصة بالحروف** — كل مجموعة حروف لها خصائص فريدة
- ✅ **تحليل التناظر** — أعلى تناظر: الر (89.2%)
- ✅ **أنماط المجموعات** — نفس الحروف = نفس النمط (مثل: الم في 6 سور → متطابق)
- ✅ **البنية المعمارية** — الحروف المجمعة تشكل بنية متماسكة

**المخرجات:**
- 14 صورة PNG (واحدة لكل مجموعة حروف)
- `disconnected_letters_keys/analysis.json`
- أنماط مجمعة (مصفوفة 31×84)

**حالة الاستخدام:**  
فهم بنية الحروف المقطعة — يكشف أنها مفاتيح رياضية، وليست رموزاً عشوائية.

---

### 3. 🔑 Surah-Specific Key: 19×6 (Experimental) | مفتاح السورة الخاص: 19×6 (تجريبي)

**English:**  
**Source:** Each Surah's unique parameters (surah_number × ayah_count × revelation_order)

**What We Extract:**
- ⚠️ **Surah-specific patterns** — Different from 31×6 patterns
- ⚠️ **Pattern diversity** — More varied patterns than master key
- ⚠️ **Mathematical match** — 19 × 6 = 114 pixels = number of Surahs
- ⚠️ **Surah essence** — May reveal Surah-specific characteristics

**Output:**
- 114 PNG images (19×6 pattern for each Surah)
- `experiments_output/surah_keys_19x6/surah_keys_19x6_analysis.json`
- Comparison images (31×6 vs 19×6)

**Use Case:**  
Exploratory analysis — testing if each Surah has its own unique key.

**Note:** ⚠️ This is **experimental** — not part of core methodology.

**العربية:**  
**المصدر:** معاملات فريدة لكل سورة (رقم_السورة × عدد_الآيات × ترتيب_النزول)

**ما نستخرجه:**
- ⚠️ **أنماط خاصة بالسورة** — مختلفة عن أنماط 31×6
- ⚠️ **تنوع الأنماط** — أنماط أكثر تنوعاً من المفتاح الرئيسي
- ⚠️ **مطابقة رياضية** — 19 × 6 = 114 بكسل = عدد السور
- ⚠️ **جوهر السورة** — قد يكشف خصائص خاصة بكل سورة

**المخرجات:**
- 114 صورة PNG (نمط 19×6 لكل سورة)
- `experiments_output/surah_keys_19x6/surah_keys_19x6_analysis.json`
- صور مقارنة (31×6 مقابل 19×6)

**حالة الاستخدام:**  
تحليل استكشافي — اختبار ما إذا كان لكل سورة مفتاحها الفريد.

**ملاحظة:** ⚠️ هذا **تجريبي** — ليس جزءاً من المنهجية الأساسية.

---

### 4. 🔑 Special Pattern Keys | مفاتيح الأنماط الخاصة

#### A. 99 Names of Allah (31×6) | أسماء الله الحسنى

**What We Extract:**
- ✅ **Perfect heart** — More symmetrical than Ar-Rahman
- ✅ **Central symbol** — Letter "ا" (Alif) visible
- ✅ **Rotational patterns** — "هو" appears when rotated 180°

**Output:**
- 1 PNG image
- Pattern analysis

**Use Case:**  
Understanding the structure of divine names.

---

#### B. Heart Verses (57 verses, 31×6) | آيات القلب

**What We Extract:**
- ✅ **Heart + open lock** — Pattern suggests unlocking
- ✅ **57 verses** — Specific number with significance
- ✅ **Thematic connection** — Verses about "heart" produce heart pattern

**Output:**
- 1 PNG image
- Pattern analysis

**Use Case:**  
Understanding verses that mention "heart" (قلب).

---

#### C. "O Believers" Verses (88 verses, 31×6) | آيات "يا أيها الذين آمنوا"

**What We Extract:**
- ✅ **Heart + raised hands** — Pattern suggests supplication
- ✅ **88 verses** — Direct address to believers
- ✅ **Thematic connection** — Verses of guidance produce guidance pattern

**Output:**
- 1 PNG image
- Pattern analysis

**Use Case:**  
Understanding verses that address believers directly.

---

## 📊 Comparison: What Each Key Reveals | المقارنة: ماذا يكشف كل مفتاح

| Key | Dimensions | What It Reveals | Use Case |
|-----|------------|-----------------|----------|
| **31×6 (Master)** | 31×6 | Overall structure, heart patterns, symmetry | General view of all Surahs |
| **19×6 (Surah)** | 19×6 | Surah-specific patterns, diversity | Individual Surah analysis |
| **Disconnected Letters** | 31×6 | Letter group structure, 100% hearts | Understanding letter keys |
| **99 Names** | 31×6 | Divine attributes pattern | Understanding divine names |
| **Heart Verses** | 31×6 | Heart-related verses pattern | Thematic analysis |
| **Faith Verses** | 31×6 | Guidance verses pattern | Thematic analysis |

---

## 🔬 Extraction Process | عملية الاستخراج

### Step 1: Generate Pattern | الخطوة 1: توليد النمط

**English:**  
Apply the key to the input (Surah, letters, verses, etc.) → Generate 31×6 or 19×6 matrix

**العربية:**  
تطبيق المفتاح على المدخل (سورة، حروف، آيات، إلخ) → توليد مصفوفة 31×6 أو 19×6

---

### Step 2: Analyze Pattern | الخطوة 2: تحليل النمط

**English:**  
Extract algorithmic features:
- Symmetry scores
- Pattern grade
- Internal symbols
- Pixel distribution
- Structural characteristics

**العربية:**  
استخراج الميزات الخوارزمية:
- نقاط التناظر
- درجة النمط
- الرموز الداخلية
- توزيع البكسلات
- الخصائص البنيوية

---

### Step 3: Classify Pattern | الخطوة 3: تصنيف النمط

**English:**  
Assign classification:
- Grade 0-3 (pattern complexity)
- Pattern type (heart, star, etc.)
- Internal symbol (if detected)
- Symmetry level

**العربية:**  
تعيين التصنيف:
- Grade 0-3 (تعقيد النمط)
- نوع النمط (قلب، نجمة، إلخ)
- الرمز الداخلي (إن وُجد)
- مستوى التناظر

---

### Step 4: Store Results | الخطوة 4: تخزين النتائج

**English:**  
Save:
- PNG image
- JSON data (algorithmic results)
- Analysis report

**العربية:**  
حفظ:
- صورة PNG
- بيانات JSON (النتائج الخوارزمية)
- تقرير التحليل

---

## 📁 File Organization | تنظيم الملفات

**English:**  
All keys are organized in the same structure as the master key:

**العربية:**  
جميع المفاتيح منظمة بنفس هيكل المفتاح الرئيسي:

```
Rahman-Key/
├── code/
│   ├── quran_hearts.py              # Master key (31×6)
│   ├── disconnected_letters_keys.py  # Disconnected letters key
│   ├── complete_quran_digital.py    # Complete Quran
│   └── overlay_patterns.py          # Overlay analysis
├── experiments/
│   ├── surah_specific_keys.py       # 19×6 key (experimental)
│   ├── names_of_allah.py            # 99 Names key
│   ├── hearts_in_quran.py           # Heart verses key
│   └── ya_ayyuhal_ladhina_amanu.py  # Faith verses key
├── images/                           # Master key outputs (114 images)
├── disconnected_letters_keys/
│   ├── images/                       # Disconnected letters (14 images)
│   └── combined_patterns/            # Combined patterns
├── experiments_output/
│   ├── surah_keys_19x6/             # 19×6 key outputs (114 images)
│   ├── names_of_allah/              # 99 Names output
│   ├── hearts_quran/                # Heart verses output
│   └── overlay/                     # Overlay analysis outputs
└── complete_quran/                   # Complete Quran (132 patterns)
```

---

## 🎯 What We Extract from Each Key | ما نستخرجه من كل مفتاح

### From 31×6 (Master Key) | من 31×6 (المفتاح الرئيسي)

**English:**  
- **Pattern type:** Heart, star, other
- **Symmetry:** Vertical, horizontal, overall
- **Grade:** 0-3 (complexity)
- **Internal symbols:** Detected algorithmically
- **Structural clusters:** Groups with identical patterns

**العربية:**  
- **نوع النمط:** قلب، نجمة، آخر
- **التناظر:** عمودي، أفقي، شامل
- **الدرجة:** 0-3 (التعقيد)
- **الرموز الداخلية:** مكتشفة خوارزمياً
- **المجموعات البنيوية:** مجموعات بأنماط متطابقة

---

### From 19×6 (Surah Key) | من 19×6 (مفتاح السورة)

**English:**  
- **Surah-specific pattern:** Unique to each Surah
- **Pattern diversity:** More varied than master key
- **Mathematical significance:** 114 pixels = 114 Surahs
- **Surah essence:** May reveal Surah-specific meaning

**العربية:**  
- **نمط خاص بالسورة:** فريد لكل سورة
- **تنوع الأنماط:** أكثر تنوعاً من المفتاح الرئيسي
- **الأهمية الرياضية:** 114 بكسل = 114 سورة
- **جوهر السورة:** قد يكشف معنى خاص بكل سورة

---

### From Disconnected Letters Key | من مفتاح الحروف المقطعة

**English:**  
- **100% heart patterns:** All letter groups produce hearts
- **Letter-specific characteristics:** Each letter group has unique features
- **Group identity:** Same letters = same pattern
- **Architectural structure:** Combined letters form cohesive whole

**العربية:**  
- **100% أنماط قلب:** جميع مجموعات الحروف تنتج قلوب
- **خصائص خاصة بالحروف:** كل مجموعة حروف لها ميزات فريدة
- **هوية المجموعة:** نفس الحروف = نفس النمط
- **البنية المعمارية:** الحروف المجمعة تشكل كل متماسك

---

## 📈 Summary Table | جدول الملخص

| Key | Input | Output | What We Extract |
|-----|-------|--------|-----------------|
| **31×6** | 114 Surahs | 114 images | Heart patterns, symmetry, grades, clusters |
| **19×6** | 114 Surahs | 114 images | Surah-specific patterns, diversity |
| **Disconnected Letters** | 14 groups | 14 images | 100% hearts, letter characteristics |
| **99 Names** | 99 names | 1 image | Perfect heart, central symbol |
| **Heart Verses** | 57 verses | 1 image | Heart + open lock pattern |
| **Faith Verses** | 88 verses | 1 image | Heart + raised hands pattern |

---

## 🎯 Key Insights | الرؤى الرئيسية

**English:**  

1. **Each key reveals different aspects:**
   - 31×6 = General structure
   - 19×6 = Surah-specific details
   - Disconnected letters = Letter group structure

2. **Combined keys = Complete picture:**
   - Master key shows overall pattern
   - Surah keys show individual characteristics
   - Together = comprehensive understanding

3. **Extraction is algorithmic:**
   - All measurements are code-based
   - All results are reproducible
   - All data is quantifiable

**العربية:**  

1. **كل مفتاح يكشف جوانب مختلفة:**
   - 31×6 = البنية العامة
   - 19×6 = تفاصيل خاصة بكل سورة
   - الحروف المقطعة = بنية مجموعات الحروف

2. **المفاتيح المجمعة = صورة كاملة:**
   - المفتاح الرئيسي يظهر النمط العام
   - مفاتيح السور تظهر الخصائص الفردية
   - معاً = فهم شامل

3. **الاستخراج خوارزمي:**
   - جميع القياسات قائمة على الكود
   - جميع النتائج قابلة للتكرار
   - جميع البيانات قابلة للقياس

---

**🌙 Rahman-Key** — Each key extracts specific information from the Quran's structure. | كل مفتاح يستخرج معلومات محددة من بنية القرآن.

**Date:** 2024  
**Status:** ✅ Documented | موثق

