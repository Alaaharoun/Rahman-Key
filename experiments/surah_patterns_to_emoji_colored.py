"""
Convert Surah Patterns to COLORED Emoji - Enhanced Version
تحويل أنماط السور إلى إيموجي ملون - نسخة محسنة

This script ensures emoji output is ALWAYS colored, not grayscale
"""

import numpy as np
from PIL import Image, ImageEnhance
from pathlib import Path
import sys
import json
import matplotlib.pyplot as plt
import importlib.util

# Add path for emoji conversion
emoji_module_path = Path(__file__).parent / 'experiments_output' / 'AI_SEES_WORLD_AS_EMOJIS' / 'packages' / 'quality-vision' / 'advanced_heart_emoji_chatgpt_improvements.py'

if emoji_module_path.exists():
    spec = importlib.util.spec_from_file_location("emoji_module", emoji_module_path)
    emoji_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(emoji_module)
    advanced_heart_emoji_chatgpt = emoji_module.advanced_heart_emoji_chatgpt
    print("✅ Loaded emoji conversion method")
else:
    print(f"❌ Emoji module not found: {emoji_module_path}")
    sys.exit(1)

def convert_grayscale_to_colored(image_array):
    """
    Convert grayscale image to colorful version
    تحويل الصورة الأبيض والأسود إلى نسخة ملونة
    """
    h, w = image_array.shape[:2]
    
    # Check if grayscale
    if len(image_array.shape) == 2:
        gray = image_array
        colored = np.zeros((h, w, 3), dtype=np.uint8)
    else:
        r, g, b = image_array[:, :, 0], image_array[:, :, 1], image_array[:, :, 2]
        if np.allclose(r, g) and np.allclose(g, b):
            gray = r
            colored = np.zeros((h, w, 3), dtype=np.uint8)
        else:
            return image_array  # Already colored
    
    # Create colorful mapping
    # Black pixels → various dark colors
    black_mask = gray < 128
    black_indices = np.where(black_mask)
    num_black = len(black_indices[0])
    
    if num_black > 0:
        # Distribute across dark colors
        dark_colors = np.array([
            [30, 60, 120],   # Dark blue
            [20, 40, 100],   # Navy
            [80, 40, 100],   # Purple
            [100, 50, 30],   # Brown
            [60, 30, 80],    # Dark purple
            [40, 80, 120],   # Teal
            [120, 60, 40],   # Dark orange
        ])
        
        for i, (y, x) in enumerate(zip(black_indices[0], black_indices[1])):
            color_idx = i % len(dark_colors)
            colored[y, x] = dark_colors[color_idx]
    
    # White pixels → various light colors
    white_mask = gray >= 128
    white_indices = np.where(white_mask)
    num_white = len(white_indices[0])
    
    if num_white > 0:
        # Distribute across light colors
        light_colors = np.array([
            [255, 250, 240],  # Cream white
            [240, 248, 255],  # Light blue
            [255, 255, 240],  # Light yellow
            [250, 250, 250],  # Off white
            [245, 245, 255],  # Light lavender
            [255, 240, 245],  # Light pink
            [240, 255, 240],  # Light green
        ])
        
        for i, (y, x) in enumerate(zip(white_indices[0], white_indices[1])):
            color_idx = i % len(light_colors)
            colored[y, x] = light_colors[color_idx]
    
    return colored

