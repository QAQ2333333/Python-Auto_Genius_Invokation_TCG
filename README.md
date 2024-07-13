
# 七圣召唤全自动化项目（GPT写的.md(bushi

## 项目简介
本项目使用 OpenCV 和 Pyautogui 实现了《原神》七圣召唤的全自动化。通过该脚本，玩家可以在游戏内自动进行选卡和操作，提高游戏体验和效率。

## 功能特性
- 自动识别并选择卡牌
- 自动进行游戏内的操作

## 安装指南

在运行脚本之前，请确保满足以下要求：

1. **以管理员身份运行该脚本**
2. **屏幕分辨率必须为 1600x900**

### 所需库

请确保安装以下 Python 库：

```python
import time
import cv2
import numpy as np
import pygetwindow as gw
import pyautogui
import pytesseract
```

### 安装 Tesseract-OCR

1. 下载并安装 Tesseract-OCR：[下载链接](https://github.com/tesseract-ocr/tesseract)
2. 安装完成后，将 Tesseract-OCR 安装路径添加到环境变量中
3. 在脚本中指定 Tesseract-OCR 的安装路径，例如：

```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### 必备图片

确保脚本所在目录下包含以下 16 张图片：

```
就是根目录下的那图片
```

## 使用方法

1. 进入游戏内初始选卡阶段
2. 运行脚本

## 注意事项

- **一定要以管理员身份运行该脚本！！！**
- **屏幕分辨率必须为 1600x900！！！**

## 待完善功能

- 当前版本尚未适配冻结、超载等特殊情况，后续版本会尽快更新以支持更多功能。

## 贡献

欢迎对本项目提出建议或贡献代码，感谢大家的支持和帮助！

---

如果你对该项目有任何疑问或建议，欢迎通过 GitHub Issues 或 Pull Requests 与我联系。
