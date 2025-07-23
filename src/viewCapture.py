# MIT License
# Copyright (c) 2025 KOMOIKE Takuma
# Website: https://bourbakidesign.com
# Email: info@bourbakidesign.com
#
# This file is distributed under the terms of the MIT license.
# See the LICENSE file in the project root for full license information.

#venv: site-packages
import System.Drawing
import scriptcontext as sc

def capture_viewport(filepath: str, width: int = 1920, height: int = 1080):
    """
    アクティブなRhinoビューのビューポートを指定サイズでキャプチャし、PNG形式で保存します。

    Args:
        filepath (str): 画像の保存先フルパス（例: "C:\\images\\viewport.png"）
        width (int): キャプチャ画像の幅（デフォルト: 1920）
        height (int): キャプチャ画像の高さ（デフォルト: 1080）
    """
    # Rhino上でアクティブなビューを取得
    view = sc.doc.Views.ActiveView
    if not view:
        raise RuntimeError("アクティブなビューが取得できません。Rhinoでビューポートを選択してください。")
    
    # 指定サイズでビューポートをキャプチャ
    bmp = view.CaptureToBitmap(System.Drawing.Size(width, height))
    if not bmp:
        raise RuntimeError("ビューポートのキャプチャに失敗しました。")
    
    # 指定パスにPNGとして保存
    bmp.Save(filepath, System.Drawing.Imaging.ImageFormat.Png)