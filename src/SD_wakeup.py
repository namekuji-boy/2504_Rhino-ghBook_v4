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

# webui-user.bat実行
def run_bat():
    """指定されたバッチファイルを管理者権限で実行します。"""
    # パス設定
    wakeupTrigger_path = set_default_path("stable-diffusion-webui", "webui-user.bat")
    wakeupTrigger_dir = os.path.dirname(wakeupTrigger_path)

    # バッチファイルパス表示
    print(f"Runnig batch file: {wakeupTrigger_path}")
    # バッチファイルの管理者権限実行
    try:
        command = f"cd /d {wakeupTrigger_dir} && {wakeupTrigger_path}"
        subprocess.run(["powershell", "-Command", f"Start-Process cmd -ArgumentList '/c {command}' -Verb runAs"], check=True)
        print("webui-user.bat is runnig.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to run the batch file: {e}")
    except FileNotFoundError as fnf_error:
        print(f"Error: PowerShell not found: {fnf_error}")
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")

if __name__ == "__main__":
    run_bat()