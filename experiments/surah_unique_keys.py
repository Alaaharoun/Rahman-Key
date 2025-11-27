"""
Surah Unique Keys System | نظام المفاتيح الفريدة للسور

This implements the unique key system where each Surah has:
- A unique key number (e.g., 133, 247, 189)
- A unique matrix dimension (e.g., 19×6, 31×6, 25×6, 22×6)
- Unique patterns extracted

⚠️ EXPERIMENTAL - This is exploratory research
"""

import numpy as np
import matplotlib.pyplot as plt
import json
from pathlib import Path

def to_6bit(n):
    """Convert number to 6-bit binary string"""
    return format(n % 64, '06b')

def calculate_surah_key(surah_number, ayah_count, revelation_order):
    """
    Calculate unique key for a Surah
    
    Formula: (surah_number × ayah_count × revelation_order) % 1000
    This gives a 3-digit key (0-999)
    """
    key = (surah_number * ayah_count * revelation_order) % 1000
    return key

def calculate_matrix_dimensions(key, ayah_count):
    """
    Calculate matrix dimensions based on key and ayah count
    
    The dimensions are derived from the key to create unique patterns
    """
    # Use key to determine rows (between 19 and 31)
    rows = 19 + (key % 13)  # 19 to 31
    cols = 6  # Always 6 columns (binary representation)
    
    return rows, cols

def generate_surah_pattern(surah_number, ayah_count, revelation_order):
    """
    Generate unique pattern for a Surah using its unique key
    
    Returns:
        - key: Unique key number (e.g., 133, 247)
        - matrix: Binary matrix with unique dimensions
        - patterns: Detected patterns
    """
    # Calculate unique key
    key = calculate_surah_key(surah_number, ayah_count, revelation_order)
    
    # Calculate matrix dimensions
    rows, cols = calculate_matrix_dimensions(key, ayah_count)
    
    # Generate sequence based on key
    sequence = []
    for i in range(rows):
        # Use key to generate unique sequence
        value = ((key + i * surah_number + ayah_count) % 64)
        sequence.append(value)
    
    # Convert to binary matrix
    matrix = np.array([[int(b) for b in to_6bit(n)] for n in sequence])
    
    # Analyze patterns
    patterns = analyze_patterns(matrix, key)
    
    return key, matrix, patterns, (rows, cols)

