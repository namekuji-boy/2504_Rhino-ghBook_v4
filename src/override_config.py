#venv: site-packages
import os

from utils import set_default_path

# バッチファイル上書き
def bat_override():
    """バッチファイルを上書き作成します。存在しない場合は新規作成します。"""
    # パス設定
    bat_path = set_default_path("stable-diffusion-webui", "webui-user.bat")
    python_path = set_default_path("AppData", "Local", "Programs", "Python", "Python310", "python.exe")

    # バッチファイル内容作成
    bat_override_content = [
        "@echo off",
        "",
        f"set PYTHON={python_path}",
        "set GIT=",
        "set VENV_DIR=",
        "set COMMANDLINE_ARGS=--xformers --medvram --api --nowebui --skip-torch-cuda-test",
        "",
        "call webui.bat",
        "pause"
    ]
    # バッチファイル作成または上書き
    try:
        with open(bat_path, "w", encoding="utf-8") as f:
            f.write("\n".join(bat_override_content))
        print(f"Batch file successfully created/overwritten: {bat_path}")
    except Exception as ex:
        print(f"Failed to write batch file: {ex}")

def req_override():
    """requirements_versions.txt を上書き作成"""
    # パス設定
    req_path = set_default_path("stable-diffusion-webui", "requirements_versions.txt")
    
    # バッチファイル内容作成
    req_override_content = [
        "setuptools==69.5.1  # temp fix for compatibility with some old packages",
        "GitPython==3.1.32",
        "Pillow==9.5.0",
        "accelerate==0.21.0",
        "blendmodes==2022",
        "clean-fid==0.1.35",
        "diskcache==5.6.3",
        "einops==0.4.1",
        "facexlib==0.3.0",
        "fastapi==0.94.0",
        "gradio==3.41.2",
        "httpcore==0.15",
        "inflection==0.5.1",
        "jsonmerge==1.8.0",
        "kornia==0.6.7",
        "lark==1.1.2",
        "numpy==1.26.2",
        "omegaconf==2.2.3",
        "open-clip-torch==2.20.0",
        "piexif==1.1.3",
        "protobuf==3.20.0",
        "psutil==5.9.5",
        "pytorch_lightning==1.9.4",
        "resize-right==0.0.2",
        "safetensors==0.4.2",
        "scikit-image==0.21.0",
        "spandrel==0.3.4",
        "spandrel-extra-arches==0.1.1",
        "tomesd==0.1.3",
        "torch",
        "torchdiffeq==0.2.3",
        "torchsde==0.2.6",
        "transformers==4.30.2",
        "httpx==0.24.1",
        "pillow-avif-plugin==1.4.3",
        "",
        "numpy==1.26.2",
        "opencv-python==4.9.0.80",
        "opencv-contrib-python==4.9.0.80",
        "",
        "pydantic==1.10.13",
        "albumentations==1.3.1"
    ]
    # バッチファイル作成または上書き
    try:
        with open(req_path, "w", encoding="utf-8") as f:
            f.write("\n".join(req_override_content))
        print(f"Requirements file successfully created/overwritten: {req_path}")
    except Exception as ex:
        print(f"Failed to write requirements file: {ex}")

if __name__ == "__main__":
    bat_override()
    req_override()
