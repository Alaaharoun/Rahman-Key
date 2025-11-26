"""
Detailed Pattern Analyzer - Advanced pattern detection
محلل الأنماط التفصيلي - كشف الأنماط المتقدم
"""
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / 'code'))
from quran_hearts import generate_bitmap

def to_6bit(n):
    return format(n, '06b')

def detect_vertical_patterns(matrix):
    """Detect vertical patterns that might form letters or shapes"""
    rows, cols = matrix.shape
    patterns = {}
    
    # Check each column for vertical lines
    for col in range(cols):
        column = matrix[:, col]
        black_count = np.sum(column == 1)
        white_count = np.sum(column == 0)
        
        # Vertical line (mostly black)
        if black_count > rows * 0.7:
            patterns[f'col_{col}_vertical_line'] = True
        else:
            patterns[f'col_{col}_vertical_line'] = False
        
        # Check for alternating pattern (might indicate letter structure)
        if rows > 5:
            # Check if pattern alternates
            changes = np.sum(np.diff(column) != 0)
            if changes > rows * 0.3:
                patterns[f'col_{col}_alternating'] = True
            else:
                patterns[f'col_{col}_alternating'] = False
    
    return patterns

def detect_horizontal_patterns(matrix):
    """Detect horizontal patterns"""
    rows, cols = matrix.shape
    patterns = {}
    
    # Check middle rows for horizontal lines
    middle_rows = [rows//2 - 1, rows//2, rows//2 + 1]
    for row_idx in middle_rows:
        if 0 <= row_idx < rows:
            row = matrix[row_idx, :]
            black_count = np.sum(row == 1)
            
            # Horizontal line
            if black_count > cols * 0.7:
                patterns[f'row_{row_idx}_horizontal_line'] = True
            else:
                patterns[f'row_{row_idx}_horizontal_line'] = False
    
    return patterns

def detect_kaaba_shape(matrix):
    """
    Detect Kaaba-like shape (square/rectangular shape in center)
    الكعبة: شكل مربع أو مستطيل في الوسط
    """
    rows, cols = matrix.shape
    center_row, center_col = rows // 2, cols // 2
    
    # Look for rectangular/square pattern in center
    # Check 3x3 region around center
    if center_row > 1 and center_col > 1 and center_row < rows-1 and center_col < cols-1:
        center_region = matrix[center_row-1:center_row+2, center_col-1:center_col+2]
        
        # Kaaba: square pattern (mostly black in center, white around)
        # Or: rectangular pattern
        center_black = np.sum(center_region == 1)
        total_cells = center_region.size
        
        # Check if center is dense (like Kaaba)
        is_kaaba_like = center_black >= total_cells * 0.6
        
        # Check for square/rectangular boundary
        # Look for white pixels around black center
        if is_kaaba_like:
            # Check if there's a boundary (white pixels around)
            boundary_white = 0
            if center_row > 2:
                boundary_white += np.sum(matrix[center_row-2, center_col-1:center_col+2] == 0)
            if center_row < rows-2:
                boundary_white += np.sum(matrix[center_row+2, center_col-1:center_col+2] == 0)
            if center_col > 2:
                boundary_white += np.sum(matrix[center_row-1:center_row+2, center_col-2] == 0)
            if center_col < cols-2:
                boundary_white += np.sum(matrix[center_row-1:center_row+2, center_col+2] == 0)
            
            is_kaaba_like = boundary_white > 2  # Has white boundary
    else:
        is_kaaba_like = False
    
    return is_kaaba_like

def detect_hu_pattern(matrix):
    """
    Detect "هو" (He) pattern
    "هو" يتكون من:
    - حرف الهاء: عمود رأسي مع خط أفقي
    - حرف الواو: شكل دائري أو منحني
    """
    rows, cols = matrix.shape
    
    # Look for vertical line (هاء)
    vertical_lines = []
    for col in range(cols):
        column = matrix[:, col]
        if np.sum(column == 1) > rows * 0.6:  # Mostly black
            vertical_lines.append(col)
    
    # Look for horizontal line connected to vertical (هاء)
    has_horizontal_connection = False
    if len(vertical_lines) > 0:
        for v_col in vertical_lines:
            # Check middle rows for horizontal line
            middle = rows // 2
            if middle > 0 and middle < rows:
                row = matrix[middle, :]
                # Check if there's horizontal line near vertical
                if v_col < cols - 1:
                    if np.sum(row[v_col:v_col+2] == 1) >= 1:
                        has_horizontal_connection = True
    
    # Look for curved pattern (واو)
    # Check for U-shape or C-shape pattern
    has_curved_pattern = False
    middle = rows // 2
    if middle > 2 and middle < rows - 2:
        # Check for U-shape in middle columns
        for col in range(1, cols-1):
            # Check if pattern forms U or C
            top = matrix[middle-2, col]
            middle_val = matrix[middle, col]
            bottom = matrix[middle+2, col]
            
            # U-shape: black at top and bottom, white in middle
            # Or: white at top and bottom, black in middle
            if (top == 1 and bottom == 1 and middle_val == 0) or \
               (top == 0 and bottom == 0 and middle_val == 1):
                has_curved_pattern = True
                break
    
    is_hu_pattern = len(vertical_lines) > 0 and (has_horizontal_connection or has_curved_pattern)
    
    return {
        'is_hu': is_hu_pattern,
        'vertical_lines': len(vertical_lines),
        'has_horizontal_connection': has_horizontal_connection,
        'has_curved_pattern': has_curved_pattern
    }

def analyze_detailed(matrix, name):
    """Detailed analysis with symbol detection"""
    print(f"\n{'='*60}")
    print(f"Detailed Analysis: {name}")
    print(f"التحليل التفصيلي: {name}")
    print(f"{'='*60}")
    
    rows, cols = matrix.shape
    print(f"Matrix: {rows}×{cols}")
    print(f"Black pixels: {np.sum(matrix)} ({np.sum(matrix)/matrix.size*100:.1f}%)")
    
    # Symmetry
    if cols % 2 == 0:
        left = matrix[:, :cols//2]
        right = np.flip(matrix[:, cols//2:], axis=1)
        vertical_sym = np.sum(left == right) / left.size
    else:
        left = matrix[:, :cols//2]
        right = np.flip(matrix[:, cols//2+1:], axis=1)
        vertical_sym = np.sum(left == right) / left.size
    
    if rows % 2 == 0:
        top = matrix[:rows//2, :]
        bottom = np.flip(matrix[rows//2:, :], axis=0)
        horizontal_sym = np.sum(top == bottom) / top.size
    else:
        top = matrix[:rows//2, :]
        bottom = np.flip(matrix[rows//2+1:, :], axis=0)
        horizontal_sym = np.sum(top == bottom) / top.size
    
    print(f"\n📊 Symmetry:")
    print(f"   Vertical: {vertical_sym*100:.1f}%")
    print(f"   Horizontal: {horizontal_sym*100:.1f}%")
    
    # Heart detection
    widths = []
    for i in range(rows):
        row = matrix[i, :]
        black = np.where(row == 1)[0]
        widths.append(black[-1] - black[0] + 1 if len(black) > 0 else 0)
    
    middle = rows // 2
    top_w = np.mean(widths[:middle//2]) if middle//2 > 0 else 0
    mid_w = np.mean(widths[middle//2:middle+middle//2]) if middle+middle//2 <= rows else np.mean(widths[middle//2:])
    bot_w = np.mean(widths[middle+middle//2:]) if middle+middle//2 < rows else 0
    
    is_heart = (mid_w > top_w and mid_w > bot_w) or (top_w > bot_w and top_w > 0)
    
    print(f"\n❤️ Heart Shape:")
    print(f"   Detected: {'YES ✅' if is_heart else 'NO ❌'}")
    print(f"   Widths - Top: {top_w:.1f}, Middle: {mid_w:.1f}, Bottom: {bot_w:.1f}")
    
    # Kaaba detection
    kaaba = detect_kaaba_shape(matrix)
    print(f"\n🕋 Kaaba Shape:")
    print(f"   Detected: {'YES ✅' if kaaba else 'NO ❌'}")
    
    # "هو" detection
    hu = detect_hu_pattern(matrix)
    print(f"\n🔤 'هو' (He) Pattern:")
    print(f"   Detected: {'YES ✅' if hu['is_hu'] else 'NO ❌'}")
    print(f"   Vertical lines: {hu['vertical_lines']}")
    print(f"   Horizontal connection: {'YES ✅' if hu['has_horizontal_connection'] else 'NO ❌'}")
    print(f"   Curved pattern: {'YES ✅' if hu['has_curved_pattern'] else 'NO ❌'}")
    
    # Visual patterns
    vertical_pat = detect_vertical_patterns(matrix)
    horizontal_pat = detect_horizontal_patterns(matrix)
    
    print(f"\n📐 Pattern Details:")
    v_lines = sum(1 for k, v in vertical_pat.items() if 'vertical_line' in k and v)
    h_lines = sum(1 for k, v in horizontal_pat.items() if 'horizontal_line' in k and v)
    print(f"   Vertical lines: {v_lines}")
    print(f"   Horizontal lines: {h_lines}")
    
    return {
        'symmetry': {'vertical': vertical_sym, 'horizontal': horizontal_sym},
        'heart': is_heart,
        'kaaba': kaaba,
        'hu': hu,
        'matrix': matrix
    }

def main():
    """Analyze key patterns"""
    print("="*60)
    print("Detailed Pattern Analyzer")
    print("محلل الأنماط التفصيلي")
    print("="*60)
    
    # Al-Fatiha
    print("\n" + "="*60)
    print("1. Al-Fatiha (7 verses)")
    print("="*60)
    fatiha_matrix = generate_bitmap(7)
    fatiha_result = analyze_detailed(fatiha_matrix, "Al-Fatiha")
    
    # 99 Names
    print("\n" + "="*60)
    print("2. 99 Names of Allah")
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
    result_99 = analyze_detailed(matrix_99, "99 Names")
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY | الملخص")
    print("="*60)
    print("\nAl-Fatiha:")
    print(f"  Heart: {'✅' if fatiha_result['heart'] else '❌'}")
    print(f"  Kaaba: {'✅' if fatiha_result['kaaba'] else '❌'}")
    print(f"  'هو': {'✅' if fatiha_result['hu']['is_hu'] else '❌'}")
    
    print("\n99 Names:")
    print(f"  Heart: {'✅' if result_99['heart'] else '❌'}")
    print(f"  Kaaba: {'✅' if result_99['kaaba'] else '❌'}")
    print(f"  'هو': {'✅' if result_99['hu']['is_hu'] else '❌'}")

if __name__ == "__main__":
    main()

