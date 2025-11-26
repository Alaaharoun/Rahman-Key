"""
Basmalah (114 times) - Rahman Key Experiment
البسملة (114 مرة) - تجربة مفتاح الرحمن

Applies the 31×6 key to Basmalah appearing 114 times in Quran
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def to_6bit(n):
    """Convert number to 6-bit binary string"""
    return format(n, '06b')

def generate_basmalah_heart():
    """
    Generate heart pattern from Basmalah (114 times)
    
    Method:
    - Basmalah appears 114 times in Quran
    - Take digits: [1, 1, 4]
    - Repeat until ≥31 rows → take first 31
    - Convert each number to 6-bit binary → 31×6 matrix → bitmap
    """
    # أرقام البسملة: 114 → [1, 1, 4]
    sequence = [1, 1, 4]
    
    # تكرار حتى 31 صف
    rows = []
    while len(rows) < 31:
        for v in sequence:
            if len(rows) < 31:
                rows.append(to_6bit(v))
            else:
                break
    
    # تحويل إلى مصفوفة
    matrix = np.array([[int(b) for b in row] for row in rows])
    
    # رسم
    fig, ax = plt.subplots(figsize=(5, 9))
    ax.imshow(matrix, cmap='binary', interpolation='nearest', aspect='auto')
    ax.axis('off')
    ax.set_title('Basmalah (114 times) - 31×6\nالبسملة (114 مرة)', 
                 fontsize=12, pad=20)
    
    # حفظ
    project_root = Path(__file__).parent.parent
    output_dir = project_root / 'experiments_output' / 'basmalah'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    plt.savefig(output_dir / 'Basmalah_114.png', 
                dpi=150, bbox_inches='tight', pad_inches=0.1)
    plt.close()
    
    print("✅ Generated: Basmalah_114.png")
    print(f"   Location: {output_dir / 'Basmalah_114.png'}")
    print(f"   Matrix shape: {matrix.shape}")
    print(f"   Sequence used: [1, 1, 4] (repeated)")

if __name__ == "__main__":
    print("=" * 60)
    print("Basmalah (114 times) - Rahman Key Experiment")
    print("البسملة (114 مرة) - تجربة مفتاح الرحمن")
    print("=" * 60)
    generate_basmalah_heart()
    print("=" * 60)
    print("✅ Complete!")
    print("\nNote: Any visual interpretations (like 'wings' or 'bism') are")
    print("      subjective observations, not part of the methodology.")

