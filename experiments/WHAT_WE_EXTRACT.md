# 🔍 What We Extract from Each Key | ما نستخرجه من كل مفتاح

**English:**  
This document provides a clear summary of what we extract from each key in the Rahman-Key project.

**العربية:**  
هذا المستند يوفر ملخصاً واضحاً لما نستخرجه من كل مفتاح في مشروع Rahman-Key.

---

## 📊 Quick Reference Table | جدول مرجعي سريع

| Key | Dimensions | What We Extract | Output Location | Status |
|-----|------------|-----------------|-----------------|--------|
| **31×6 (Master)** | 31×6 | Heart patterns (95.6%), symmetry, grades, clusters | `images/` | ✅ Core |
| **19×6 (Surah)** | 19×6 | Surah-specific patterns, diversity | `experiments_output/surah_keys_19x6/` | ⚠️ Experimental |
| **Disconnected Letters** | 31×6 | 100% hearts, letter structure, groups | `disconnected_letters_keys/` | ✅ Core |
| **99 Names** | 31×6 | Perfect heart, central symbol | `experiments_output/names_of_allah/` | ✅ Core |
| **Heart Verses** | 31×6 | Heart + open lock pattern | `experiments_output/hearts_quran/` | ✅ Core |
| **Faith Verses** | 31×6 | Heart + raised hands pattern | `experiments_output/ya_ayyuhal_ladhina_amanu/` | ✅ Core |
| **Basmalah** | 31×6 | Small heart pattern | `experiments_output/basmalah/` | ✅ Core |
| **Overlay** | 31×6 | Kaaba, Heart, Eye patterns | `experiments_output/overlay/` | ✅ Core |

---

## 🔑 Detailed Extraction | الاستخراج التفصيلي

### 1. 31×6 Master Key | المفتاح الرئيسي 31×6

**What We Extract:**

**Algorithmic:**
- ✅ Heart pattern detection (109 of 114 Surahs = 95.6%)
- ✅ Symmetry scores (vertical, horizontal, overall)
- ✅ Pattern grades (0-3 classification)
- ✅ Internal symbols (algorithmically detected: dot, line)
- ✅ Structural clusters (e.g., 5 Surahs with 11 verses = identical structure)

**Output:**
- 114 PNG images (one per Surah)
- `descriptions.json` (algorithmic data only)
- Classification reports

**Location:**
- Code: `code/quran_hearts.py`
- Output: `images/`

---

### 2. 19×6 Surah Key | مفتاح السورة 19×6

**What We Extract:**

**Algorithmic:**
- ⚠️ Pattern type (detected by algorithm)
- ⚠️ Black/white pixel counts
- ⚠️ Matrix shape (19×6)
- ⚠️ Seed value (unique to each Surah)
- ⚠️ Pattern diversity (compared to 31×6)

**Visual (Separate):**
- ⚠️ Pattern descriptions (subjective)
- ⚠️ Symbol recognition (not verified algorithmically)

**Output:**
- 114 PNG images (19×6 pattern for each Surah)
- Comparison images (31×6 vs 19×6)
- `surah_keys_19x6_analysis.json`

**Location:**
- Code: `experiments/surah_specific_keys.py`
- Output: `experiments_output/surah_keys_19x6/`

**Status:** ⚠️ Experimental

---

### 3. Disconnected Letters Key | مفتاح الحروف المقطعة

**What We Extract:**

**Algorithmic:**
- ✅ 100% heart patterns (all 14 letter groups)
- ✅ Letter-specific characteristics
- ✅ Group patterns (same letters = same pattern)
- ✅ Highest symmetry: الر (89.2%)
- ✅ Architectural structure (when combined)

**Output:**
- 14 PNG images (one per letter group)
- Combined patterns (31×84 matrix)
- `analysis.json`

**Location:**
- Code: `code/disconnected_letters_keys.py`
- Output: `disconnected_letters_keys/`

---

### 4. 99 Names of Allah | أسماء الله الحسنى

**What We Extract:**

**Algorithmic:**
- ✅ Perfect heart pattern
- ✅ Symmetry score
- ✅ Central symbol detection (Alif)

**Visual (Separate):**
- ⚠️ "Crown" shape (visual interpretation)
- ⚠️ "هو" when rotated (visual interpretation)

**Output:**
- 1 PNG image
- Pattern analysis

**Location:**
- Code: `experiments/names_of_allah.py`
- Output: `experiments_output/names_of_allah/`

---

### 5. Heart Verses | آيات القلب

**What We Extract:**

