"""
Pattern Analyzer - Analyze generated bitmaps for heart shapes and symbols
محلل الأنماط - تحليل الصور المولدة للبحث عن أشكال القلب والرموز
"""
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
try:
    from PIL import Image
except ImportError:
    import subprocess
    subprocess.check_call(["pip", "install", "pillow", "--quiet"])
    from PIL import Image

def load_bitmap_image(image_path):
    """Load a bitmap image and convert to binary matrix"""
    img = Image.open(image_path).convert('L')  # Convert to grayscale
    img_array = np.array(img)
    # Threshold: values > 128 become 1 (black), <= 128 become 0 (white)
    binary = (img_array > 128).astype(int)
    return binary

def analyze_symmetry(matrix):
    """Analyze vertical and horizontal symmetry"""
    rows, cols = matrix.shape
    
    # Vertical symmetry (left-right)
    left_half = matrix[:, :cols//2]
    right_half = np.flip(matrix[:, cols//2:], axis=1)
    
    # Horizontal symmetry (top-bottom)
    top_half = matrix[:rows//2, :]
    bottom_half = np.flip(matrix[rows//2:, :], axis=0)
    
    vertical_symmetry = np.sum(left_half == right_half) / left_half.size
    horizontal_symmetry = np.sum(top_half == bottom_half) / top_half.size
    
    return {
        'vertical_symmetry': vertical_symmetry,
        'horizontal_symmetry': horizontal_symmetry,
        'overall_symmetry': (vertical_symmetry + horizontal_symmetry) / 2
    }

def detect_heart_shape(matrix):
    """
    Detect if the pattern resembles a heart shape
    Heart characteristics:
    - Wider at top, narrower at bottom (or vice versa)
    - Symmetrical
    - Curved edges
    """
    rows, cols = matrix.shape
    
    # Calculate width at different heights
    widths = []
    for i in range(rows):
        row = matrix[i, :]
        # Find first and last black pixel
        black_indices = np.where(row == 1)[0]
        if len(black_indices) > 0:
            width = black_indices[-1] - black_indices[0] + 1
        else:
            width = 0
        widths.append(width)
    
    # Heart shape: typically wider in middle, narrower at edges
    # Or: wider at top, tapering to bottom
    middle = rows // 2
    top_width = np.mean(widths[:middle//2])
    middle_width = np.mean(widths[middle//2:middle+middle//2])
    bottom_width = np.mean(widths[middle+middle//2:])
    
    # Check if pattern is heart-like
    is_heart_like = False
    if middle_width > top_width and middle_width > bottom_width:
        is_heart_like = True  # Wider in middle
    elif top_width > bottom_width:
        is_heart_like = True  # Tapering from top to bottom
    
    return {
        'is_heart_like': is_heart_like,
        'widths': widths,
        'top_width': top_width,
        'middle_width': middle_width,
        'bottom_width': bottom_width
    }

def detect_central_pattern(matrix):
    """Detect patterns in the center of the image"""
    rows, cols = matrix.shape
    center_row = rows // 2
    center_col = cols // 2
    
    # Extract center region (3x3 around center)
    center_region = matrix[center_row-1:center_row+2, center_col-1:center_col+2]
    
    # Check for specific patterns
    patterns = {
        'center_dense': np.sum(center_region) > 4,  # Mostly black in center
        'center_sparse': np.sum(center_region) < 2,  # Mostly white in center
        'vertical_line': np.sum(center_region[:, 1]) == 3,  # Vertical line
        'horizontal_line': np.sum(center_region[1, :]) == 3,  # Horizontal line
    }
    
    return patterns

def analyze_image(image_path):
    """Complete analysis of an image"""
    print(f"\n{'='*60}")
    print(f"Analyzing: {image_path.name}")
    print(f"{'='*60}")
    
    # Load image
    matrix = load_bitmap_image(image_path)
    print(f"Matrix shape: {matrix.shape}")
    print(f"Total pixels: {matrix.size}")
    print(f"Black pixels: {np.sum(matrix)} ({np.sum(matrix)/matrix.size*100:.1f}%)")
    
    # Symmetry analysis
    symmetry = analyze_symmetry(matrix)
    print(f"\n📊 Symmetry Analysis:")
    print(f"   Vertical symmetry: {symmetry['vertical_symmetry']*100:.1f}%")
    print(f"   Horizontal symmetry: {symmetry['horizontal_symmetry']*100:.1f}%")
    print(f"   Overall symmetry: {symmetry['overall_symmetry']*100:.1f}%")
    
    # Heart shape detection
    heart = detect_heart_shape(matrix)
    print(f"\n❤️ Heart Shape Detection:")
    print(f"   Is heart-like: {'YES ✅' if heart['is_heart_like'] else 'NO ❌'}")
    print(f"   Top width: {heart['top_width']:.1f}")
    print(f"   Middle width: {heart['middle_width']:.1f}")
    print(f"   Bottom width: {heart['bottom_width']:.1f}")
    
    # Central pattern
    center = detect_central_pattern(matrix)
    print(f"\n🎯 Central Pattern:")
    for key, value in center.items():
        print(f"   {key}: {'YES ✅' if value else 'NO ❌'}")
    
    return {
        'matrix': matrix,
        'symmetry': symmetry,
        'heart': heart,
        'center': center
    }

def main():
    """Analyze key images"""
    project_root = Path(__file__).parent.parent
    
    images_to_analyze = [
        project_root / 'Images' / '001_Al-Fatiha.png',
        project_root / 'experiments_output' / 'names_of_allah' / '099_Names_Of_Allah.png',
        project_root / 'experiments_output' / 'hearts_quran' / 'Hearts_VerseOrder.png',
    ]
    
    results = {}
    for img_path in images_to_analyze:
        if img_path.exists():
            results[img_path.name] = analyze_image(img_path)
        else:
            print(f"\n⚠️ Image not found: {img_path}")
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY | الملخص")
    print(f"{'='*60}")
    
    for name, result in results.items():
        print(f"\n{name}:")
        print(f"  Symmetry: {result['symmetry']['overall_symmetry']*100:.1f}%")
        print(f"  Heart-like: {'YES ✅' if result['heart']['is_heart_like'] else 'NO ❌'}")
        print(f"  Center dense: {'YES ✅' if result['center']['center_dense'] else 'NO ❌'}")

if __name__ == "__main__":
    try:
        import cv2
    except ImportError:
        print("⚠️ OpenCV not installed. Installing...")
        print("Run: pip install opencv-python")
        cv2 = None
    
    main()

