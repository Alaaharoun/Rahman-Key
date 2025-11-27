"""
Complete Quran Digital - جمع كل أنماط القرآن في صورة واحدة
القرآن الكامل - النسخة الرقمية 31×3006
جمع كل الأنماط في صورة واحدة
"""
import numpy as np
import matplotlib.pyplot as plt
import json
import importlib.util
from pathlib import Path

# Load modules
quran_hearts_path = Path(__file__).parent / 'quran_hearts.py'
spec = importlib.util.spec_from_file_location("quran_hearts", quran_hearts_path)
quran_hearts = importlib.util.module_from_spec(spec)
spec.loader.exec_module(quran_hearts)

disconnected_path = Path(__file__).parent / 'disconnected_letters_keys.py'
spec2 = importlib.util.spec_from_file_location("disconnected_letters_keys", disconnected_path)
disconnected_module = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(disconnected_module)

# Get functions
generate_bitmap = quran_hearts.generate_bitmap
SURAHS = quran_hearts.SURAHS
disconnected_letters_to_bitmap = disconnected_module.disconnected_letters_to_bitmap
DISCONNECTED_LETTERS = disconnected_module.DISCONNECTED_LETTERS
ABJAD = disconnected_module.ABJAD

def to_6bit(n):
    """Convert number to 6-bit binary string"""
    return format(n, '06b')

def generate_31x6_from_sequence(sequence):
    """Generate 31×6 matrix from a sequence of numbers"""
    seq = list(sequence)
    while len(seq) < 31:
        seq += seq[:31 - len(seq)]
    seq = seq[:31]
    
    binary = [to_6bit(n) for n in seq]
    matrix = np.array([[int(b) for b in row] for row in binary])
    return matrix

