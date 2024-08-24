# -*- encoding: utf-8 -*-
"""MCLangCN-Hant Converter"""

from pathlib import Path
import zipfile as zf

import mclang
import opencc

# Initialize OpenCC converter
converter = opencc.OpenCC("s2tw.json")

# Set paths
P = Path(__file__).resolve().parent
REPO_DIR = P / "mclangcn"
LANG_OUTPUT_DIR = P / "texts"
LANG_ZH_CN_PATH = REPO_DIR / "texts" / "zh_CN.lang"
LANG_OUTPUT_PATH = LANG_OUTPUT_DIR / "zh_TW.lang"

# Load language file
with LANG_ZH_CN_PATH.open("r", encoding="utf-8") as r:
    lang_zh_cn = mclang.load(r)

lang_output = {k: converter.convert(v) for k, v in lang_zh_cn.items()}

# Save language file
with LANG_OUTPUT_PATH.open("w", encoding="utf-8") as w:
    mclang.dump(lang_output, w)

# Compress resource pack
pack_path = P / "Bedrock.Translation.Patch.ST.zip"
with zf.ZipFile(pack_path, "w", compression=zf.ZIP_DEFLATED, compresslevel=9) as z:
    z.write(REPO_DIR / "manifest.json", arcname="manifest.json")
    z.write(REPO_DIR / "loading_messages.json", arcname="loading_messages.json")
    z.write(REPO_DIR / "contents.json", arcname="contents.json")
    z.write(REPO_DIR / "splashes.json", arcname="splashes.json")
    z.write(REPO_DIR / "pack_icon.png", arcname="pack_icon.png")
    z.write(LANG_ZH_CN_PATH, arcname="texts/zh_CN.lang")
    z.write(LANG_OUTPUT_PATH, arcname="texts/zh_TW.lang")
    z.write(LANG_OUTPUT_DIR / "languages.json", arcname="texts/languages.json")
