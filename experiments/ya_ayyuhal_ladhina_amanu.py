"""
Verses Starting with "O Believers" - Rahman Key Experiment
آيات "يا أيها الذين آمنوا" - تجربة مفتاح الرحمن

Applies the 31×6 key to verses starting with "يا أيها الذين آمنوا"
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def to_6bit(n):
    """Convert number to 6-bit binary string"""
    return format(n, '06b')

def generate_believers_heart():
    """
    Generate heart pattern from verses starting with "يا أيها الذين آمنوا"
    
    Method:
    - Collected 88 verses starting with "يا أيها الذين آمنوا"
    - Take sequence 1→88 (order of appearance)
    - Repeat until ≥31 rows → take first 31
    - Convert each number to 6-bit binary → 31×6 matrix → bitmap
    """
    # ترتيب الآيات: 1 → 88
    sequence = list(range(1, 89))
    
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
    ax.set_title('"O Believers" Verses (88) - 31×6\nآيات "يا أيها الذين آمنوا"', 
                 fontsize=12, pad=20)
    
    # حفظ
    project_root = Path(__file__).parent.parent
    output_dir = project_root / 'experiments_output' / 'ya_ayyuhal_ladhina_amanu'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    plt.savefig(output_dir / 'Yaa_Ayyuhal_Ladhina_Amanu_88.png', 
                dpi=150, bbox_inches='tight', pad_inches=0.1)
    plt.close()
    
    print("✅ Generated: Yaa_Ayyuhal_Ladhina_Amanu_88.png")
    print(f"   Location: {output_dir / 'Yaa_Ayyuhal_Ladhina_Amanu_88.png'}")
    print(f"   Matrix shape: {matrix.shape}")
    print(f"   Total verses: 88")
    print(f"   First 31 used for matrix")

if __name__ == "__main__":
    print("=" * 60)
    print('Verses "O Believers" - Rahman Key Experiment')
    print('آيات "يا أيها الذين آمنوا" - تجربة مفتاح الرحمن')
    print("=" * 60)
    generate_believers_heart()
    print("=" * 60)
    print("✅ Complete!")
    print("\nNote: The 'raised hands' and 'halo' shapes are visual interpretations,")
    print("      not part of the algorithmic methodology.")

