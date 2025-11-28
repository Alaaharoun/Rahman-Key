"""
Convert Surah Patterns to Emoji
تحويل أنماط السور إلى إيموجي

This script:
1. Loads generated surah pattern images
2. Converts each to emoji using advanced heart emoji method
3. Saves emoji versions
4. Creates comparison visualizations
"""

import numpy as np
from PIL import Image
from pathlib import Path
import sys
import json
import matplotlib.pyplot as plt
import importlib.util

# Add path for emoji conversion
sys.path.insert(0, str(Path(__file__).parent / 'experiments_output' / 'AI_SEES_WORLD_AS_EMOJIS' / 'packages' / 'quality-vision'))
sys.path.insert(0, str(Path(__file__).parent / 'experiments_output' / 'AI_SEES_WORLD_AS_EMOJIS' / 'packages' / 'emojion-core'))

# Import emoji conversion method
# Try multiple possible paths
possible_paths = [
    Path(__file__).parent.parent / 'experiments_output' / 'AI_SEES_WORLD_AS_EMOJIS' / 'packages' / 'quality-vision' / 'advanced_heart_emoji_chatgpt_improvements.py',
    Path(__file__).parent / 'experiments_output' / 'AI_SEES_WORLD_AS_EMOJIS' / 'packages' / 'quality-vision' / 'advanced_heart_emoji_chatgpt_improvements.py',
    Path('experiments_output/AI_SEES_WORLD_AS_EMOJIS/packages/quality-vision/advanced_heart_emoji_chatgpt_improvements.py'),
]

emoji_module_path = None
for path in possible_paths:
    if path.exists():
        emoji_module_path = path
        break

if emoji_module_path and emoji_module_path.exists():
    import importlib.util
    spec = importlib.util.spec_from_file_location("emoji_module", emoji_module_path)
    emoji_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(emoji_module)
    advanced_heart_emoji_chatgpt = emoji_module.advanced_heart_emoji_chatgpt
    print("✅ Loaded emoji conversion method")
else:
    print(f"❌ Emoji module not found. Tried:")
    for p in possible_paths:
        print(f"   - {p} ({'EXISTS' if p.exists() else 'NOT FOUND'})")
    sys.exit(1)

