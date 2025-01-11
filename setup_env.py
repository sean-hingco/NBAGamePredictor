import os
import subprocess
import sys

def create_venv():
    venv_dir = "venv"
    python_executable = sys.executable

    # Check if venv already exists
    if os.path.exists(venv_dir):
        print(f"Virtual environment already exists at {venv_dir}.")
        return

    # Create virtual environment
    print(f"Creating virtual environment using {python_executable}...")
    subprocess.run([python_executable, "-m", "venv", venv_dir], check=True)
    print(f"Virtual environment created at {venv_dir}.")

def activate_venv():
    venv_dir = "venv"
    if sys.platform == "win32":
        activate_script = os.path.join(venv_dir, "Scripts", "activate.bat")
    else:
        activate_script = os.path.join(venv_dir, "bin", "activate")

    if os.path.exists(activate_script):
        print(f"To activate the virtual environment, run:")
        if sys.platform == "win32":
            print(f"    {activate_script}")
        else:
            print(f"    source {activate_script}")
    else:
        print("Activation script not found. Something went wrong.")

def install_requirements():
    requirements_file = "requirements.txt"
    if os.path.exists(requirements_file):
        print("Installing dependencies from requirements.txt...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", requirements_file], check=True)
        print("Dependencies installed.")
    else:
        print(f"{requirements_file} not found. Skipping dependency installation.")

if __name__ == "__main__":
    create_venv()
    install_requirements()
    activate_venv()
