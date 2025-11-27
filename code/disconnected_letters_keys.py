"""
Disconnected Letters Keys - Apply Rahman Key (31×6) to Quranic Disconnected Letters
مفاتيح الحروف المقطعة - تطبيق مفتاح الرحمن (31×6) على الحروف المقطعة في القرآن
"""
import numpy as np
import matplotlib.pyplot as plt
import json
import os
from pathlib import Path

# Abjad (Arabic letter numerical values) - Short version
ABJAD = {
    'أ': 1, 'ب': 2, 'ج': 3, 'د': 4, 'ه': 5, 'و': 6, 'ز': 7, 'ح': 8, 'ط': 9,
    'ي': 10, 'ك': 20, 'ل': 30, 'م': 40, 'ن': 50, 'س': 60, 'ع': 70, 'ف': 80,
    'ص': 90, 'ق': 100, 'ر': 200, 'ش': 300, 'ت': 400, 'ث': 500, 'خ': 600,
    'ذ': 700, 'ض': 800, 'ظ': 900, 'غ': 1000
}

# Complete list of disconnected letters and their Surahs
DISCONNECTED_LETTERS = {
    "الم": ["Al-Baqarah", "Ali 'Imran", "Ta-Ha", "Ash-Shu'ara", "Ar-Rum", "As-Sajdah"],
    "الر": ["Yunus", "Hud", "Yusuf", "Ibrahim", "Al-Hijr", "Ar-Ra'd"],
    "المص": ["Al-A'raf"],
    "طسم": ["Ash-Shu'ara", "Al-Qasas"],
    "طه": ["Ta-Ha"],
    "يس": ["Ya-Sin"],
    "ص": ["Sad"],
    "حم": ["Fussilat", "Az-Zukhruf", "Ad-Dukhan", "Al-Jathiyah", "Al-Ahqaf"],
    "ق": ["Qaf"],
    "ن": ["Al-Qalam"],
    "كهيعص": ["Maryam"],
    "طس": ["An-Naml"],
    "المص": ["Al-A'raf"],
    "المر": ["Ar-Ra'd"],
    "حم عسق": ["Ash-Shura"],
    "طسم": ["Ash-Shu'ara", "Al-Qasas"],
}

def to_6bit(n):
    """Convert number to 6-bit binary string"""
    return format(n, '06b')

def disconnected_letters_to_bitmap(letters, surah_name=""):
    """
    Convert disconnected letters to 31×6 bitmap using Rahman Key methodology
    نفس منهجية مفتاح الرحمن بالضبط
    """
    # Convert letters to numbers (using % 64 for numbers > 63)
    nums = [ABJAD.get(ch, 0) % 64 for ch in letters]
    
    if not nums:
        return None
    
    # Repeat sequence until we have at least 31 rows
    seq = []
    while len(seq) < 31:
        seq += nums[:31 - len(seq)]
    
    # Take only first 31
    seq = seq[:31]
    
    # Convert to 6-bit binary
    binary = [to_6bit(n) for n in seq]
    matrix = np.array([[int(b) for b in row] for row in binary])
    
    return matrix, seq

