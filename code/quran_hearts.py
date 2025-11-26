"""
Rahman-Key: Digital Hearts of the Quran
Converts Quranic verses into binary images (bitmaps) using 31×6 bits methodology
"""

import matplotlib.pyplot as plt
import numpy as np
import json
import os
from pathlib import Path

# Complete list of 114 Surahs with verse counts
SURAHS = [
    ("Al-Fatiha", 7),
    ("Al-Baqarah", 286),
    ("Ali 'Imran", 200),
    ("An-Nisa", 176),
    ("Al-Ma'idah", 120),
    ("Al-An'am", 165),
    ("Al-A'raf", 206),
    ("Al-Anfal", 75),
    ("At-Tawbah", 129),
    ("Yunus", 109),
    ("Hud", 123),
    ("Yusuf", 111),
    ("Ar-Ra'd", 43),
    ("Ibrahim", 52),
    ("Al-Hijr", 99),
    ("An-Nahl", 128),
    ("Al-Isra", 111),
    ("Al-Kahf", 110),
    ("Maryam", 98),
    ("Ta-Ha", 135),
    ("Al-Anbiya", 112),
    ("Al-Hajj", 78),
    ("Al-Mu'minun", 118),
    ("An-Nur", 64),
    ("Al-Furqan", 77),
    ("Ash-Shu'ara", 227),
    ("An-Naml", 93),
    ("Al-Qasas", 88),
    ("Al-Ankabut", 69),
    ("Ar-Rum", 60),
    ("Luqman", 34),
    ("As-Sajdah", 30),
    ("Al-Ahzab", 73),
    ("Saba", 54),
    ("Fatir", 45),
    ("Ya-Sin", 83),
    ("As-Saffat", 182),
    ("Sad", 88),
    ("Az-Zumar", 75),
    ("Ghafir", 85),
    ("Fussilat", 54),
    ("Ash-Shura", 53),
    ("Az-Zukhruf", 89),
    ("Ad-Dukhan", 59),
    ("Al-Jathiyah", 37),
    ("Al-Ahqaf", 35),
    ("Muhammad", 38),
    ("Al-Fath", 29),
    ("Al-Hujurat", 18),
    ("Qaf", 45),
    ("Adh-Dhariyat", 60),
    ("At-Tur", 49),
    ("An-Najm", 62),
    ("Al-Qamar", 55),
    ("Ar-Rahman", 78),
    ("Al-Waqi'ah", 96),
    ("Al-Hadid", 29),
    ("Al-Mujadila", 22),
    ("Al-Hashr", 24),
    ("Al-Mumtahanah", 13),
    ("As-Saff", 14),
    ("Al-Jumu'ah", 11),
    ("Al-Munafiqun", 11),
    ("At-Taghabun", 18),
    ("At-Talaq", 12),
    ("At-Tahrim", 12),
    ("Al-Mulk", 30),
    ("Al-Qalam", 52),
    ("Al-Haqqah", 52),
    ("Al-Ma'arij", 44),
    ("Nuh", 28),
    ("Al-Jinn", 28),
    ("Al-Muzzammil", 20),
    ("Al-Muddaththir", 56),
    ("Al-Qiyamah", 40),
    ("Al-Insan", 31),
    ("Al-Mursalat", 50),
    ("An-Naba", 40),
    ("An-Nazi'at", 46),
    ("Abasa", 42),
    ("At-Takwir", 29),
    ("Al-Infitar", 19),
    ("Al-Mutaffifin", 36),
    ("Al-Inshiqaq", 25),
    ("Al-Buruj", 22),
    ("At-Tariq", 17),
    ("Al-A'la", 19),
    ("Al-Ghashiyah", 26),
    ("Al-Fajr", 30),
    ("Al-Balad", 20),
    ("Ash-Shams", 15),
    ("Al-Layl", 21),
    ("Ad-Duha", 11),
    ("Ash-Sharh", 8),
    ("At-Tin", 8),
    ("Al-Alaq", 19),
    ("Al-Qadr", 5),
    ("Al-Bayyinah", 8),
    ("Az-Zalzalah", 8),
    ("Al-Adiyat", 11),
    ("Al-Qari'ah", 11),
    ("At-Takathur", 8),
    ("Al-Asr", 3),
    ("Al-Humazah", 9),
    ("Al-Fil", 5),
    ("Quraysh", 4),
    ("Al-Ma'un", 7),
    ("Al-Kawthar", 3),
    ("Al-Kafirun", 6),
    ("An-Nasr", 3),
    ("Al-Masad", 5),
    ("Al-Ikhlas", 4),
    ("Al-Falaq", 5),
    ("An-Nas", 6),
]


