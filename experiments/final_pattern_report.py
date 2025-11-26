"""
Final Pattern Analysis Report
تقرير التحليل النهائي للأنماط
"""
import numpy as np
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / 'code'))
from quran_hearts import generate_bitmap

def to_6bit(n):
    return format(n, '06b')

def print_matrix_visualization(matrix, name):
    """Print matrix as visual representation"""
    rows, cols = matrix.shape
    print(f"\n📊 {name} Matrix Visualization:")
    print("   " + " ".join([str(i) for i in range(cols)]))
    for i, row in enumerate(matrix):
        row_str = " ".join(["█" if cell == 1 else "░" for cell in row])
        print(f"{i:2d} {row_str}")

def analyze_al_fatiha_detailed():
    """Detailed analysis of Al-Fatiha"""
    print("="*60)
    print("Al-Fatiha Detailed Analysis | تحليل الفاتحة التفصيلي")
    print("="*60)
    
    matrix = generate_bitmap(7)
    rows, cols = matrix.shape
    
    print(f"\nMatrix: {rows}×{cols}")
    print(f"Black pixels: {np.sum(matrix)} ({np.sum(matrix)/matrix.size*100:.1f}%)")
    
    # Print visualization
    print_matrix_visualization(matrix, "Al-Fatiha")
    
    # Analyze each column
    print("\n📐 Column Analysis:")
    for col in range(cols):
        column = matrix[:, col]
        black_count = np.sum(column == 1)
        pattern = "".join(["█" if c == 1 else "░" for c in column])
        print(f"   Column {col}: {black_count} black | {pattern}")
    
    # Check for "هو" in different ways
    print("\n🔤 'هو' Detection Methods:")
    
    # Method 1: Look for vertical line (هاء)
    vertical_lines = []
    for col in range(cols):
        column = matrix[:, col]
        if np.sum(column == 1) > rows * 0.4:  # At least 40% black
            vertical_lines.append(col)
            print(f"   Column {col}: Vertical structure detected ✅")
    
    # Method 2: Look for horizontal connection
    middle = rows // 2
    if middle > 0 and middle < rows:
        middle_row = matrix[middle, :]
        middle_black = np.sum(middle_row == 1)
        print(f"   Middle row ({middle}): {middle_black} black pixels")
        if middle_black >= 2:
            print(f"   Horizontal structure detected ✅")
    
    # Method 3: Look for curved pattern (واو)
    curved_detected = False
    for col in range(1, cols-1):
        column = matrix[:, col]
        # Check for U or C shape
        top = np.sum(column[:rows//3] == 1)
        mid = np.sum(column[rows//3:2*rows//3] == 1)
        bot = np.sum(column[2*rows//3:] == 1)
        
        if (top > 2 and bot > 2 and mid < 2) or (top < 2 and bot < 2 and mid > 2):
            print(f"   Column {col}: Curved pattern detected ✅")
            curved_detected = True
    
    # Heart detection
    widths = []
    for i in range(rows):
        row = matrix[i, :]
        black = np.where(row == 1)[0]
        widths.append(black[-1] - black[0] + 1 if len(black) > 0 else 0)
    
    is_heart = np.mean(widths[:rows//3]) < np.mean(widths[rows//3:2*rows//3]) or \
               np.mean(widths[:rows//2]) > np.mean(widths[rows//2:])
    
    print(f"\n❤️ Heart Shape: {'YES ✅' if is_heart else 'NO ❌'}")
    print(f"   Width progression: {[f'{w:.1f}' for w in widths[::5]]}")
    
    # Kaaba detection
    center_row, center_col = rows // 2, cols // 2
    if center_row > 1 and center_col > 1:
        center_region = matrix[center_row-1:center_row+2, center_col-1:center_col+2]
        center_density = np.sum(center_region == 1) / center_region.size
        is_kaaba = center_density > 0.5
        
        print(f"\n🕋 Kaaba Shape: {'YES ✅' if is_kaaba else 'NO ❌'}")
        print(f"   Center density: {center_density*100:.1f}%")
        print(f"   Center region:")
        for i, row in enumerate(center_region):
            row_str = " ".join(["█" if cell == 1 else "░" for cell in row])
            print(f"      {row_str}")
    
    return {
        'matrix': matrix,
        'heart': is_heart,
        'kaaba': is_kaaba if center_row > 1 and center_col > 1 else False,
        'hu': len(vertical_lines) > 0 or curved_detected
    }

def main():
    """Generate final report"""
    print("="*60)
    print("Final Pattern Analysis Report")
    print("تقرير التحليل النهائي للأنماط")
    print("="*60)
    
    # Al-Fatiha
    fatiha_result = analyze_al_fatiha_detailed()
    
    # Summary
    print("\n" + "="*60)
    print("FINAL RESULTS | النتائج النهائية")
    print("="*60)
    print("\nAl-Fatiha (7 verses):")
    print(f"  ❤️ Heart: {'✅ YES' if fatiha_result['heart'] else '❌ NO'}")
    print(f"  🔤 'هو': {'✅ YES' if fatiha_result['hu'] else '❌ NO'}")
    print(f"  🕋 Kaaba: {'✅ YES' if fatiha_result['kaaba'] else '❌ NO'}")
    
    print("\n" + "="*60)
    print("Note: Visual interpretations require human observation.")
    print("The algorithmic analysis provides structural patterns only.")
    print("="*60)

if __name__ == "__main__":
    main()

