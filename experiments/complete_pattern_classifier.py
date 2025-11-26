"""
Complete Pattern Classifier - Classify all 114 Surahs using 0-3 grading system
مصنف الأنماط الكامل - تصنيف جميع السور الـ 114 باستخدام نظام الدرجات 0-3
"""
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import json
import sys
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent.parent / 'code'))
from quran_hearts import generate_bitmap, SURAHS

def to_6bit(n):
    return format(n, '06b')

# Classification criteria from the table
CLASSIFICATION_CRITERIA = {
    0: {
        'name_ar': 'لا قلب',
        'name_en': 'No Heart',
        'criterion_ar': 'لا منحنى علوي مغلق، ولا تناظر عمودي',
        'criterion_en': 'No closed upper curve, and no vertical symmetry'
    },
    1: {
        'name_ar': 'قلب بدائي',
        'name_en': 'Primitive Heart',
        'criterion_ar': 'منحنى علوي مغلق، لكن قاع مفتوح أو غير متناظر',
        'criterion_en': 'Closed upper curve, but open or asymmetrical bottom'
    },
    2: {
        'name_ar': 'قلب متطور',
        'name_en': 'Developed Heart',
        'criterion_ar': 'قلب مغلق + رمز داخلي بسيط (مثل: نقطة، خط)',
        'criterion_en': 'Closed heart + simple internal symbol (e.g., dot, line)'
    },
    3: {
        'name_ar': 'قلب متكامل',
        'name_en': 'Integrated/Complete Heart',
        'criterion_ar': 'قلب متناظر + رمز داخلي واضح + ارتباط موضوعي قوي',
        'criterion_en': 'Symmetrical heart + clear internal symbol + strong thematic connection'
    }
}

def calculate_symmetry(matrix):
    """Calculate vertical and horizontal symmetry"""
    rows, cols = matrix.shape
    
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
    
    return {
        'vertical': vertical_sym,
        'horizontal': horizontal_sym,
        'overall': (vertical_sym + horizontal_sym) / 2
    }