class CompleteQuranDigital:
    def __init__(self):
        self.all_patterns = []
        self.pattern_metadata = []
        
    def generate_surah_patterns(self):
        """114 سورة - مفتاح الرحمن الأصلي"""
        print("📖 توليد 114 سورة...")
        for surah_num, (surah_name, verse_count) in enumerate(SURAHS, 1):
            matrix = generate_bitmap(verse_count)
            self.all_patterns.append(matrix)
            self.pattern_metadata.append({
                "type": "سورة",
                "number": surah_num,
                "name": surah_name,
                "verse_count": verse_count,
                "columns": (len(self.all_patterns) - 1) * 6 + 1,
                "columns_end": len(self.all_patterns) * 6
            })
        print(f"✅ تم توليد {len(self.all_patterns)} سورة")
    
    def generate_disconnected_letters(self):
        """29 حروف مقطعة"""
        print("🔑 توليد الحروف المقطعة...")
        unique_letters = list(DISCONNECTED_LETTERS.keys())
        
        for letters in unique_letters:
            matrix, _ = disconnected_letters_to_bitmap(letters, "")
            if matrix is not None:
                self.all_patterns.append(matrix)
                self.pattern_metadata.append({
                    "type": "حروف مقطعة",
                    "letters": letters,
                    "surahs": DISCONNECTED_LETTERS[letters],
                    "columns": (len(self.all_patterns) - 1) * 6 + 1,
                    "columns_end": len(self.all_patterns) * 6
                })
        print(f"✅ تم توليد {len([p for p in self.pattern_metadata if p['type'] == 'حروف مقطعة'])} مجموعة حروف مقطعة")
    
    def generate_names_of_allah(self):
        """99 اسم الله الحسنى"""
        print("🤲 توليد 99 اسم الله...")
        # Sequence 1→99
        sequence = list(range(1, 100))
        matrix = generate_31x6_from_sequence(sequence)
        self.all_patterns.append(matrix)
        self.pattern_metadata.append({
            "type": "أسماء الله",
            "count": 99,
            "columns": (len(self.all_patterns) - 1) * 6 + 1,
            "columns_end": len(self.all_patterns) * 6
        })
        print("✅ تم توليد أسماء الله الحسنى")
    
    def generate_heart_verses(self):
        """57 آية قلب"""
        print("❤️ توليد 57 آية قلب...")
        # Sequence 1→57 (verse order)
        sequence = list(range(1, 58))
        matrix = generate_31x6_from_sequence(sequence)
        self.all_patterns.append(matrix)
        self.pattern_metadata.append({
            "type": "آيات القلب",
            "count": 57,
            "columns": (len(self.all_patterns) - 1) * 6 + 1,
            "columns_end": len(self.all_patterns) * 6
        })
        print("✅ تم توليد آيات القلب")
    
    def generate_faith_verses(self):
        """88 آية إيمان (يا أيها الذين آمنوا)"""
        print("🙌 توليد 88 آية إيمان...")
        # Sequence 1→88
        sequence = list(range(1, 89))
        matrix = generate_31x6_from_sequence(sequence)
        self.all_patterns.append(matrix)
        self.pattern_metadata.append({
            "type": "آيات الإيمان",
            "count": 88,
            "columns": (len(self.all_patterns) - 1) * 6 + 1,
            "columns_end": len(self.all_patterns) * 6
        })
        print("✅ تم توليد آيات الإيمان")
    
    def generate_revelation_order(self):
        """114 ترتيب النزول"""
        print("📜 توليد ترتيب النزول...")
        # Sequence 1→114 (revelation order)
        sequence = list(range(1, 115))
        matrix = generate_31x6_from_sequence(sequence)
        self.all_patterns.append(matrix)
        self.pattern_metadata.append({
            "type": "ترتيب النزول",
            "count": 114,
            "columns": (len(self.all_patterns) - 1) * 6 + 1,
            "columns_end": len(self.all_patterns) * 6
        })
        print("✅ تم توليد ترتيب النزول")
    
    def generate_complete_quran(self):
        """الجمع الكامل"""
        print("="*60)
        print("🚀 بدء توليد القرآن الرقمي الكامل...")
        print("="*60)
        
        # 1. السور
        self.generate_surah_patterns()
        
        # 2. الحروف المقطعة  
        self.generate_disconnected_letters()
        
        # 3. أسماء الله
        self.generate_names_of_allah()
        
        # 4. آيات القلب
        self.generate_heart_verses()
        
        # 5. آيات الإيمان
        self.generate_faith_verses()
        
        # 6. ترتيب النزول
        self.generate_revelation_order()
        
        # **الجمع العظيم**
        print("\n🔗 جمع كل الأنماط...")
        complete_quran_matrix = np.hstack(self.all_patterns)
        
        print(f"\n✅ اكتمل القرآن الرقمي!")
        print(f"📊 الأبعاد: {complete_quran_matrix.shape}")
        print(f"🔢 إجمالي الأنماط: {len(self.all_patterns)}")
        print(f"🖼️  إجمالي البكسلات: {complete_quran_matrix.size}")
        print(f"📏 الأعمدة الكلية: {complete_quran_matrix.shape[1]}")
        
        return complete_quran_matrix
    
    def save_complete_quran(self, matrix):
        """حفظ القرآن الكامل"""
        output_dir = Path('complete_quran')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        print("\n💾 حفظ القرآن الرقمي الكامل...")
        
        # 1. الصورة الكاملة
        print("   📸 إنشاء الصورة الكاملة...")
        # Calculate figure size (max width for display)
        fig_width = min(100, matrix.shape[1] / 10)
        plt.figure(figsize=(fig_width, 10))
        plt.imshow(matrix, cmap='gray_r', aspect='auto', interpolation='nearest')
        plt.axis('off')
        plt.title("القرآن الكريم - النسخة الرقمية الكاملة\n"
                 f"{len(self.all_patterns)} نمط × 31×6 = {matrix.shape[1]} عمود\n"
                 "مفتاح الرحمن لكل القرآن", 
                 fontsize=16, pad=20)
        plt.tight_layout()
        plt.savefig(output_dir / 'quran_complete_digital.png', 
                   dpi=300, bbox_inches='tight', facecolor='white')
        plt.savefig(output_dir / 'quran_complete_digital.jpg', 
                   dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        print(f"   ✅ {output_dir / 'quran_complete_digital.png'}")
        
        # 2. حفظ البيانات
        print("   💾 حفظ البيانات...")
        with open(output_dir / 'metadata.json', 'w', encoding='utf-8') as f:
            json.dump(self.pattern_metadata, f, ensure_ascii=False, indent=2)
        print(f"   ✅ {output_dir / 'metadata.json'}")
        
        # 3. تقسيم لأجزاء أصغر (للعرض)
        print("   📑 تقسيم لأجزاء...")
        parts_dir = output_dir / 'parts'
        parts_dir.mkdir(exist_ok=True)
        
        chunk_size = 10  # 10 أنماط في كل صورة
        num_parts = (len(self.all_patterns) + chunk_size - 1) // chunk_size
        
        for i in range(0, len(self.all_patterns), chunk_size):
            chunk_patterns = self.all_patterns[i:i+chunk_size]
            chunk = np.hstack(chunk_patterns)
            
            plt.figure(figsize=(max(12, chunk.shape[1]//5), 6))
            plt.imshow(chunk, cmap='gray_r', aspect='auto', interpolation='nearest')
            plt.axis('off')
            part_num = i // chunk_size + 1
            plt.title(f"القرآن الرقمي - الجزء {part_num} من {num_parts}\n"
                     f"الأنماط {i+1} إلى {min(i+chunk_size, len(self.all_patterns))}", 
                     fontsize=12, pad=10)
            plt.tight_layout()
            plt.savefig(parts_dir / f'part_{part_num:03d}.png', 
                       dpi=300, bbox_inches='tight', facecolor='white')
            plt.close()
        
        print(f"   ✅ {num_parts} جزء في {parts_dir}")
        
        # 4. إحصائيات
        stats = {
            'total_patterns': len(self.all_patterns),
            'matrix_shape': list(matrix.shape),
            'total_pixels': int(matrix.size),
            'black_pixels': int(np.sum(matrix == 1)),
            'white_pixels': int(np.sum(matrix == 0)),
            'pattern_types': {}
        }
        
        for pattern in self.pattern_metadata:
            ptype = pattern['type']
            stats['pattern_types'][ptype] = stats['pattern_types'].get(ptype, 0) + 1
        
        with open(output_dir / 'statistics.json', 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        
        print(f"   ✅ {output_dir / 'statistics.json'}")
        
        # Print summary
        print("\n" + "="*60)
        print("📊 ملخص الأنماط:")
        print("="*60)
        for ptype, count in stats['pattern_types'].items():
            print(f"   {ptype}: {count}")
        print(f"\n📏 الأبعاد النهائية: {matrix.shape[0]} × {matrix.shape[1]}")
        print(f"🖼️  إجمالي البكسلات: {matrix.size:,}")
        print(f"⚫ البكسلات السوداء: {stats['black_pixels']:,}")
        print(f"⚪ البكسلات البيضاء: {stats['white_pixels']:,}")

# **تنفيذ القرآن الكامل**
if __name__ == "__main__":
    quran_digital = CompleteQuranDigital()
    complete_matrix = quran_digital.generate_complete_quran()
    quran_digital.save_complete_quran(complete_matrix)
    
    print("\n" + "="*60)
    print("🎉 تم إنشاء القرآن الرقمي الكامل!")
    print("="*60)
    print("\n📁 الملفات:")
    print("   complete_quran/quran_complete_digital.png")
    print("   complete_quran/quran_complete_digital.jpg")
    print("   complete_quran/parts/part_001.png ...")
    print("   complete_quran/metadata.json")
    print("   complete_quran/statistics.json")

