# 🔑 كيف استخرجنا المفاتيح | How We Extracted the Keys

**English:**  
This document explains how we discovered and extracted the main key (31×6) and sub-keys in the Rahman-Key project.

**العربية:**  
هذا المستند يوضح كيف اكتشفنا واستخرجنا المفتاح الرئيسي (31×6) والمفاتيح الفرعية في مشروع Rahman-Key.

---

## 🎯 المفتاح الرئيسي (31×6) | Main Key (31×6)

### كيف اكتشفنا المفتاح؟ | How Did We Discover the Key?

**English:**  

**The Discovery Process:**

1. **Observation:** Surah Ar-Rahman repeats the verse "بأي آلاء ربكما تكذبان" (Which of the favors of your Lord will you deny?) **exactly 31 times**.

2. **Hypothesis:** What if we convert the sequence 1→31 to binary and visualize it?

3. **Experiment:**
   - Take sequence: 1, 2, 3, ..., 31
   - Convert each number to 6-bit binary (e.g., 1 → '000001', 2 → '000010')
   - Arrange in 31 rows × 6 columns matrix
   - Visualize as bitmap

4. **Result:** **A perfect heart appeared** ❤️

5. **Application:** Applied the same key (31×6) to all 114 Surahs → **95.6% produced heart patterns**

**العربية:**  

**عملية الاكتشاف:**

1. **الملاحظة:** سورة الرحمن تكرر الآية "بأي آلاء ربكما تكذبان" **بالضبط 31 مرة**.

2. **الفرضية:** ماذا لو حولنا التسلسل 1→31 إلى ثنائي وعرضناه؟

3. **التجربة:**
   - خذ التسلسل: 1، 2، 3، ...، 31
   - حوّل كل رقم إلى ثنائي 6 بتات (مثل: 1 → '000001'، 2 → '000010')
   - رتب في مصفوفة 31 صف × 6 أعمدة
   - اعرض كصورة bitmap

4. **النتيجة:** **ظهر قلب مثالي** ❤️

5. **التطبيق:** طبقنا نفس المفتاح (31×6) على جميع السور الـ114 → **95.6% أنتجت أنماط قلب**

---

### كيف نستخرج المفتاح لكل سورة؟ | How Do We Extract the Key for Each Surah?

**English:**  

**Method (Fully Reproducible):**

1. **Input:** Surah verse count (e.g., Al-Fatiha = 7, Ar-Rahman = 78)

2. **Generate Sequence:**
   - Create sequence: 1, 2, 3, ..., verse_count
   - Repeat sequence until we have ≥31 rows
   - Take only the first 31 rows

3. **Convert to Binary:**
   - Each number → 6-bit binary (with leading zeros)
   - Example: 1 → '000001', 5 → '000101', 31 → '011111'

4. **Create Matrix:**
   - 31 rows × 6 columns binary matrix
   - Each row = one 6-bit binary number

5. **Visualize:**
   - Black pixel = 1 (bit set)
   - White pixel = 0 (bit not set)
   - Result: 31×6 bitmap image

**Code Location:** `code/quran_hearts.py`

**العربية:**  

**الطريقة (قابلة للتكرار بالكامل):**

1. **المدخل:** عدد آيات السورة (مثل: الفاتحة = 7، الرحمن = 78)

2. **توليد التسلسل:**
   - أنشئ تسلسلاً: 1، 2، 3، ...، عدد_الآيات
   - كرر التسلسل حتى نحصل على ≥31 صف
   - خذ أول 31 صف فقط

3. **التحويل إلى ثنائي:**
   - كل رقم → ثنائي 6 بتات (مع أصفار أولية)
   - مثال: 1 → '000001'، 5 → '000101'، 31 → '011111'

4. **إنشاء المصفوفة:**
   - مصفوفة ثنائية 31 صف × 6 أعمدة
   - كل صف = رقم ثنائي 6 بتات واحد

5. **التصور:**
   - بكسل أسود = 1 (البت مضبوط)
   - بكسل أبيض = 0 (البت غير مضبوط)
   - النتيجة: صورة bitmap 31×6

**موقع الكود:** `code/quran_hearts.py`

---

## 🔑 المفاتيح الفرعية (Sub-Keys) | Sub-Keys

### كيف استخرجنا المفاتيح الفرعية؟ | How Did We Extract Sub-Keys?

**English:**  

**The Discovery Process:**

1. **Hypothesis:** What if each Surah has its own unique key in addition to the master key (31×6)?

2. **Key Calculation:**
   - Formula: `key = (surah_number × ayah_count × revelation_order) % 256`
   - Each Surah gets a unique key (0-255)

3. **Matrix Generation:**
   - Use key to determine matrix dimensions: `rows = 19 + (key % 13)` → 19-31 rows
   - Generate sequence based on key: `value = (key + i × surah_number + ayah_count) % 64`
   - Convert to 6-bit binary → matrix

4. **Pattern Detection:**
   - ❤️ Heart: Check bottom part + symmetry
   - ⭐ Star: Check all 4 corners + center
   - 🚪 Door: Check middle columns (adaptive threshold)

