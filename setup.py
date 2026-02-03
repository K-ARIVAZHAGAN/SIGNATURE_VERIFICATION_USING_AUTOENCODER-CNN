#!/usr/bin/env python3
"""
Setup script for Signature Verification System
This script helps set up the project environment and dependencies
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def create_directories():
    """Create necessary directories"""
    directories = [
        'uploads',
        'data/genuine_signatures', 
        'data/forged_signatures',
        'data/user_contributed',
        'models',
        'logs'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Created directory: {directory}")
        else:
            print(f"✅ Directory exists: {directory}")
    
    # Create .gitkeep files for empty directories
    for directory in directories:
        gitkeep_path = os.path.join(directory, '.gitkeep')
        if not os.path.exists(gitkeep_path):
            with open(gitkeep_path, 'w') as f:
                f.write('')
            print(f"📄 Created .gitkeep in {directory}")

def install_dependencies():
    """Install Python dependencies"""
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt not found")
        return False
    
    return run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing Python dependencies"
    )

def check_models():
    """Check if model files exist"""
    model_files = ['models/model.h5', 'models/autoencoder.h5']
    missing_models = []
    
    for model_file in model_files:
        if not os.path.exists(model_file):
            missing_models.append(model_file)
        else:
            print(f"✅ Model found: {model_file}")
    
    if missing_models:
        print(f"\n⚠️  Missing model files: {missing_models}")
        print("You'll need to train the models using the Jupyter notebook:")
        print("1. Open Signature_verification_system.ipynb")
        print("2. Run all cells to train the models")
        print("3. Models will be saved to the models/ directory")
    
    return len(missing_models) == 0

def setup_jupyter():
    """Set up Jupyter notebook"""
    return run_command(
        f"{sys.executable} -m ipykernel install --user --name signature-verification",
        "Setting up Jupyter kernel"
    )

def run_tests():
    """Run basic tests to verify setup"""
    print("\n🧪 Running basic tests...")
    
    # Test imports
    try:
        import flask
        import tensorflow as tf
        import numpy as np
        from PIL import Image
        print("✅ All required packages imported successfully")
        
        # Test TensorFlow GPU
        if tf.config.list_physical_devices('GPU'):
            print("✅ GPU support detected")
        else:
            print("⚠️  No GPU detected, using CPU")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up Signature Verification System")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Create directories
    create_directories()
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed: Could not install dependencies")
        return False
    
    # Set up Jupyter
    setup_jupyter()
    
    # Run tests
    if not run_tests():
        print("\n❌ Setup failed: Import errors detected")
        return False
    
    # Check models
    models_exist = check_models()
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed!")
    print("\nNext steps:")
    print("1. If models are missing, run the Jupyter notebook to train them")
    print("2. Start the web application: python app.py")
    print("3. Open your browser to http://localhost:5000")
    
    if not models_exist:
        print("\n⚠️  Don't forget to train the models first!")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)