def generate_bitmap(surah_verse_count):
    """
    Generate a 31×6 binary bitmap from surah verse count.
    
    Args:
        surah_verse_count: Number of verses in the surah
        
    Returns:
        numpy array: 31×6 binary matrix
    """
    # Repeat sequence until we have at least 31 rows
    seq = list(range(1, surah_verse_count + 1))
    while len(seq) < 31:
        seq += seq[:31 - len(seq)]
    
    # Take only first 31
    seq = seq[:31]
    
    # Convert to 6-bit binary
    binary = [format(n, '06b') for n in seq]
    matrix = np.array([[int(b) for b in row] for row in binary])
    
    return matrix


def describe_pattern(matrix):
    """
    Generate a simple description of the pattern.
    This is a basic pattern recognition - can be enhanced.
    """
    # Count ones in different regions
    top = np.sum(matrix[:10, :])
    middle = np.sum(matrix[10:21, :])
    bottom = np.sum(matrix[21:, :])
    left = np.sum(matrix[:, :3])
    right = np.sum(matrix[:, 3:])
    
    # Simple pattern detection
    total_ones = np.sum(matrix)
    density = total_ones / (31 * 6)
    
    if density < 0.3:
        return "Sparse pattern with scattered points"
    elif density > 0.7:
        return "Dense pattern with rich texture"
    elif top > middle and top > bottom:
        return "Heart shape with open top"
    elif middle > top and middle > bottom:
        return "Heart shape with central focus"
    elif left > right:
        return "Heart shape leaning left"
    elif right > left:
        return "Heart shape leaning right"
    else:
        return "Balanced heart-like pattern"


def generate_all_hearts():
    """
    Generate all 114 surah bitmaps and save them.
    Also creates descriptions.json with pattern descriptions.
    """
    # Get project root directory (parent of code directory)
    project_root = Path(__file__).parent.parent
    images_dir = project_root / "images"
    images_dir.mkdir(exist_ok=True)
    
    descriptions = {}
    
    print("Generating 114 Quranic Digital Hearts...")
    print("=" * 50)
    
    for idx, (surah_name, verse_count) in enumerate(SURAHS, 1):
        # Generate bitmap
        matrix = generate_bitmap(verse_count)
        
        # Create figure
        fig, ax = plt.subplots(figsize=(5, 9))
        ax.imshow(matrix, cmap='binary', interpolation='nearest', aspect='auto')
        ax.axis('off')
        
        # Save image
        filename = f"{idx:03d}_{surah_name.replace(' ', '_').replace(chr(39), '')}.png"
        filepath = images_dir / filename
        plt.savefig(filepath, bbox_inches='tight', pad_inches=0, dpi=100)
        plt.close()
        
        # Generate description
        pattern_desc = describe_pattern(matrix)
        descriptions[surah_name] = {
            "surah_number": idx,
            "verse_count": verse_count,
            "pattern_description": pattern_desc
        }
        
        print(f"✓ {idx:03d} - {surah_name} ({verse_count} verses) - {pattern_desc}")
    
    # Save descriptions.json in project root
    descriptions_file = project_root / "descriptions.json"
    with open(descriptions_file, "w", encoding="utf-8") as f:
        json.dump(descriptions, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 50)
    print(f"✓ Generated {len(SURAHS)} images in 'images/' directory")
    print("✓ Created descriptions.json")
    print("\nDone! All Quranic Digital Hearts are ready.")


def visualize_single(surah_number):
    """
    Visualize a single surah (1-114).
    """
    if surah_number < 1 or surah_number > 114:
        print("Invalid surah number. Must be between 1 and 114.")
        return
    
    surah_name, verse_count = SURAHS[surah_number - 1]
    matrix = generate_bitmap(verse_count)
    
    plt.figure(figsize=(5, 9))
    plt.imshow(matrix, cmap='binary', interpolation='nearest', aspect='auto')
    plt.axis('off')
    plt.title(f'{surah_number:03d} - {surah_name}\n({verse_count} verses)', 
              fontsize=14, pad=20)
    plt.tight_layout()
    plt.show()
    
    pattern_desc = describe_pattern(matrix)
    print(f"Pattern: {pattern_desc}")


if __name__ == "__main__":
    # Generate all hearts
    generate_all_hearts()

