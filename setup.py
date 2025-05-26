#!/usr/bin/env python3
"""
Setup script for Ollama Web Search
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False
    return True

def check_ollama():
    """Check if Ollama is available"""
    print("🔍 Checking Ollama installation...")
    try:
        import ollama
        ollama.list()
        print("✅ Ollama is available!")
        return True
    except ImportError:
        print("❌ Ollama package not found. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "ollama"])
            print("✅ Ollama package installed!")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install Ollama package")
            return False
    except Exception as e:
        print(f"⚠️  Ollama might not be running: {e}")
        print("💡 Make sure to run 'ollama serve' before using the search tool")
        return True

def main():
    print("🚀 Setting up Ollama Web Search...")
    print("=" * 50)
    
    if not install_requirements():
        sys.exit(1)
    
    if not check_ollama():
        sys.exit(1)
    
    print("\n🎉 Setup complete!")
    print("\n📖 Usage:")
    print("  python main.py              # Interactive mode")
    print("  python main.py --history    # Show search history")
    print("  python main.py --help       # Show help")
    print("\n💡 Make sure Ollama is running with: ollama serve")
    print("🔧 Edit config.json to customize settings")

if __name__ == "__main__":
    main()