def detect_upper_curve(matrix):
    """Detect closed upper curve (top of heart)"""
    rows, cols = matrix.shape
    top_quarter = max(rows // 4, 5)  # At least 5 rows
    
    # Check top region for curved pattern
    top_region = matrix[:top_quarter, :]
    
    # Calculate width progression in top region
    widths = []
    for i in range(top_quarter):
        row = top_region[i, :]
        black = np.where(row == 1)[0]
        widths.append(black[-1] - black[0] + 1 if len(black) > 0 else 0)
    
    # Upper curve: wider in middle of top region, narrower at edges
    if len(widths) >= 3:
        first = widths[0] if widths[0] > 0 else 0.1
        middle = np.mean(widths[1:-1]) if len(widths) > 2 else widths[len(widths)//2]
        last = widths[-1] if widths[-1] > 0 else 0.1
        
        # Closed curve: middle wider than edges (more lenient)
        is_closed = (middle > first * 1.1 and middle > last * 1.1) or \
                    (middle > 0 and first == 0 and last == 0)  # Curved shape
    else:
        is_closed = False
    
    # Also check for any curved pattern in top half
    if not is_closed:
        top_half = matrix[:rows//2, :]
        widths_half = []
        for i in range(rows//2):
            row = top_half[i, :]
            black = np.where(row == 1)[0]
            widths_half.append(black[-1] - black[0] + 1 if len(black) > 0 else 0)
        
        if len(widths_half) >= 3:
            first_h = widths_half[0] if widths_half[0] > 0 else 0.1
            mid_h = np.mean(widths_half[1:-1]) if len(widths_half) > 2 else widths_half[len(widths_half)//2]
            last_h = widths_half[-1] if widths_half[-1] > 0 else 0.1
            is_closed = mid_h > first_h * 1.05 and mid_h > last_h * 1.05
    
    return is_closed

def detect_closed_heart(matrix):
    """Detect closed heart (both top and bottom curves)"""
    rows, cols = matrix.shape
    
    # Check width progression
    widths = []
    for i in range(rows):
        row = matrix[i, :]
        black = np.where(row == 1)[0]
        widths.append(black[-1] - black[0] + 1 if len(black) > 0 else 0)
    
    top_third = rows // 3
    middle_third = rows // 3
    bottom_third = rows - 2 * (rows // 3)
    
    top_w = np.mean(widths[:top_third]) if top_third > 0 else 0
    mid_w = np.mean(widths[top_third:top_third+middle_third]) if top_third+middle_third <= rows else np.mean(widths[top_third:])
    bot_w = np.mean(widths[-bottom_third:]) if bottom_third > 0 else 0
    
    # Closed heart: wider in middle, tapering at both ends
    is_closed = (mid_w > top_w * 1.1 and mid_w > bot_w * 1.1) or \
                (top_w > 0 and bot_w > 0 and mid_w > 0)
    
    return is_closed

def detect_internal_symbol(matrix):
    """Detect simple internal symbol (dot, line)"""
    rows, cols = matrix.shape
    center_row, center_col = rows // 2, cols // 2
    
    # Check center region
    if center_row > 1 and center_col > 1:
        center_region = matrix[center_row-1:center_row+2, center_col-1:center_col+2]
        
        # Simple symbol: dot (single pixel) or line (vertical/horizontal)
        center_density = np.sum(center_region == 1) / center_region.size
        
        # Dot: single black pixel in center
        is_dot = center_region[1, 1] == 1 and np.sum(center_region == 1) == 1
        
        # Line: vertical or horizontal line through center
        vertical_line = np.sum(center_region[:, 1] == 1) == center_region.shape[0]
        horizontal_line = np.sum(center_region[1, :] == 1) == center_region.shape[1]
        is_line = vertical_line or horizontal_line
        
        is_simple_symbol = is_dot or is_line
    else:
        is_simple_symbol = False
    
    return is_simple_symbol

def detect_clear_internal_symbol(matrix):
    """Detect clear internal symbol (more complex than simple)"""
    rows, cols = matrix.shape
    center_row, center_col = rows // 2, cols // 2
    
    if center_row > 2 and center_col > 2:
        center_region = matrix[center_row-2:center_row+3, center_col-2:center_col+3]
        center_density = np.sum(center_region == 1) / center_region.size
        
        # Clear symbol: structured pattern in center (not just scattered)
        # Check for recognizable shapes
        is_clear = center_density > 0.3 and center_density < 0.8
        
        # Check for symmetry in center
        if center_region.shape[0] % 2 == 0 and center_region.shape[1] % 2 == 0:
            left = center_region[:, :center_region.shape[1]//2]
            right = np.flip(center_region[:, center_region.shape[1]//2:], axis=1)
            center_sym = np.sum(left == right) / left.size
            is_clear = is_clear and center_sym > 0.5
    else:
        is_clear = False
    
    return is_clear

def classify_surah(matrix, surah_name, verse_count):
    """Classify surah according to 0-3 grading system"""
    symmetry = calculate_symmetry(matrix)
    upper_curve = detect_upper_curve(matrix)
    closed_heart = detect_closed_heart(matrix)
    simple_symbol = detect_internal_symbol(matrix)
    clear_symbol = detect_clear_internal_symbol(matrix)
    
    # Calculate additional metrics
    rows, cols = matrix.shape
    widths = []
    for i in range(rows):
        row = matrix[i, :]
        black = np.where(row == 1)[0]
        widths.append(black[-1] - black[0] + 1 if len(black) > 0 else 0)
    
    # Check for heart-like width progression
    top_w = np.mean(widths[:rows//3]) if rows//3 > 0 else 0
    mid_w = np.mean(widths[rows//3:2*rows//3]) if 2*rows//3 <= rows else np.mean(widths[rows//3:])
    bot_w = np.mean(widths[2*rows//3:]) if 2*rows//3 < rows else 0
    
    has_heart_shape = (mid_w > top_w * 1.1 and mid_w > bot_w * 1.1) or \
                      (top_w > bot_w * 1.2) or \
                      (mid_w > 0 and top_w > 0 and bot_w > 0)
    
    # Grade 3: Integrated/Complete heart
    # Symmetrical heart + clear internal symbol + high symmetry
    if closed_heart and clear_symbol and symmetry['overall'] >= 0.55:
        grade = 3
        reason = "Symmetrical heart with clear internal symbol and high symmetry"
    
    # Grade 2: Developed heart
    # Closed heart + simple internal symbol OR high symmetry with heart shape
    elif (closed_heart and simple_symbol) or \
         (has_heart_shape and symmetry['overall'] >= 0.5 and simple_symbol):
        grade = 2
        reason = "Closed heart with simple internal symbol"
    
    # Grade 1: Primitive heart
    # Closed upper curve BUT open or asymmetrical bottom
    # OR heart shape with moderate symmetry
    elif upper_curve and (not closed_heart or symmetry['vertical'] < 0.5):
        grade = 1
        reason = "Closed upper curve but open/asymmetrical bottom"
    elif has_heart_shape and symmetry['vertical'] >= 0.35:
        grade = 1
        reason = "Heart-like shape with moderate symmetry"
    
    # Grade 0: No heart
    # No closed upper curve AND no vertical symmetry AND no heart shape
    else:
        grade = 0
        reason = "No closed upper curve, low vertical symmetry, and no heart shape"
    
    return {
        'grade': grade,
        'grade_name_ar': CLASSIFICATION_CRITERIA[grade]['name_ar'],
        'grade_name_en': CLASSIFICATION_CRITERIA[grade]['name_en'],
        'symmetry': symmetry,
        'upper_curve': upper_curve,
        'closed_heart': closed_heart,
        'simple_symbol': simple_symbol,
        'clear_symbol': clear_symbol,
        'has_heart_shape': has_heart_shape,
        'reason': reason
    }

def analyze_all_surahs():
    """Analyze and classify all 114 Surahs"""
    print("="*60)
    print("Complete Pattern Classification - All 114 Surahs")
    print("تصنيف الأنماط الكامل - جميع السور الـ 114")
    print("="*60)
    
    results = []
    grade_counts = defaultdict(int)
    
    for surah_name, verse_count in SURAHS:
        print(f"\nAnalyzing: {surah_name} ({verse_count} verses)...")
        
        matrix = generate_bitmap(verse_count)
        classification = classify_surah(matrix, surah_name, verse_count)
        
        result = {
            'surah_name': surah_name,
            'verse_count': verse_count,
            'grade': classification['grade'],
            'grade_name_ar': classification['grade_name_ar'],
            'grade_name_en': classification['grade_name_en'],
            'symmetry': {
                'vertical': float(classification['symmetry']['vertical']),
                'horizontal': float(classification['symmetry']['horizontal']),
                'overall': float(classification['symmetry']['overall'])
            },
            'features': {
                'upper_curve': bool(classification['upper_curve']),
                'closed_heart': bool(classification['closed_heart']),
                'simple_symbol': bool(classification['simple_symbol']),
                'clear_symbol': bool(classification['clear_symbol']),
                'has_heart_shape': bool(classification.get('has_heart_shape', False))
            },
            'reason': classification['reason']
        }
        
        results.append(result)
        grade_counts[classification['grade']] += 1
        
        print(f"  Grade: {classification['grade']} - {classification['grade_name_en']}")
        print(f"  Symmetry: {classification['symmetry']['overall']*100:.1f}%")
        print(f"  Reason: {classification['reason']}")
    
    # Summary
    print("\n" + "="*60)
    print("CLASSIFICATION SUMMARY | ملخص التصنيف")
    print("="*60)
    
    for grade in sorted(grade_counts.keys()):
        count = grade_counts[grade]
        grade_info = CLASSIFICATION_CRITERIA[grade]
        print(f"\nGrade {grade} - {grade_info['name_en']} ({grade_info['name_ar']}): {count} Surahs")
        print(f"  Criterion: {grade_info['criterion_en']}")
    
    # Save results
    output_dir = Path('experiments_output/complete_classification')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save JSON
    with open(output_dir / 'all_classifications.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    # Save by grade
    by_grade = defaultdict(list)
    for result in results:
        by_grade[result['grade']].append({
            'surah': result['surah_name'],
            'verses': result['verse_count'],
            'symmetry': result['symmetry']['overall'],
            'reason': result['reason']
        })
    
    with open(output_dir / 'classified_by_grade.json', 'w', encoding='utf-8') as f:
        json.dump(dict(by_grade), f, ensure_ascii=False, indent=2)
    
    # Create detailed report
    report = f"""# Complete Pattern Classification - All 114 Surahs
# تصنيف الأنماط الكامل - جميع السور الـ 114

## Classification System | نظام التصنيف

"""
    for grade, info in CLASSIFICATION_CRITERIA.items():
        report += f"### Grade {grade}: {info['name_en']} ({info['name_ar']})\n\n"
        report += f"**Criterion:** {info['criterion_en']}\n\n"
        report += f"**المعيار:** {info['criterion_ar']}\n\n"
    
    report += "\n## Distribution | التوزيع\n\n"
    for grade in sorted(grade_counts.keys()):
        count = grade_counts[grade]
        percentage = (count / 114) * 100
        grade_info = CLASSIFICATION_CRITERIA[grade]
        report += f"- **Grade {grade} - {grade_info['name_en']}**: {count} Surahs ({percentage:.1f}%)\n"
    
    report += "\n## Detailed Results by Grade | النتائج التفصيلية حسب الدرجة\n\n"
    
    for grade in sorted(by_grade.keys(), reverse=True):
        grade_info = CLASSIFICATION_CRITERIA[grade]
        report += f"### Grade {grade}: {grade_info['name_en']} ({grade_info['name_ar']})\n\n"
        
        surahs = sorted(by_grade[grade], key=lambda x: -x['symmetry'])
        for surah in surahs:
            report += f"- **{surah['surah']}** ({surah['verses']} verses) - "
            report += f"Symmetry: {surah['symmetry']*100:.1f}%\n"
            report += f"  - {surah['reason']}\n"
        report += "\n"
    
    with open(output_dir / 'CLASSIFICATION_REPORT.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    # Generate images for each grade
    print("\n" + "="*60)
    print("Generating images by grade...")
    print("="*60)
    
    for grade in sorted(by_grade.keys(), reverse=True):
        grade_info = CLASSIFICATION_CRITERIA[grade]
        grade_dir = output_dir / f"grade_{grade}_{grade_info['name_en'].lower().replace(' ', '_')}"
        grade_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\nGrade {grade} - {grade_info['name_en']}:")
        for surah_data in by_grade[grade][:10]:  # First 10 of each grade
            surah_name = surah_data['surah']
            verse_count = surah_data['verses']
            
            matrix = generate_bitmap(verse_count)
            
            plt.figure(figsize=(3, 6))
            plt.imshow(matrix, cmap='binary', interpolation='nearest', aspect='auto')
            plt.axis('off')
            plt.title(f'{surah_name}\nGrade {grade}: {grade_info["name_en"]}\nSymmetry: {surah_data["symmetry"]*100:.1f}%', 
                     fontsize=9, pad=10)
            plt.tight_layout()
            
            filename = f"{surah_name.replace(' ', '_').replace("'", '')}.png"
            plt.savefig(grade_dir / filename, dpi=150, bbox_inches='tight')
            plt.close()
            
            print(f"  ✅ {surah_name}")
    
    print(f"\n✅ Complete classification saved to: {output_dir}")
    print(f"   - all_classifications.json: Complete analysis")
    print(f"   - classified_by_grade.json: Grouped by grade")
    print(f"   - CLASSIFICATION_REPORT.md: Detailed report")
    print(f"   - grade_* folders: Sample images by grade")
    
    return results

if __name__ == "__main__":
    results = analyze_all_surahs()