def analyze_patterns(matrix, key):
    """
    Analyze patterns in the matrix
    
    Returns list of detected patterns
    """
    patterns = []
    rows, cols = matrix.shape
    
    # 1. Heart detection (bottom part)
    if rows >= 19:
        heart_score = np.sum(matrix[rows-5:, 1:5])
        if heart_score > 10:
            patterns.append("heart")
    
    # 2. Star detection (corners)
    star_score = (np.sum(matrix[0, :]) + np.sum(matrix[rows-1, :]) + 
                  np.sum(matrix[:, 0]) + np.sum(matrix[:, cols-1]))
    if star_score > 8:
        patterns.append("star")
    
    # 3. Door detection (middle columns)
    if cols >= 4:
        door_score = np.sum(matrix[:, cols//2-1:cols//2+1])
        if door_score > rows * 0.4:
            patterns.append("door")
    
    # 4. Key detection (center point)
    center_score = np.sum(matrix[rows//2-1:rows//2+1, cols//2-1:cols//2+1])
    if center_score > 3:
        patterns.append("key")
    
    return patterns

def get_pattern_emoji(patterns):
    """Convert pattern names to emojis"""
    emoji_map = {
        "heart": "❤️",
        "star": "⭐",
        "door": "🚪",
        "key": "🔑"
    }
    return "".join([emoji_map.get(p, "") for p in patterns])

def get_pattern_interpretation(surah_name, patterns, key):
    """
    Get interpretation based on patterns and key
    
    This is a simple mapping - can be expanded
    """
    if "heart" in patterns and "star" in patterns:
        return "قلب مهتدي" if key < 200 else "قلب مفتوح"
    elif "heart" in patterns and "door" in patterns:
        return "قلب مفتوح"
    elif "heart" in patterns:
        return "جوهر الرحمة"
    elif "star" in patterns and "door" in patterns:
        return "هداية وفتح"
    elif "heart" in patterns and "star" in patterns and "door" in patterns:
        return "المفتاح الكامل"
    else:
        return "نمط خاص"

def generate_all_unique_keys():
    """
    Generate unique keys for all 114 Surahs
    """
    print("="*60)
    print("Surah Unique Keys System | نظام المفاتيح الفريدة للسور")
    print("="*60)
    print("\n⚠️ EXPERIMENTAL - This is exploratory research")
    print("⚠️ تجريبي - هذا بحث استكشافي\n")
    
    # Load Surahs data
    import importlib.util
    quran_hearts_path = Path('code/quran_hearts.py')
    spec = importlib.util.spec_from_file_location("quran_hearts", quran_hearts_path)
    quran_hearts = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(quran_hearts)
    SURAHS = quran_hearts.SURAHS
    
    # Load revelation order
    REVELATION_ORDER = {}
    try:
        with open('surah_revelation_order.csv', 'r', encoding='utf-8') as f:
            import csv
            reader = csv.DictReader(f)
            for row in reader:
                surah_name = row['Surah Name'].strip()
                rev_order = int(row['Revelation Order'].strip())
                REVELATION_ORDER[surah_name] = rev_order
    except:
        print("⚠️ Could not load revelation order CSV, using fallback")
        # Fallback revelation order (approximate)
        REVELATION_ORDER = {
            "Al-Fatiha": 1, "Al-Baqarah": 87, "Ali 'Imran": 89,
            "An-Nisa": 92, "Al-Maidah": 112
        }
    
    results = {}
    output_dir = Path('experiments_output/surah_unique_keys')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📖 Generating unique keys for {len(SURAHS)} Surahs...\n")
    
    for surah_num, (surah_name, ayah_count) in enumerate(SURAHS, 1):
        # Get revelation order
        rev_order = REVELATION_ORDER.get(surah_name, surah_num)
        
        # Generate unique pattern
        key, matrix, patterns, (rows, cols) = generate_surah_pattern(
            surah_num, ayah_count, rev_order
        )
        
        # Get emoji and interpretation
        emoji = get_pattern_emoji(patterns)
        interpretation = get_pattern_interpretation(surah_name, patterns, key)
        
        # Store results
        results[surah_name] = {
            "surah_number": surah_num,
            "surah_name": surah_name,
            "ayah_count": ayah_count,
            "revelation_order": rev_order,
            "key": key,
            "matrix_dimensions": f"{rows}×{cols}",
            "rows": rows,
            "cols": cols,
            "patterns": patterns,
            "pattern_emoji": emoji,
            "interpretation": interpretation,
            "black_pixels": int(np.sum(matrix)),
            "white_pixels": int(rows * cols - np.sum(matrix))
        }
        
        # Save image
        plt.figure(figsize=(3, rows/3))
        plt.imshow(matrix, cmap='gray_r', aspect='auto')
        plt.axis('off')
        plt.title(f"{surah_num:03d}_{surah_name}\nKey: {key} | {rows}×{cols}\n{emoji} {interpretation}", 
                 fontsize=8, pad=10)
        
        filename = f"{surah_num:03d}_{surah_name.replace(' ', '_').replace(chr(39), '')}_key{key}.png"
        plt.savefig(output_dir / filename, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close()
        
        # Print progress
        if surah_num <= 5 or surah_num % 20 == 0:
            print(f"✅ {surah_num:03d}. {surah_name}: Key {key} | {rows}×{cols} | {emoji} {interpretation}")
    
    # Save results
    with open(output_dir / 'surah_unique_keys_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    # Generate summary table
    generate_summary_table(results, output_dir)
    
    print(f"\n✅ Generated {len(results)} unique keys!")
    print(f"📁 Output: {output_dir}/")
    print(f"📊 Analysis: {output_dir}/surah_unique_keys_analysis.json")
    print(f"📋 Summary: {output_dir}/SUMMARY_TABLE.md")
    
    return results

def generate_summary_table(results, output_dir):
    """Generate summary table in Markdown format"""
    
    table_content = """# 📊 Surah Unique Keys Summary | ملخص المفاتيح الفريدة للسور

**English:**  
This table shows the unique key, matrix dimensions, patterns, and interpretation for each Surah.

**العربية:**  
هذا الجدول يظهر المفتاح الفريد، أبعاد المصفوفة، الأنماط، والتفسير لكل سورة.

---

## 📋 Results Table | جدول النتائج

| السورة | المفتاح | المصفوفة | الأنماط | التفسير |
|--------|---------|----------|---------|---------|
"""
    
    # Sort by surah number
    sorted_results = sorted(results.items(), key=lambda x: x[1]['surah_number'])
    
    for surah_name, data in sorted_results:
        table_content += f"| {data['surah_name']} | {data['key']} | {data['matrix_dimensions']} | {data['pattern_emoji']} | {data['interpretation']} |\n"
    
    table_content += "\n---\n\n"
    table_content += "**🌙 Rahman-Key** — Unique keys for each Surah. | مفاتيح فريدة لكل سورة.\n\n"
    table_content += "**Date:** 2024\n"
    table_content += "**Status:** ⚠️ Experimental | تجريبي\n"
    
    with open(output_dir / 'SUMMARY_TABLE.md', 'w', encoding='utf-8') as f:
        f.write(table_content)

if __name__ == "__main__":
    results = generate_all_unique_keys()
    
    print("\n" + "="*60)
    print("🎯 Example Results (First 5 Surahs):")
    print("="*60)
    
    for i, (surah_name, data) in enumerate(list(results.items())[:5], 1):
        print(f"\n{i}. {data['surah_name']}:")
        print(f"   Key: {data['key']}")
        print(f"   Matrix: {data['matrix_dimensions']}")
        print(f"   Patterns: {data['pattern_emoji']} ({', '.join(data['patterns'])})")
        print(f"   Interpretation: {data['interpretation']}")

