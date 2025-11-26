"""
Analyze Grade 2 Surahs with rotations to see internal symbols
تحليل السور Grade 2 مع التدوير لرؤية الرموز الداخلية
"""
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / 'code'))
from quran_hearts import generate_bitmap, SURAHS

# السور المصنفة كـ Grade 2 (قلب متطور)
GRADE_2_SURAHS = [
    ("Al-Jumu'ah", 11),
    ("Al-Munafiqun", 11),
    ("Ad-Duha", 11),
    ("Al-Adiyat", 11),
    ("Al-Qari'ah", 11)
]

def analyze_internal_symbol(matrix, surah_name):
    """Analyze internal symbol in different rotations"""
    rows, cols = matrix.shape
    center_row, center_col = rows // 2, cols // 2
    
    print(f"\n{'='*60}")
    print(f"Analyzing: {surah_name}")
    print(f"{'='*60}")
    
    # Original orientation
    print("\n📐 Original (0°):")
    if center_row > 1 and center_col > 1:
        center_region = matrix[center_row-1:center_row+2, center_col-1:center_col+2]
        print(f"   Center region (3×3):")
        for i, row in enumerate(center_region):
            row_str = " ".join(["█" if cell == 1 else "░" for cell in row])
            print(f"      {row_str}")
        
        # Check for dot
        is_dot = center_region[1, 1] == 1 and np.sum(center_region == 1) == 1
        # Check for vertical line
        vertical_line = np.sum(center_region[:, 1] == 1) == center_region.shape[0]
        # Check for horizontal line
        horizontal_line = np.sum(center_region[1, :] == 1) == center_region.shape[1]
        
        print(f"   Dot: {'✅ YES' if is_dot else '❌ NO'}")
        print(f"   Vertical line: {'✅ YES' if vertical_line else '❌ NO'}")
        print(f"   Horizontal line: {'✅ YES' if horizontal_line else '❌ NO'}")
    
    # Check all columns for vertical patterns
    print(f"\n📊 Column Analysis:")
    for col in range(cols):
        column = matrix[:, col]
        black_count = np.sum(column == 1)
        pattern = "".join(["█" if c == 1 else "░" for c in column])
        print(f"   Col {col}: {black_count}/{rows} black | {pattern}")
    
    # Check all rows for horizontal patterns
    print(f"\n📊 Row Analysis (middle rows):")
    for row_idx in [rows//2 - 1, rows//2, rows//2 + 1]:
        if 0 <= row_idx < rows:
            row = matrix[row_idx, :]
            black_count = np.sum(row == 1)
            pattern = "".join(["█" if c == 1 else "░" for c in row])
            print(f"   Row {row_idx:2d}: {black_count}/{cols} black | {pattern}")

def visualize_rotations(matrix, surah_name, verse_count):
    """Visualize matrix in different rotations"""
    output_dir = Path('experiments_output/grade2_rotations')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    rotations = [
        (0, "Original"),
        (90, "Rotated 90°"),
        (180, "Rotated 180°"),
        (270, "Rotated 270°")
    ]
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 12))
    axes = axes.flatten()
    
    for idx, (angle, title) in enumerate(rotations):
        if angle == 0:
            rotated_matrix = matrix
        else:
            # Rotate: 90° = 1 rotation, 180° = 2 rotations, 270° = 3 rotations
            num_rotations = angle // 90
            rotated_matrix = np.rot90(matrix, num_rotations)
        
        ax = axes[idx]
        ax.imshow(rotated_matrix, cmap='binary', interpolation='nearest', aspect='auto')
        ax.axis('off')
        ax.set_title(f'{surah_name}\n{title}\n({verse_count} verses)', fontsize=10, pad=10)
        
        # Highlight center region
        r_rows, r_cols = rotated_matrix.shape
        r_center_row, r_center_col = r_rows // 2, r_cols // 2
        
        if r_center_row > 1 and r_center_col > 1:
            # Draw rectangle around center
            rect = plt.Rectangle((r_center_col - 1.5, r_center_row - 1.5), 3, 3, 
                                linewidth=2, edgecolor='red', facecolor='none')
            ax.add_patch(rect)
    
    plt.tight_layout()
    filename = f"{surah_name.replace(' ', '_').replace("'", '')}_rotations.png"
    plt.savefig(output_dir / filename, dpi=200, bbox_inches='tight')
    plt.close()
    
    print(f"  ✅ Saved: {filename}")

def analyze_rotated_symbols(matrix, surah_name):
    """Analyze symbols in all rotations"""
    print(f"\n{'='*60}")
    print(f"Symbol Analysis in All Rotations: {surah_name}")
    print(f"{'='*60}")
    
    rotations = [0, 90, 180, 270]
    
    for angle in rotations:
        if angle == 0:
            rotated = matrix
        else:
            num_rotations = angle // 90
            rotated = np.rot90(matrix, num_rotations)
        
        rows, cols = rotated.shape
        center_row, center_col = rows // 2, cols // 2
        
        print(f"\n📐 Rotation {angle}°:")
        
        if center_row > 1 and center_col > 1:
            center_region = rotated[center_row-1:center_row+2, center_col-1:center_col+2]
            
            # Check for patterns
            is_dot = center_region[1, 1] == 1 and np.sum(center_region == 1) == 1
            vertical_line = np.sum(center_region[:, 1] == 1) == center_region.shape[0]
            horizontal_line = np.sum(center_region[1, :] == 1) == center_region.shape[1]
            
            # Check for other patterns
            center_density = np.sum(center_region == 1) / center_region.size
            
            print(f"   Center density: {center_density*100:.1f}%")
            print(f"   Dot: {'✅' if is_dot else '❌'}")
            print(f"   Vertical line: {'✅' if vertical_line else '❌'}")
            print(f"   Horizontal line: {'✅' if horizontal_line else '❌'}")
            
            # Visual representation
            print(f"   Center region:")
            for i, row in enumerate(center_region):
                row_str = " ".join(["█" if cell == 1 else "░" for cell in row])
                print(f"      {row_str}")

def main():
    """Analyze all Grade 2 Surahs with rotations"""
    print("="*60)
    print("Grade 2 Surahs - Internal Symbol Analysis with Rotations")
    print("السور Grade 2 - تحليل الرمز الداخلي مع التدوير")
    print("="*60)
    
    for surah_name, verse_count in GRADE_2_SURAHS:
        matrix = generate_bitmap(verse_count)
        
        # Analyze original
        analyze_internal_symbol(matrix, surah_name)
        
        # Analyze in all rotations
        analyze_rotated_symbols(matrix, surah_name)
        
        # Visualize rotations
        visualize_rotations(matrix, surah_name, verse_count)
    
    print("\n" + "="*60)
    print("✅ Analysis complete!")
    print("   Check experiments_output/grade2_rotations/ for rotation images")
    print("="*60)

if __name__ == "__main__":
    main()