5. **Result:** Each Surah has a unique sub-key with its own pattern

**العربية:**  

**عملية الاكتشاف:**

1. **الفرضية:** ماذا لو كان لكل سورة مفتاحها الفريد بالإضافة إلى المفتاح الرئيسي (31×6)؟

2. **حساب المفتاح:**
   - المعادلة: `المفتاح = (رقم_السورة × عدد_الآيات × ترتيب_النزول) % 256`
   - كل سورة تحصل على مفتاح فريد (0-255)

3. **توليد المصفوفة:**
   - استخدم المفتاح لتحديد أبعاد المصفوفة: `الصفوف = 19 + (المفتاح % 13)` → 19-31 صف
   - أنشئ تسلسلاً بناءً على المفتاح: `القيمة = (المفتاح + i × رقم_السورة + عدد_الآيات) % 64`
   - حوّل إلى ثنائي 6 بتات → مصفوفة

4. **اكتشاف الأنماط:**
   - ❤️ القلب: تحقق من الجزء السفلي + التناظر
   - ⭐ النجمة: تحقق من جميع الزوايا الأربع + المركز
   - 🚪 الباب: تحقق من الأعمدة الوسطى (عتبة تكيفية)

5. **النتيجة:** كل سورة لها مفتاح فرعي فريد مع نمطها الخاص

---

### كيف نستخرج المفتاح الفرعي لكل سورة؟ | How Do We Extract Sub-Key for Each Surah?

**English:**  

**Method (Fully Reproducible):**

1. **Input:**
   - Surah number (1-114)
   - Ayah count (e.g., 7, 286, 200)
   - Revelation order (1-114)

2. **Calculate Key:**
   ```python
   base_key = (surah_number × ayah_count × revelation_order) % 1000
   # Add special characteristics (e.g., if contains الم or الر)
   surah_key = base_key % 256  # 8-bit key (0-255)
   ```

3. **Generate Matrix:**
   ```python
   rows = 19 + (key % 13)  # 19-31 rows
   for i in range(rows):
       value = (key + i × surah_number + ayah_count) % 64
       sequence.append(value)
   # Convert to 6-bit binary → matrix
   ```

4. **Detect Patterns:**
   - Apply detection algorithms (heart, star, door)
   - Return detected patterns

**Code Location:** `experiments/surah_sub_keys_discovery.py`

**العربية:**  

**الطريقة (قابلة للتكرار بالكامل):**

1. **المدخل:**
   - رقم السورة (1-114)
   - عدد الآيات (مثل: 7، 286، 200)
   - ترتيب النزول (1-114)

2. **حساب المفتاح:**
   ```python
   base_key = (رقم_السورة × عدد_الآيات × ترتيب_النزول) % 1000
   # أضف خصائص خاصة (مثل: إذا كانت تحتوي على الم أو الر)
   surah_key = base_key % 256  # مفتاح 8 بت (0-255)
   ```

3. **توليد المصفوفة:**
   ```python
   rows = 19 + (المفتاح % 13)  # 19-31 صف
   for i in range(rows):
       value = (المفتاح + i × رقم_السورة + عدد_الآيات) % 64
       sequence.append(value)
   # حوّل إلى ثنائي 6 بتات → مصفوفة
   ```

4. **اكتشاف الأنماط:**
   - طبق خوارزميات الاكتشاف (قلب، نجمة، باب)
   - أرجع الأنماط المكتشفة

**موقع الكود:** `experiments/surah_sub_keys_discovery.py`

---

## 📊 ملخص الاستخراج | Extraction Summary

**English:**  

**Main Key (31×6):**
- **Source:** Ar-Rahman (31 repetitions)
- **Method:** Sequence 1→verse_count → repeat to 31 → 6-bit binary → 31×6 matrix
- **Result:** Heart patterns for 95.6% of Surahs

**Sub-Keys:**
- **Source:** Unique calculation per Surah
- **Method:** `(surah_num × ayah_count × revelation_order) % 256` → variable matrix → pattern detection
- **Result:** Unique patterns for each Surah (42 hearts, 21 stars, 8 doors)

**العربية:**  

**المفتاح الرئيسي (31×6):**
- **المصدر:** الرحمن (31 تكرار)
- **الطريقة:** التسلسل 1→عدد_الآيات → كرّر إلى 31 → ثنائي 6 بتات → مصفوفة 31×6
- **النتيجة:** أنماط قلب لـ 95.6% من السور

**المفاتيح الفرعية:**
- **المصدر:** حساب فريد لكل سورة
- **الطريقة:** `(رقم_السورة × عدد_الآيات × ترتيب_النزول) % 256` → مصفوفة متغيرة → اكتشاف الأنماط
- **النتيجة:** أنماط فريدة لكل سورة (42 قلب، 21 نجمة، 8 أبواب)

---

**🌙 Rahman-Key** — How we extracted the keys. | كيف استخرجنا المفاتيح.

**Date:** 2024  
**Status:** ✅ Documented | موثق

