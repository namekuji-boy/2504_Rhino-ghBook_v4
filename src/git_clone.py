#venv: site-packages
import os
import subprocess
import shutil

from utils import set_default_path as set_clone_path
from utils import handle_remove_readonly

# リポジトリのクローン
def clone_repository(path: str, git_url: str, version: str = None):
    """
    指定されたリポジトリをクローンし、オプションで特定のバージョンにチェックアウトします。
    
    Args:
        path (str): クローン先のパス。
        git_url (str): GitリポジトリのURL。
        version (str, optional): チェックアウトするバージョン。デフォルトはNone。
    """
    # 既存リポジトリ削除
    if os.path.exists(path):
        print(f"Removing existing directory: {path}")
        try:
            shutil.rmtree(path, onerror=handle_remove_readonly)
        except Exception as ex:
            print(f"Failed to remove existing directory: {ex}")
            return
    # リポジトリクローン
    try:
        print(f"Cloning repository from {git_url} to {path}")
        subprocess.run([r"C:\Program Files\Git\cmd\git.exe", "clone", git_url, path], check=True)
        print("Repository cloned successfully.")
        # 指定バージョンのチェックアウト
        if version:
            print(f"Checking out version: {version}")
            subprocess.run([r"C:\Program Files\Git\cmd\git.exe", "-C", path, "checkout", version], check=True)
            print(f"Checked out to version: {version}")
    except subprocess.CalledProcessError as cpe:
        print(f"Error during Git operation: {cpe}")
    except FileNotFoundError as fnf_error:
        print(f"Git executable not found: {fnf_error}")
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")

if __name__ == "__main__":
    # StableDiffusion をインストール
    dir_SD = set_clone_path("stable-diffusion-webui")
    clone_repository(dir_SD, "https://github.com/AUTOMATIC1111/stable-diffusion-webui.git", "v1.10.0")
    
    # StableDiffusion_Controlnet をインストール
    dir_Controlnet = set_clone_path("stable-diffusion-webui", "extensions", "sd-webui-controlnet")
    clone_repository(dir_Controlnet, "https://github.com/Mikubill/sd-webui-controlnet.git", "1.1.436")