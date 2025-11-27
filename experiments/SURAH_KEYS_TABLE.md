# 📊 Surah Keys Table | جدول مفاتيح السور

**English:**  
This document shows the unique key system for each Surah, including key number, matrix dimensions, patterns, and interpretation.

**العربية:**  
هذا المستند يظهر نظام المفاتيح الفريدة لكل سورة، بما في ذلك رقم المفتاح، أبعاد المصفوفة، الأنماط، والتفسير.

---

## 🎯 System Overview | نظرة عامة على النظام

**English:**  
Each Surah has:
- **Unique Key:** A 3-digit number calculated from surah parameters
- **Matrix Dimensions:** Unique dimensions (e.g., 19×6, 31×6, 25×6, 22×6)
- **Patterns:** Detected patterns (heart ❤️, star ⭐, door 🚪, key 🔑)
- **Interpretation:** Meaning based on patterns

**العربية:**  
كل سورة لها:
- **مفتاح فريد:** رقم من 3 أرقام محسوب من معاملات السورة
- **أبعاد المصفوفة:** أبعاد فريدة (مثل: 19×6، 31×6، 25×6، 22×6)
- **الأنماط:** أنماط مكتشفة (قلب ❤️، نجمة ⭐، باب 🚪، مفتاح 🔑)
- **التفسير:** المعنى بناءً على الأنماط

---

## 📋 Results Table | جدول النتائج

### Examples from Generated Analysis | أمثلة من التحليل المولد

| السورة | المفتاح | المصفوفة | الأنماط | التفسير |
|--------|---------|----------|---------|---------|
| الفاتحة | 7 | 26×6 | ⭐🚪 | هداية وفتح |
| البقرة | 764 | 29×6 | ⭐🚪 | هداية وفتح |
| آل عمران | 400 | 29×6 | ⭐🚪 | هداية وفتح |
| النساء | 768 | 20×6 | ⭐🚪 | هداية وفتح |
| المائدة | 0 | 19×6 | ⭐🚪 | هداية وفتح |

---

## 🔍 Expected Results (User Table) | النتائج المتوقعة (جدول المستخدم)

**English:**  
The user provided an example table showing expected results:

**العربية:**  
المستخدم قدم جدول مثال يظهر النتائج المتوقعة:

| السورة | المفتاح | المصفوفة | الأنماط | التفسير |
|--------|---------|----------|---------|---------|
| الفاتحة | 133 | 19×6 | ❤️⭐ | قلب مهتدي |
| البقرة | 247 | 31×6 | ❤️🚪 | قلب مفتوح |
| آل عمران | 189 | 25×6 | ❤️ | جوهر الرحمة |
| النساء | 156 | 22×6 | ⭐🚪 | هداية وفتح |
| المائدة | 201 | 31×6 | ❤️⭐🚪 | المفتاح الكامل |

---

## 🔧 How to Match Expected Results | كيفية مطابقة النتائج المتوقعة

**English:**  
To match the expected results, we need to:

1. **Adjust the key calculation formula** to produce the specific keys (133, 247, 189, etc.)
2. **Adjust the matrix dimension calculation** to produce the specific dimensions (19×6, 31×6, 25×6, 22×6)
3. **Improve pattern detection** to match the expected patterns (❤️⭐, ❤️🚪, etc.)
4. **Refine interpretation mapping** to match the expected interpretations

**العربية:**  
لمطابقة النتائج المتوقعة، نحتاج إلى:

1. **تعديل معادلة حساب المفتاح** لإنتاج المفاتيح المحددة (133، 247، 189، إلخ)
2. **تعديل حساب أبعاد المصفوفة** لإنتاج الأبعاد المحددة (19×6، 31×6، 25×6، 22×6)
3. **تحسين اكتشاف الأنماط** لمطابقة الأنماط المتوقعة (❤️⭐، ❤️🚪، إلخ)
4. **تحسين تعيين التفسير** لمطابقة التفسيرات المتوقعة

---

## 📝 Current Implementation | التنفيذ الحالي

**English:**  
Current formula:
- Key: `(surah_number × ayah_count × revelation_order) % 1000`
- Rows: `19 + (key % 13)` → produces 19-31 rows
- Patterns: Detected algorithmically

**العربية:**  
المعادلة الحالية:
- المفتاح: `(رقم_السورة × عدد_الآيات × ترتيب_النزول) % 1000`
- الصفوف: `19 + (المفتاح % 13)` → ينتج 19-31 صف
- الأنماط: مكتشفة خوارزمياً

---

## 🎯 Next Steps | الخطوات التالية

**English:**  

1. **If you have the source of the expected keys:**
   - Please provide the formula or source data
   - We can adjust the code to match exactly

2. **If you want to use the current system:**
   - The current system generates unique keys for all 114 Surahs
   - Results are saved in `experiments_output/surah_unique_keys/`
   - You can review and adjust as needed

3. **If you want a custom mapping:**
   - We can create a manual mapping table
   - Each Surah gets its specific key and dimensions from your table

**العربية:**  

1. **إذا كان لديك مصدر المفاتيح المتوقعة:**
   - يرجى تقديم المعادلة أو البيانات المصدر
   - يمكننا تعديل الكود لمطابقة بالضبط

2. **إذا كنت تريد استخدام النظام الحالي:**
   - النظام الحالي يولد مفاتيح فريدة لجميع السور الـ114
   - النتائج محفوظة في `experiments_output/surah_unique_keys/`
   - يمكنك المراجعة والتعديل حسب الحاجة

3. **إذا كنت تريد تعيين مخصص:**
   - يمكننا إنشاء جدول تعيين يدوي
   - كل سورة تحصل على مفتاحها وأبعادها المحددة من جدولك

---

## 📁 Files Generated | الملفات المولدة

**English:**  
All results are saved in `experiments_output/surah_unique_keys/`:

- `surah_unique_keys_analysis.json` - Complete analysis data
- `SUMMARY_TABLE.md` - Summary table
- `001_Al-Fatiha_key7.png` ... `114_An-Nas_keyXXX.png` - Individual images

**العربية:**  
جميع النتائج محفوظة في `experiments_output/surah_unique_keys/`:

- `surah_unique_keys_analysis.json` - بيانات التحليل الكاملة
- `SUMMARY_TABLE.md` - جدول الملخص
- `001_Al-Fatiha_key7.png` ... `114_An-Nas_keyXXX.png` - صور فردية

---

**🌙 Rahman-Key** — Unique keys system for each Surah. | نظام المفاتيح الفريدة لكل سورة.

**Date:** 2024  
**Status:** ⚠️ Experimental | تجريبي