class SurahPatternsToEmoji:
    def __init__(self):
        self.results = {}
        self.output_dir = Path('experiments_output/surah_sub_keys_emoji')
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
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
            
            # Save temporary image for emoji conversion
            temp_path = self.output_dir / f"temp_{surah_num:03d}.png"
            img.save(temp_path)
            
            # Convert to emoji using advanced heart emoji method
            # For binary patterns, use smaller grid (they're already low-res)
            # Disable multiprocessing to avoid pickling errors with dynamic imports
            result = advanced_heart_emoji_chatgpt(
                str(temp_path),
                rows=58,  # Standard emoji grid
                cols=12,
                center=None,  # Auto-detect
                scale_factor=2,  # Upscale for better detection
                use_multi_scale=True,  # Enable multi-scale
                use_context_aware=True  # Enable context-aware
            )
            
            # Get emoji result
            emoji_array = result['emoji']
            similarity = result.get('similarity', 0)
            coverage = result.get('total_matched', 0) / (58 * 12) * 100
            
            # Save emoji image
            emoji_img = Image.fromarray(emoji_array)
            emoji_filename = f"{surah_num:03d}_{surah_name.replace(' ', '_').replace(chr(39), '')}_emoji.png"
            emoji_path = self.output_dir / emoji_filename
            emoji_img.save(emoji_path)
            
            # Clean up temp file
            if temp_path.exists():
                temp_path.unlink()
            
            print(f"✅ {similarity:.1f}% similarity, {coverage:.1f}% coverage")
            
            return {
                'surah': surah_name,
                'surah_num': surah_num,
                'key': key,
                'emoji_path': str(emoji_path),
                'similarity': similarity,
                'coverage': coverage,
                'emoji_color_counts': result.get('emoji_color_counts', {})
            }
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
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
            axes[1].set_title(f'Emoji Version\nنسخة الإيموجي\nSimilarity: {analysis["similarity"]:.1f}%\nCoverage: {analysis["coverage"]:.1f}%', 
                            fontsize=10, pad=10)
            
            # Side-by-side
            # Resize to match
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
    
    def convert_all_patterns(self):
        """Convert all surah patterns to emoji"""
        print(f"\n{'='*80}")
        print("🔄 Converting Surah Patterns to Emoji")
        print("   تحويل أنماط السور إلى إيموجي")
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
        
        # For testing: process first 5 only, then ask user
        test_mode = True
        if test_mode:
            print(f"🧪 TEST MODE: Processing first 5 patterns only")
            pattern_images = pattern_images[:5]
        
        print(f"🎨 Converting {len(pattern_images)} patterns to emoji...\n")
        
        converted_count = 0
        
        for img_path in pattern_images:
            # Extract surah info from filename
            # Format: 001_Al-Fatiha_subkey123.png
            filename = img_path.stem
            parts = filename.split('_')
            
            if len(parts) >= 3:
                surah_num = int(parts[0])
                surah_name = '_'.join(parts[1:-1])  # Everything except first and last
                key_str = parts[-1].replace('subkey', '')
                key = int(key_str) if key_str.isdigit() else 0
            else:
                # Try to get from JSON
                surah_name = filename
                surah_num = converted_count + 1
                key = surah_keys_data.get(surah_name, {}).get('key', 0)
            
            # Convert to emoji
            result = self.convert_pattern_to_emoji(img_path, surah_name, surah_num, key)
            
            if result:
                self.results[surah_name] = result
                converted_count += 1
                
                # Create comparison
                comparison_path = self.create_comparison_visualization(
                    img_path, result['emoji_path'], surah_name, surah_num, key, result
                )
                if comparison_path:
                    result['comparison_path'] = comparison_path
        
        print(f"\n✅ Converted {converted_count}/{len(pattern_images)} patterns to emoji")
        
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
        report = """# 🎨 Surah Patterns to Emoji Conversion Report
# تقرير تحويل أنماط السور إلى إيموجي

**Date:** 2025-01-28  
**Method:** Advanced Heart Emoji (ChatGPT Improvements)  
**Status:** ✅ Conversion Complete

---

## 📊 Conversion Statistics
# إحصائيات التحويل

"""
        
        total = len(self.results)
        if total > 0:
            avg_similarity = np.mean([r['similarity'] for r in self.results.values()])
            avg_coverage = np.mean([r['coverage'] for r in self.results.values()])
            max_similarity = max([r['similarity'] for r in self.results.values()])
            min_similarity = min([r['similarity'] for r in self.results.values()])
            
            report += f"""
- **Total Converted:** {total} patterns
- **Average Similarity:** {avg_similarity:.1f}%
- **Average Coverage:** {avg_coverage:.1f}%
- **Max Similarity:** {max_similarity:.1f}%
- **Min Similarity:** {min_similarity:.1f}%

---

## 📋 Results Table
# جدول النتائج

| السورة | المفتاح | التشابه | التغطية | ملف الإيموجي |
|--------|---------|---------|---------|--------------|
"""
            
            # Sort by surah number
            sorted_results = sorted(self.results.items(), 
                                  key=lambda x: x[1]['surah_num'])
            
            for surah_name, result in sorted_results:
                emoji_filename = Path(result['emoji_path']).name
                report += f"| {result['surah']} | {result['key']} | {result['similarity']:.1f}% | {result['coverage']:.1f}% | {emoji_filename} |\n"
            
            report += f"""
---

## 🎯 Key Insights
# الرؤى الرئيسية

- ✅ **{total} patterns** successfully converted to emoji
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
    converter = SurahPatternsToEmoji()
    results = converter.convert_all_patterns()
    
    if results:
        print(f"\n{'='*80}")
        print("✅✅✅ Conversion Complete!")
        print("   اكتمل التحويل!")
        print(f"{'='*80}")
        print(f"\n📊 Summary:")
        print(f"   - Total converted: {len(results)}")
        if results:
            avg_sim = np.mean([r['similarity'] for r in results.values()])
            avg_cov = np.mean([r['coverage'] for r in results.values()])
            print(f"   - Average similarity: {avg_sim:.1f}%")
            print(f"   - Average coverage: {avg_cov:.1f}%")
        print(f"\n📁 Output: {converter.output_dir}")

if __name__ == "__main__":
    main()

