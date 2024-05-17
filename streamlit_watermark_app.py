import streamlit as st
import zipfile
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import os

# 定数の設定（デフォルト値）
DEFAULT_FONT_PATH = 'Roboto-Regular.ttf'  # 使用するフォントファイルのパス
DEFAULT_FONT_SIZE = 36  # フォントサイズ
DEFAULT_WATERMARK_TEXT = 'Sample Watermark'  # ウォーターマークのテキスト
DEFAULT_WATERMARK_POSITION = 2  # ウォーターマークの位置（1=上部、2=中央、3=下部）
DEFAULT_TRANSPARENCY = 50  # ウォーターマークの透明度（100=完全不透明、0=透明）
DEFAULT_SHADOW_OFFSET = 2  # 影のオフセット（ピクセル）
DEFAULT_SHADOW_ENABLED = True  # 影を有効にするかどうか
DEFAULT_SHADOW_TRANSPARENCY = 70  # 影の透明度（100=完全不透明、0=透明）
IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.bmp']  # 処理対象の画像ファイル拡張子

def add_watermark_with_shadow(image_path, output_path, text, font_size, position):
    """
    指定された画像にウォーターマークを追加する関数

    Args:
        image_path (str): 入力画像のファイルパス
        output_path (str): ウォーターマークを追加した画像の保存先ファイルパス
        text (str): ウォーターマークのテキスト
        font_size (int): ウォーターマークのフォントサイズ
        position (int): ウォーターマークの位置（1=上部、2=中央、3=下部）
    """
    st.write(f"Processing image: {image_path}")

    if not os.path.exists(DEFAULT_FONT_PATH):
        st.error(f"Font file {DEFAULT_FONT_PATH} not found.")
        return

    with Image.open(image_path).convert("RGBA") as base:
        # 画像をRGBA形式に変換して開く

        # ウォーターマークを追加するための透明レイヤーを作成
        watermark_layer = Image.new("RGBA", base.size)
        draw = ImageDraw.Draw(watermark_layer)
        font = ImageFont.truetype(DEFAULT_FONT_PATH, font_size)

        # テキストのバウンディングボックスからテキストサイズを計算
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        # ウォーターマークの位置を計算
        if position == 1:
            pos = ((base.width - text_width) / 2, (base.height / 4) - text_height / 2)
        elif position == 2:
            pos = ((base.width - text_width) / 2, (base.height / 2) - text_height / 2)
        elif position == 3:
            pos = ((base.width - text_width) / 2, (3 * base.height / 4) - text_height / 2)

        # 影を描画する場合
        if DEFAULT_SHADOW_ENABLED:
            shadow_position = (pos[0] + DEFAULT_SHADOW_OFFSET, pos[1] + DEFAULT_SHADOW_OFFSET)
            shadow_color = (0, 0, 0, int(255 * DEFAULT_SHADOW_TRANSPARENCY / 100))
            draw.text(shadow_position, text, font=font, fill=shadow_color)

        # メインのテキストを描画
        text_color = (255, 255, 255, int(255 * DEFAULT_TRANSPARENCY / 100))
        draw.text(pos, text, font=font, fill=text_color)

        # 透明レイヤーを基本画像に合成し、RGB形式に変換
        combined = Image.alpha_composite(base, watermark_layer).convert("RGB")
        # 処理後の画像を保存
        combined.save(output_path, 'JPEG')
    st.write(f"Saved watermarked image to: {output_path}")

def process_images_in_zip(zip_file, text, font_size, position):
    """
    アップロードされたZIPファイル内の画像にウォーターマークを追加し、ZIPに圧縮して返す関数

    Args:
        zip_file (BytesIO): アップロードされたZIPファイル
        text (str): ウォーターマークのテキスト
        font_size (int): ウォーターマークのフォントサイズ
        position (int): ウォーターマークの位置（1=上部、2=中央、3=下部）

    Returns:
        BytesIO: ウォーターマークが追加された画像を含むZIPファイル
    """
    st.write("Extracting ZIP file...")
    # 一時ディレクトリの作成
    if not os.path.exists('temp_images'):
        os.makedirs('temp_images')
    
    # ZIPファイルを一時ディレクトリに解凍
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall('temp_images')  # 一時ディレクトリ'temp_images'に全てのファイルを展開

    st.write("Files in temporary directory after extraction:")
    st.write(os.listdir('temp_images'))

    st.write("Processing extracted images...")
    # 新しいZIPファイルを作成するためのBytesIOオブジェクトを用意
    output_zip = BytesIO()
    with zipfile.ZipFile(output_zip, 'w') as zip_out:
        # 一時ディレクトリ内の全ファイルを処理
        for root, dirs, files in os.walk('temp_images'):
            for filename in files:
                st.write(f"Found file: {filename}")
                file_path = os.path.join(root, filename)  # 各ファイルのフルパスを取得
                file_ext = os.path.splitext(filename)[1].lower()  # 拡張子を小文字で取得
                # 画像ファイルであるかどうかをチェック
                if os.path.isfile(file_path) and any(file_ext == ext for ext in IMAGE_EXTENSIONS):
                    output_path = os.path.join(root, f"wm_{filename}")  # 出力ファイルパスを設定
                    add_watermark_with_shadow(file_path, output_path, text, font_size, position)  # ウォーターマークを追加
                    zip_out.write(output_path, arcname=f"wm_{filename}")  # 新しいZIPファイルに追加
                    st.write(f"Added {output_path} to ZIP")

    # 出力ZIPファイルのポインタを先頭にリセット
    output_zip.seek(0)
    
    # デバッグ用メッセージ
    st.write("Processed files in ZIP:")
    with zipfile.ZipFile(output_zip, 'r') as zip_ref:
        st.write(zip_ref.namelist())

    return output_zip  # ウォーターマークが追加された画像を含むZIPファイルを返す

# Streamlitインターフェース
st.title("Watermark Image Processor")

# ウォーターマークの設定
watermark_text = st.text_input("Watermark Text", DEFAULT_WATERMARK_TEXT)
watermark_position = st.selectbox("Watermark Position", options=[1, 2, 3], index=1, format_func=lambda x: ["Top", "Center", "Bottom"][x-1])
font_size = st.slider("Font Size", min_value=10, max_value=100, value=DEFAULT_FONT_SIZE)

uploaded_zip = st.file_uploader("Upload a ZIP file containing images", type="zip")

if uploaded_zip is not None:
    st.write("Processing file...")
    watermarked_zip = process_images_in_zip(uploaded_zip, watermark_text, font_size, watermark_position)
    
    st.download_button(
        label="Download Watermarked Images",
        data=watermarked_zip,
        file_name="watermarked_images.zip",
        mime="application/zip"
    )
