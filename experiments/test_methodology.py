"""Test if experiments follow the same methodology as main code"""
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'code'))
from quran_hearts import generate_bitmap

def method_main_code(verse_count):
    """Method from quran_hearts.py"""
    seq = list(range(1, verse_count + 1))
    while len(seq) < 31:
        seq += seq[:31 - len(seq)]
    seq = seq[:31]
    binary = [format(n, '06b') for n in seq]
    matrix = np.array([[int(b) for b in row] for row in binary])
    return matrix

def method_experiments(sequence):
    """Method from experiments files"""
    rows = []
    while len(rows) < 31:
        for v in sequence:
            if len(rows) < 31:
                rows.append(format(v, '06b'))
            else:
                break
    matrix = np.array([[int(b) for b in row] for row in rows])
    return matrix

# Test with Al-Fatiha (7 verses)
print("Testing Al-Fatiha (7 verses):")
m1 = method_main_code(7)
m2 = method_experiments(list(range(1, 8)))

print(f"Method 1 (main): shape {m1.shape}, first row: {m1[0]}")
print(f"Method 2 (experiments): shape {m2.shape}, first row: {m2[0]}")
print(f"Are they equal? {np.array_equal(m1, m2)}")

if not np.array_equal(m1, m2):
    print("\n⚠️ DIFFERENCE DETECTED!")
    print("First 10 rows comparison:")
    for i in range(min(10, len(m1))):
        print(f"Row {i}: Main={m1[i]}, Exp={m2[i]}, Match={np.array_equal(m1[i], m2[i])}")

# Test with 99 Names
print("\n" + "="*60)
print("Testing 99 Names:")
seq_99 = list(range(1, 100))
m1_99 = method_main_code(99)  # This won't work directly, need to adapt
m2_99 = method_experiments(seq_99)

print(f"Method 2 (experiments): shape {m2_99.shape}, first row: {m2_99[0]}")

