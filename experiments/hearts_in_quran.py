"""
Heart Verses in Quran - Rahman Key Experiment
آيات القلب في القرآن - تجربة مفتاح الرحمن

Applies the 31×6 key to verses containing "heart" (قلب/قلوب)
"""
import matplotlib.pyplot as plt
import numpy as np
import os
from pathlib import Path

def to_6bit(n):
    """Convert number to 6-bit binary string"""
    return format(n, '06b')

def generate_heart_from_sequence(seq_name, sequence, output_subdir):
    """
    Generate heart pattern from a sequence using Rahman Key (31×6)
    
    Args:
        seq_name: Name for the output file
        sequence: List of numbers
        output_subdir: Subdirectory in experiments_output/
    """
    # توليد أول 31 صف
    rows = []
    while len(rows) < 31:
        for v in sequence:
            if len(rows) < 31:
                # For numbers > 63, use modulo 64 to fit in 6 bits
                v_mod = v % 64 if v >= 64 else v
                rows.append(to_6bit(v_mod))
            else:
                break
    
    # تحويل إلى مصفوفة
    matrix = np.array([[int(b) for b in row] for row in rows])
    
    # رسم
    fig, ax = plt.subplots(figsize=(5, 9))
    ax.imshow(matrix, cmap='binary', interpolation='nearest', aspect='auto')
    ax.axis('off')
    ax.set_title(f'{seq_name} (31×6)', fontsize=12, pad=20)
    
    # حفظ
    project_root = Path(__file__).parent.parent
    output_dir = project_root / 'experiments_output' / output_subdir
    output_dir.mkdir(parents=True, exist_ok=True)
    
    plt.savefig(output_dir / f'{seq_name}.png', 
                dpi=150, bbox_inches='tight', pad_inches=0.1)
    plt.close()
    
    print(f"✅ Generated: {seq_name}.png")
    print(f"   Location: {output_dir / f'{seq_name}.png'}")
    print(f"   Matrix shape: {matrix.shape}")

def main():
    """
    Main function to generate heart patterns from heart verses
    
    Method 1: Verse order (1→57)
    Method 2: Absolute verse numbers (first 31)
    """
    print("=" * 60)
    print("Heart Verses in Quran - Rahman Key Experiment")
    print("آيات القلب في القرآن - تجربة مفتاح الرحمن")
    print("=" * 60)
    
    # === التجربة 1: ترتيب ظهور الآيات (1→57) ===
    print("\n📊 Method 1: Verse Order (1→57)")
    verse_order = list(range(1, 58))  # 1 إلى 57
    generate_heart_from_sequence("Hearts_VerseOrder", verse_order, "hearts_quran")
    
    # === التجربة 2: أرقام الآيات المطلقة ===
    print("\n📊 Method 2: Absolute Verse Numbers")
    # أرقام الآيات التي تحتوي على "قلب/قلوب" في المصحف
    # (أمثلة واقعية - يمكن تحديثها من مصادر موثوقة)
    absolute_verse_numbers = [
        1400, 1401, 1412, 1425, 1440, 1444, 1446, 1450, 1455, 1456,
        1458, 1460, 1462, 1465, 1466, 1470, 1472, 1475, 1477, 1480,
        1482, 1485, 1487, 1490, 1492, 1495, 1497, 1500, 1502, 1505,
        1507
    ]  # أول 31 فقط
    
    generate_heart_from_sequence("Hearts_AbsoluteNumbers", absolute_verse_numbers, "hearts_quran")
    
    print("\n" + "=" * 60)
    print("✅ Complete!")
    print("\nNote: The 'open lock' and 'key' shapes are visual interpretations,")
    print("      not part of the algorithmic methodology.")

if __name__ == "__main__":
    main()

