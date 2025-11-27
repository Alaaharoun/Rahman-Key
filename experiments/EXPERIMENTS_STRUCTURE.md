# 📁 Experiments Structure | هيكل التجارب

**English:**  
This document explains the organization of all experiments in the Rahman-Key project, matching the structure of the main Quran analysis.

**العربية:**  
هذا المستند يوضح تنظيم جميع التجارب في مشروع Rahman-Key، مطابقاً لهيكل تحليل القرآن الرئيسي.

---

## 🎯 Organization Principle | مبدأ التنظيم

**English:**  
All experiments follow the same structure as the main project:
- **Code** in `experiments/` directory
- **Output** in `experiments_output/` directory
- **Documentation** in `experiments/` directory (Markdown files)

**العربية:**  
جميع التجارب تتبع نفس هيكل المشروع الرئيسي:
- **الكود** في مجلد `experiments/`
- **المخرجات** في مجلد `experiments_output/`
- **التوثيق** في مجلد `experiments/` (ملفات Markdown)

---

## 📊 Complete Structure | الهيكل الكامل

```
Rahman-Key/
├── code/                              # Main code (core methodology)
│   ├── quran_hearts.py               # 31×6 master key
│   ├── disconnected_letters_keys.py  # Disconnected letters
│   ├── complete_quran_digital.py     # Complete Quran
│   └── overlay_patterns.py           # Overlay analysis
│
├── experiments/                       # Experimental code
│   ├── surah_specific_keys.py       # 19×6 key (experimental)
│   ├── names_of_allah.py             # 99 Names
│   ├── hearts_in_quran.py           # Heart verses
│   ├── ya_ayyuhal_ladhina_amanu.py  # Faith verses
│   ├── basmalah_114.py              # Basmalah
│   ├── run_all.py                    # Run all experiments
│   ├── advanced_experiments.ipynb    # Jupyter notebook
│   │
│   └── Documentation/
│       ├── README.md                 # Experiments overview
│       ├── KEY_EXTRACTION_ANALYSIS.md # What we extract
│       ├── KEYS_COMPARISON.md        # Key comparison
│       ├── SURAH_KEYS_README.md      # Surah keys guide
│       ├── SURAH_KEYS_ANALYSIS.md    # 19×6 analysis
│       └── PERSONAL_ANALYSIS.md      # Personal insights
│
├── images/                            # Main outputs (31×6)
│   └── 001_Al-Fatiha.png ... 114_An-Nas.png
│
├── experiments_output/                # Experimental outputs
│   ├── surah_keys_19x6/             # 19×6 key outputs
│   │   ├── 001_Al-Fatiha_19x6.png ... 114_An-Nas_19x6.png
│   │   ├── comparison/               # 31×6 vs 19×6
│   │   └── surah_keys_19x6_analysis.json
│   │
│   ├── names_of_allah/               # 99 Names output
│   │   └── 099_Names_Of_Allah.png
│   │
│   ├── hearts_quran/                 # Heart verses output
│   │   ├── Hearts_VerseOrder.png
│   │   └── Hearts_AbsoluteNumbers.png
│   │
│   ├── ya_ayyuhal_ladhina_amanu/    # Faith verses output
│   │   └── Believers_Pattern.png
│   │
│   ├── basmalah/                     # Basmalah output
│   │   └── Basmalah_114.png
│   │
│   └── overlay/                      # Overlay analysis
│       ├── all_surahs_overlay.png
│       ├── or_kaaba.png
│       ├── avg_heart.png
│       └── max_eye.png
│
├── disconnected_letters_keys/        # Disconnected letters
│   ├── images/                       # 14 images
│   ├── combined_patterns/            # Combined patterns
│   └── analysis.json
│
└── complete_quran/                   # Complete Quran
    ├── quran_complete_digital.png
    ├── parts/                        # 14 parts
    └── metadata.json
```

---

## 🔑 What We Extract from Each Key | ما نستخرجه من كل مفتاح

### 1. 31×6 (Master Key) | المفتاح الرئيسي

**Location:** `code/quran_hearts.py` → `images/`

**What We Extract:**
- ✅ Heart patterns (95.6% of Surahs)
- ✅ Symmetry scores
- ✅ Pattern grades (0-3)
- ✅ Internal symbols (algorithmic)
- ✅ Structural clusters

**Output:**
- 114 PNG images
- `descriptions.json`

---

### 2. 19×6 (Surah Key) | مفتاح السورة

**Location:** `experiments/surah_specific_keys.py` → `experiments_output/surah_keys_19x6/`

**What We Extract:**
- ⚠️ Surah-specific patterns
- ⚠️ Pattern diversity
- ⚠️ Mathematical match (114 pixels)
- ⚠️ Seed-based uniqueness

**Output:**
- 114 PNG images (19×6)
- Comparison images (31×6 vs 19×6)
- `surah_keys_19x6_analysis.json`

