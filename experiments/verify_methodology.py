"""Verify that all experiments follow the exact methodology from quran_hearts.py"""
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'code'))
from quran_hearts import generate_bitmap

def method_from_quran_hearts(verse_count):
    """Exact method from quran_hearts.py"""
    seq = list(range(1, verse_count + 1))
    while len(seq) < 31:
        seq += seq[:31 - len(seq)]
    seq = seq[:31]
    binary = [format(n, '06b') for n in seq]
    matrix = np.array([[int(b) for b in row] for row in binary])
    return matrix

def method_from_experiments(sequence):
    """Method used in experiments files"""
    rows = []
    while len(rows) < 31:
        for v in sequence:
            if len(rows) < 31:
                rows.append(format(v, '06b'))
            else:
                break
    matrix = np.array([[int(b) for b in row] for row in rows])
    return matrix

print("="*60)
print("Methodology Verification")
print("التحقق من المنهجية")
print("="*60)

# Test 1: Al-Fatiha (7 verses)
print("\n1. Al-Fatiha (7 verses):")
m_main = method_from_quran_hearts(7)
m_exp = method_from_experiments(list(range(1, 8)))
match = np.array_equal(m_main, m_exp)
print(f"   Main code method: {m_main.shape}")
print(f"   Experiments method: {m_exp.shape}")
print(f"   Match: {'✅ YES' if match else '❌ NO'}")

if not match:
    print("   ⚠️ DIFFERENCE!")
    diff = np.where(m_main != m_exp)
    print(f"   Differences at: {len(diff[0])} positions")

# Test 2: Small sequence (4 verses - like Al-Ikhlas)
print("\n2. Small sequence (4 verses):")
m_main_4 = method_from_quran_hearts(4)
m_exp_4 = method_from_experiments(list(range(1, 5)))
match_4 = np.array_equal(m_main_4, m_exp_4)
print(f"   Match: {'✅ YES' if match_4 else '❌ NO'}")

# Test 3: Large sequence (99 - like Names of Allah)
print("\n3. Large sequence (99):")
# For large sequences, we need to adapt
seq_99 = list(range(1, 100))
# Main method: extend sequence first, then take 31
seq_main = seq_99.copy()
while len(seq_main) < 31:
    seq_main += seq_main[:31 - len(seq_main)]
seq_main = seq_main[:31]

# Experiments method
rows_exp = []
while len(rows_exp) < 31:
    for v in seq_99:
        if len(rows_exp) < 31:
            rows_exp.append(format(v, '06b'))
        else:
            break

m_main_99 = np.array([[int(b) for b in format(n, '06b')] for n in seq_main])
m_exp_99 = np.array([[int(b) for b in row] for row in rows_exp])

match_99 = np.array_equal(m_main_99, m_exp_99)
print(f"   Main code method: first 5 rows from {seq_main[:5]}")
print(f"   Experiments method: first 5 rows from {[int(r, 2) for r in rows_exp[:5]]}")
print(f"   Match: {'✅ YES' if match_99 else '❌ NO'}")

if not match_99:
    print("   ⚠️ DIFFERENCE!")
    print(f"   Main first row: {m_main_99[0]}")
    print(f"   Exp first row: {m_exp_99[0]}")

print("\n" + "="*60)
print("CONCLUSION:")
if match and match_4 and match_99:
    print("✅ All methods match - Methodology is consistent!")
else:
    print("⚠️ Some differences detected - Need to align methods")

