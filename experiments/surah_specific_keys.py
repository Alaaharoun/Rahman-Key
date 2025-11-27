"""
Surah-Specific Keys Discovery - Experimental Analysis
اكتشاف مفاتيح السور الخاصة - تحليل تجريبي

This is an EXPLORATORY experiment to test the hypothesis:
"Could each Surah have its own unique key (e.g., 19×6) in addition to the master key (31×6)?"

⚠️ IMPORTANT: This is experimental - not part of the core methodology.
Results should be interpreted as exploratory findings, not definitive conclusions.
"""
import numpy as np
import matplotlib.pyplot as plt
import json
import csv
from pathlib import Path

def to_6bit(n):
    """Convert number to 6-bit binary string"""
    return format(n, '06b')

# Load revelation order
REVELATION_ORDER = {}
try:
    with open('surah_revelation_order.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            surah_name = row['Surah Name'].strip()
            rev_order = int(row['Revelation Order'].strip())
            REVELATION_ORDER[surah_name] = rev_order
except:
    # Fallback: create basic mapping
    print("⚠️ Could not load revelation order CSV, using basic mapping")
    REVELATION_ORDER = {}

def generate_19x6_pattern(surah_number, ayah_count, revelation_order=None):
    """
    Generate 19×6 pattern for a Surah
    
    Key insight: 19 × 6 = 114 pixels = exactly the number of Surahs!
    This makes 19×6 a potentially significant key.
    """
    # Create unique seed from Surah parameters
    if revelation_order:
        seed = (surah_number * ayah_count * revelation_order) % 64
    else:
        seed = (surah_number * ayah_count) % 64
    
    # Generate 19 rows
    sequence = []
    for i in range(19):
        row_value = ((seed + i * surah_number) % 64)
        sequence.append(row_value)
    
    # Convert to 19×6 matrix
    matrix = np.array([[int(b) for b in to_6bit(n)] for n in sequence])
    
    return matrix, seed

def analyze_19x6_pattern(matrix):
    """Analyze patterns in 19×6 matrix"""
    patterns = []
    
    # 1. Heart detection (bottom part)
    heart_score = np.sum(matrix[14:19, 1:5])
    if heart_score > 12:
        patterns.append("heart")
    
    # 2. Star detection (corners)
    star_score = (np.sum(matrix[0, :]) + np.sum(matrix[18, :]) + 
                  np.sum(matrix[:, 0]) + np.sum(matrix[:, 5]))
    if star_score > 10:
        patterns.append("star")
    
    # 3. Door detection (middle columns)
    door_score = np.sum(matrix[:, 2:4])
    if door_score > 25:
        patterns.append("door")
    
    # 4. Key detection (center point)
    center_score = np.sum(matrix[9:11, 2:4])
    if center_score > 6:
        patterns.append("key")
    
    # 5. Crescent detection (right side)
    crescent_score = np.sum(matrix[:, 4:6])
    if 20 < crescent_score < 30:
        patterns.append("crescent")
    
    return patterns

def get_surah_revelation_order(surah_name):
    """Get revelation order for a Surah"""
    # Try to find in CSV data
    for key, value in REVELATION_ORDER.items():
        if surah_name.lower() in key.lower() or key.lower() in surah_name.lower():
            return value
    
    # Fallback: use approximate order based on common knowledge
    # This is a simplified mapping - not 100% accurate
    common_orders = {
        "Al-Fatiha": 1, "Al-Baqarah": 87, "Ali 'Imran": 89,
        "Ar-Rahman": 97, "Al-Ikhlas": 22, "An-Nas": 21
    }
    
    for key, value in common_orders.items():
        if key.lower() in surah_name.lower():
            return value
    
    return None

def discover_surah_keys():
    """Discover keys for all Surahs using 19×6"""
    print("="*60)
    print("Surah-Specific Keys Discovery (19×6)")
    print("اكتشاف مفاتيح السور الخاصة (19×6)")
    print("="*60)
    print("\n⚠️ EXPERIMENTAL - This is exploratory analysis")
    print("⚠️ تجريبي - هذا تحليل استكشافي\n")
    
    # Load Surahs from quran_hearts
    import importlib.util
    quran_hearts_path = Path('code/quran_hearts.py')
    spec = importlib.util.spec_from_file_location("quran_hearts", quran_hearts_path)
    quran_hearts = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(quran_hearts)
    SURAHS = quran_hearts.SURAHS
    
    results = {}
    output_dir = Path('experiments_output/surah_keys_19x6')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📖 Analyzing {len(SURAHS)} Surahs...\n")
    
    for surah_num, (surah_name, ayah_count) in enumerate(SURAHS, 1):
        # Get revelation order
        revelation_order = get_surah_revelation_order(surah_name)
        
        # Generate 19×6 pattern
        matrix, seed = generate_19x6_pattern(surah_num, ayah_count, revelation_order)
        
        # Analyze patterns
        patterns = analyze_19x6_pattern(matrix)
        
        # Save result
        results[surah_name] = {
            "surah_number": surah_num,
            "ayah_count": ayah_count,
            "revelation_order": revelation_order,
            "seed": int(seed),
            "patterns": patterns,
            "pattern_count": len(patterns),
            "matrix_shape": list(matrix.shape),
            "black_pixels": int(np.sum(matrix)),
            "white_pixels": int(np.sum(matrix == 0))
        }
        
        # Save image
        plt.figure(figsize=(3, 4))
        plt.imshow(matrix, cmap='gray_r', aspect='auto', interpolation='nearest')
        plt.axis('off')
        
        pattern_str = ", ".join(patterns) if patterns else "no clear pattern"
        plt.title(f"{surah_name}\n19×6 Key\n{pattern_str}", 
                 fontsize=9, pad=5)
        plt.tight_layout()
        
        filename = f"{surah_num:03d}_{surah_name.replace(' ', '_').replace("'", '')}_19x6.png"
        plt.savefig(output_dir / filename, 
                   dpi=200, bbox_inches='tight', facecolor='white')
        plt.close()
        
        # Print progress
        if surah_num % 20 == 0 or surah_num <= 10 or surah_name == "Ar-Rahman":
            status = "🔥" if len(patterns) >= 3 else "⭐" if len(patterns) == 2 else "✓"
            print(f"{status} {surah_num:3d}. {surah_name:20s} | Patterns: {len(patterns)} | {pattern_str}")
    
    # Save results
    with open(output_dir / 'surah_keys_19x6_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    # Statistics
    total_patterns = sum(len(r['patterns']) for r in results.values())
    surahs_with_3plus = sum(1 for r in results.values() if len(r['patterns']) >= 3)
    surahs_with_heart = sum(1 for r in results.values() if 'heart' in r['patterns'])
    
    print("\n" + "="*60)
    print("📊 Statistics | الإحصائيات")
    print("="*60)
    print(f"Total Surahs analyzed: {len(results)}")
    print(f"Total patterns detected: {total_patterns}")
    print(f"Surahs with 3+ patterns: {surahs_with_3plus}")
    print(f"Surahs with heart pattern: {surahs_with_heart}")
    
    # Special analysis: Ar-Rahman
    if "Ar-Rahman" in results:
        rahman = results["Ar-Rahman"]
        print(f"\n🔥 Ar-Rahman Special Analysis:")
        print(f"   Patterns: {rahman['patterns']}")
        print(f"   Pattern count: {rahman['pattern_count']}")
        print(f"   Seed: {rahman['seed']}")
        if rahman['pattern_count'] >= 4:
            print(f"   ⭐ Ar-Rahman shows the MOST patterns in 19×6 key!")
    
    return results

def compare_31x6_vs_19x6():
    """Compare 31×6 vs 19×6 for key Surahs"""
    print("\n" + "="*60)
    print("Comparison: 31×6 vs 19×6")
    print("مقارنة: 31×6 مقابل 19×6")
    print("="*60)
    
    # Load 31×6 generator
    import importlib.util
    quran_hearts_path = Path('code/quran_hearts.py')
    spec = importlib.util.spec_from_file_location("quran_hearts", quran_hearts_path)
    quran_hearts = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(quran_hearts)
    generate_bitmap = quran_hearts.generate_bitmap
    SURAHS = quran_hearts.SURAHS
    
    # Test on key Surahs
    test_surahs = [
        ("Al-Fatiha", 7),
        ("Ar-Rahman", 78),
        ("Al-Ikhlas", 4),
        ("Al-Baqarah", 286)
    ]
    
    output_dir = Path('experiments_output/surah_keys_19x6/comparison')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for surah_name, ayah_count in test_surahs:
        # 31×6
        matrix_31x6 = generate_bitmap(ayah_count)
        
        # 19×6
        surah_num = next(i for i, (n, _) in enumerate(SURAHS, 1) if n == surah_name)
        matrix_19x6, _ = generate_19x6_pattern(surah_num, ayah_count, 
                                               get_surah_revelation_order(surah_name))
        
        # Create comparison
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 6))
        
        ax1.imshow(matrix_31x6, cmap='gray_r', aspect='auto', interpolation='nearest')
        ax1.set_title(f'{surah_name}\n31×6 (Master Key)', fontsize=10)
        ax1.axis('off')
        
        ax2.imshow(matrix_19x6, cmap='gray_r', aspect='auto', interpolation='nearest')
        patterns = analyze_19x6_pattern(matrix_19x6)
        pattern_str = ", ".join(patterns) if patterns else "no clear pattern"
        ax2.set_title(f'{surah_name}\n19×6 (Surah Key)\n{pattern_str}', fontsize=10)
        ax2.axis('off')
        
        plt.tight_layout()
        filename = f"{surah_name.replace(' ', '_').replace("'", '')}_comparison.png"
        plt.savefig(output_dir / filename, 
                   dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        print(f"✅ {surah_name}: Comparison saved")

def main():
    """Run all experiments"""
    print("🚀 Starting Surah-Specific Keys Discovery")
    print("="*60)
    print("⚠️ EXPERIMENTAL ANALYSIS - Not Core Methodology")
    print("⚠️ تحليل تجريبي - ليس جزءاً من المنهجية الأساسية\n")
    
    # Discover all keys
    results = discover_surah_keys()
    
    # Compare key Surahs
    compare_31x6_vs_19x6()
    
    print("\n" + "="*60)
    print("✅ Experiments Completed!")
    print("="*60)
    print("\n📁 Results saved in:")
    print("   - experiments_output/surah_keys_19x6/")
    print("   - experiments_output/surah_keys_19x6/comparison/")
    print("\n⚠️ Remember: These are exploratory findings, not definitive conclusions.")

if __name__ == "__main__":
    main()