**Status:** ⚠️ Experimental

---

### 3. Disconnected Letters Key | مفتاح الحروف المقطعة

**Location:** `code/disconnected_letters_keys.py` → `disconnected_letters_keys/`

**What We Extract:**
- ✅ 100% heart patterns
- ✅ Letter-specific characteristics
- ✅ Group patterns
- ✅ Architectural structure

**Output:**
- 14 PNG images
- Combined patterns (31×84)
- `analysis.json`

---

### 4. 99 Names of Allah | أسماء الله الحسنى

**Location:** `experiments/names_of_allah.py` → `experiments_output/names_of_allah/`

**What We Extract:**
- ✅ Perfect heart pattern
- ✅ Central symbol (Alif)
- ✅ Rotational patterns ("هو")

**Output:**
- 1 PNG image
- Pattern analysis

---

### 5. Heart Verses | آيات القلب

**Location:** `experiments/hearts_in_quran.py` → `experiments_output/hearts_quran/`

**What We Extract:**
- ✅ Heart + open lock pattern
- ✅ 57 verses structure
- ✅ Thematic connection

**Output:**
- 2 PNG images (verse order + absolute numbers)

---

### 6. Faith Verses | آيات الإيمان

**Location:** `experiments/ya_ayyuhal_ladhina_amanu.py` → `experiments_output/ya_ayyuhal_ladhina_amanu/`

**What We Extract:**
- ✅ Heart + raised hands pattern
- ✅ 88 verses structure
- ✅ Guidance pattern

**Output:**
- 1 PNG image

---

### 7. Basmalah | البسملة

**Location:** `experiments/basmalah_114.py` → `experiments_output/basmalah/`

**What We Extract:**
- ✅ Small heart pattern
- ✅ 114 repetitions structure

**Output:**
- 1 PNG image

---

### 8. Overlay Analysis | تحليل الدمج

**Location:** `code/overlay_patterns.py` → `experiments_output/overlay/`

**What We Extract:**
- ✅ Kaaba pattern (OR method)
- ✅ Heart + Light (Average method)
- ✅ Eye pattern (Max method)

**Output:**
- 3 PNG images (different methods)
- Overlay metadata

---

## 📈 Extraction Summary Table | جدول ملخص الاستخراج

| Key | Code Location | Output Location | What We Extract | Status |
|-----|---------------|-----------------|-----------------|--------|
| **31×6** | `code/quran_hearts.py` | `images/` | Heart patterns, symmetry, grades | ✅ Core |
| **19×6** | `experiments/surah_specific_keys.py` | `experiments_output/surah_keys_19x6/` | Surah-specific patterns | ⚠️ Experimental |
| **Disconnected Letters** | `code/disconnected_letters_keys.py` | `disconnected_letters_keys/` | 100% hearts, letter structure | ✅ Core |
| **99 Names** | `experiments/names_of_allah.py` | `experiments_output/names_of_allah/` | Perfect heart, symbols | ✅ Core |
| **Heart Verses** | `experiments/hearts_in_quran.py` | `experiments_output/hearts_quran/` | Heart + lock pattern | ✅ Core |
| **Faith Verses** | `experiments/ya_ayyuhal_ladhina_amanu.py` | `experiments_output/ya_ayyuhal_ladhina_amanu/` | Heart + hands pattern | ✅ Core |
| **Basmalah** | `experiments/basmalah_114.py` | `experiments_output/basmalah/` | Small heart pattern | ✅ Core |
| **Overlay** | `code/overlay_patterns.py` | `experiments_output/overlay/` | Kaaba, Heart, Eye patterns | ✅ Core |

---

## 🎯 Key Insights | الرؤى الرئيسية

**English:**  

1. **Each key extracts different information:**
   - Master key (31×6) = Overall structure
   - Surah key (19×6) = Individual characteristics
   - Special keys = Thematic patterns

2. **Organization matches main project:**
   - Code in `experiments/`
   - Output in `experiments_output/`
   - Documentation in `experiments/`

3. **All keys are reproducible:**
   - Same input = same output
   - Open source code
   - Verifiable results

**العربية:**  

1. **كل مفتاح يستخرج معلومات مختلفة:**
   - المفتاح الرئيسي (31×6) = البنية العامة
   - مفتاح السورة (19×6) = الخصائص الفردية
   - المفاتيح الخاصة = الأنماط الموضوعية

2. **التنظيم يطابق المشروع الرئيسي:**
   - الكود في `experiments/`
   - المخرجات في `experiments_output/`
   - التوثيق في `experiments/`

3. **جميع المفاتيح قابلة للتكرار:**
   - نفس المدخل = نفس المخرج
   - كود مفتوح المصدر
   - نتائج قابلة للتحقق

---

**🌙 Rahman-Key** — Organized structure for all keys and experiments. | هيكل منظم لجميع المفاتيح والتجارب.

**Date:** 2024  
**Status:** ✅ Documented | موثق

