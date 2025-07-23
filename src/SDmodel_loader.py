#venv: site-packages
import os
import shutil

from utils import set_default_path

def get_model_dir() -> str:
    """Stable Diffusion モデルの保存先ディレクトリを返します"""
    return set_default_path("stable-diffusion-webui", "models", "Stable-diffusion")

# モデルコピー
def model_load(src_path: str):
    """
    モデルファイルを指定のディレクトリにコピーします。

    Args:
        src_path (str): コピー元のファイルパス。

    Returns:
        str: コピーしたファイル名（成功時）。
    """
    # 入力パスを整形
    src_path = src_path.strip('"')  # 引用符を削除
    filename = os.path.basename(src_path)  # ファイル名を取得

    # コピー先ディレクトリを構築
    dest_dir = get_model_dir()
    dest_path = os.path.join(dest_dir, filename)

    # コピー先ディレクトリの作成（存在しない場合）
    if not os.path.exists(dest_dir):
        try:
            os.makedirs(dest_dir, exist_ok=True)
            print(f"コピー先ディレクトリを作成しました: {dest_dir}")
        except Exception as e:
            print(f"エラー: コピー先ディレクトリの作成に失敗しました: {e}")
            return None

    # モデルコピー
    try:
        shutil.copy2(src_path, dest_path)
        print(f"モデルファイルをコピーしました: {dest_path}")
        return filename
    except PermissionError as e:
        print(f"エラー: 権限が不足しています: {e}")
    except FileNotFoundError as e:
        print(f"エラー: 入力ファイルが見つかりません: {e}")
    except Exception as e:
        print(f"予期しないエラーが発生しました: {e}")

if __name__ == "__main__":
    test_model = input("コピー元モデルファイルのパスを入力: ")
    model_load(test_model)