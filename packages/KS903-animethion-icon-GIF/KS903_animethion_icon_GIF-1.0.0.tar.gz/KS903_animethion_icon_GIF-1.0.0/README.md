# README.md

# KS903_animethion_icon_GIF

## 概要

`KS903_animethion_icon_GIF` は、KS903 のためのアニメーションアイコンGIFライブラリです。このライブラリを使用することで、簡単にアニメーションGIFをアイコンとして設定できます。

## インストール

このライブラリは、`pip` を使用してインストールできます。

```bash
pip install KS903_animethion_icon_GIF

使い方の例として
import tkinter as tk
from KS903_animetion_icon.ks_903_animetion_icon2.ks903_animate_i2con import KS903_animethion_icon_GIF

# ウィンドウを作成
root = tk.Tk()
root.geometry("300x300")

# アニメーションアイコンを設定
gif_path = "ico.gif"  # GIFファイルへのパスを設定
icon = KS903_animethion_icon_GIF(root, gif_path)

root.mainloop()

