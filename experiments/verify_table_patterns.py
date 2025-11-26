"""
Verify patterns from the classification table
التحقق من الأنماط من جدول التصنيف
"""
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / 'code'))
from quran_hearts import generate_bitmap, SURAHS

def to_6bit(n):
    return format(n, '06b')

# Table data from the image
TABLE_DATA = [
    {
        'revelation_order': 1,
        'surah_name_ar': 'العلق',
        'surah_name_en': 'Al-Alaq',
        'expected_pattern': 'قلب + علقة جنينية',
        'expected_en': 'Heart + embryonic clot',
        'grade': 3
    },
    {
        'revelation_order': 5,
        'surah_name_ar': 'الفاتحة',
        'surah_name_en': 'Al-Fatiha',
        'expected_pattern': 'قلب + يدين مرفوعتين',
        'expected_en': 'Heart + two raised hands',
        'grade': 3
    },
    {
        'revelation_order': 11,
        'surah_name_ar': 'الشرح',
        'surah_name_en': 'Al-Sharh',
        'expected_pattern': 'قلب مفتوح (كصدر منشرح)',
        'expected_en': 'Open heart (like an expanded chest)',
        'grade': 3
    },
    {
        'revelation_order': 14,
        'surah_name_ar': 'الإخلاص',
        'surah_name_en': 'Al-Ikhlas',
        'expected_pattern': 'قلب + نجمة داود',
        'expected_en': 'Heart + Star of David',
        'grade': 3
    },
    {
        'revelation_order': 97,
        'surah_name_ar': 'الرحمن',
        'surah_name_en': 'Ar-Rahman',
        'expected_pattern': 'قلب مثالي — بدون رموز، نقاء عددي محض',
        'expected_en': 'Perfect heart — without symbols, pure numerical purity',
        'grade': '3 (أعلى تنقية)'
    },
    {
        'revelation_order': 111,
        'surah_name_ar': 'النصر',
        'surah_name_en': 'An-Nasr',
        'expected_pattern': 'قلب منقسم + سيف',
        'expected_en': 'Divided heart + sword',
        'grade': 2
    }
]

# Map Arabic names to verse counts
SURAH_VERSE_COUNTS = {
    'Al-Alaq': 19,
    'Al-Fatiha': 7,
    'Al-Sharh': 8,
    'Al-Ikhlas': 4,
    'Ar-Rahman': 78,
    'An-Nasr': 3
}

