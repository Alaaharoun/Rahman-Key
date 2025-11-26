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

**English:**
- ✅ Python code to generate bitmaps for any Surah
- ✅ Complete Surah data (verse count for all 114 Surahs)
- ✅ Pre-generated PNGs for all 114 Surahs (in `images/` directory)
- ✅ Simple usage guide
- ✅ Jupyter notebook ready to run online
- ✅ Pattern descriptions in `descriptions.json`

**العربية:**
- ✅ كود Python لتوليد الصور الثنائية لأي سورة
- ✅ بيانات كاملة للسور (عدد آيات جميع السور الـ 114)
- ✅ صور PNG مسبقة التوليد لجميع السور الـ 114 (في مجلد `images/`)
- ✅ دليل استخدام بسيط
- ✅ Jupyter notebook جاهز للتشغيل أونلاين
- ✅ أوصاف الأنماط في `descriptions.json`

---

## 🚀 Quick Start | التشغيل السريع (10 ثواني)

### Option 1: Run the Python Script | الخيار 1: تشغيل سكريبت Python
```bash
cd code
python quran_hearts.py
```

**English:** This will generate all 114 images automatically in the `images/` directory.  
**العربية:** سيتم توليد جميع الصور الـ 114 تلقائياً في مجلد `images/`.

### Option 2: Use Jupyter Notebook | الخيار 2: استخدام Jupyter Notebook
**English:** Open `notebook.ipynb` and click **Run All** — that's it!  
**العربية:** افتح `notebook.ipynb` واضغط **Run All** — هذا كل شيء!

---

## 📌 Important Note | ملاحظة مهمة

**English:**
This experiment does not imply that the Quran is "codes", but rather reveals — if present — an additional layer of numerical coherence in the text's structure, discoverable only when humanity reaches a certain technological stage.

**العربية:**
هذه التجربة لا تعني أن القرآن "رموز"، بل تكشف — إن وُجدت — طبقة إضافية من التماسك العددي في بنية النص، لا يمكن اكتشافها إلا عندما تصل البشرية إلى مرحلة تكنولوجية معينة.

---

## 🔬 Methodology | المنهجية

**English - For each Surah:**
1. Take the verse count (e.g., 7 for Al-Fatiha, 78 for Ar-Rahman)
2. Create a sequence: 1, 2, 3, ..., verse_count
3. Repeat the sequence until we have at least 31 rows
4. Take only the first 31 rows
5. Convert each number (1-31) to 6-bit binary format
6. Create a 31×6 binary matrix
7. Visualize as a bitmap image

**العربية - لكل سورة:**
1. خذ عدد الآيات (مثلاً: 7 للفاتحة، 78 للرحمن)
2. أنشئ تسلسلاً: 1، 2، 3، ...، عدد_الآيات
3. كرر التسلسل حتى نحصل على 31 صف على الأقل
4. خذ أول 31 صف فقط
5. حوّل كل رقم (1-31) إلى تنسيق ثنائي 6 بتات
6. أنشئ مصفوفة ثنائية 31×6
7. اعرضها كصورة bitmap

**Example | مثال:**
- Al-Fatiha has 7 verses → sequence: [1,2,3,4,5,6,7] | الفاتحة لها 7 آيات → التسلسل: [1,2,3,4,5,6,7]
- Repeat to get ≥31: [1,2,3,4,5,6,7,1,2,3,4,5,6,7,1,2,3,4,5,6,7,1,2,3,4,5,6,7,1,2,3] | كرر للحصول على ≥31
- Take first 31: [1,2,3,4,5,6,7,1,2,3,4,5,6,7,1,2,3,4,5,6,7,1,2,3,4,5,6,7,1,2,3] | خذ أول 31
- Convert to 6-bit binary → 31×6 matrix → bitmap | حوّل إلى ثنائي 6 بتات → مصفوفة 31×6 → bitmap

---

## 🎯 Try It Yourself | جرب بنفسك

**جرب بنفسك – الكود مفتوح 100% – لا يوجد أي تعديل يدوي على الصور**

**Try it yourself – 100% open code – No manual image editing**

**English:** All code is open source. No manual modifications to images. Everything is generated algorithmically.  
**العربية:** جميع الكود مفتوح المصدر. لا توجد تعديلات يدوية على الصور. كل شيء يتم توليده خوارزمياً.

---

## 📁 Project Structure | هيكل المشروع

```
Rahman-Key/
├── text/
│   └── README.md              (This file)
├── code/
│   └── quran_hearts.py        (Main code)
├── images/
│   └── (114 PNG images)       (Generated automatically - binary bitmaps)
├── Images/
│   └── (114 PNG images + visual representations)  (Visual representations of Surah meanings with hearts)
├── descriptions.json          (Pattern descriptions)
├── notebook.ipynb             (Jupyter notebook)
└── LICENSE                    (MIT License)
```

**English:** The `Images/` folder contains visual representations of Surah meanings combined with the heart patterns, providing a richer visual context.  
**العربية:** مجلد `Images/` يحتوي على تمثيلات بصرية لمعاني السور مدمجة مع أنماط القلوب، مما يوفر سياقاً بصرياً أغنى.

---

## 🖼️ Visual Comparison | المقارنة البصرية

*[Placeholder for comparison image between Ar-Rahman bitmap and ❤️ emoji]*

**English:** A high-resolution comparison image between Ar-Rahman Surah's bitmap and the ❤️ emoji will be added here.  
**العربية:** سيتم إضافة صورة مقارنة عالية الدقة بين bitmap سورة الرحمن وإيموجي ❤️ هنا.

---

## 📊 Results | النتائج

**English:**  
All 114 Surahs have been processed and their digital "hearts" are available in the `images/` directory.

Each image is named: `001_Al-Fatiha.png`, `002_Al-Baqarah.png`, ..., `114_An-Nas.png`

Pattern descriptions are stored in `descriptions.json`.

**العربية:**  
تمت معالجة جميع السور الـ 114 و"قلوبها" الرقمية متاحة في مجلد `images/`.

كل صورة مسماة: `001_Al-Fatiha.png`, `002_Al-Baqarah.png`, ..., `114_An-Nas.png`

أوصاف الأنماط مخزنة في `descriptions.json`.

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

**English:**  
This is a digital exploration project. The methodology is reproducible and open for anyone to verify and extend.

**العربية:**  
هذا مشروع استكشاف رقمي. المنهجية قابلة للتكرار ومفتوحة لأي شخص للتحقق والتوسع.

---

**🌙 Rahman-Key** — A window into numerical patterns, if they exist. | نافذة على الأنماط العددية، إن وُجدت.

