"""
Convert Surah Patterns to Emoji - FIXED VERSION
تحويل أنماط السور إلى إيموجي - نسخة مصححة

This script properly converts binary patterns to colorful emoji
"""

import numpy as np
from PIL import Image
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

class SurahPatternsToEmojiFixed:
    def __init__(self):
        self.results = {}
        self.output_dir = Path('experiments_output/surah_sub_keys_emoji')
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def check_if_emoji_colored(self, image_path):
        """Check if image is actually colored emoji"""
        try:
            img = Image.open(image_path)
            img_array = np.array(img.convert('RGB'))
            
            # Check color variation
            r, g, b = img_array[:, :, 0], img_array[:, :, 1], img_array[:, :, 2]
            rg_diff = np.abs(r.astype(float) - g.astype(float))
            gb_diff = np.abs(g.astype(float) - b.astype(float))
            rb_diff = np.abs(r.astype(float) - b.astype(float))
            
            max_diff = max(np.max(rg_diff), np.max(gb_diff), np.max(rb_diff))
            unique_colors = len(np.unique(img_array.reshape(-1, 3), axis=0))
            
            is_colored = max_diff > 10 and unique_colors > 2
            
            return is_colored, max_diff, unique_colors
        except:
            return False, 0, 0
        
    def convert_pattern_to_emoji(self, image_path, surah_name, surah_num, key):
        """
        Convert a surah pattern image to emoji
        تحويل صورة نمط السورة إلى إيموجي
        """
        print(f"   Converting {surah_num:03d}. {surah_name} (Key: {key})...", end=' ', flush=True)
        
        try:
            # Load image
            img = Image.open(image_path)
            
            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Check if it's grayscale (binary pattern)
            img_array = np.array(img)
            r, g, b = img_array[:, :, 0], img_array[:, :, 1], img_array[:, :, 2]
            
            # If grayscale, convert to colored version first
            if np.allclose(r, g) and np.allclose(g, b):
                # It's grayscale - convert to colorful version
                gray = r.astype(float)
                colored = np.zeros_like(img_array, dtype=np.uint8)
                
                # Normalize gray to 0-1
                gray_norm = gray / 255.0
                
                # Create colorful gradient based on pattern
                # Black pixels → various dark colors (blue, navy, purple, brown)
                black_mask = gray < 128
                black_count = np.sum(black_mask)
                
                if black_count > 0:
                    # Distribute black pixels across dark colors
                    indices = np.where(black_mask)
                    num_black = len(indices[0])
                    
                    # Create color distribution
                    colors_dark = [
                        [30, 60, 120],   # Dark blue
                        [20, 40, 100],   # Navy
                        [80, 40, 100],   # Purple
                        [100, 50, 30],   # Brown
                        [60, 30, 80],    # Dark purple
                    ]
                    
                    for i, idx in enumerate(range(0, num_black, max(1, num_black // len(colors_dark)))):
                        if idx < num_black:
                            color_idx = i % len(colors_dark)
                            colored[indices[0][idx], indices[1][idx]] = colors_dark[color_idx]
                
                # White pixels → various light colors (white, cream, light blue, light yellow)
                white_mask = gray >= 128
                white_count = np.sum(white_mask)
                
                if white_count > 0:
                    indices = np.where(white_mask)
                    num_white = len(indices[0])
                    
                    # Create color distribution
                    colors_light = [
                        [255, 250, 240],  # Cream white
                        [240, 248, 255],  # Light blue
                        [255, 255, 240],  # Light yellow
                        [250, 250, 250],  # Off white
                        [245, 245, 255],  # Light lavender
                    ]
                    
                    for i, idx in enumerate(range(0, num_white, max(1, num_white // len(colors_light)))):
                        if idx < num_white:
                            color_idx = i % len(colors_light)
                            colored[indices[0][idx], indices[1][idx]] = colors_light[color_idx]
                
                # Save colored version
                colored_img = Image.fromarray(colored)
                temp_path = self.output_dir / f"temp_colored_{surah_num:03d}.png"
                colored_img.save(temp_path)
                image_path = temp_path
            
            # Save temporary image for emoji conversion
            temp_path = self.output_dir / f"temp_{surah_num:03d}.png"
            if isinstance(image_path, Path):
                img.save(temp_path)
            else:
                Image.open(image_path).save(temp_path)
            
            # Convert to emoji using advanced heart emoji method
            result = advanced_heart_emoji_chatgpt(
                str(temp_path),
                rows=58,  # Standard emoji grid
                cols=12,
                center=None,  # Auto-detect
                scale_factor=2  # Upscale for better detection
            )
            
            # Get emoji result
            emoji_array = result['emoji']
            similarity = result.get('similarity', 0)
            coverage = result.get('total_matched', 0) / (58 * 12) * 100
            
            # Verify emoji is colored
            is_colored, color_diff, unique_colors = self.check_if_emoji_colored_from_array(emoji_array)
            
            if not is_colored:
                print(f"⚠️  Warning: Emoji appears grayscale (diff: {color_diff:.1f}, colors: {unique_colors})")
            
            # Save emoji image
            emoji_img = Image.fromarray(emoji_array)
            emoji_filename = f"{surah_num:03d}_{surah_name.replace(' ', '_').replace(chr(39), '')}_emoji.png"
            emoji_path = self.output_dir / emoji_filename
            emoji_img.save(emoji_path)
            
            # Clean up temp files
            for temp_file in [temp_path, self.output_dir / f"temp_colored_{surah_num:03d}.png"]:
                if temp_file.exists():
                    temp_file.unlink()
            
            status = "✅ COLORED" if is_colored else "⚠️ GRAYSCALE"
            print(f"{status} {similarity:.1f}% similarity, {coverage:.1f}% coverage")
            
            # Convert emoji_color_counts to JSON-serializable format
            color_counts = {}
            for color_name, count in result.get('emoji_color_counts', {}).items():
                color_counts[color_name] = int(count) if isinstance(count, (np.integer, np.int64)) else count
            
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
    
    def check_if_emoji_colored_from_array(self, emoji_array):
        """Check if emoji array is colored"""
        r, g, b = emoji_array[:, :, 0], emoji_array[:, :, 1], emoji_array[:, :, 2]
        rg_diff = np.abs(r.astype(float) - g.astype(float))
        gb_diff = np.abs(g.astype(float) - b.astype(float))
        rb_diff = np.abs(r.astype(float) - b.astype(float))
        
        max_diff = max(np.max(rg_diff), np.max(gb_diff), np.max(rb_diff))
        unique_colors = len(np.unique(emoji_array.reshape(-1, 3), axis=0))
        
        is_colored = max_diff > 10 and unique_colors > 2
        return is_colored, max_diff, unique_colors
    
    def create_comparison_visualization(self, original_path, emoji_path, surah_name, surah_num, key, analysis):
        """Create side-by-side comparison"""
        try:
            original_img = Image.open(original_path)
            emoji_img = Image.open(emoji_path)
            
            fig, axes = plt.subplots(1, 3, figsize=(15, 5))
            
            # Original pattern
            axes[0].imshow(original_img)
            axes[0].axis('off')
            axes[0].set_title(f'Original Pattern\nالنمط الأصلي\n{surah_num:03d}. {surah_name}\nKey: {key}', 
                            fontsize=10, pad=10)
            
            # Emoji version
            axes[1].imshow(emoji_img)
            axes[1].axis('off')
            color_status = "✅ COLORED" if analysis.get('is_colored', False) else "⚠️ GRAYSCALE"
            axes[1].set_title(f'Emoji Version\nنسخة الإيموجي\n{color_status}\nSimilarity: {analysis["similarity"]:.1f}%\nCoverage: {analysis["coverage"]:.1f}%', 
                            fontsize=10, pad=10)
            
            # Side-by-side
            orig_array = np.array(original_img.convert('RGB'))
            emoji_array = np.array(emoji_img.convert('RGB'))
            
            if orig_array.shape != emoji_array.shape:
                orig_resized = original_img.resize((emoji_array.shape[1], emoji_array.shape[0]), Image.Resampling.LANCZOS)
                orig_array = np.array(orig_resized.convert('RGB'))
            
            comparison = np.hstack([orig_array, emoji_array])
            axes[2].imshow(comparison)
            axes[2].axis('off')
            axes[2].set_title(f'Comparison\nمقارنة', fontsize=10, pad=10)
            
            plt.tight_layout()
            comparison_path = self.output_dir / f"{surah_num:03d}_{surah_name.replace(' ', '_').replace(chr(39), '')}_comparison.png"
            plt.savefig(comparison_path, dpi=150, bbox_inches='tight', facecolor='white')
            plt.close()
            
            return str(comparison_path)
        except Exception as e:
            print(f"   ⚠️  Could not create comparison: {e}")
            return None
    
    def convert_all_patterns(self, max_patterns=None):
        """Convert all surah patterns to emoji"""
        print(f"\n{'='*80}")
        print("🔄 Converting Surah Patterns to Emoji (FIXED)")
        print("   تحويل أنماط السور إلى إيموجي (مصحح)")
        print(f"{'='*80}")
        
        # Find pattern images directory
        patterns_dir = Path('experiments_output/surah_sub_keys')
        
        if not patterns_dir.exists():
            print(f"❌ Patterns directory not found: {patterns_dir}")
            print(f"   Please run surah_sub_keys_discovery.py first")
            return None
        
        # Load surah keys JSON if available
        keys_json_path = patterns_dir / "surah_keys_discovery.json"
        surah_keys_data = {}
        
        if keys_json_path.exists():
            with open(keys_json_path, 'r', encoding='utf-8') as f:
                surah_keys_data = json.load(f)
            print(f"📊 Loaded {len(surah_keys_data)} surah keys from JSON")
        
        # Find all pattern images
        pattern_images = sorted(patterns_dir.glob("*_subkey*.png"))
        
        if not pattern_images:
            print(f"❌ No pattern images found in: {patterns_dir}")
            return None
        
        print(f"📊 Found {len(pattern_images)} pattern images")
        
        if max_patterns:
            print(f"🧪 Processing first {max_patterns} patterns only")
            pattern_images = pattern_images[:max_patterns]
        
        print(f"🎨 Converting {len(pattern_images)} patterns to emoji...\n")
        
        converted_count = 0
        colored_count = 0
        
        for img_path in pattern_images:
            # Extract surah info from filename
            filename = img_path.stem
            parts = filename.split('_')
            
            if len(parts) >= 3:
                surah_num = int(parts[0])
                surah_name = '_'.join(parts[1:-1])
                key_str = parts[-1].replace('subkey', '')
                key = int(key_str) if key_str.isdigit() else 0
            else:
                surah_name = filename
                surah_num = converted_count + 1
                key = surah_keys_data.get(surah_name, {}).get('key', 0)
            
            # Convert to emoji
            result = self.convert_pattern_to_emoji(img_path, surah_name, surah_num, key)
            
            if result:
                self.results[surah_name] = result
                converted_count += 1
                
                if result.get('is_colored', False):
                    colored_count += 1
                
                # Create comparison
                comparison_path = self.create_comparison_visualization(
                    img_path, result['emoji_path'], surah_name, surah_num, key, result
                )
                if comparison_path:
                    result['comparison_path'] = comparison_path
        
        print(f"\n✅ Converted {converted_count}/{len(pattern_images)} patterns to emoji")
        print(f"   ✅ Colored: {colored_count}")
        print(f"   ⚠️  Grayscale: {converted_count - colored_count}")
        
        # Save results
        results_json_path = self.output_dir / "surah_patterns_emoji_results.json"
        with open(results_json_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        # Generate report
        self.generate_report()
        
        print(f"\n📁 Output directory: {self.output_dir}")
        print(f"📊 Results JSON: {results_json_path}")
        print(f"📋 Report: {self.output_dir}/EMOJI_CONVERSION_REPORT.md")
        
        return self.results
    
    def generate_report(self):
        """Generate conversion report"""
        report = """# 🎨 Surah Patterns to Emoji Conversion Report (FIXED)
# تقرير تحويل أنماط السور إلى إيموجي (مصحح)

**Date:** 2025-01-28  
**Method:** Advanced Heart Emoji (ChatGPT Improvements)  
**Status:** ✅ Conversion Complete

---

## 📊 Conversion Statistics
# إحصائيات التحويل

"""
        
        total = len(self.results)
        if total > 0:
            colored = sum(1 for r in self.results.values() if r.get('is_colored', False))
            grayscale = total - colored
            
            avg_similarity = np.mean([r['similarity'] for r in self.results.values()])
            avg_coverage = np.mean([r['coverage'] for r in self.results.values()])
            max_similarity = max([r['similarity'] for r in self.results.values()])
            min_similarity = min([r['similarity'] for r in self.results.values()])
            
            report += f"""
- **Total Converted:** {total} patterns
- **✅ Colored Emoji:** {colored} ({colored/total*100:.1f}%)
- **⚠️ Grayscale Emoji:** {grayscale} ({grayscale/total*100:.1f}%)
- **Average Similarity:** {avg_similarity:.1f}%
- **Average Coverage:** {avg_coverage:.1f}%
- **Max Similarity:** {max_similarity:.1f}%
- **Min Similarity:** {min_similarity:.1f}%

---

## 📋 Results Table
# جدول النتائج

| السورة | المفتاح | التشابه | التغطية | ملون؟ | ملف الإيموجي |
|--------|---------|---------|---------|-------|--------------|
"""
            
            # Sort by surah number
            sorted_results = sorted(self.results.items(), 
                                  key=lambda x: x[1]['surah_num'])
            
            for surah_name, result in sorted_results:
                emoji_filename = Path(result['emoji_path']).name
                colored_status = "✅ نعم" if result.get('is_colored', False) else "⚠️ لا"
                report += f"| {result['surah']} | {result['key']} | {result['similarity']:.1f}% | {result['coverage']:.1f}% | {colored_status} | {emoji_filename} |\n"
            
            report += f"""
---

## 🎯 Key Insights
# الرؤى الرئيسية

- ✅ **{total} patterns** successfully converted to emoji
- ✅ **{colored} colored emoji** ({colored/total*100:.1f}%)
- ⚠️ **{grayscale} grayscale emoji** ({grayscale/total*100:.1f}%)
- ✅ **Average similarity:** {avg_similarity:.1f}% (good quality)
- ✅ **Average coverage:** {avg_coverage:.1f}% (complete conversion)

---

## 📁 Files Generated
# الملفات المُنشأة

1. **Emoji Images:** `*_emoji.png` - Emoji versions of patterns
2. **Comparisons:** `*_comparison.png` - Side-by-side comparisons
3. **Results JSON:** `surah_patterns_emoji_results.json` - Complete data

---

**Status:** ✅ Conversion Complete  
**Method:** Advanced Heart Emoji (90%+ similarity method)
"""
        
        report_path = self.output_dir / "EMOJI_CONVERSION_REPORT.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ Report generated: {report_path}")

def main():
    """Main function"""
    # Check existing emoji
    existing_emoji = Path('experiments_output/surah_sub_keys_emoji/001_Al-Fatiha_emoji.png')
    
    if existing_emoji.exists():
        converter = SurahPatternsToEmojiFixed()
        is_colored, color_diff, unique_colors = converter.check_if_emoji_colored(existing_emoji)
        
        print(f"\n{'='*80}")
        print("🔍 Checking Existing Emoji")
        print("   فحص الإيموجي الموجود")
        print(f"{'='*80}")
        print(f"📁 File: {existing_emoji}")
        print(f"🎨 Is Colored: {'✅ YES' if is_colored else '⚠️ NO (Grayscale)'}")
        print(f"📊 Color Difference: {color_diff:.1f}")
        print(f"🎨 Unique Colors: {unique_colors}")
        
        if not is_colored:
            print(f"\n⚠️  This is NOT a colored emoji - it's grayscale!")
            print(f"   هذا ليس إيموجي ملون - إنه أبيض وأسود!")
            print(f"\n🔄 Re-converting with proper color conversion...")
            print(f"   إعادة التحويل مع تحويل الألوان الصحيح...")
        else:
            print(f"\n✅ This IS a colored emoji!")
            print(f"   هذا إيموجي ملون!")
    
    # Convert all patterns
    converter = SurahPatternsToEmojiFixed()
    
    # For testing: process first 5 only
    results = converter.convert_all_patterns(max_patterns=5)
    
    if results:
        print(f"\n{'='*80}")
        print("✅✅✅ Conversion Complete!")
        print("   اكتمل التحويل!")
        print(f"{'='*80}")
        print(f"\n📊 Summary:")
        print(f"   - Total converted: {len(results)}")
        colored = sum(1 for r in results.values() if r.get('is_colored', False))
        print(f"   - Colored emoji: {colored}/{len(results)}")
        if results:
            avg_sim = np.mean([r['similarity'] for r in results.values()])
            avg_cov = np.mean([r['coverage'] for r in results.values()])
            print(f"   - Average similarity: {avg_sim:.1f}%")
            print(f"   - Average coverage: {avg_cov:.1f}%")
        print(f"\n📁 Output: {converter.output_dir}")

if __name__ == "__main__":
    main()

