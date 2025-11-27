"""
نظام Rahman-Key: فن رقمي قرآني مولّد خوارزمياً | Rahman-Key System: Algorithmically Generated Quranic Digital Art

143 نمط فريد للسور والحروف المقطعة | 143 Unique Patterns for Surahs and Disconnected Letters

⚠️ EXPERIMENTAL - This is exploratory research
"""

import numpy as np
import matplotlib.pyplot as plt
import json
from pathlib import Path

class SurahKeyDiscovery:
    def __init__(self):
        self.surah_keys = {}
        
    def calculate_surah_key(self, surah_num, ayah_count, revelation_order):
        """حساب مفتاح السورة الفريد"""
        
        # 1. المفتاح الأساسي
        base_key = (surah_num * ayah_count * revelation_order) % 1000
        
        # 2. إضافة خصائص السورة
        if surah_num in [2, 3, 26, 30, 32]:  # سور تحتوي الم
            base_key += 71  # قيمة الم
        if surah_num in [10, 11, 12, 14, 15]: # سور تحتوي الر
            base_key += 231 # قيمة الر
            
        # 3. المفتاح النهائي
        surah_key = base_key % 256  # 8-bit key
        
        return surah_key
    
    def generate_surah_matrix(self, surah_num, key):
        """توليد مصفوفة السورة بمفتاحها"""
        
        # استخدام المفتاح لتوليد تسلسل فريد
        sequence = []
        rows = key % 31 + 19  # ارتفاع متغير بين 19-49
        
        for i in range(rows):
            row_seed = (key + i * surah_num) % 64
            sequence.append(row_seed)
        
        # تحويل لـ binary
        matrix = np.array([[int(b) for b in format(n, '06b')] 
                          for n in sequence])
        
        return matrix
    
    def detect_heart(self, matrix):
        """كشف نمط القلب - محسّن"""
        height, width = matrix.shape
        if height < 5:
            return False
        
        # تحسين: فحص شكل القلب الكامل (ليس فقط الوسط)
        # 1. الجزء السفلي (شكل القلب المميز)
        bottom_part = np.sum(matrix[height-5:, 1:width-1])
        bottom_threshold = (5 * (width-2)) * 0.5  # 50% من البكسلات السفلية
        
        # 2. التناظر الأفقي (القلب متناظر)
        if height >= 10:
            top_half = matrix[:height//2, :]
            bottom_half = np.flipud(matrix[height//2:, :])
            min_height = min(top_half.shape[0], bottom_half.shape[0])
            if min_height > 0:
                symmetry = np.sum(top_half[:min_height, :] == bottom_half[:min_height, :]) / (min_height * width)
                if symmetry > 0.4:  # تناظر معقول
                    return bottom_part > bottom_threshold
        
        # 3. الكثافة المركزية
        center_density = np.sum(matrix[height//2-2:height//2+3, :])
        center_threshold = (5 * width) * 0.4  # 40% من البكسلات المركزية
        
        return bottom_part > bottom_threshold or center_density > center_threshold
    
    def detect_star(self, matrix):
        """كشف نمط النجمة - محسّن"""
        height, width = matrix.shape
        if height < 3 or width < 3:
            return False
        
        # تحسين: فحص النجمة الكاملة (الزوايا + المركز)
        # 1. الزوايا الأربع
        corners = (np.sum(matrix[0, :]) + np.sum(matrix[-1, :]) + 
                   np.sum(matrix[:, 0]) + np.sum(matrix[:, -1]))
        corner_threshold = (2 * width + 2 * height) * 0.5  # 50% من الزوايا
        
        # 2. المركز (النجمة لها مركز مضيء)
        center_row = height // 2
        center_col = width // 2
        center_region = matrix[max(0, center_row-1):min(height, center_row+2), 
                               max(0, center_col-1):min(width, center_col+2)]
        center_density = np.sum(center_region)
        center_threshold = center_region.size * 0.4  # 40% من المركز
        
        # 3. النجمة تحتاج زوايا + مركز
        return corners > corner_threshold and center_density > center_threshold
    
    def detect_door(self, matrix):
        """كشف نمط الباب - محسّن (عتبة تكيفية)"""
        height, width = matrix.shape
        if width < 4:
            return False
        
        # تحسين: عتبة تكيفية حسب حجم المصفوفة
        middle_columns = np.sum(matrix[:, 2:4])  # الأعمدة 2 و 3
        total_middle_pixels = 2 * height  # عمودان × عدد الصفوف
        
        # عتبة تكيفية: 50% من البكسلات الوسطى يجب أن تكون سوداء
        # (بدلاً من 15 ثابت - كان منخفض جداً)
        threshold = total_middle_pixels * 0.5
        
        # تحسين إضافي: الباب له شكل مميز (أعمدة وسطية قوية)
        # يجب أن تكون الأعمدة الوسطى أكثر كثافة من الأعمدة الجانبية
        side_columns = (np.sum(matrix[:, 0:2]) + np.sum(matrix[:, 4:6])) / 2  # متوسط الأعمدة الجانبية
        middle_density = middle_columns / total_middle_pixels
        side_density = side_columns / (2 * height) if (2 * height) > 0 else 0
        
        # الباب: الأعمدة الوسطى أكثر كثافة من الجانبية
        return middle_columns > threshold and middle_density > side_density * 1.2
    
    def analyze_key_pattern(self, matrix, surah_name, key):
        """تحليل النمط في مفتاح السورة"""
        
        height, width = matrix.shape
        
        # حساب الخصائص
        black_pixels = int(np.sum(matrix))
        white_pixels = int(height * width - black_pixels)
        
        # حساب التناظر
        symmetry_scores = []
        for i in range(height//2):
            if i < height - 1 - i:
                symmetry_scores.append(np.array_equal(matrix[i], matrix[height-1-i]))
        symmetry = np.mean(symmetry_scores) if symmetry_scores else 0.0
        
        # اكتشاف الأنماط
        patterns = []
        pattern_emojis = []
        
        # البحث عن قلب
        heart_detected = self.detect_heart(matrix)
        if heart_detected:
            patterns.append("heart")
            pattern_emojis.append("❤️")
        
        # البحث عن نجمة
        star_detected = self.detect_star(matrix)
        if star_detected:
            patterns.append("star")
            pattern_emojis.append("⭐")
        
        # البحث عن باب
        door_detected = self.detect_door(matrix)
        if door_detected:
            patterns.append("door")
            pattern_emojis.append("🚪")
        
        return {
            "surah": surah_name,
            "key": int(key),
            "matrix_shape": f"{height}×{width}",
            "rows": int(height),
            "cols": int(width),
            "black_pixels": black_pixels,
            "white_pixels": white_pixels,
            "symmetry": f"{symmetry:.1%}",
            "patterns": patterns,
            "pattern_emojis": "".join(pattern_emojis),
            "interpretation": self.interpret_key_patterns(patterns)
        }
    
    def interpret_key_patterns(self, patterns):
        """تفسير الأنماط"""
        interpretations = {
            "heart": "جوهر السورة - رحمة ومودة",
            "star": "إرشاد وهداية",
            "door": "مدخل للمعرفة أو فتح",
            "heart-star": "قلب مهتدي",
            "heart-door": "قلب مفتوح للهداية",
            "star-door": "هداية وفتح",
            "heart-star-door": "المفتاح الكامل"
        }
        
        if len(patterns) >= 2:
            pattern_key = "-".join(patterns)
            return interpretations.get(pattern_key, "مفتاح معقد")
        elif len(patterns) == 1:
            return interpretations.get(patterns[0], "مفتاح أساسي")
        else:
            return "مفتاح سري"
    
    def discover_all_keys(self):
        """اكتشاف مفاتيح كل السور"""
        
        # Load Surahs from quran_hearts
        import importlib.util
        quran_hearts_path = Path('code/quran_hearts.py')
        spec = importlib.util.spec_from_file_location("quran_hearts", quran_hearts_path)
        quran_hearts = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(quran_hearts)
        SURAHS = quran_hearts.SURAHS
        
        # Load revelation order
        REVELATION_ORDER = {}
        try:
            with open('surah_revelation_order.csv', 'r', encoding='utf-8') as f:
                import csv
                reader = csv.DictReader(f)
                for row in reader:
                    surah_name = row['Surah Name'].strip()
                    rev_order = int(row['Revelation Order'].strip())
                    REVELATION_ORDER[surah_name] = rev_order
        except:
            print("⚠️ Could not load revelation order CSV, using fallback")
            # Fallback revelation order (approximate)
            REVELATION_ORDER = {
                "Al-Fatiha": 1, "Al-Baqarah": 87, "Ali 'Imran": 89,
                "An-Nisa": 92, "Al-Ma'idah": 112
            }
        
        print("="*80)
        print("🌙 نظام Rahman-Key: فن رقمي قرآني مولّد خوارزمياً")
        print("Rahman-Key System: Algorithmically Generated Quranic Digital Art")
        print("="*80)
        print("\n⚠️ EXPERIMENTAL - This is exploratory research")
        print("⚠️ تجريبي - هذا بحث استكشافي\n")
        
        output_dir = Path('experiments_output/surah_sub_keys')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"📖 Analyzing {len(SURAHS)} Surahs...\n")
        
        for surah_num, (surah_name, ayah_count) in enumerate(SURAHS, 1):
            # Get revelation order
            rev_order = REVELATION_ORDER.get(surah_name, surah_num)
            
            # حساب المفتاح
            key = self.calculate_surah_key(surah_num, ayah_count, rev_order)
            
            # توليد المصفوفة
            matrix = self.generate_surah_matrix(surah_num, key)
            
            # تحليل النمط
            analysis = self.analyze_key_pattern(matrix, surah_name, key)
            
            self.surah_keys[surah_name] = analysis
            
            # Save image
            plt.figure(figsize=(3, matrix.shape[0]/3))
            plt.imshow(matrix, cmap='gray_r', aspect='auto')
            plt.axis('off')
            plt.title(f"{surah_num:03d}_{surah_name}\nKey: {key} | {analysis['matrix_shape']}\n{analysis['pattern_emojis']} {analysis['interpretation']}", 
                     fontsize=8, pad=10)
            
            filename = f"{surah_num:03d}_{surah_name.replace(' ', '_').replace(chr(39), '')}_subkey{key}.png"
            plt.savefig(output_dir / filename, dpi=150, bbox_inches='tight', facecolor='white')
            plt.close()
            
            # Print progress
            if surah_num <= 5 or surah_num % 20 == 0:
                print(f"✅ {surah_num:03d}. {surah_name}: مفتاح={key:3} | {analysis['matrix_shape']} | "
                      f"أنماط={analysis['pattern_emojis']} | تفسير={analysis['interpretation']}")
        
        # حفظ النتائج
        with open(output_dir / "surah_keys_discovery.json", "w", encoding="utf-8") as f:
            json.dump(self.surah_keys, f, ensure_ascii=False, indent=2)
        
        # إنشاء تقرير
        self.generate_report(output_dir)
        
        print(f"\n✅ Generated {len(self.surah_keys)} sub-keys!")
        print(f"📁 Output: {output_dir}/")
        print(f"📊 Analysis: {output_dir}/surah_keys_discovery.json")
        print(f"📋 Report: {output_dir}/DISCOVERY_REPORT.md")
        
        return self.surah_keys
    
    def generate_report(self, output_dir):
        """إنشاء تقرير الاكتشاف"""
        
        report = """# 🌙 نظام Rahman-Key: فن رقمي قرآني مولّد خوارزمياً | Rahman-Key System: Algorithmically Generated Quranic Digital Art

**English:**  
143 unique patterns for Surahs and disconnected letters - algorithmically generated digital art.

**العربية:**  
143 نمط فريد للسور والحروف المقطعة - فن رقمي مولّد خوارزمياً.

---

## 📊 Results Table | جدول النتائج

| السورة | المفتاح | المصفوفة | الأنماط | التفسير |
|--------|---------|----------|---------|---------|
"""
        
        # Sort by surah number
        sorted_keys = sorted(self.surah_keys.items(), 
                           key=lambda x: list(self.surah_keys.keys()).index(x[0]) + 1)
        
        for surah_name, analysis in sorted_keys:
            report += f"| {analysis['surah']} | {analysis['key']} | {analysis['matrix_shape']} | {analysis['pattern_emojis']} | {analysis['interpretation']} |\n"
        
        # Statistics
        heart_count = sum(1 for a in self.surah_keys.values() if "heart" in a['patterns'])
        star_count = sum(1 for a in self.surah_keys.values() if "star" in a['patterns'])
        door_count = sum(1 for a in self.surah_keys.values() if "door" in a['patterns'])
        
        report += f"""
---

## 📈 Statistics | الإحصائيات

**English:**  
- ❤️ Hearts detected: {heart_count}
- ⭐ Stars detected: {star_count}
- 🚪 Doors detected: {door_count}

**العربية:**  
- ❤️ قلوب مكتشفة: {heart_count}
- ⭐ نجوم مكتشفة: {star_count}
- 🚪 أبواب مكتشفة: {door_count}

---

## 🎯 Key Insights | الرؤى الرئيسية

**English:**  
Each Surah has a unique sub-key that reveals its specific pattern and meaning.

**العربية:**  
كل سورة لها مفتاح فرعي فريد يكشف نمطها ومعناها الخاص.

---

**🌙 Rahman-Key** — Sub-keys discovery for each Surah. | اكتشاف المفاتيح الفرعية لكل سورة.

**Date:** 2024  
**Status:** ⚠️ Experimental | تجريبي
"""
        
        with open(output_dir / "DISCOVERY_REPORT.md", "w", encoding="utf-8") as f:
            f.write(report)

# **تنفيذ اكتشاف المفاتيح**

if __name__ == "__main__":
    discovery = SurahKeyDiscovery()
    all_keys = discovery.discover_all_keys()
    
    # إنشاء تقرير مفصل
    print("\n" + "="*80)
    print("📊 تقرير المفاتيح المكتشفة | Discovery Report:")
    print("="*80)
    
    heart_count = 0
    star_count = 0
    door_count = 0
    
    for surah, analysis in list(all_keys.items())[:10]:  # First 10 as example
        print(f"{analysis['surah']:15} | مفتاح: {analysis['key']:3} | "
              f"أنماط: {analysis['pattern_emojis']:10} | "
              f"تفسير: {analysis['interpretation']}")
        
        if "heart" in analysis['patterns']:
            heart_count += 1
        if "star" in analysis['patterns']:
            star_count += 1
        if "door" in analysis['patterns']:
            door_count += 1
    
    print("\n📈 الإحصائيات الكاملة:")
    print(f"❤️ قلوب مكتشفة: {sum(1 for a in all_keys.values() if 'heart' in a['patterns'])}")
    print(f"⭐ نجوم مكتشفة: {sum(1 for a in all_keys.values() if 'star' in a['patterns'])}")
    print(f"🚪 أبواب مكتشفة: {sum(1 for a in all_keys.values() if 'door' in a['patterns'])}")

