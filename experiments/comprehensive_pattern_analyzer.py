"""
Comprehensive Pattern Analyzer - Analyze all 114 Surahs
محلل الأنماط الشامل - تحليل جميع السور الـ 114
"""
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import json
import sys
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent.parent / 'code'))
from quran_hearts import generate_bitmap, SURAHS

def detect_heart_shape(matrix):
    """Detect heart shape with improved algorithm"""
    rows, cols = matrix.shape
    widths = []
    for i in range(rows):
        row = matrix[i, :]
        black = np.where(row == 1)[0]
        widths.append(black[-1] - black[0] + 1 if len(black) > 0 else 0)
    
    # Symmetry
    if cols % 2 == 0:
        left = matrix[:, :cols//2]
        right = np.flip(matrix[:, cols//2:], axis=1)
        vertical_sym = np.sum(left == right) / left.size
    else:
        vertical_sym = 0
    
    # Width progression
    top_w = np.mean(widths[:rows//3]) if rows//3 > 0 else 0
    mid_w = np.mean(widths[rows//3:2*rows//3]) if 2*rows//3 <= rows else np.mean(widths[rows//3:])
    bot_w = np.mean(widths[2*rows//3:]) if 2*rows//3 < rows else 0
    
    # Heart: wider at top/middle, tapering to bottom
    is_heart = (top_w > bot_w * 1.1) or (mid_w > bot_w * 1.1) or (top_w > 0 and bot_w == 0)
    
    # Classic heart curve
    if len(widths) >= 5:
        first_third = np.mean(widths[:rows//3])
        second_third = np.mean(widths[rows//3:2*rows//3])
        third_third = np.mean(widths[2*rows//3:])
        if second_third > first_third * 1.2 and second_third > third_third * 1.2:
            is_heart = True
    
    return {
        'is_heart': is_heart,
        'symmetry': vertical_sym,
        'confidence': vertical_sym if is_heart else 0
    }

def detect_star_pattern(matrix):
    """Detect star/hexagonal pattern"""
    rows, cols = matrix.shape
    center_row, center_col = rows // 2, cols // 2
    
    # Star: triangular density distribution
    top_triangle = np.sum(matrix[:rows//2, :] == 1)
    bottom_triangle = np.sum(matrix[rows//2:, :] == 1)
    
    # Check for symmetry and triangular shape
    is_star = abs(top_triangle - bottom_triangle) < (top_triangle + bottom_triangle) * 0.2
    
    # Also check for hexagonal pattern (6-pointed star)
    if center_row > 2 and center_col > 2:
        center_region = matrix[center_row-2:center_row+3, center_col-2:center_col+3]
        center_density = np.sum(center_region == 1) / center_region.size
        is_star = is_star or (center_density > 0.4 and center_density < 0.7)
    
    return is_star

def detect_vertical_structures(matrix):
    """Detect vertical lines/structures"""
    rows, cols = matrix.shape
    vertical_lines = []
    
    for col in range(cols):
        column = matrix[:, col]
        black_ratio = np.sum(column == 1) / rows
        
        if black_ratio > 0.5:  # Strong vertical line
            vertical_lines.append({
                'column': col,
                'strength': black_ratio,
                'type': 'strong'
            })
        elif black_ratio > 0.3:  # Moderate vertical structure
            vertical_lines.append({
                'column': col,
                'strength': black_ratio,
                'type': 'moderate'
            })
    
    return vertical_lines

def detect_horizontal_structures(matrix):
    """Detect horizontal lines/structures"""
    rows, cols = matrix.shape
    horizontal_lines = []
    
    for row_idx in range(rows):
        row = matrix[row_idx, :]
        black_ratio = np.sum(row == 1) / cols
        
        if black_ratio > 0.7:  # Strong horizontal line
            horizontal_lines.append({
                'row': row_idx,
                'strength': black_ratio,
                'type': 'strong'
            })
    
    return horizontal_lines

def detect_divided_pattern(matrix):
    """Detect divided/split pattern"""
    rows, cols = matrix.shape
    middle_col = cols // 2
    
    # Check for vertical gap in middle
    middle_region = matrix[:, max(0, middle_col-1):min(cols, middle_col+2)]
    has_gap = np.sum(middle_region[:, 1] == 0) > rows * 0.3
    
    return has_gap

def detect_open_heart(matrix):
    """Detect open heart (expanded chest)"""
    rows, cols = matrix.shape
    widths = []
    
    for i in range(rows):
        row = matrix[i, :]
        black = np.where(row == 1)[0]
        widths.append(black[-1] - black[0] + 1 if len(black) > 0 else 0)
    
    top_w = np.mean(widths[:rows//3])
    mid_w = np.mean(widths[rows//3:2*rows//3])
    bot_w = np.mean(widths[2*rows//3:])
    
    is_open = mid_w > top_w * 1.5 and mid_w > bot_w * 1.5
    
    return is_open

def detect_sword_pattern(matrix):
    """Detect sword/blade pattern"""
    rows, cols = matrix.shape
    
    # Sword: strong vertical line
    for col in range(cols):
        column = matrix[:, col]
        if np.sum(column == 1) > rows * 0.6:
            return True
    
    return False

def detect_crown_pattern(matrix):
    """Detect crown pattern (wider at top)"""
    rows, cols = matrix.shape
    widths = []
    
    for i in range(rows):
        row = matrix[i, :]
        black = np.where(row == 1)[0]
        widths.append(black[-1] - black[0] + 1 if len(black) > 0 else 0)
    
    top_w = np.mean(widths[:rows//3])
    mid_w = np.mean(widths[rows//3:2*rows//3])
    bot_w = np.mean(widths[2*rows//3:])
    
    # Crown: significantly wider at top
    is_crown = top_w > mid_w * 1.3 and top_w > bot_w * 1.3
    
    return is_crown

def detect_key_pattern(matrix):
    """Detect key pattern (vertical with horizontal extension)"""
    rows, cols = matrix.shape
    
    # Key: vertical line with horizontal extension
    vertical_lines = detect_vertical_structures(matrix)
    horizontal_lines = detect_horizontal_structures(matrix)
    
    has_vertical = len([v for v in vertical_lines if v['type'] == 'strong']) > 0
    has_horizontal = len(horizontal_lines) > 0
    
    is_key = has_vertical and has_horizontal
    
    return is_key

def detect_lock_pattern(matrix):
    """Detect lock pattern (rectangular/square center)"""
    rows, cols = matrix.shape
    center_row, center_col = rows // 2, cols // 2
    
    if center_row > 1 and center_col > 1:
        center_region = matrix[center_row-1:center_row+2, center_col-1:center_col+2]
        center_density = np.sum(center_region == 1) / center_region.size
        
        # Lock: dense center with clear boundaries
        is_lock = center_density > 0.6
        
        # Check for boundaries
        if is_lock:
            if center_row > 2:
                top_edge = matrix[center_row-2, center_col-1:center_col+2]
                if np.sum(top_edge == 0) >= 1:
                    return True
        
        return is_lock
    
    return False

def detect_raised_hands(matrix):
    """Detect raised hands (two vertical structures on sides)"""
    rows, cols = matrix.shape
    
    left_col = matrix[:, 0]
    right_col = matrix[:, -1]
    
    left_vertical = np.sum(left_col == 1) > rows * 0.3
    right_vertical = np.sum(right_col == 1) > rows * 0.3
    
    if cols >= 4:
        left_inner = matrix[:, 1]
        right_inner = matrix[:, -2]
        left_inner_vertical = np.sum(left_inner == 1) > rows * 0.3
        right_inner_vertical = np.sum(right_inner == 1) > rows * 0.3
        
        is_hands = (left_vertical or left_inner_vertical) and (right_vertical or right_inner_vertical)
    else:
        is_hands = left_vertical and right_vertical
    
    if is_hands:
        top_half = matrix[:rows//2, :]
        bottom_half = matrix[rows//2:, :]
        top_density = np.sum(top_half == 1) / top_half.size
        bottom_density = np.sum(bottom_half == 1) / bottom_half.size
        is_hands = top_density > bottom_density * 1.1
    
    return is_hands

def detect_embryonic_clot(matrix):
    """Detect embryonic clot (dense, irregular center)"""
    rows, cols = matrix.shape
    center_row, center_col = rows // 2, cols // 2
    
    center_region = matrix[max(0, center_row-2):min(rows, center_row+3), 
                          max(0, center_col-2):min(cols, center_col+3)]
    
    center_density = np.sum(center_region == 1) / center_region.size
    
    if cols % 2 == 0:
        left = matrix[:, :cols//2]
        right = np.flip(matrix[:, cols//2:], axis=1)
        symmetry = np.sum(left == right) / left.size
    else:
        symmetry = 0.5
    
    is_clot = center_density > 0.4 and symmetry < 0.7
    
    return is_clot

def analyze_surah(surah_name, verse_count):
    """Comprehensive analysis of a single surah"""
    matrix = generate_bitmap(verse_count)
    
    # Run all detectors
    heart = detect_heart_shape(matrix)
    star = detect_star_pattern(matrix)
    vertical = detect_vertical_structures(matrix)
    horizontal = detect_horizontal_structures(matrix)
    divided = detect_divided_pattern(matrix)
    open_heart = detect_open_heart(matrix)
    sword = detect_sword_pattern(matrix)
    crown = detect_crown_pattern(matrix)
    key = detect_key_pattern(matrix)
    lock = detect_lock_pattern(matrix)
    hands = detect_raised_hands(matrix)
    clot = detect_embryonic_clot(matrix)
    
    # Calculate overall symmetry
    rows, cols = matrix.shape
    if cols % 2 == 0:
        left = matrix[:, :cols//2]
        right = np.flip(matrix[:, cols//2:], axis=1)
        vertical_sym = np.sum(left == right) / left.size
    else:
        vertical_sym = 0
    
    if rows % 2 == 0:
        top = matrix[:rows//2, :]
        bottom = np.flip(matrix[rows//2:, :], axis=0)
        horizontal_sym = np.sum(top == bottom) / top.size
    else:
        horizontal_sym = 0
    
    overall_symmetry = (vertical_sym + horizontal_sym) / 2
    
    # Collect detected patterns
    patterns = []
    if heart['is_heart']:
        patterns.append('Heart')
    if star:
        patterns.append('Star')
    if len(vertical) >= 2:
        patterns.append('Vertical Structures')
    if len(horizontal) > 0:
        patterns.append('Horizontal Lines')
    if divided:
        patterns.append('Divided')
    if open_heart:
        patterns.append('Open Heart')
    if sword:
        patterns.append('Sword')
    if crown:
        patterns.append('Crown')
    if key:
        patterns.append('Key')
    if lock:
        patterns.append('Lock')
    if hands:
        patterns.append('Raised Hands')
    if clot:
        patterns.append('Embryonic Clot')
    
    if not patterns:
        patterns.append('Other Pattern')
    
    return {
        'surah_name': surah_name,
        'verse_count': verse_count,
        'patterns': patterns,
        'symmetry': overall_symmetry,
        'heart_confidence': heart['confidence'],
        'details': {
            'heart': heart['is_heart'],
            'star': star,
            'vertical_structures': len(vertical),
            'horizontal_lines': len(horizontal),
            'divided': divided,
            'open_heart': open_heart,
            'sword': sword,
            'crown': crown,
            'key': key,
            'lock': lock,
            'hands': hands,
            'clot': clot
        }
    }

def main():
    """Analyze all 114 Surahs"""
    print("="*60)
    print("Comprehensive Pattern Analysis - All 114 Surahs")
    print("تحليل الأنماط الشامل - جميع السور الـ 114")
    print("="*60)
    
    results = []
    pattern_counts = defaultdict(int)
    
    for surah_name, verse_count in SURAHS:
        print(f"\nAnalyzing: {surah_name} ({verse_count} verses)...")
        result = analyze_surah(surah_name, verse_count)
        results.append(result)
        
        # Count patterns
        for pattern in result['patterns']:
            pattern_counts[pattern] += 1
        
        print(f"  Patterns: {', '.join(result['patterns'])}")
        print(f"  Symmetry: {result['symmetry']*100:.1f}%")
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY | الملخص")
    print("="*60)
    
    print(f"\nPattern Distribution:")
    for pattern, count in sorted(pattern_counts.items(), key=lambda x: -x[1]):
        print(f"  {pattern}: {count} Surahs")
    
    # Save results
    output_dir = Path('experiments_output/comprehensive_analysis')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save JSON
    with open(output_dir / 'all_patterns.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    # Save categorized results
    categorized = defaultdict(list)
    for result in results:
        for pattern in result['patterns']:
            categorized[pattern].append({
                'surah': result['surah_name'],
                'verses': result['verse_count'],
                'symmetry': result['symmetry'],
                'heart_confidence': result['heart_confidence']
            })
    
    with open(output_dir / 'categorized_patterns.json', 'w', encoding='utf-8') as f:
        json.dump(dict(categorized), f, ensure_ascii=False, indent=2)
    
    # Create summary report
    report = f"""# Comprehensive Pattern Analysis - All 114 Surahs
# تحليل الأنماط الشامل - جميع السور الـ 114

## Pattern Distribution | توزيع الأنماط

"""
    for pattern, count in sorted(pattern_counts.items(), key=lambda x: -x[1]):
        report += f"- **{pattern}**: {count} Surahs\n"
    
    report += "\n## Detailed Results | النتائج التفصيلية\n\n"
    
    # Group by pattern
    for pattern in sorted(pattern_counts.keys()):
        report += f"### {pattern}\n\n"
        surahs_with_pattern = [r for r in results if pattern in r['patterns']]
        for r in sorted(surahs_with_pattern, key=lambda x: -x['heart_confidence']):
            report += f"- **{r['surah_name']}** ({r['verse_count']} verses) - Symmetry: {r['symmetry']*100:.1f}%\n"
        report += "\n"
    
    with open(output_dir / 'ANALYSIS_REPORT.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ Analysis complete!")
    print(f"   Results saved to: {output_dir}")
    print(f"   - all_patterns.json: Complete analysis")
    print(f"   - categorized_patterns.json: Patterns by category")
    print(f"   - ANALYSIS_REPORT.md: Summary report")
    
    # Highlight special cases
    print("\n" + "="*60)
    print("SPECIAL CASES | حالات خاصة")
    print("="*60)
    
    # High symmetry
    high_sym = sorted([r for r in results if r['symmetry'] > 0.7], 
                      key=lambda x: -x['symmetry'])[:5]
    print("\nHighest Symmetry:")
    for r in high_sym:
        print(f"  {r['surah_name']}: {r['symmetry']*100:.1f}% - {', '.join(r['patterns'])}")
    
    # Strong heart patterns
    strong_hearts = sorted([r for r in results if r['heart_confidence'] > 0.5],
                           key=lambda x: -x['heart_confidence'])[:5]
    print("\nStrongest Heart Patterns:")
    for r in strong_hearts:
        print(f"  {r['surah_name']}: {r['heart_confidence']*100:.1f}% confidence - {', '.join(r['patterns'])}")
    
    # Multiple patterns
    multiple = sorted([r for r in results if len(r['patterns']) > 2],
                     key=lambda x: -len(x['patterns']))[:5]
    print("\nMost Complex Patterns (multiple symbols):")
    for r in multiple:
        print(f"  {r['surah_name']}: {', '.join(r['patterns'])}")

if __name__ == "__main__":
    main()

