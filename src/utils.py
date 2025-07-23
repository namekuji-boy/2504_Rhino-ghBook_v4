# MIT License
# Copyright (c) 2025 KOMOIKE Takuma
# Website: https://bourbakidesign.com
# Email: info@bourbakidesign.com
#
# This file is distributed under the terms of the MIT license.
# See the LICENSE file in the project root for full license information.

#venv: site-packages
import os
import stat

# インストール先設定
def set_default_path(*subdirs: str, create: bool = False) -> str:
    """
    ホームディレクトリからの相対パスを受け取り、インストール先の絶対パスを返します。
    `create=True` の場合、存在しなければディレクトリを作成します。

    Args:
        *subdirs (str): ホーム配下のサブディレクトリを順に指定（例："stable-diffusion-webui", "models", "ControlNet"）

    Returns:
        str: 絶対パス
    """
    home_path = os.path.expanduser("~")
    full_path = os.path.join(home_path, *subdirs)
    if create:
        os.makedirs(full_path, exist_ok=True)
    return full_path

# 読み取り専用属性解除のエラー処理
def handle_remove_readonly(func, path: str, exc_info: str):
    """読取専用ファイルを削除できるように属性を変更"""
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception as ex:
        print(f"Failed to remove readonly attribute: {path}, error: {ex}")