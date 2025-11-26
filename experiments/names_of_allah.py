"""
99 Names of Allah - Rahman Key Experiment
أسماء الله الحسنى - تجربة مفتاح الرحمن

Applies the 31×6 key to the 99 names of Allah
"""
import matplotlib.pyplot as plt
import numpy as np
import os
from pathlib import Path

def to_6bit(n):
    """Convert number to 6-bit binary string"""
    return format(n, '06b')

def generate_names_99():
    """
    Generate heart pattern from 99 Names of Allah using Rahman Key (31×6)
    
    Method:
    - Take sequence 1→99 (order of names)
    - Repeat until ≥31 rows → take first 31
    - Convert each number to 6-bit binary → 31×6 matrix → bitmap
    """
    # ترتيب الأسماء: 1 → 99
    sequence = list(range(1, 100))
    
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
    ax.set_title('99 Names of Allah (31×6)\nأسماء الله الحسنى', 
                 fontsize=12, pad=20)
    
    # حفظ
    project_root = Path(__file__).parent.parent
    output_dir = project_root / 'experiments_output' / 'names_of_allah'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    plt.savefig(output_dir / '099_Names_Of_Allah.png', 
                dpi=150, bbox_inches='tight', pad_inches=0.1)
    plt.close()
    
    print("✅ Generated: 099_Names_Of_Allah.png")
    print(f"   Location: {output_dir / '099_Names_Of_Allah.png'}")
    print(f"   Matrix shape: {matrix.shape}")
    print(f"   Total black pixels: {np.sum(matrix)}")

if __name__ == "__main__":
    print("=" * 60)
    print("99 Names of Allah - Rahman Key Experiment")
    print("أسماء الله الحسنى - تجربة مفتاح الرحمن")
    print("=" * 60)
    generate_names_99()
    print("=" * 60)
    print("✅ Complete!")

