# 🌙 قلوب القرآن الرقمية – مفتاح سورة الرحمن
# Digital Hearts of the Quran – The Rahman Key

📌 **لا توجد صورة واحدة تم تعديلها يدويًّا. كلها ناتجة عن التنفيذ الآلي للكود نفسه.**  
📌 **No single image has been manually edited. All are the result of automatic code execution.**

---

## 📖 About | حول المشروع

**English:**
A simple digital experiment to convert Quranic verses into binary images (bitmaps) using a fixed methodology: **31×6 bits** — and visually inspect them for symmetrical or symbolic patterns.

This project does not aim to "prove" anything, but to empower the experimenter to see what can be seen — without prior interpretation, using reproducible tools.

**العربية:**
تجربة رقمية بسيطة لتحويل آيات القرآن الكريم إلى صور ثنائية (bitmaps) باستخدام منهجية ثابتة: **31×6 بت** — وفحصها بصريًا للبحث عن أنماط متناظرة أو رمزية.

هذا المشروع لا يهدف إلى "إثبات" أي شيء، بل إلى تمكين المجرب من رؤية ما يمكن رؤيته — دون تفسير مسبق، باستخدام أدوات قابلة للتكرار.

---

## ✅ What's Included | ما الموجود

- ✅ Python code to generate bitmaps for any Surah
- ✅ Complete Surah data (verse count for all 114 Surahs)
- ✅ Pre-generated PNGs for all 114 Surahs (in `images/` directory)
- ✅ Simple usage guide
- ✅ Jupyter notebook ready to run online
- ✅ Pattern descriptions in `descriptions.json`

---

## 🚀 Quick Start | التشغيل السريع (10 ثواني)

### Option 1: Run the Python Script
```bash
cd code
python quran_hearts.py
```

This will generate all 114 images automatically in the `images/` directory.

### Option 2: Use Jupyter Notebook
Open `notebook.ipynb` and click **Run All** — that's it!

---

## 📌 Important Note | ملاحظة مهمة

**English:**
This experiment does not imply that the Quran is "codes", but rather reveals — if present — an additional layer of numerical coherence in the text's structure, discoverable only when humanity reaches a certain technological stage.

**العربية:**
هذه التجربة لا تعني أن القرآن "رموز"، بل تكشف — إن وُجدت — طبقة إضافية من التماسك العددي في بنية النص، لا يمكن اكتشافها إلا عندما تصل البشرية إلى مرحلة تكنولوجية معينة.

---

## 🔬 Methodology | المنهجية

For each Surah:
1. Take the verse count (e.g., 7 for Al-Fatiha, 78 for Ar-Rahman)
2. Create a sequence: 1, 2, 3, ..., verse_count
3. Repeat the sequence until we have at least 31 rows
4. Take only the first 31 rows
5. Convert each number (1-31) to 6-bit binary format
6. Create a 31×6 binary matrix
7. Visualize as a bitmap image

**Example:**
- Al-Fatiha has 7 verses → sequence: [1,2,3,4,5,6,7]
- Repeat to get ≥31: [1,2,3,4,5,6,7,1,2,3,4,5,6,7,1,2,3,4,5,6,7,1,2,3,4,5,6,7,1,2,3]
- Take first 31: [1,2,3,4,5,6,7,1,2,3,4,5,6,7,1,2,3,4,5,6,7,1,2,3,4,5,6,7,1,2,3]
- Convert to 6-bit binary → 31×6 matrix → bitmap

---

## 🎯 Try It Yourself | جرب بنفسك

**جرب بنفسك – الكود مفتوح 100% – لا يوجد أي تعديل يدوي على الصور**

**Try it yourself – 100% open code – No manual image editing**

All code is open source. No manual modifications to images. Everything is generated algorithmically.

---

## 📁 Project Structure | هيكل المشروع

```
Rahman-Key/
├── text/
│   └── README.md              (This file)
├── code/
│   └── quran_hearts.py        (Main code)
├── images/
│   └── (114 PNG images)       (Generated automatically)
├── descriptions.json          (Pattern descriptions)
├── notebook.ipynb             (Jupyter notebook)
└── LICENSE                    (MIT License)
```

---

## 🖼️ Visual Comparison | المقارنة البصرية

*[Placeholder for comparison image between Ar-Rahman bitmap and ❤️ emoji]*

**Note:** A high-resolution comparison image between Ar-Rahman Surah's bitmap and the ❤️ emoji will be added here.

---

## 📊 Results | النتائج

All 114 Surahs have been processed and their digital "hearts" are available in the `images/` directory.

Each image is named: `001_Al-Fatiha.png`, `002_Al-Baqarah.png`, ..., `114_An-Nas.png`

Pattern descriptions are stored in `descriptions.json`.

---

## 🔧 Requirements | المتطلبات

```bash
pip install matplotlib numpy
```

---

## 📝 License | الترخيص

MIT License - See `LICENSE` file for details.

---

## 🙏 Acknowledgments | شكر وتقدير

This is a digital exploration project. The methodology is reproducible and open for anyone to verify and extend.

---

**🌙 Rahman-Key** — A window into numerical patterns, if they exist.