**Algorithmic:**
- ✅ Heart pattern
- ✅ Pattern structure (57 verses)
- ✅ Thematic connection (verses about "heart")

**Visual (Separate):**
- ⚠️ "Open lock" (visual interpretation)
- ⚠️ "Key" (visual interpretation)

**Output:**
- 2 PNG images (verse order + absolute numbers)

**Location:**
- Code: `experiments/hearts_in_quran.py`
- Output: `experiments_output/hearts_quran/`

---

### 6. Faith Verses | آيات الإيمان

**What We Extract:**

**Algorithmic:**
- ✅ Heart pattern
- ✅ Pattern structure (88 verses)
- ✅ Thematic connection (verses addressing believers)

**Visual (Separate):**
- ⚠️ "Raised hands" (visual interpretation)
- ⚠️ "Halo" (visual interpretation)

**Output:**
- 1 PNG image

**Location:**
- Code: `experiments/ya_ayyuhal_ladhina_amanu.py`
- Output: `experiments_output/ya_ayyuhal_ladhina_amanu/`

---

### 7. Basmalah | البسملة

**What We Extract:**

**Algorithmic:**
- ✅ Small heart pattern
- ✅ Pattern structure (114 repetitions)

**Output:**
- 1 PNG image

**Location:**
- Code: `experiments/basmalah_114.py`
- Output: `experiments_output/basmalah/`

---

### 8. Overlay Analysis | تحليل الدمج

**What We Extract:**

**Algorithmic:**
- ✅ OR overlay pattern (Kaaba-like structure)
- ✅ Average overlay pattern (Heart + Light)
- ✅ Max overlay pattern (Eye-like structure)
- ✅ Pixel density analysis
- ✅ Statistical measures

**Output:**
- 3 PNG images (different overlay methods)
- Overlay metadata

**Location:**
- Code: `code/overlay_patterns.py`
- Output: `experiments_output/overlay/`

---

## 📈 Extraction Categories | فئات الاستخراج

### ✅ Algorithmic Extractions | الاستخراجات الخوارزمية

**English:**  
These are **measured by code** and **100% reproducible**:

**العربية:**  
هذه **مقاسة بالكود** و**100% قابلة للتكرار**:

- Pattern type (heart, star, etc.)
- Symmetry scores (percentages)
- Pattern grades (0-3)
- Internal symbols (algorithmically detected)
- Pixel counts (black, white)
- Matrix dimensions
- Structural clusters
- Statistical measures

---

### ⚠️ Visual Interpretations | التأويلات البصرية

**English:**  
These are **subjective observations** and **not part of algorithmic methodology**:

**العربية:**  
هذه **ملاحظات ذاتية** و**ليست جزءاً من المنهجية الخوارزمية**:

- "Resembles a key"
- "Looks like a crescent"
- "Contains the word HU"
- "Shows prostrating human"
- "Appears as Kaaba structure"

**Note:** These should be stored in `VISUAL_NOTES.md`, not in `descriptions.json`.

---

## 🎯 Summary | الملخص

**English:**  

**From 31×6 (Master Key):**
- Overall structure of all 114 Surahs
- Heart patterns, symmetry, grades
- Structural clusters

**From 19×6 (Surah Key):**
- Surah-specific characteristics
- Pattern diversity
- Individual Surah essence

**From Special Keys:**
- Thematic patterns (heart verses, faith verses)
- Special structures (99 Names, Basmalah)
- Combined patterns (overlay analysis)

**All extractions are:**
- ✅ Reproducible
- ✅ Measurable
- ✅ Verifiable
- ✅ Algorithmic (when marked as such)

**العربية:**  

**من 31×6 (المفتاح الرئيسي):**
- البنية العامة لجميع السور الـ114
- أنماط القلب، التناظر، الدرجات
- المجموعات البنيوية

**من 19×6 (مفتاح السورة):**
- خصائص خاصة بكل سورة
- تنوع الأنماط
- جوهر السورة الفردي

**من المفاتيح الخاصة:**
- أنماط موضوعية (آيات القلب، آيات الإيمان)
- هياكل خاصة (99 اسم، البسملة)
- أنماط مجمعة (تحليل الدمج)

**جميع الاستخراجات:**
- ✅ قابلة للتكرار
- ✅ قابلة للقياس
- ✅ قابلة للتحقق
- ✅ خوارزمية (عند وسمها كذالك)

---

**🌙 Rahman-Key** — Clear extraction from each key. | استخراج واضح من كل مفتاح.

**Date:** 2024  
**Status:** ✅ Documented | موثق

