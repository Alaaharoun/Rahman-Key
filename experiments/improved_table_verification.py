"""
Improved Pattern Verification - Enhanced detection algorithms
التحقق المحسّن من الأنماط - خوارزميات كشف محسّنة
"""
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / 'code'))
from quran_hearts import generate_bitmap

# Surah verse counts
SURAH_DATA = {
    'Al-Alaq': 19,
    'Al-Fatiha': 7,
    'Al-Sharh': 8,
    'Al-Ikhlas': 4,
    'Ar-Rahman': 78,
    'An-Nasr': 3
}

def analyze_matrix_detailed(matrix, surah_name):
    """Detailed matrix analysis"""
    rows, cols = matrix.shape
    
    # Print matrix for visual inspection
    print(f"\nMatrix Visualization ({rows}×{cols}):")
    print("   " + " ".join([str(i) for i in range(cols)]))
    for i, row in enumerate(matrix):
        row_str = " ".join(["█" if cell == 1 else "░" for cell in row])
        print(f"{i:2d} {row_str}")
    
    # Column analysis
    print(f"\nColumn Analysis:")
    for col in range(cols):
        column = matrix[:, col]
        black_count = np.sum(column == 1)
        pattern = "".join(["█" if c == 1 else "░" for c in column])
        print(f"   Col {col}: {black_count}/{rows} black | {pattern}")
    
    # Row analysis
    print(f"\nRow Analysis (width of black region):")
    widths = []
    for i, row in enumerate(matrix):
        black = np.where(row == 1)[0]
        width = black[-1] - black[0] + 1 if len(black) > 0 else 0
        widths.append(width)
        if i < 5 or i >= rows - 5 or i == rows // 2:
            print(f"   Row {i:2d}: width={width}")
    
    return widths

