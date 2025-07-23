import requests
import base64
import io
from PIL import Image

def run_sd(prompt: str, n_prompt: str, image_path: str, output_path: str, model: str = "Model", controlnet: bool = "ControlNet"):
    """
    Stable Diffusion WebUI API (txt2img) にリクエストを送信し、画像を生成して保存します。
    ControlNet (Canny) を有効にして元画像に基づく生成を行います。

    Args:
        prompt (str): ポジティブプロンプト（生成したい内容の指示）
        n_prompt (str): ネガティブプロンプト（避けたい内容の指示）
        image_path (str): Canny用の入力画像ファイルパス
        output_path (str): 生成画像の保存先ファイルパス
        model (str): 使用するモデル名（例: "Anything-V5.safetensors"）
        controlnet (bool): ControlNet を使用するかどうか（True/False）
    """
    # 入力画像を読み込み、Base64エンコード
    img = Image.open(image_path)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    img_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")

    # WebUIのAPIエンドポイント
    url = "http://127.0.0.1:7861/sdapi/v1/txt2img"
    # APIへ送信するペイロード構築
    payload = {
        "prompt": prompt,
        "negative_prompt": n_prompt,
        "steps": 20,                    # 生成ステップ数
        "sampler_index": "DPM++ 2M",    # サンプラー
        "width": 768,
        "height": 512,
        "cfg_scale": 7,                 # guidance scale（大きいほどプロンプトに忠実）
        "seed": -1,                     # ランダムシード（固定したいときは数値指定）
        "alwayson_scripts": {
            "controlnet": {
                "args": [
                    {
                        "enabled": controlnet,
                        "module": "canny",      # ControlNetの前処理モジュール
                        "model": "control_v11p_sd15_canny_fp16",
                        "weight": 1.0,          # ControlNetの強さ
                        "image": img_b64,
                        "low_vram": True,
                        "processor_res": 512,
                        "control_mode": "Balanced",
                        "pixel_perfect": False,
                        "threshold_a": 100,     # Cannyの下限閾値
                        "threshold_b": 200      # Cannyの上限閾値
                    }
                ]
            }
        },
        "override_settings": {
            "sd_model_checkpoint": model        # 指定モデルを明示
        }
    }

    # POSTリクエスト
    res = requests.post(url, json=payload)
    res.raise_for_status()

    # Base64エンコードされた画像をデコードして保存
    gen_img = res.json()["images"][0]
    with open(output_path, "wb") as f:
        f.write(base64.b64decode(gen_img))

if __name__ == "__main__":
    # サンプルプロンプト
    pos_prompt = "a futuristic robot in a neon-lit alley, detailed, cinematic lighting"
    neg_prompt = "low quality, blurry, distorted"

    # 入力画像（ControlNetのcanny対象）
    src_image_path = "./prompt/20250723_srcImage_a_futuristic_0001.png"  # 実際のパスに合わせて変更
    # 出力画像
    output_image_path = "./genImages/20250723_genImg_a_futuristic_0001.png"  # 実際のパスに合わせて変更

    # モデル名（WebUI上で指定されたチェックポイント名）
    model_name = "anything-v5.safetensors"  # 実環境に合わせて変更

    # 実行
    try:
        run_sd(
            prompt=pos_prompt,
            n_prompt=neg_prompt,
            image_path=src_image_path,
            output_path=output_image_path,
            model=model_name,
            controlnet=True
        )
        print(f"画像生成が完了しました: {output_image_path}")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
