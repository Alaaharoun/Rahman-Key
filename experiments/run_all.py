"""
Run All Advanced Experiments
تشغيل جميع التجارب المتقدمة

This script runs all advanced experiments in sequence.
"""
import subprocess
import sys
from pathlib import Path

def run_experiment(script_name):
    """Run a single experiment script"""
    print(f"\n{'='*60}")
    print(f"Running: {script_name}")
    print(f"{'='*60}\n")
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            cwd=Path(__file__).parent,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(result.stdout)
            print(f"✅ {script_name} completed successfully")
            return True
        else:
            print(f"❌ Error in {script_name}:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Exception in {script_name}: {e}")
        return False

def main():
    """Run all experiments"""
    experiments = [
        "names_of_allah.py",
        "hearts_in_quran.py",
        "ya_ayyuhal_ladhina_amanu.py",
        "basmalah_114.py"
    ]
    
    print("=" * 60)
    print("Rahman-Key Advanced Experiments")
    print("تجارب مفتاح الرحمن المتقدمة")
    print("=" * 60)
    
    results = []
    for exp in experiments:
        success = run_experiment(exp)
        results.append((exp, success))
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY | الملخص")
    print("=" * 60)
    
    for exp, success in results:
        status = "✅" if success else "❌"
        print(f"{status} {exp}")
    
    successful = sum(1 for _, s in results if s)
    print(f"\nCompleted: {successful}/{len(results)}")
    print("=" * 60)

if __name__ == "__main__":
    main()

