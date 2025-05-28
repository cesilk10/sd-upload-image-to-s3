import os
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import boto3
from modules import script_callbacks, shared


# AWS設定
session = boto3.Session(profile_name="")
s3 = session.client("s3", region_name="ap-northeast-1")
bucket_name = ""


def current_jst_date() -> str:
    japan_now = datetime.now(ZoneInfo("Asia/Tokyo"))
    return japan_now.strftime("%Y-%m-%d")


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

    date = current_jst_date()

    try:
        s3_path = f"outputs/{date}/{path.name}"
        s3.upload_file(str(path), bucket_name, s3_path)

        print(f"[S3 UPLOAD] {s3_path}")

        jpg_path = Path(params.filename.replace(".png", ".jpg"))

        if jpg_path.exists():
            s3_path2 = f"outputs/{date}/{jpg_path.name}"
            s3.upload_file(str(jpg_path), bucket_name, s3_path2)

            print(f"[S3 UPLOAD JPG] {s3_path2}")
    except Exception as e:
        print(f"[S3 ERROR] {e}")

script_callbacks.on_image_saved(on_image_saved)


def clean_outputs_before_save(params):
    outputs_dir = Path("outputs")
    if outputs_dir.exists():
        for file in outputs_dir.rglob("*"):
            if file.is_file():
                try:
                    file.unlink()
                    print(f"[CLEANUP] Deleted: {file}")
                except Exception as e:
                    print(f"[CLEANUP ERROR] {file}: {e}")

# 保存前にフックする
script_callbacks.on_before_image_saved(clean_outputs_before_save)