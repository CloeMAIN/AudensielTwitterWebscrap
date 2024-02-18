import os
import subprocess

def install_playwright():
    # Installation de Playwright
    try:
        subprocess.run(["python", "-m", "playwright", "install"], check=True)
        print("Playwright a été installé avec succès.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'installation de Playwright : {e}")
        raise

if __name__ == "__main__":
    install_playwright()
