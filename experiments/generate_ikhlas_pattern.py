"""
Generate Al-Ikhlas pattern image
توليد صورة نمط سورة الإخلاص
"""
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / 'code'))
from quran_hearts import generate_bitmap

def generate_ikhlas_image():
    """Generate Al-Ikhlas (4 verses) pattern"""
    surah_name = "Al-Ikhlas"
    verse_count = 4
    
    # Generate matrix using the same methodology
    matrix = generate_bitmap(verse_count)
    
    # Create high-resolution image
    fig, ax = plt.subplots(figsize=(4, 8))
    ax.imshow(matrix, cmap='binary', interpolation='nearest', aspect='auto')
    ax.axis('off')
    ax.set_title(f'{surah_name} (سورة الإخلاص)\n{verse_count} verses | 31×6 Pattern', 
                 fontsize=12, pad=15)
    
    # Add grid for better visualization
    rows, cols = matrix.shape
    for i in range(rows + 1):
        ax.axhline(i - 0.5, color='gray', linewidth=0.3, alpha=0.3)
    for j in range(cols + 1):
        ax.axvline(j - 0.5, color='gray', linewidth=0.3, alpha=0.3)
    
    plt.tight_layout()
    
    # Save
    output_dir = Path('experiments_output')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_path = output_dir / 'Al-Ikhlas_Pattern.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"✅ Image saved: {output_path}")
    print(f"   Matrix shape: {matrix.shape}")
    print(f"   Black pixels: {np.sum(matrix)} ({np.sum(matrix)/matrix.size*100:.1f}%)")
    
    # Print matrix visualization
    print(f"\n📊 Matrix Visualization:")
    print("   " + " ".join([str(i) for i in range(cols)]))
    for i, row in enumerate(matrix):
        row_str = " ".join(["█" if cell == 1 else "░" for cell in row])
        print(f"{i:2d} {row_str}")
    
    return output_path

if __name__ == "__main__":
    print("="*60)
    print("Generating Al-Ikhlas Pattern")
    print("توليد نمط سورة الإخلاص")
    print("="*60)
    
    path = generate_ikhlas_image()
    print(f"\n✅ Done! Check: {path}")

