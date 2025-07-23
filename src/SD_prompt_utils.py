# MIT License
# Copyright (c) 2025 KOMOIKE Takuma
# Website: https://bourbakidesign.com
# Email: info@bourbakidesign.com
#
# This file is distributed under the terms of the MIT license.
# See the LICENSE file in the project root for full license information.

#venv: site-packages
import os
import re
import glob
from datetime import datetime

# プロンプト保存ディレクトリ設定
base_prompt_dir = os.path.join(os.path.dirname(__file__), "..", "prompt")
# 生成画像保存ディレクトリ設定
gen_images_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "genImages"))

def sanitize_prompt(prompt: str) -> str:
    """
    ファイル名に使用できる形式にプロンプトを変換。
    - 英数字と「_」「-」「.」「空白」以外の文字は「_」に変換。
    - 最大長は30文字に制限。
    """
    return re.sub(r'[^\w\-_\. ]', '_', prompt)[:30]

def generate_filename(prefix: str, extension: str, prompt: str = "", base_dir: str = base_prompt_dir) -> str:
    """
    指定されたプロンプトに基づき、重複しないファイル名を自動生成します。

    Args:
        prefix (str): ファイル名の先頭（例: posPrompt, negPrompt）
        extension (str): ファイル拡張子（例: txt, png）
        prompt (str): ファイル名に含めるプロンプト（オプション）
        base_dir (str): 保存先のディレクトリ（デフォルトはプロンプト用）

    Returns:
        str: 一意のファイルパス
    """
    today = datetime.now().strftime("%Y%m%d")
    sanitized = sanitize_prompt(prompt)
    base = f"{today}_{prefix}_{sanitized}"
    pattern = os.path.join(base_dir, f"{base}_*.{extension}")
    existing = glob.glob(pattern)     # 既存ファイル数を確認して連番を振る
    index = len(existing) + 1
    return os.path.join(base_dir, f"{base}_{index:04d}.{extension}")

def prepare_prompt_files(pos: str, neg: str):
    """
    ポジティブ・ネガティブプロンプト用テキストファイルと画像のファイルパスを準備します。

    - prompt/ フォルダに `posPrompt_*.txt`、`negPrompt_*.txt` を保存
    - prompt/ フォルダに `srcImage_*.png` のファイル名を予約（書き込みは別途）
    - genImages/ フォルダに `genImg_*.png` のファイル名を予約（生成画像用）

    Args:
        pos (str): ポジティブプロンプト文字列
        neg (str): ネガティブプロンプト文字列

    Returns:
        Tuple[str, str, str, str]: 書き込まれた/書き込む予定のファイルパス（pos, neg, srcImage, genImage）
    """
    # 保存先ディレクトリ作成
    os.makedirs(base_prompt_dir, exist_ok=True)
    os.makedirs(gen_images_dir, exist_ok=True)
    # 各ファイルパス生成
    pos_path = generate_filename("posPrompt", "txt", pos)
    neg_path = generate_filename("negPrompt", "txt", neg)
    src_img_path = generate_filename("srcImage", "png", pos)
    gen_img_path = generate_filename("genImg", "png", pos, base_dir=gen_images_dir)

    # プロンプトテキストを保存
    with open(pos_path, "w", encoding="utf-8") as f:
        f.write(pos)
    with open(neg_path, "w", encoding="utf-8") as f:
        f.write(neg)

    # ファイルパスを返却（後続処理で使用）
    return pos_path, neg_path, src_img_path, gen_img_path

if __name__ == "__main__":
    # テスト用のプロンプト文字列を用意
    pos_prompt = "a futuristic cityscape at night, cyberpunk style"
    neg_prompt = "low quality, blurry, watermark"

    # 関数を呼び出してファイルを準備
    pos_path, neg_path, src_img_path, gen_img_path = prepare_prompt_files(pos_prompt, neg_prompt)

    # ファイルパスを表示
    print("ポジティブプロンプト保存先:", pos_path)
    print("ネガティブプロンプト保存先:", neg_path)
    print("元画像ファイルパス（予約）:", src_img_path)
    print("生成画像ファイルパス（予約）:", gen_img_path)