def detect_heart_improved(matrix):
    """Improved heart detection"""
    rows, cols = matrix.shape
    
    # Calculate widths
    widths = []
    for i in range(rows):
        row = matrix[i, :]
        black = np.where(row == 1)[0]
        widths.append(black[-1] - black[0] + 1 if len(black) > 0 else 0)
    
    # Heart characteristics:
    # 1. Symmetrical
    # 2. Wider in middle or top, narrower at bottom
    # 3. Curved edges
    
    # Check symmetry
    if cols % 2 == 0:
        left = matrix[:, :cols//2]
        right = np.flip(matrix[:, cols//2:], axis=1)
        vertical_sym = np.sum(left == right) / left.size
    else:
        vertical_sym = 0
    
    # Check width progression
    top_w = np.mean(widths[:rows//3])
    mid_w = np.mean(widths[rows//3:2*rows//3])
    bot_w = np.mean(widths[2*rows//3:])
    
    # Heart: wider at top/middle, tapering to bottom
    is_heart = (top_w > bot_w * 1.1) or (mid_w > bot_w * 1.1) or (top_w > 0 and bot_w == 0)
    
    # Also check for heart-like curve
    if len(widths) >= 5:
        # Heart curve: increase then decrease
        first_third = np.mean(widths[:rows//3])
        second_third = np.mean(widths[rows//3:2*rows//3])
        third_third = np.mean(widths[2*rows//3:])
        
        # Classic heart: wider in middle, narrow at top and bottom
        if second_third > first_third * 1.2 and second_third > third_third * 1.2:
            is_heart = True
    
    return {
        'is_heart': is_heart,
        'symmetry': vertical_sym,
        'widths': widths,
        'top_width': top_w,
        'middle_width': mid_w,
        'bottom_width': bot_w
    }

def detect_open_heart_improved(matrix):
    """Improved open heart detection"""
    rows, cols = matrix.shape
    
    widths = []
    for i in range(rows):
        row = matrix[i, :]
        black = np.where(row == 1)[0]
        widths.append(black[-1] - black[0] + 1 if len(black) > 0 else 0)
    
    # Open heart: significantly wider in middle
    top_w = np.mean(widths[:rows//3])
    mid_w = np.mean(widths[rows//3:2*rows//3])
    bot_w = np.mean(widths[2*rows//3:])
    
    # Open heart: middle much wider (like expanded chest)
    is_open = mid_w > top_w * 1.5 and mid_w > bot_w * 1.5
    
    # Also check for "opening" - white space in center
    center_row = rows // 2
    center_col = cols // 2
    if center_row > 0 and center_col > 0:
        center_val = matrix[center_row, center_col]
        # Open: center might be white or sparse
        center_region = matrix[max(0, center_row-1):min(rows, center_row+2), 
                               max(0, center_col-1):min(cols, center_col+2)]
        center_density = np.sum(center_region == 1) / center_region.size
        # Open heart: wider middle but not too dense in center
        is_open = is_open and (center_density < 0.7 or mid_w > top_w * 2)
    
    return is_open

def detect_raised_hands_improved(matrix):
    """Improved raised hands detection"""
    rows, cols = matrix.shape
    
    # Raised hands: two vertical structures, one on each side
    # Could be in columns 0 and 5, or columns 1 and 4, etc.
    
    # Check outer columns
    left_col = matrix[:, 0]
    right_col = matrix[:, -1]
    
    left_vertical = np.sum(left_col == 1) > rows * 0.3
    right_vertical = np.sum(right_col == 1) > rows * 0.3
    
    # Also check inner columns
    if cols >= 4:
        left_inner = matrix[:, 1]
        right_inner = matrix[:, -2]
        left_inner_vertical = np.sum(left_inner == 1) > rows * 0.3
        right_inner_vertical = np.sum(right_inner == 1) > rows * 0.3
        
        # Hands: vertical structures on both sides
        is_hands = (left_vertical or left_inner_vertical) and (right_vertical or right_inner_vertical)
    else:
        is_hands = left_vertical and right_vertical
    
    # Check if they're "raised" - more black in upper half
    if is_hands:
        top_half = matrix[:rows//2, :]
        bottom_half = matrix[rows//2:, :]
        top_density = np.sum(top_half == 1) / top_half.size
        bottom_density = np.sum(bottom_half == 1) / bottom_half.size
        
        # Raised: more density in top half
        is_hands = top_density > bottom_density * 1.1
    
    return is_hands

def detect_perfect_heart_improved(matrix):
    """Improved perfect heart detection"""
    rows, cols = matrix.shape
    
    # Perfect heart: very high symmetry, clean pattern
    
    # Vertical symmetry
    if cols % 2 == 0:
        left = matrix[:, :cols//2]
        right = np.flip(matrix[:, cols//2:], axis=1)
        vertical_sym = np.sum(left == right) / left.size
    else:
        vertical_sym = 0
    
    # Horizontal symmetry
    if rows % 2 == 0:
        top = matrix[:rows//2, :]
        bottom = np.flip(matrix[rows//2:, :], axis=0)
        horizontal_sym = np.sum(top == bottom) / top.size
    else:
        horizontal_sym = 0
    
    overall_sym = (vertical_sym + horizontal_sym) / 2
    
    # Perfect heart: very high symmetry (>75%)
    # Also check for clean pattern (not too many scattered pixels)
    widths = []
    for i in range(rows):
        row = matrix[i, :]
        black = np.where(row == 1)[0]
        widths.append(black[-1] - black[0] + 1 if len(black) > 0 else 0)
    
    # Clean: consistent width pattern
    width_variance = np.var(widths)
    is_clean = width_variance < np.mean(widths) * 2
    
    is_perfect = overall_sym > 0.75 and is_clean
    
    return {
        'is_perfect': is_perfect,
        'symmetry': overall_sym,
        'clean': is_clean
    }

def verify_surah(surah_name_ar, surah_name_en, expected_pattern, verse_count):
    """Verify a single surah"""
    print(f"\n{'='*60}")
    print(f"{surah_name_ar} ({surah_name_en})")
    print(f"Expected: {expected_pattern}")
    print(f"Verse count: {verse_count}")
    print(f"{'='*60}")
    
    # Generate matrix
    matrix = generate_bitmap(verse_count)
    
    # Detailed analysis
    widths = analyze_matrix_detailed(matrix, surah_name_en)
    
    # Improved detections
    heart = detect_heart_improved(matrix)
    open_heart = detect_open_heart_improved(matrix)
    hands = detect_raised_hands_improved(matrix)
    perfect = detect_perfect_heart_improved(matrix)
    
    # Other detections (from previous script)
    from verify_table_patterns import (
        detect_divided_heart, detect_star_of_david, 
        detect_embryonic_clot, detect_sword
    )
    
    divided = detect_divided_heart(matrix)
    star = detect_star_of_david(matrix)
    clot = detect_embryonic_clot(matrix)
    sword = detect_sword(matrix)
    
    print(f"\n📊 Improved Algorithmic Results:")
    print(f"   Heart shape: {'✅ YES' if heart['is_heart'] else '❌ NO'} (symmetry: {heart['symmetry']*100:.1f}%)")
    print(f"   Open heart: {'✅ YES' if open_heart else '❌ NO'}")
    print(f"   Raised hands: {'✅ YES' if hands else '❌ NO'}")
    print(f"   Perfect heart: {'✅ YES' if perfect['is_perfect'] else '❌ NO'} (symmetry: {perfect['symmetry']*100:.1f}%)")
    print(f"   Divided heart: {'✅ YES' if divided else '❌ NO'}")
    print(f"   Star of David: {'✅ YES' if star else '❌ NO'}")
    print(f"   Embryonic clot: {'✅ YES' if clot else '❌ NO'}")
    print(f"   Sword: {'✅ YES' if sword else '❌ NO'}")
    
    # Match expected
    expected_lower = expected_pattern.lower()
    matches = []
    
    if 'قلب' in expected_pattern or 'heart' in expected_lower:
        if 'مثالي' in expected_pattern or 'perfect' in expected_lower:
            matches.append(('Perfect heart', perfect['is_perfect']))
        elif 'مفتوح' in expected_pattern or 'open' in expected_lower:
            matches.append(('Open heart', open_heart))
        elif 'منقسم' in expected_pattern or 'divided' in expected_lower:
            matches.append(('Divided heart', divided))
        else:
            matches.append(('Heart', heart['is_heart']))
    
    if 'يدين' in expected_pattern or 'hands' in expected_lower:
        matches.append(('Raised hands', hands))
    
    if 'نجمة' in expected_pattern or 'star' in expected_lower:
        matches.append(('Star of David', star))
    
    if 'علقة' in expected_pattern or 'clot' in expected_lower:
        matches.append(('Embryonic clot', clot))
    
    if 'سيف' in expected_pattern or 'sword' in expected_lower:
        matches.append(('Sword', sword))
    
    print(f"\n🎯 Pattern Matching:")
    for pattern_name, detected in matches:
        status = '✅ MATCH' if detected else '❌ NOT DETECTED'
        print(f"   {pattern_name}: {status}")
    
    return {
        'heart': heart,
        'open_heart': open_heart,
        'hands': hands,
        'perfect': perfect,
        'matches': matches
    }

def main():
    """Run improved verification"""
    print("="*60)
    print("Improved Pattern Verification")
    print("التحقق المحسّن من الأنماط")
    print("="*60)
    
    test_cases = [
        ('العلق', 'Al-Alaq', 'قلب + علقة جنينية', 19),
        ('الفاتحة', 'Al-Fatiha', 'قلب + يدين مرفوعتين', 7),
        ('الشرح', 'Al-Sharh', 'قلب مفتوح (كصدر منشرح)', 8),
        ('الإخلاص', 'Al-Ikhlas', 'قلب + نجمة داود', 4),
        ('الرحمن', 'Ar-Rahman', 'قلب مثالي — بدون رموز، نقاء عددي محض', 78),
        ('النصر', 'An-Nasr', 'قلب منقسم + سيف', 3),
    ]
    
    results = []
    for surah_ar, surah_en, expected, verse_count in test_cases:
        result = verify_surah(surah_ar, surah_en, expected, verse_count)
        results.append((surah_en, result))
    
    # Summary
    print("\n" + "="*60)
    print("IMPROVED SUMMARY | الملخص المحسّن")
    print("="*60)
    
    for (surah_en, result), (_, _, expected, _) in zip(results, test_cases):
        print(f"\n{surah_en}:")
        detected = sum(1 for _, d in result['matches'] if d)
        total = len(result['matches'])
        if total > 0:
            print(f"  Detected: {detected}/{total} patterns ({detected/total*100:.0f}%)")
        print(f"  Heart: {result['heart']['is_heart']}, Perfect: {result['perfect']['is_perfect']}")

if __name__ == "__main__":
    main()

