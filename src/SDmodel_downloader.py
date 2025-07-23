# MIT License
# Copyright (c) 2025 KOMOIKE Takuma
# Website: https://bourbakidesign.com
# Email: info@bourbakidesign.com
#
# This file is distributed under the terms of the MIT license.
# See the LICENSE file in the project root for full license information.

#venv: site-packages
import os
import subprocess

from utils import set_default_path

# インストール先設定 (オプション: create=True)
def set_model_path(*subdirs: str) -> str:
    """モデル専用：create=True 固定で set_clone_path を呼出"""
    return set_default_path(*subdirs, create=True)

# モデルURL設定
def build_model_url(repo_url: str, filename: str) -> str:
    """
    HuggingFace 形式のモデルURLを組み立てて返します。

    Args:
        repo_url (str): モデルのHuggingFaceリポジトリURL（例: https://huggingface.co/xxx）
        filename (str): safetensorsなどのファイル名（例: control_*.safetensors）

    Returns:
        str: ダウンロード用の完全URL
    """
    return f"{repo_url.rstrip('/')}/resolve/main/{filename}"

def download_file(url: str, save_path: str):
    """
    指定されたURLからファイルをダウンロードし、指定のパスに保存します。
    
    Args:
        url (str): ダウンロード元のURL。
        save_path (str): 保存先のファイルパス。
    """
    # 既存ファイル削除
    if os.path.exists(save_path):
        print(f"Removing existing file: {save_path}")
        try:
            os.remove(save_path)
        except Exception as ex:
            print(f"Failed to remove existing file: {ex}")
    # ダウンロード処理
    try:
        print(f"Downloading from: {url}")
        subprocess.run(["curl", "-L", url, "-o", save_path], check=True)
        print(f"Saved to: {save_path}")
    except subprocess.CalledProcessError as cpe:
        print(f"Download failed: {cpe}")
    except FileNotFoundError:
        print("curl is not installed or not found in PATH.")
    except Exception as ex:
        print(f"An unexpected error occurred during download: {ex}")

if __name__ == "__main__":
    # リポジトリURL設定
    repo_url = "https://huggingface.co/comfyanonymous/ControlNet-v1-1_fp16_safetensors"
    filename = "control_v11p_sd15_canny_fp16.safetensors"
    url = build_model_url(repo_url, filename)

    # 保存先設定
    model_dir = set_model_path("stable-diffusion-webui", "models", "ControlNet", create=True)
    download_path = os.path.join(model_dir, filename)

    # インストール
    download_file(url, download_path)
