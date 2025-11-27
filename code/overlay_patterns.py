"""
Overlay Patterns Analysis - Combining All Patterns
تحليل الأنماط المجمعة - جمع كل الأنماط
"""
import numpy as np
import matplotlib.pyplot as plt
import json
import os
from pathlib import Path

# Import directly from files
import importlib.util

# Load quran_hearts module
quran_hearts_path = Path(__file__).parent / 'quran_hearts.py'
spec = importlib.util.spec_from_file_location("quran_hearts", quran_hearts_path)
quran_hearts = importlib.util.module_from_spec(spec)
spec.loader.exec_module(quran_hearts)

# Load disconnected_letters_keys module
disconnected_path = Path(__file__).parent / 'disconnected_letters_keys.py'
spec2 = importlib.util.spec_from_file_location("disconnected_letters_keys", disconnected_path)
disconnected_module = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(disconnected_module)

# Get functions and data
generate_bitmap = quran_hearts.generate_bitmap
SURAHS = quran_hearts.SURAHS
disconnected_letters_to_bitmap = disconnected_module.disconnected_letters_to_bitmap
DISCONNECTED_LETTERS = disconnected_module.DISCONNECTED_LETTERS

def generate_31x6_from_sequence(sequence):
    """Generate 31×6 matrix from a sequence of numbers"""
    seq = list(sequence)
    while len(seq) < 31:
        seq += seq[:31 - len(seq)]
    seq = seq[:31]
    
    binary = [format(n, '06b') for n in seq]
    matrix = np.array([[int(b) for b in row] for row in binary])
    return matrix

