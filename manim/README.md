# Manim 动画工具

本目录存放所有 Manim（3Blue1Brown 风格）动画脚本及渲染说明。
渲染产生的 GIF/MP4 文件放入 `docs/public/` 后即可在 VitePress 文章中直接引用。

---

## 环境要求

| 依赖 | 版本 | 说明 |
|------|------|------|
| Python | ≥ 3.10 | 系统自带或 pyenv |
| ffmpeg | ≥ 6.x | 视频合成 |
| Cairo + Pango + HarfBuzz | 系统包 | 文字与矢量渲染 |
| Manim Community | 0.20.x | 动画引擎 |

---

## 安装步骤（Ubuntu / Debian）

### 1. 安装系统依赖

通常 Ubuntu 22.04 / 24.04 已预装 ffmpeg、libcairo2、libpango，只缺少开发头文件：

```bash
sudo apt-get install -y \
  ffmpeg \
  libcairo2-dev \
  libpango1.0-dev \
  libharfbuzz-dev \
  pkg-config \
  python3-dev
```

> **已知问题**：在某些 Ubuntu 24.04 环境中，`pkg-config` 无法自动找到 Cairo / Pango 头文件路径。
> 需要通过 `C_INCLUDE_PATH` 手动告知 GCC：

```bash
export C_INCLUDE_PATH=\
/usr/include/cairo:\
/usr/include/glib-2.0:\
/usr/lib/x86_64-linux-gnu/glib-2.0/include:\
/usr/include/pango-1.0:\
/usr/include/harfbuzz
```

### 2. 安装 Python 包

```bash
# 先单独构建 manimpango（依赖上面的 C_INCLUDE_PATH）
C_INCLUDE_PATH=/usr/include/cairo:/usr/include/glib-2.0:/usr/lib/x86_64-linux-gnu/glib-2.0/include:/usr/include/pango-1.0:/usr/include/harfbuzz \
  pip3 install manimpango

# 再安装 manim（其余依赖会自动二进制安装，不需要特殊路径）
pip3 install manim
```

验证安装：

```bash
python3 -c "import manim; print(manim.__version__)"
# 预期输出：0.20.1
```

> **注意**：Manim 不需要 LaTeX。所有脚本均使用 `Text`（Pango 渲染），不使用 `MathTex`/`Tex`。

---

## 目录结构

```
manim/
├── README.md               ← 本文件
├── rotation_anims.py       ← 旋转等价性动画（对应文章 rotation-equivalence.md）
└── media/                  ← 渲染输出（已加入 .gitignore）
```

---

## 渲染命令

所有渲染命令均在 `manim/` 目录下执行。

### 渲染全部 GIF（供文章使用）

```bash
cd manim/

# 内旋 Z-Y-X 动画
manim -qm --format gif rotation_anims.py IntrinsicZYX

# 外旋 X-Y-Z 动画
manim -qm --format gif rotation_anims.py ExtrinsicXYZ

# 等价性对比动画
manim -qm --format gif rotation_anims.py Equivalence
```

渲染完成后，将输出文件复制到 `docs/public/`：

```bash
cp media/videos/rotation_anims/720p30/GIF/*.gif ../docs/public/
```

### 质量参数说明

| 参数 | 分辨率 | 帧率 | 用途 |
|------|--------|------|------|
| `-ql` | 480p | 15 fps | 快速预览 |
| `-qm` | 720p | 30 fps | 文章正文 |
| `-qh` | 1080p | 60 fps | 精细输出 |

### 预览单个场景（不渲染为文件）

```bash
manim -p rotation_anims.py IntrinsicZYX
```

---

## 在文章中引用

VitePress 的静态资源根目录为 `docs/public/`，引用时以 `/auto-robot-nav-2026-note/` 为前缀：

```markdown
![内旋 Z-Y-X 动画](/intrinsic-zyx.gif)
```
