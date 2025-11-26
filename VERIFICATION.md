# 🔍 Verification Guide | دليل التحقق

This document provides evidence that all images are generated automatically without manual editing.

---

## 📸 Terminal Execution Screenshot

*[Placeholder: Add a screenshot of running `python code/quran_hearts.py` in terminal]*

**How to capture:**
1. Open terminal in project root
2. Run: `cd code && python quran_hearts.py`
3. Take screenshot showing the generation process

---

## 🖼️ Visual Comparison: Ar-Rahman vs ❤️ Emoji

*[Placeholder: Add side-by-side comparison image]*

**Image 1:** `055_Ar-Rahman.png` (generated bitmap)  
**Image 2:** ❤️ Emoji

This comparison demonstrates that the heart-like pattern in Ar-Rahman Surah is not a visual illusion but a reproducible algorithmic result.

---

## 🚀 Run Online (Google Colab)

You can run this experiment directly in your browser using Google Colab:

1. Upload `notebook.ipynb` to Google Colab
2. Upload the `code/` directory
3. Click **Run All**

**Or use this direct link (if you create a Colab notebook):**
*[Add Colab link here if available]*

---

## ✅ Verification Checklist

- [x] All 114 images generated automatically
- [x] No manual image editing
- [x] Reproducible results (same input = same output)
- [x] Code is open source and verifiable
- [x] Methodology is documented

---

## 🔬 How to Verify Yourself

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Alaaharoun/Rahman-Key.git
   cd Rahman-Key
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Delete existing images (optional, to test from scratch):**
   ```bash
   rm images/*.png
   rm descriptions.json
   ```

4. **Run the code:**
   ```bash
   cd code
   python quran_hearts.py
   ```

5. **Verify:**
   - Check that 114 PNG files are created in `images/`
   - Check that `descriptions.json` is created
   - Compare your results with the repository images

---

## 📝 Notes

- All images are generated using the exact same algorithm
- The methodology is fixed: 31×6 bits for all Surahs
- No cherry-picking or manual selection of results
- Every Surah follows the same transformation process

---

**🌙 Rahman-Key** — Transparent, reproducible, verifiable.

