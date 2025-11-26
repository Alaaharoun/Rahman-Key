"""
Advanced Symbol Detector - Detect "هو", Kaaba, and other symbols
كاشف الرموز المتقدم - كشف "هو"، الكعبة، ورموز أخرى
"""
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / 'code'))
from quran_hearts import generate_bitmap

def to_6bit(n):
    return format(n, '06b')

def visualize_matrix(matrix, title, save_path=None):
    """Visualize matrix with annotations"""
    fig, ax = plt.subplots(figsize=(6, 10))
    ax.imshow(matrix, cmap='binary', interpolation='nearest', aspect='auto')
    ax.axis('off')
    ax.set_title(title, fontsize=12, pad=20)
    
    # Add grid for better visualization
    rows, cols = matrix.shape
    for i in range(rows + 1):
        ax.axhline(i - 0.5, color='gray', linewidth=0.5, alpha=0.3)
    for j in range(cols + 1):
        ax.axvline(j - 0.5, color='gray', linewidth=0.5, alpha=0.3)
    
    if save_path:
        plt.savefig(save_path, dpi=200, bbox_inches='tight')
    plt.close()

def detect_hu_advanced(matrix):
    """
    Advanced detection of "هو" pattern
    "هو" = هاء (vertical line with horizontal) + واو (curved)
    """
    rows, cols = matrix.shape
    results = {
        'has_vertical_structure': False,
        'has_horizontal_structure': False,
        'has_curved_structure': False,
        'potential_hu': False
    }
    
    # Method 1: Look for vertical line (هاء)
    for col in range(cols):
        column = matrix[:, col]
        black_ratio = np.sum(column == 1) / rows
        
        # Strong vertical line
        if black_ratio > 0.5:
            results['has_vertical_structure'] = True
            
            # Check for horizontal connection (middle of vertical)
            middle = rows // 2
            if middle > 0 and middle < rows - 1:
                # Check adjacent columns for horizontal line
                for adj_col in [col-1, col+1]:
                    if 0 <= adj_col < cols:
                        if matrix[middle, adj_col] == 1:
                            results['has_horizontal_structure'] = True
    
    # Method 2: Look for curved pattern (واو)
    # Check for U-shape or C-shape in columns
    for col in range(1, cols-1):
        column = matrix[:, col]
        
        # Check for U-shape: black at top and bottom, white in middle
        top_third = np.sum(column[:rows//3] == 1)
        middle_third = np.sum(column[rows//3:2*rows//3] == 1)
        bottom_third = np.sum(column[2*rows//3:] == 1)
        
        # U-shape pattern
        if (top_third > rows//6 and bottom_third > rows//6 and middle_third < rows//6) or \
           (top_third < rows//6 and bottom_third < rows//6 and middle_third > rows//6):
            results['has_curved_structure'] = True
    
    # "هو" requires both vertical and curved structures
    results['potential_hu'] = (results['has_vertical_structure'] or results['has_horizontal_structure']) and \
                              results['has_curved_structure']
    
    return results

def detect_kaaba_advanced(matrix):
    """
    Advanced Kaaba detection
    الكعبة: شكل مربع/مستطيل في الوسط
    """
    rows, cols = matrix.shape
    center_row, center_col = rows // 2, cols // 2
    
    # Check multiple regions around center
    kaaba_score = 0
    
    # Region 1: 3x3 center
    if center_row > 1 and center_col > 1:
        center_3x3 = matrix[center_row-1:center_row+2, center_col-1:center_col+2]
        center_density = np.sum(center_3x3 == 1) / center_3x3.size
        
        # Kaaba should have dense center
        if center_density > 0.5:
            kaaba_score += 1
        
        # Check for rectangular boundary
        # Top edge
        if center_row > 2:
            top_edge = matrix[center_row-2, center_col-1:center_col+2]
            if np.sum(top_edge == 0) >= 1:  # Has white boundary
                kaaba_score += 1
        
        # Bottom edge
        if center_row < rows - 2:
            bottom_edge = matrix[center_row+2, center_col-1:center_col+2]
            if np.sum(bottom_edge == 0) >= 1:
                kaaba_score += 1
        
        # Left edge
        if center_col > 2:
            left_edge = matrix[center_row-1:center_row+2, center_col-2]
            if np.sum(left_edge == 0) >= 1:
                kaaba_score += 1
        
        # Right edge
        if center_col < cols - 2:
            right_edge = matrix[center_row-1:center_row+2, center_col+2]
            if np.sum(right_edge == 0) >= 1:
                kaaba_score += 1
    
    # Kaaba-like if score >= 2
    is_kaaba = kaaba_score >= 2
    
    return {
        'is_kaaba': is_kaaba,
        'score': kaaba_score,
        'center_density': center_density if center_row > 1 and center_col > 1 else 0
    }

def analyze_with_rotations(matrix, name):
    """Analyze matrix in original and rotated orientations"""
    print(f"\n{'='*60}")
    print(f"Advanced Analysis: {name}")
    print(f"{'='*60}")
    
    results = {}
    
    # Original orientation
    print("\n📐 Original Orientation:")
    hu_orig = detect_hu_advanced(matrix)
    kaaba_orig = detect_kaaba_advanced(matrix)
    
    print(f"   'هو' pattern: {'YES ✅' if hu_orig['potential_hu'] else 'NO ❌'}")
    print(f"   Kaaba shape: {'YES ✅' if kaaba_orig['is_kaaba'] else 'NO ❌'}")
    
    results['original'] = {'hu': hu_orig, 'kaaba': kaaba_orig}
    
    # Rotated 90 degrees
    matrix_90 = np.rot90(matrix, 1)
    print("\n📐 Rotated 90°:")
    hu_90 = detect_hu_advanced(matrix_90)
    kaaba_90 = detect_kaaba_advanced(matrix_90)
    
    print(f"   'هو' pattern: {'YES ✅' if hu_90['potential_hu'] else 'NO ❌'}")
    print(f"   Kaaba shape: {'YES ✅' if kaaba_90['is_kaaba'] else 'NO ❌'}")
    
    results['rotated_90'] = {'hu': hu_90, 'kaaba': kaaba_90}
    
    # Rotated 180 degrees
    matrix_180 = np.rot90(matrix, 2)
    print("\n📐 Rotated 180°:")
    hu_180 = detect_hu_advanced(matrix_180)
    kaaba_180 = detect_kaaba_advanced(matrix_180)
    
    print(f"   'هو' pattern: {'YES ✅' if hu_180['potential_hu'] else 'NO ❌'}")
    print(f"   Kaaba shape: {'YES ✅' if kaaba_180['is_kaaba'] else 'NO ❌'}")
    
    results['rotated_180'] = {'hu': hu_180, 'kaaba': kaaba_180}
    
    # Best result
    best_hu = any([hu_orig['potential_hu'], hu_90['potential_hu'], hu_180['potential_hu']])
    best_kaaba = any([kaaba_orig['is_kaaba'], kaaba_90['is_kaaba'], kaaba_180['is_kaaba']])
    
    print(f"\n🎯 Best Result (any orientation):")
    print(f"   'هو' pattern: {'YES ✅' if best_hu else 'NO ❌'}")
    print(f"   Kaaba shape: {'YES ✅' if best_kaaba else 'NO ❌'}")
    
    results['best'] = {'hu': best_hu, 'kaaba': best_kaaba}
    
    return results

def main():
    """Analyze Al-Fatiha and 99 Names"""
    print("="*60)
    print("Advanced Symbol Detector")
    print("كاشف الرموز المتقدم")
    print("="*60)
    
    # Al-Fatiha
    print("\n" + "="*60)
    print("1. Al-Fatiha (7 verses) | الفاتحة")
    print("="*60)
    fatiha_matrix = generate_bitmap(7)
    fatiha_results = analyze_with_rotations(fatiha_matrix, "Al-Fatiha")
    
    # Visualize
    output_dir = Path('experiments_output/analysis')
    output_dir.mkdir(parents=True, exist_ok=True)
    visualize_matrix(fatiha_matrix, "Al-Fatiha (Original)\nالفاتحة", 
                     output_dir / 'Al-Fatiha_Original.png')
    visualize_matrix(np.rot90(fatiha_matrix, 1), "Al-Fatiha (Rotated 90°)\nالفاتحة", 
                     output_dir / 'Al-Fatiha_Rotated90.png')
    visualize_matrix(np.rot90(fatiha_matrix, 2), "Al-Fatiha (Rotated 180°)\nالفاتحة", 
                     output_dir / 'Al-Fatiha_Rotated180.png')
    
    # 99 Names
    print("\n" + "="*60)
    print("2. 99 Names of Allah | أسماء الله الحسنى")
    print("="*60)
    seq_99 = list(range(1, 100))
    rows_99 = []
    while len(rows_99) < 31:
        for v in seq_99:
            if len(rows_99) < 31:
                rows_99.append(to_6bit(v))
            else:
                break
    matrix_99 = np.array([[int(b) for b in row] for row in rows_99])
    results_99 = analyze_with_rotations(matrix_99, "99 Names")
    
    # Summary
    print("\n" + "="*60)
    print("FINAL SUMMARY | الملخص النهائي")
    print("="*60)
    print("\nAl-Fatiha:")
    print(f"  Heart: ✅ (detected in previous analysis)")
    print(f"  'هو': {'✅' if fatiha_results['best']['hu'] else '❌'}")
    print(f"  Kaaba: {'✅' if fatiha_results['best']['kaaba'] else '❌'}")
    
    print("\n99 Names:")
    print(f"  Heart: ❌ (not detected)")
    print(f"  'هو': {'✅' if results_99['best']['hu'] else '❌'}")
    print(f"  Kaaba: {'✅' if results_99['best']['kaaba'] else '❌'}")

if __name__ == "__main__":
    main()