def detect_heart_shape(matrix):
    """Detect heart shape"""
    rows, cols = matrix.shape
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
    
    # Calculate symmetry
    if cols % 2 == 0:
        left = matrix[:, :cols//2]
        right = np.flip(matrix[:, cols//2:], axis=1)
        vertical_sym = np.sum(left == right) / left.size
    else:
        left = matrix[:, :cols//2]
        right = np.flip(matrix[:, cols//2+1:], axis=1)
        vertical_sym = np.sum(left == right) / left.size
    
    return {
        'is_heart': is_heart,
        'symmetry': vertical_sym,
        'widths': widths,
        'top_width': top_w,
        'middle_width': mid_w,
        'bottom_width': bot_w
    }

def detect_open_heart(matrix):
    """Detect open heart (expanded chest pattern)"""
    rows, cols = matrix.shape
    middle = rows // 2
    
    # Open heart: wider in middle, narrow at top and bottom
    widths = []
    for i in range(rows):
        row = matrix[i, :]
        black = np.where(row == 1)[0]
        widths.append(black[-1] - black[0] + 1 if len(black) > 0 else 0)
    
    top_w = np.mean(widths[:rows//3])
    mid_w = np.mean(widths[rows//3:2*rows//3])
    bot_w = np.mean(widths[2*rows//3:])
    
    # Open heart: middle significantly wider
    is_open = mid_w > top_w * 1.3 and mid_w > bot_w * 1.3
    
    return is_open

def detect_divided_heart(matrix):
    """Detect divided heart (split pattern)"""
    rows, cols = matrix.shape
    middle_col = cols // 2
    
    # Check if there's a vertical gap in the middle
    middle_region = matrix[:, max(0, middle_col-1):min(cols, middle_col+2)]
    
    # Divided: white line in middle
    has_gap = np.sum(middle_region[:, 1] == 0) > rows * 0.3
    
    return has_gap

def detect_star_of_david(matrix):
    """Detect Star of David pattern (hexagonal/star shape)"""
    rows, cols = matrix.shape
    center_row, center_col = rows // 2, cols // 2
    
    # Star of David: triangular patterns
    # Check for triangular density distribution
    top_triangle = np.sum(matrix[:rows//2, :] == 1)
    bottom_triangle = np.sum(matrix[rows//2:, :] == 1)
    
    # Check for symmetry and triangular shape
    is_star = abs(top_triangle - bottom_triangle) < (top_triangle + bottom_triangle) * 0.2
    
    return is_star

def detect_raised_hands(matrix):
    """Detect raised hands pattern (two vertical structures at sides)"""
    rows, cols = matrix.shape
    
    # Check left and right columns for vertical structures
    left_col = matrix[:, 0]
    right_col = matrix[:, -1]
    
    left_vertical = np.sum(left_col == 1) > rows * 0.4
    right_vertical = np.sum(right_col == 1) > rows * 0.4
    
    # Raised hands: vertical structures on both sides
    is_hands = left_vertical and right_vertical
    
    return is_hands

def detect_embryonic_clot(matrix):
    """Detect embryonic clot pattern (dense center with irregular shape)"""
    rows, cols = matrix.shape
    center_row, center_col = rows // 2, cols // 2
    
    # Embryonic clot: dense, irregular center
    center_region = matrix[max(0, center_row-2):min(rows, center_row+3), 
                          max(0, center_col-2):min(cols, center_col+3)]
    
    center_density = np.sum(center_region == 1) / center_region.size
    
    # Check for irregularity (not perfectly symmetric)
    if cols % 2 == 0:
        left = matrix[:, :cols//2]
        right = np.flip(matrix[:, cols//2:], axis=1)
        symmetry = np.sum(left == right) / left.size
    else:
        symmetry = 0.5
    
    is_clot = center_density > 0.4 and symmetry < 0.7  # Dense but irregular
    
    return is_clot

def detect_sword(matrix):
    """Detect sword pattern (vertical line or blade)"""
    rows, cols = matrix.shape
    
    # Sword: strong vertical line
    for col in range(cols):
        column = matrix[:, col]
        if np.sum(column == 1) > rows * 0.6:  # Mostly black
            return True
    
    return False

def detect_perfect_heart(matrix):
    """Detect perfect heart (high symmetry, pure pattern)"""
    rows, cols = matrix.shape
    
    # Calculate symmetry
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
    
    overall_sym = (vertical_sym + horizontal_sym) / 2
    
    # Perfect heart: very high symmetry (>80%)
    is_perfect = overall_sym > 0.8
    
    return {
        'is_perfect': is_perfect,
        'symmetry': overall_sym
    }

def analyze_surah(surah_data):
    """Analyze a single surah"""
    surah_name = surah_data['surah_name_en']
    verse_count = SURAH_VERSE_COUNTS[surah_name]
    
    print(f"\n{'='*60}")
    print(f"{surah_data['surah_name_ar']} ({surah_name})")
    print(f"Revelation Order: {surah_data['revelation_order']}")
    print(f"Expected: {surah_data['expected_pattern']}")
    print(f"{'='*60}")
    
    # Generate matrix
    matrix = generate_bitmap(verse_count)
    
    # Detect patterns
    heart = detect_heart_shape(matrix)
    open_heart = detect_open_heart(matrix)
    divided = detect_divided_heart(matrix)
    star = detect_star_of_david(matrix)
    hands = detect_raised_hands(matrix)
    clot = detect_embryonic_clot(matrix)
    sword = detect_sword(matrix)
    perfect = detect_perfect_heart(matrix)
    
    # Results
    print(f"\n📊 Algorithmic Results:")
    print(f"   Heart shape: {'✅ YES' if heart['is_heart'] else '❌ NO'} (symmetry: {heart['symmetry']*100:.1f}%)")
    print(f"   Open heart: {'✅ YES' if open_heart else '❌ NO'}")
    print(f"   Divided heart: {'✅ YES' if divided else '❌ NO'}")
    print(f"   Star of David: {'✅ YES' if star else '❌ NO'}")
    print(f"   Raised hands: {'✅ YES' if hands else '❌ NO'}")
    print(f"   Embryonic clot: {'✅ YES' if clot else '❌ NO'}")
    print(f"   Sword: {'✅ YES' if sword else '❌ NO'}")
    print(f"   Perfect heart: {'✅ YES' if perfect['is_perfect'] else '❌ NO'} (symmetry: {perfect['symmetry']*100:.1f}%)")
    
    # Match expected pattern
    expected = surah_data['expected_pattern']
    matches = []
    
    if 'قلب' in expected or 'heart' in expected.lower():
        matches.append(('Heart', heart['is_heart']))
    
    if 'مفتوح' in expected or 'open' in expected.lower():
        matches.append(('Open heart', open_heart))
    
    if 'منقسم' in expected or 'divided' in expected.lower():
        matches.append(('Divided heart', divided))
    
    if 'نجمة' in expected or 'star' in expected.lower():
        matches.append(('Star of David', star))
    
    if 'يدين' in expected or 'hands' in expected.lower():
        matches.append(('Raised hands', hands))
    
    if 'علقة' in expected or 'clot' in expected.lower():
        matches.append(('Embryonic clot', clot))
    
    if 'سيف' in expected or 'sword' in expected.lower():
        matches.append(('Sword', sword))
    
    if 'مثالي' in expected or 'perfect' in expected.lower():
        matches.append(('Perfect heart', perfect['is_perfect']))
    
    print(f"\n🎯 Pattern Matching:")
    for pattern_name, detected in matches:
        status = '✅ MATCH' if detected else '❌ NOT DETECTED'
        print(f"   {pattern_name}: {status}")
    
    # Visualize
    output_dir = Path('experiments_output/table_verification')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    fig, ax = plt.subplots(figsize=(4, 8))
    ax.imshow(matrix, cmap='binary', interpolation='nearest', aspect='auto')
    ax.axis('off')
    ax.set_title(f"{surah_data['surah_name_ar']}\n{surah_name}\n{surah_data['expected_pattern']}", 
                 fontsize=10, pad=10)
    plt.tight_layout()
    plt.savefig(output_dir / f"{surah_data['revelation_order']:03d}_{surah_name}.png", 
                dpi=150, bbox_inches='tight')
    plt.close()
    
    return {
        'surah': surah_name,
        'heart': heart,
        'open_heart': open_heart,
        'divided': divided,
        'star': star,
        'hands': hands,
        'clot': clot,
        'sword': sword,
        'perfect': perfect,
        'matches': matches
    }

def main():
    """Verify all patterns from the table"""
    print("="*60)
    print("Pattern Verification from Classification Table")
    print("التحقق من الأنماط من جدول التصنيف")
    print("="*60)
    
    results = []
    for surah_data in TABLE_DATA:
        result = analyze_surah(surah_data)
        results.append(result)
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY | الملخص")
    print("="*60)
    
    for surah_data, result in zip(TABLE_DATA, results):
        print(f"\n{surah_data['surah_name_ar']} ({surah_data['surah_name_en']}):")
        print(f"  Expected: {surah_data['expected_pattern']}")
        
        # Count matches
        detected_count = sum(1 for _, detected in result['matches'] if detected)
        total_count = len(result['matches'])
        
        if total_count > 0:
            match_rate = detected_count / total_count * 100
            print(f"  Detected: {detected_count}/{total_count} patterns ({match_rate:.0f}%)")
        else:
            print(f"  Detected: Heart={result['heart']['is_heart']}, Perfect={result['perfect']['is_perfect']}")
    
    print("\n" + "="*60)
    print("✅ Verification complete! Check experiments_output/table_verification/ for images")
    print("="*60)

if __name__ == "__main__":
    main()