def combine_disconnected_letters_patterns():
    """Combine all disconnected letters patterns horizontally"""
    print("="*60)
    print("Combining Disconnected Letters Patterns")
    print("جمع أنماط الحروف المقطعة")
    print("="*60)
    
    all_matrices = []
    pattern_names = []
    
    # Get unique letter groups
    unique_letters = list(DISCONNECTED_LETTERS.keys())
    
    for letters in unique_letters:
        matrix, _ = disconnected_letters_to_bitmap(letters, "")
        if matrix is not None:
            all_matrices.append(matrix)
            pattern_names.append(letters)
            print(f"  ✅ Added: {letters}")
    
    # Combine horizontally
    if all_matrices:
        combined = np.hstack(all_matrices)
        print(f"\n✅ Combined {len(all_matrices)} patterns")
        print(f"📏 Final size: {combined.shape} (31 rows × {combined.shape[1]} columns)")
        
        # Save
        output_dir = Path('disconnected_letters_keys/combined_patterns')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        plt.figure(figsize=(max(12, combined.shape[1]//10), 8))
        plt.imshow(combined, cmap='gray_r', aspect='auto', interpolation='nearest')
        plt.axis('off')
        plt.title(f'Combined Disconnected Letters Patterns\n{len(all_matrices)} patterns × 6 columns = {combined.shape[1]} columns', 
                 fontsize=14, pad=20)
        plt.tight_layout()
        plt.savefig(output_dir / 'all_disconnected_letters_combined.png', 
                   dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        # Save metadata
        metadata = {
            'total_patterns': len(all_matrices),
            'matrix_shape': list(combined.shape),
            'patterns': pattern_names,
            'total_pixels': int(combined.size),
            'black_pixels': int(np.sum(combined == 1)),
            'white_pixels': int(np.sum(combined == 0))
        }
        
        with open(output_dir / 'combined_metadata.json', 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Saved: {output_dir / 'all_disconnected_letters_combined.png'}")
        return combined, metadata
    
    return None, None

def combine_major_letters():
    """Combine the most common letter groups: الم + الر + حم"""
    print("\n" + "="*60)
    print("Combining Major Letter Groups (الم + الر + حم)")
    print("جمع المجموعات الرئيسية (الم + الر + حم)")
    print("="*60)
    
    patterns = {
        "الم": [1, 30, 40],
        "الر": [1, 30, 8],  # ر = 200 % 64 = 8
        "حم": [8, 40]
    }
    
    all_matrices = []
    pattern_names = []
    
    for letters, nums in patterns.items():
        matrix = generate_31x6_from_sequence(nums)
        all_matrices.append(matrix)
        pattern_names.append(letters)
        print(f"  ✅ {letters}: {nums}")
    
    # Combine horizontally
    combined = np.hstack(all_matrices)
    print(f"\n✅ Combined 3 major patterns")
    print(f"📏 Size: {combined.shape} (31 rows × 18 columns)")
    
    # Save
    output_dir = Path('disconnected_letters_keys/combined_patterns')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    plt.figure(figsize=(10, 8))
    plt.imshow(combined, cmap='gray_r', aspect='auto', interpolation='nearest')
    plt.axis('off')
    plt.title('Major Letter Groups Combined\nالم + الر + حم (17 Surahs)', 
             fontsize=14, pad=20)
    plt.tight_layout()
    plt.savefig(output_dir / 'major_letters_combined.png', 
               dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"💾 Saved: {output_dir / 'major_letters_combined.png'}")
    return combined

def overlay_all_surahs():
    """Overlay all 114 Surahs using OR, Average, and Max methods"""
    print("\n" + "="*60)
    print("Overlaying All 114 Surahs")
    print("دمج جميع السور الـ114")
    print("="*60)
    
    all_matrices = []
    
    for surah_name, verse_count in SURAHS:
        matrix = generate_bitmap(verse_count)
        all_matrices.append(matrix)
    
    # Stack all matrices
    stack = np.stack(all_matrices)  # (114, 31, 6)
    print(f"✅ Loaded {len(all_matrices)} Surahs")
    print(f"📏 Stack shape: {stack.shape}")
    
    # 1. OR Overlay: if black in any surah → black
    overlay_or = np.max(stack, axis=0)
    
    # 2. Average: density of appearance
    overlay_avg = np.mean(stack, axis=0)
    
    # 3. Max (same as OR for binary)
    overlay_max = np.max(stack, axis=0)
    
    # Save
    output_dir = Path('experiments_output/overlay')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create visualization
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    
    axs[0].imshow(overlay_or, cmap='gray_r', aspect='auto', interpolation='nearest')
    axs[0].set_title('OR Overlay → Kaaba\n(Black if appears in any Surah)', fontsize=12)
    axs[0].axis('off')
    
    axs[1].imshow(overlay_avg, cmap='hot', aspect='auto', interpolation='nearest')
    axs[1].set_title('Average → Heart + Light\n(Density of appearance)', fontsize=12)
    axs[1].axis('off')
    
    axs[2].imshow(overlay_max, cmap='gray_r', aspect='auto', interpolation='nearest')
    axs[2].set_title('Max → Eye\n(Maximum intensity)', fontsize=12)
    axs[2].axis('off')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'all_surahs_overlay.png', 
               dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    # Save individual overlays
    for name, overlay, cmap in [('or_kaaba', overlay_or, 'gray_r'),
                                ('avg_heart', overlay_avg, 'hot'),
                                ('max_eye', overlay_max, 'gray_r')]:
        plt.figure(figsize=(4, 8))
        plt.imshow(overlay, cmap=cmap, aspect='auto', interpolation='nearest')
        plt.axis('off')
        plt.title(f'{name.replace("_", " ").title()}', fontsize=12)
        plt.tight_layout()
        plt.savefig(output_dir / f'{name}.png', 
                   dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
    
    # Save metadata
    metadata = {
        'total_surahs': 114,
        'overlay_shape': list(overlay_or.shape),
        'or_black_pixels': int(np.sum(overlay_or == 1)),
        'or_white_pixels': int(np.sum(overlay_or == 0)),
        'avg_mean': float(np.mean(overlay_avg)),
        'avg_max': float(np.max(overlay_avg)),
        'avg_min': float(np.min(overlay_avg))
    }
    
    with open(output_dir / 'overlay_metadata.json', 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    print(f"💾 Saved overlays to: {output_dir}")
    return overlay_or, overlay_avg, overlay_max

def main():
    """Run all overlay experiments"""
    print("🚀 Starting Overlay Patterns Analysis")
    print("="*60)
    
    # 1. Combine disconnected letters
    combined_letters, metadata_letters = combine_disconnected_letters_patterns()
    
    # 2. Combine major letters
    major_combined = combine_major_letters()
    
    # 3. Overlay all Surahs
    overlay_or, overlay_avg, overlay_max = overlay_all_surahs()
    
    print("\n" + "="*60)
    print("✅ All Overlay Experiments Completed!")
    print("="*60)
    print("\n📁 Results saved in:")
    print("   - disconnected_letters_keys/combined_patterns/")
    print("   - experiments_output/overlay/")

if __name__ == "__main__":
    main()
