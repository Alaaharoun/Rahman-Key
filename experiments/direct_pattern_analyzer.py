"""
Direct Pattern Analyzer - Analyze patterns directly from code matrices
محلل الأنماط المباشر - تحليل الأنماط مباشرة من مصفوفات الكود
"""
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys

# Add code directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'code'))
from quran_hearts import generate_bitmap, SURAHS

def to_6bit(n):
    """Convert number to 6-bit binary string"""
    return format(n, '06b')

def analyze_matrix(matrix, name):
    """Complete analysis of a binary matrix"""
    print(f"\n{'='*60}")
    print(f"Analyzing: {name}")
    print(f"{'='*60}")
    
    rows, cols = matrix.shape
    print(f"Matrix shape: {matrix.shape}")
    print(f"Total pixels: {matrix.size}")
    print(f"Black pixels: {np.sum(matrix)} ({np.sum(matrix)/matrix.size*100:.1f}%)")
    
    # Symmetry analysis
    # Vertical symmetry (left-right)
    if cols % 2 == 0:
        left_half = matrix[:, :cols//2]
        right_half = np.flip(matrix[:, cols//2:], axis=1)
        vertical_symmetry = np.sum(left_half == right_half) / left_half.size
    else:
        left_half = matrix[:, :cols//2]
        right_half = np.flip(matrix[:, cols//2+1:], axis=1)
        vertical_symmetry = np.sum(left_half == right_half) / left_half.size
    
    # Horizontal symmetry (top-bottom)
    if rows % 2 == 0:
        top_half = matrix[:rows//2, :]
        bottom_half = np.flip(matrix[rows//2:, :], axis=0)
        horizontal_symmetry = np.sum(top_half == bottom_half) / top_half.size
    else:
        top_half = matrix[:rows//2, :]
        bottom_half = np.flip(matrix[rows//2+1:, :], axis=0)
        horizontal_symmetry = np.sum(top_half == bottom_half) / top_half.size
    
    overall_symmetry = (vertical_symmetry + horizontal_symmetry) / 2
    
    print(f"\n📊 Symmetry Analysis:")
    print(f"   Vertical symmetry: {vertical_symmetry*100:.1f}%")
    print(f"   Horizontal symmetry: {horizontal_symmetry*100:.1f}%")
    print(f"   Overall symmetry: {overall_symmetry*100:.1f}%")
    
    # Heart shape detection
    widths = []
    for i in range(rows):
        row = matrix[i, :]
        black_indices = np.where(row == 1)[0]
        if len(black_indices) > 0:
            width = black_indices[-1] - black_indices[0] + 1
        else:
            width = 0
        widths.append(width)
    
    middle = rows // 2
    top_width = np.mean(widths[:middle//2]) if middle//2 > 0 else 0
    middle_width = np.mean(widths[middle//2:middle+middle//2]) if middle+middle//2 <= rows else np.mean(widths[middle//2:])
    bottom_width = np.mean(widths[middle+middle//2:]) if middle+middle//2 < rows else 0
    
    is_heart_like = False
    if middle_width > top_width and middle_width > bottom_width:
        is_heart_like = True
    elif top_width > bottom_width and top_width > 0:
        is_heart_like = True
    
    print(f"\n❤️ Heart Shape Detection:")
    print(f"   Is heart-like: {'YES ✅' if is_heart_like else 'NO ❌'}")
    print(f"   Top width: {top_width:.1f}")
    print(f"   Middle width: {middle_width:.1f}")
    print(f"   Bottom width: {bottom_width:.1f}")
    
    # Central pattern analysis
    center_row = rows // 2
    center_col = cols // 2
    
    # Extract center region
    if center_row > 0 and center_col > 0:
        center_region = matrix[max(0, center_row-1):min(rows, center_row+2), 
                               max(0, center_col-1):min(cols, center_col+2)]
        
        center_dense = np.sum(center_region) > center_region.size // 2
        center_sparse = np.sum(center_region) < center_region.size // 3
        
        # Check for vertical line in center
        if center_region.shape[1] >= 3:
            vertical_line = np.sum(center_region[:, 1]) == center_region.shape[0]
        else:
            vertical_line = False
            
        # Check for horizontal line in center
        if center_region.shape[0] >= 3:
            horizontal_line = np.sum(center_region[1, :]) == center_region.shape[1]
        else:
            horizontal_line = False
    else:
        center_dense = False
        center_sparse = False
        vertical_line = False
        horizontal_line = False
    
    print(f"\n🎯 Central Pattern:")
    print(f"   Center dense: {'YES ✅' if center_dense else 'NO ❌'}")
    print(f"   Center sparse: {'YES ✅' if center_sparse else 'NO ❌'}")
    print(f"   Vertical line: {'YES ✅' if vertical_line else 'NO ❌'}")
    print(f"   Horizontal line: {'YES ✅' if horizontal_line else 'NO ❌'}")
    
    # Pattern density by region
    top_region = matrix[:rows//3, :]
    middle_region = matrix[rows//3:2*rows//3, :]
    bottom_region = matrix[2*rows//3:, :]
    
    top_density = np.sum(top_region) / top_region.size
    middle_density = np.sum(middle_region) / middle_region.size
    bottom_density = np.sum(bottom_region) / bottom_region.size
    
    print(f"\n📈 Density by Region:")
    print(f"   Top region: {top_density*100:.1f}%")
    print(f"   Middle region: {middle_density*100:.1f}%")
    print(f"   Bottom region: {bottom_density*100:.1f}%")
    
    return {
        'matrix': matrix,
        'symmetry': {
            'vertical': vertical_symmetry,
            'horizontal': horizontal_symmetry,
            'overall': overall_symmetry
        },
        'heart': {
            'is_heart_like': is_heart_like,
            'widths': widths,
            'top_width': top_width,
            'middle_width': middle_width,
            'bottom_width': bottom_width
        },
        'center': {
            'dense': center_dense,
            'sparse': center_sparse,
            'vertical_line': vertical_line,
            'horizontal_line': horizontal_line
        },
        'density': {
            'top': top_density,
            'middle': middle_density,
            'bottom': bottom_density
        }
    }

def analyze_al_fatiha():
    """Analyze Al-Fatiha (7 verses)"""
    print("\n" + "="*60)
    print("1. Al-Fatiha (7 verses) | الفاتحة")
    print("="*60)
    
    matrix = generate_bitmap(7)
    result = analyze_matrix(matrix, "Al-Fatiha")
    
    # Visualize
    plt.figure(figsize=(3, 6))
    plt.imshow(matrix, cmap='binary', interpolation='nearest', aspect='auto')
    plt.axis('off')
    plt.title('Al-Fatiha Analysis\nالفاتحة', fontsize=10)
    plt.tight_layout()
    
    output_dir = Path('experiments_output/analysis')
    output_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_dir / 'Al-Fatiha_Analysis.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    return result

def analyze_99_names():
    """Analyze 99 Names of Allah"""
    print("\n" + "="*60)
    print("2. 99 Names of Allah | أسماء الله الحسنى")
    print("="*60)
    
    sequence = list(range(1, 100))
    rows = []
    while len(rows) < 31:
        for v in sequence:
            if len(rows) < 31:
                rows.append(to_6bit(v))
            else:
                break
    
    matrix = np.array([[int(b) for b in row] for row in rows])
    result = analyze_matrix(matrix, "99 Names of Allah")
    
    # Visualize
    plt.figure(figsize=(3, 6))
    plt.imshow(matrix, cmap='binary', interpolation='nearest', aspect='auto')
    plt.axis('off')
    plt.title('99 Names Analysis\nأسماء الله الحسنى', fontsize=10)
    plt.tight_layout()
    
    output_dir = Path('experiments_output/analysis')
    output_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_dir / '99_Names_Analysis.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    return result

def analyze_hearts_verses():
    """Analyze Heart Verses (57)"""
    print("\n" + "="*60)
    print("3. Heart Verses (57) | آيات القلب")
    print("="*60)
    
    sequence = list(range(1, 58))
    rows = []
    while len(rows) < 31:
        for v in sequence:
            if len(rows) < 31:
                rows.append(to_6bit(v))
            else:
                break
    
    matrix = np.array([[int(b) for b in row] for row in rows])
    result = analyze_matrix(matrix, "Heart Verses (57)")
    
    # Visualize
    plt.figure(figsize=(3, 6))
    plt.imshow(matrix, cmap='binary', interpolation='nearest', aspect='auto')
    plt.axis('off')
    plt.title('Heart Verses Analysis\nآيات القلب', fontsize=10)
    plt.tight_layout()
    
    output_dir = Path('experiments_output/analysis')
    output_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_dir / 'Hearts_Verses_Analysis.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    return result

def main():
    """Run all analyses"""
    print("="*60)
    print("Pattern Analyzer - Direct Matrix Analysis")
    print("محلل الأنماط - التحليل المباشر للمصفوفات")
    print("="*60)
    
    results = {}
    
    # Analyze Al-Fatiha
    results['Al-Fatiha'] = analyze_al_fatiha()
    
    # Analyze 99 Names
    results['99_Names'] = analyze_99_names()
    
    # Analyze Heart Verses
    results['Heart_Verses'] = analyze_hearts_verses()
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY | الملخص")
    print("="*60)
    
    for name, result in results.items():
        print(f"\n{name}:")
        print(f"  Symmetry: {result['symmetry']['overall']*100:.1f}%")
        print(f"  Heart-like: {'YES ✅' if result['heart']['is_heart_like'] else 'NO ❌'}")
        print(f"  Center dense: {'YES ✅' if result['center']['dense'] else 'NO ❌'}")
        print(f"  Vertical line in center: {'YES ✅' if result['center']['vertical_line'] else 'NO ❌'}")
    
    print("\n" + "="*60)
    print("✅ Analysis complete! Check experiments_output/analysis/ for visualizations")
    print("="*60)

if __name__ == "__main__":
    main()

