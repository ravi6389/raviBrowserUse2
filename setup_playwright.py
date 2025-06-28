import os
import subprocess

def install_playwright():
    try:
        # Install playwright and browsers (Chromium)
        subprocess.run(["pip", "install", "playwright"], check=True)
        subprocess.run(["playwright", "install", "chrome"], check=True)
        print("Playwright and Chromium installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during installation: {e}")

if __name__ == "__main__":
    install_playwright()