def enhance_emoji_colors(emoji_array):
    """
    Enhance emoji colors to ensure it's colorful
    تحسين ألوان الإيموجي لضمان أنها ملونة
    """
    h, w = emoji_array.shape[:2]
    
    # Check if grayscale
    r, g, b = emoji_array[:, :, 0], emoji_array[:, :, 1], emoji_array[:, :, 2]
    rg_diff = np.abs(r.astype(float) - g.astype(float))
    gb_diff = np.abs(g.astype(float) - b.astype(float))
    rb_diff = np.abs(r.astype(float) - b.astype(float))
    max_diff = max(np.max(rg_diff), np.max(gb_diff), np.max(rb_diff))
    
    if max_diff < 10:  # Grayscale
        print(f"      ⚠️  Emoji is grayscale, enhancing colors...")
        
        # Convert to colorful
        enhanced = np.zeros_like(emoji_array)
        
        # Black pixels → colorful dark colors
        black_mask = r < 128
        black_indices = np.where(black_mask)
        if len(black_indices[0]) > 0:
            dark_colors = [
                [30, 60, 120],   # Dark blue
                [20, 40, 100],   # Navy
                [80, 40, 100],   # Purple
                [100, 50, 30],   # Brown
            ]
            for i, (y, x) in enumerate(zip(black_indices[0], black_indices[1])):
                enhanced[y, x] = dark_colors[i % len(dark_colors)]
        
        # White/Gray pixels → colorful light colors
        light_mask = r >= 128
        light_indices = np.where(light_mask)
        if len(light_indices[0]) > 0:
            light_colors = [
                [255, 250, 240],  # Cream
                [240, 248, 255],  # Light blue
                [255, 255, 240],  # Light yellow
                [250, 250, 250],  # Off white
            ]
            for i, (y, x) in enumerate(zip(light_indices[0], light_indices[1])):
                enhanced[y, x] = light_colors[i % len(light_colors)]
        
        return enhanced
    
    # Already colored - enhance saturation
    img = Image.fromarray(emoji_array)
    enhancer = ImageEnhance.Color(img)
    enhanced_img = enhancer.enhance(1.5)  # Increase saturation
    return np.array(enhanced_img)