def detect_heart_pattern(matrix):
    """Detect heart pattern in the bitmap"""
    rows, cols = matrix.shape
    
    # Calculate widths
    widths = []
    for i in range(rows):
        row = matrix[i, :]
        black = np.where(row == 1)[0]
        widths.append(black[-1] - black[0] + 1 if len(black) > 0 else 0)
    
    # Check symmetry
    if cols % 2 == 0:
        left = matrix[:, :cols//2]
        right = np.flip(matrix[:, cols//2:], axis=1)
        vertical_sym = np.sum(left == right) / left.size
    else:
        vertical_sym = 0
    
    # Check for heart shape
    top_w = np.mean(widths[:rows//3]) if rows//3 > 0 else 0
    mid_w = np.mean(widths[rows//3:2*rows//3]) if 2*rows//3 <= rows else np.mean(widths[rows//3:])
    bot_w = np.mean(widths[2*rows//3:]) if 2*rows//3 < rows else 0
    
    is_heart = (mid_w > top_w * 1.1 and mid_w > bot_w * 1.1) or \
               (top_w > bot_w * 1.2) or \
               (mid_w > 0 and top_w > 0 and bot_w > 0)
    
    return {
        'is_heart': is_heart,
        'symmetry': vertical_sym,
        'widths': widths
    }

def describe_pattern(matrix, letters):
    """Describe the pattern (basic pattern recognition)"""
    rows, cols = matrix.shape
    
    # Check for specific patterns
    heart = detect_heart_pattern(matrix)
    
    # Check center for symbols
    center_row, center_col = rows // 2, cols // 2
    if center_row > 1 and center_col > 1:
        center_region = matrix[center_row-1:center_row+2, center_col-1:center_col+2]
        center_density = np.sum(center_region == 1) / center_region.size
        
        # Dot
        is_dot = center_region[1, 1] == 1 and np.sum(center_region == 1) == 1
        
        # Vertical line
        vertical_line = np.sum(center_region[:, 1] == 1) == center_region.shape[0]
        
        # Horizontal line
        horizontal_line = np.sum(center_region[1, :] == 1) == center_region.shape[1]
    else:
        center_density = 0
        is_dot = False
        vertical_line = False
        horizontal_line = False
    
    # Pattern description
    pattern_parts = []
    if heart['is_heart']:
        pattern_parts.append("Heart")
        if is_dot:
            pattern_parts.append("with central dot")
        elif vertical_line:
            pattern_parts.append("with vertical line")
        elif horizontal_line:
            pattern_parts.append("with horizontal line")
    else:
        pattern_parts.append("Other pattern")
    
    return " + ".join(pattern_parts) if pattern_parts else "Sparse pattern"

def generate_all_disconnected_letters():
    """Generate bitmaps for all disconnected letters"""
    print("="*60)
    print("Generating Disconnected Letters Patterns")
    print("توليد أنماط الحروف المقطعة")
    print("="*60)
    
    output_dir = Path('disconnected_letters_keys/images')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    results = {}
    heart_count = 0
    
    for letters, surahs in DISCONNECTED_LETTERS.items():
        print(f"\nProcessing: {letters}")
        print(f"  Surahs: {', '.join(surahs)}")
        
        # Generate matrix
        matrix, sequence = disconnected_letters_to_bitmap(letters, surahs[0])
        
        if matrix is None:
            continue
        
        # Analyze pattern
        heart = detect_heart_pattern(matrix)
        pattern_desc = describe_pattern(matrix, letters)
        
        if heart['is_heart']:
            heart_count += 1
        
        # Save image for first surah of each letter group
        surah_name = surahs[0]
        plt.figure(figsize=(4, 8))
        plt.imshow(matrix, cmap='binary', interpolation='nearest', aspect='auto')
        plt.axis('off')
        plt.title(f'{surah_name}\n{letters}\n{pattern_desc}', fontsize=10, pad=10)
        plt.tight_layout()
        
        filename = f"{letters.replace(' ', '_')}_{surah_name.replace(' ', '_').replace("'", '')}.png"
        plt.savefig(output_dir / filename, dpi=200, bbox_inches='tight', facecolor='white')
        plt.close()
        
        results[letters] = {
            'letters': letters,
            'surahs': surahs,
            'sequence': [int(n) for n in sequence[:10]],  # First 10 for preview
            'pattern': pattern_desc,
            'is_heart': bool(heart['is_heart']),
            'symmetry': float(heart['symmetry']),
            'surah_count': len(surahs)
        }
        
        print(f"  ✅ Pattern: {pattern_desc}")
        print(f"  ✅ Heart: {'YES' if heart['is_heart'] else 'NO'}")
        print(f"  ✅ Symmetry: {heart['symmetry']*100:.1f}%")
        print(f"  ✅ Saved: {filename}")
    
    # Save results
    with open('disconnected_letters_keys/analysis.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY | الملخص")
    print("="*60)
    print(f"Total letter groups: {len(results)}")
    print(f"Heart patterns detected: {heart_count}/{len(results)} ({heart_count/len(results)*100:.1f}%)")
    
    return results

if __name__ == "__main__":
    results = generate_all_disconnected_letters()
    print(f"\n✅ Done! Check disconnected_letters_keys/ for results")

