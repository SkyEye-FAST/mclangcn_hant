# -*- encoding: utf-8 -*-
"""MCLangCN-Hant Converter"""

from shutil import copyfile
from pathlib import Path
import zipfile as zf

import opencc
import mclang

if __name__ == "__main__":
    # Initialize OpenCC converter
    converter = opencc.OpenCC("s2tw.json")

    # Set paths
    P = Path(__file__).resolve().parent
    REPO_DIR = P / "mclangcn"
    LANG_OUTPUT_DIR = P / "texts"
    LANG_ZH_CN_PATH = REPO_DIR / "texts" / "zh_CN.lang"
    LANG_OUTPUT_PATH = LANG_OUTPUT_DIR / "zh_TW.lang"

    # Ensure the directory exists
    LANG_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Load language file
    with LANG_ZH_CN_PATH.open("r", encoding="utf-8") as r:
        lang_zh_cn = mclang.load(r)

    # Convert language entries
    lang_output = {k: converter.convert(v) for k, v in lang_zh_cn.items()}

    # Save language file
    with LANG_OUTPUT_PATH.open("w", encoding="utf-8") as w:
        mclang.dump(lang_output, w)

    # Compress resource pack
    zip_path = P / "Bedrock.Translation.Patch.ST.zip"
    mcpack_path = P / "Bedrock.Translation.Patch.ST.mcpack"
    with zf.ZipFile(zip_path, "w", compression=zf.ZIP_DEFLATED, compresslevel=9) as z:
        for file in [
            "manifest.json",
            "loading_messages.json",
            "contents.json",
            "splashes.json",
            "pack_icon.png",
        ]:
            z.write(REPO_DIR / file, arcname=file)
        z.write(LANG_ZH_CN_PATH, arcname="texts/zh_CN.lang")
        z.write(LANG_OUTPUT_PATH, arcname="texts/zh_TW.lang")
        z.write(LANG_OUTPUT_DIR / "languages.json", arcname="texts/languages.json")
    copyfile(zip_path, mcpack_path)
