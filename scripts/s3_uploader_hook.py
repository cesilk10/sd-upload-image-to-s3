import os
from pathlib import Path
import boto3
from modules import script_callbacks, shared


# AWS設定
# s3 = boto3.client("s3", region_name="us-east-1")
session = boto3.Session(profile_name="")
s3 = session.client("s3", region_name="us-east-1")

bucket_name = ""

# shared.opts に設定追加（UIにも表示される）
def on_ui_settings():
    section = ("s3_uploader", "S3 Uploader")
    shared.opts.add_option(
        "s3_upload_enabled",
        shared.OptionInfo(False, "Upload generated images to S3", section=section)
    )

script_callbacks.on_ui_settings(on_ui_settings)

# 実際の画像保存時フック
def on_image_saved(params):
    if not shared.opts.s3_upload_enabled:
        return  # チェックボックスがOFFならスキップ

    path = Path(params.filename)
    if not path.exists():
        return
    try:
        s3.upload_file(str(path), bucket_name, path.as_posix())
        print(f"[S3 UPLOAD] {path.as_posix()}")
    except Exception as e:
        print(f"[S3 ERROR] {e}")

script_callbacks.on_image_saved(on_image_saved)