class SurahPatternsToEmojiColored:
    def __init__(self):
        self.results = {}
        self.output_dir = Path('experiments_output/surah_sub_keys_emoji')
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def convert_pattern_to_emoji(self, image_path, surah_name, surah_num, key):
        """Convert pattern to colored emoji"""
        print(f"   Converting {surah_num:03d}. {surah_name} (Key: {key})...", end=' ', flush=True)
        
        try:
            # Load image
            img = Image.open(image_path)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            img_array = np.array(img)
            
            # Convert grayscale to colored FIRST
            colored_array = convert_grayscale_to_colored(img_array)
            colored_img = Image.fromarray(colored_array)
            
            # Save colored version
            temp_path = self.output_dir / f"temp_colored_{surah_num:03d}.png"
            colored_img.save(temp_path)
            
            # Convert to emoji
            result = advanced_heart_emoji_chatgpt(
                str(temp_path),
                rows=58,
                cols=12,
                center=None,
                scale_factor=2
            )
            
            # Get emoji result
            emoji_array = result['emoji']
            
            # ENHANCE colors to ensure it's colorful
            emoji_array = enhance_emoji_colors(emoji_array)
            
            # Verify it's colored
            is_colored, color_diff, unique_colors = self.check_colors(emoji_array)
            
            similarity = result.get('similarity', 0)
            coverage = result.get('total_matched', 0) / (58 * 12) * 100
            
            # Save emoji
            emoji_img = Image.fromarray(emoji_array)
            emoji_filename = f"{surah_num:03d}_{surah_name.replace(' ', '_').replace(chr(39), '')}_emoji.png"
            emoji_path = self.output_dir / emoji_filename
            emoji_img.save(emoji_path)
            
            # Clean up
            if temp_path.exists():
                temp_path.unlink()
            
            status = "✅ COLORED" if is_colored else "⚠️ STILL GRAYSCALE"
            print(f"{status} {similarity:.1f}% similarity, {coverage:.1f}% coverage, {unique_colors} colors")
            
            # Convert color counts
            color_counts = {}
            for color_name, count in result.get('emoji_color_counts', {}).items():
                color_counts[color_name] = int(count) if isinstance(count, (np.integer, np.int64)) else int(count)
            
            return {
                'surah': surah_name,
                'surah_num': surah_num,
                'key': key,
                'emoji_path': str(emoji_path),
                'similarity': float(similarity),
                'coverage': float(coverage),
                'is_colored': bool(is_colored),
                'color_diff': float(color_diff),
                'unique_colors': int(unique_colors),
                'emoji_color_counts': color_counts
            }
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def check_colors(self, emoji_array):
        """Check if emoji is colored"""
        r, g, b = emoji_array[:, :, 0], emoji_array[:, :, 1], emoji_array[:, :, 2]
        rg_diff = np.abs(r.astype(float) - g.astype(float))
        gb_diff = np.abs(g.astype(float) - b.astype(float))
        rb_diff = np.abs(r.astype(float) - b.astype(float))
        max_diff = max(np.max(rg_diff), np.max(gb_diff), np.max(rb_diff))
        unique_colors = len(np.unique(emoji_array.reshape(-1, 3), axis=0))
        is_colored = max_diff > 10 and unique_colors > 2
        return is_colored, max_diff, unique_colors
    
    def convert_all_patterns(self, max_patterns=None):
        """Convert all patterns"""
        print(f"\n{'='*80}")
        print("🎨 Converting Surah Patterns to COLORED Emoji")
        print("   تحويل أنماط السور إلى إيموجي ملون")
        print(f"{'='*80}")
        
        patterns_dir = Path('experiments_output/surah_sub_keys')
        if not patterns_dir.exists():
            print(f"❌ Patterns directory not found")
            return None
        
        pattern_images = sorted(patterns_dir.glob("*_subkey*.png"))
        if not pattern_images:
            print(f"❌ No pattern images found")
            return None
        
        print(f"📊 Found {len(pattern_images)} pattern images")
        
        if max_patterns:
            pattern_images = pattern_images[:max_patterns]
            print(f"🧪 Processing first {max_patterns} patterns")
        
        print(f"🎨 Converting to COLORED emoji...\n")
        
        converted = 0
        colored = 0
        
        for img_path in pattern_images:
            filename = img_path.stem
            parts = filename.split('_')
            
            if len(parts) >= 3:
                surah_num = int(parts[0])
                surah_name = '_'.join(parts[1:-1])
                key_str = parts[-1].replace('subkey', '')
                key = int(key_str) if key_str.isdigit() else 0
            else:
                surah_name = filename
                surah_num = converted + 1
                key = 0
            
            result = self.convert_pattern_to_emoji(img_path, surah_name, surah_num, key)
            
            if result:
                self.results[surah_name] = result
                converted += 1
                if result.get('is_colored', False):
                    colored += 1
        
        print(f"\n✅ Converted {converted} patterns")
        print(f"   ✅ Colored: {colored}/{converted}")
        
        # Save results
        results_path = self.output_dir / "surah_patterns_emoji_results.json"
        with open(results_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        return self.results

def main():
    """Main function"""
    # Check existing
    existing = Path('experiments_output/surah_sub_keys_emoji/001_Al-Fatiha_emoji.png')
    if existing.exists():
        converter = SurahPatternsToEmojiColored()
        is_colored, color_diff, unique_colors = converter.check_colors(np.array(Image.open(existing)))
        
        print(f"\n{'='*80}")
        print("🔍 Checking Existing Emoji")
        print(f"{'='*80}")
        print(f"📁 File: {existing.name}")
        print(f"🎨 Is Colored: {'✅ YES' if is_colored else '⚠️ NO (Grayscale)'}")
        print(f"📊 Color Difference: {color_diff:.1f}")
        print(f"🎨 Unique Colors: {unique_colors}")
        
        if not is_colored:
            print(f"\n⚠️  This is NOT a colored emoji!")
            print(f"🔄 Re-converting with color enhancement...")
    
    # Convert
    converter = SurahPatternsToEmojiColored()
    results = converter.convert_all_patterns(max_patterns=5)
    
    if results:
        print(f"\n{'='*80}")
        print("✅✅✅ Conversion Complete!")
        print(f"{'='*80}")
        colored = sum(1 for r in results.values() if r.get('is_colored', False))
        print(f"📊 Colored emoji: {colored}/{len(results)}")

if __name__ == "__main__":
    main()

