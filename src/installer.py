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

# パッケージインストール
def create_and_install_package(package_id: str, version: str = "", exact: bool = True, description: str = "Package"):
    """
    指定されたパッケージをWindows環境でインストールするためのバッチファイルを作成し、実行します。
    
    Args:
        package_id (str): wingetでインストールするパッケージID。
        version (str): インストールするバージョン（指定がない場合は最新）。
        exact (bool): 正確な一致を求めるフラグ。
        description (str): インストール対象の説明。
    """
    # TEMPディレクトリにバッチファイルを作成
    temp_dir = os.environ.get("TEMP", "/tmp")  # TEMP環境変数を取得
    batch_file = os.path.join(temp_dir, f"install_{package_id.replace('.', '_')}.bat")

    # wingetコマンド組立て
    command = f"winget install --id {package_id}"
    if version:
        command += f" -v {version}"
    if exact:
        command += " -e"

    try:
        # バッチファイルを作成
        with open(batch_file, "w") as f:
            f.write("@echo off\n")
            f.write(f"{command}\n")
            f.write("pause\n")
            f.write("exit\n")
        print(f"Batch file created at: {batch_file}")

        # バッチファイルを実行
        subprocess.run(
            ["cmd.exe", "/c", f"start {batch_file}"],
            text=True,
            capture_output=False,
            check=True,
        )
        print(f"{description} installation completed.")
    except FileNotFoundError as fnf_error:
        print(f"File not found error: {fnf_error}")
    except subprocess.CalledProcessError as cpe:
        print(f"Error during {description} installation: {cpe}")
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")

if __name__ == "__main__":
    # Git をインストール
    create_and_install_package("Git.Git", description="Git")

    # Python3.10 をインストール
    create_and_install_package("Python.Python.3.10", description="Python 3.10")

    # CUDA をインストール
    create_and_install_package(package_id="Nvidia.CUDA", version="12.4", exact=True, description="NVIDIA CUDA Toolkit")
