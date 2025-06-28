import os
import subprocess
import streamlit
from playwright.sync_api import sync_playwright


def install_playwright():
    with sync_playwright() as p:
        try:
            p.chromium.install()
       
            # # Install playwright and browsers (Chromium)
            # subprocess.run(["pip", "install", "playwright"], check=True)
            # subprocess.run(["playwright", "install", "chrome"], check=True)
           
           
            # print("Playwright and Chromium installed successfully.")
            st.write('Playwright and Chromium installed successfully')
        except subprocess.CalledProcessError as e:
            st.write(f"Error during installation: {e}")

if __name__ == "__main__":
    install_playwright()
