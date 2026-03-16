"""
rotation_anims.py
=================
3Blue1Brown 风格的旋转等价性动画，对应文章 docs/articles/rotation-equivalence.md

包含三个场景：
  IntrinsicZYX  — 逐步展示内旋 Z→Y'→X'' 旋转过程
  ExtrinsicXYZ  — 逐步展示外旋 X→Y→Z 旋转过程（固定世界轴）
  Equivalence   — 并排对比，直观看出两者终态完全相同

渲染命令（在 manim/ 目录下执行）：
  manim -qm --format gif rotation_anims.py IntrinsicZYX
  manim -qm --format gif rotation_anims.py ExtrinsicXYZ
  manim -qm --format gif rotation_anims.py Equivalence

注意：本文件不依赖 LaTeX，所有文本使用 Text（Pango 渲染）。
"""

from manim import *
import numpy as np

# ---------------------------------------------------------------------------
# 全局参数
# ---------------------------------------------------------------------------

ALPHA = 45 * DEGREES   # 绕 Z 轴旋转
BETA  = 30 * DEGREES   # 绕 Y 轴旋转
GAMMA = 60 * DEGREES   # 绕 X 轴旋转

BG_COLOR    = "#0d1117"   # 深色背景
WORLD_COLOR = "#ffffff"   # 世界轴颜色
X_COLOR     = "#ff5555"   # X 轴 / X 方向：红
Y_COLOR     = "#50fa7b"   # Y 轴 / Y 方向：绿
Z_COLOR     = "#8be9fd"   # Z 轴 / Z 方向：蓝
LABEL_COLOR = "#f8f8f2"   # 普通文字
STEP_COLOR  = "#ffb86c"   # 步骤提示
FORM_COLOR  = "#bd93f9"   # 公式文字
HIGHLIGHT   = "#ff79c6"   # 高亮强调


# ---------------------------------------------------------------------------
# 工具函数
# ---------------------------------------------------------------------------

def rodrigues(axis: np.ndarray, angle: float) -> np.ndarray:
    """Rodrigues 旋转公式：绕单位 axis 旋转 angle 弧度的 3×3 旋转矩阵。"""
    axis = np.asarray(axis, dtype=float)
    axis = axis / np.linalg.norm(axis)
    c, s = np.cos(angle), np.sin(angle)
    K = np.array([
        [     0, -axis[2],  axis[1]],
        [ axis[2],      0, -axis[0]],
        [-axis[1],  axis[0],      0],
    ])
    return c * np.eye(3) + s * K + (1 - c) * np.outer(axis, axis)


def make_triad(length: float = 1.6) -> VGroup:
    """创建 RGB 颜色的 XYZ 坐标架（三支 Arrow3D）。"""
    return VGroup(
        Arrow3D(ORIGIN, RIGHT * length, color=X_COLOR, resolution=6),
        Arrow3D(ORIGIN, UP    * length, color=Y_COLOR, resolution=6),
        Arrow3D(ORIGIN, OUT   * length, color=Z_COLOR, resolution=6),
    )


def world_axes_mob() -> ThreeDAxes:
    """创建淡色世界坐标轴。"""
    return ThreeDAxes(
        x_range=[-2.5, 2.5, 1],
        y_range=[-2.5, 2.5, 1],
        z_range=[-2.5, 2.5, 1],
        x_length=5, y_length=5, z_length=5,
        axis_config={
            "stroke_width": 1.2,
            "stroke_color": WORLD_COLOR,
            "stroke_opacity": 0.20,
        },
    )


def axis_arc(axis_vec: np.ndarray, angle: float,
             radius: float = 1.0, color: str = YELLOW) -> Arc:
    """
    在与 axis_vec 垂直的平面内画一段弧，用于示意旋转方向。
    仅做示意用，不做精确的 3D ArcBetweenPoints。
    """
    arc = Arc(radius=radius, angle=angle, color=color, stroke_width=4)
    arc.set_stroke(color, opacity=0.7)
    return arc


# ---------------------------------------------------------------------------
# 场景一：内旋 Z-Y-X
# ---------------------------------------------------------------------------

class IntrinsicZYX(ThreeDScene):
    """
    逐步演示内旋（Intrinsic）Z→Y'→X'' 旋转。
    每一步绕的是随物体旋转后的新轴，矩阵从右往左累积。
    """

    def construct(self):
        self.camera.background_color = BG_COLOR
        self.set_camera_orientation(phi=65 * DEGREES, theta=-35 * DEGREES)

        world = world_axes_mob()
        triad = make_triad()

        # ── 固定在画面上的文字 ──────────────────────────────────────────────
        title = Text("内旋  Z → Y' → X''", font_size=34,
                     color=HIGHLIGHT, weight=BOLD)
        subtitle = Text("Intrinsic  Z-Y-X", font_size=22, color=LABEL_COLOR)
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.1)

        step_txt  = Text("初始状态", font_size=24, color=STEP_COLOR)
        form_txt  = Text("R = I", font_size=24, color=FORM_COLOR)

        for mob in (title_group, step_txt, form_txt):
            self.add_fixed_in_frame_mobjects(mob)
        title_group.to_corner(UL, buff=0.3)
        step_txt.to_corner(DL, buff=0.3)
        form_txt.to_corner(DR, buff=0.3)

        self.add(world, triad)
        self.wait(0.8)

        # ── 步骤 1：绕固定 Z 轴旋转 α ────────────────────────────────────────
        new_step = Text("① 绕 Z 轴旋转  α = 45°", font_size=24, color=STEP_COLOR)
        new_form = Text("R₁ = Rz(α)", font_size=24, color=FORM_COLOR)
        self.remove(step_txt, form_txt)
        self.add_fixed_in_frame_mobjects(new_step, new_form)
        new_step.to_corner(DL, buff=0.3)
        new_form.to_corner(DR, buff=0.3)

        z_axis = np.array([0.0, 0.0, 1.0])
        self.play(
            Rotate(triad, ALPHA, axis=z_axis, about_point=ORIGIN),
            run_time=1.6,
        )
        self.wait(0.5)

        # ── 步骤 2：绕新 Y' 轴旋转 β ──────────────────────────────────────────
        # Y' = Rz(α) · ĵ
        Rz_mat = rodrigues(z_axis, ALPHA)
        y_prime = Rz_mat @ np.array([0.0, 1.0, 0.0])

        s2 = Text("② 绕新 Y' 轴旋转  β = 30°", font_size=24, color=STEP_COLOR)
        f2 = Text("R₂ = Rz(α)·Ry(β)", font_size=24, color=FORM_COLOR)
        self.remove(new_step, new_form)
        self.add_fixed_in_frame_mobjects(s2, f2)
        s2.to_corner(DL, buff=0.3)
        f2.to_corner(DR, buff=0.3)

        self.play(
            Rotate(triad, BETA, axis=y_prime, about_point=ORIGIN),
            run_time=1.6,
        )
        self.wait(0.5)

        # ── 步骤 3：绕新 X'' 轴旋转 γ ─────────────────────────────────────────
        # X'' = R2 · î，R2 = Ry' · Rz
        Ry_prime = rodrigues(y_prime, BETA)
        R2 = Ry_prime @ Rz_mat
        x_double_prime = R2 @ np.array([1.0, 0.0, 0.0])

        s3 = Text("③ 绕新 X'' 轴旋转  γ = 60°", font_size=24, color=STEP_COLOR)
        f3 = Text("R = Rz(α)·Ry(β)·Rx(γ)", font_size=22, color=FORM_COLOR)
        self.remove(s2, f2)
        self.add_fixed_in_frame_mobjects(s3, f3)
        s3.to_corner(DL, buff=0.3)
        f3.to_corner(DR, buff=0.3)

        self.play(
            Rotate(triad, GAMMA, axis=x_double_prime, about_point=ORIGIN),
            run_time=1.6,
        )
        self.wait(0.5)

        # ── 结尾：绕场景缓慢转一圈 ─────────────────────────────────────────────
        done = Text("最终姿态", font_size=24, color=HIGHLIGHT)
        self.remove(s3)
        self.add_fixed_in_frame_mobjects(done)
        done.to_corner(DL, buff=0.3)

        self.begin_ambient_camera_rotation(rate=0.18)
        self.wait(3.5)
        self.stop_ambient_camera_rotation()
        self.wait(0.5)


# ---------------------------------------------------------------------------
# 场景二：外旋 X-Y-Z
# ---------------------------------------------------------------------------

class ExtrinsicXYZ(ThreeDScene):
    """
    逐步演示外旋（Extrinsic）X→Y→Z 旋转。
    每一步绕的是永远固定的世界轴，矩阵从右往左累积（左乘）。
    注意角度顺序：γ 绕 X，β 绕 Y，α 绕 Z（与内旋正好相反）。
    """

    def construct(self):
        self.camera.background_color = BG_COLOR
        self.set_camera_orientation(phi=65 * DEGREES, theta=-35 * DEGREES)

        # 世界轴：外旋里始终固定，画得更明显
        world = ThreeDAxes(
            x_range=[-2.5, 2.5, 1],
            y_range=[-2.5, 2.5, 1],
            z_range=[-2.5, 2.5, 1],
            x_length=5, y_length=5, z_length=5,
            axis_config={
                "stroke_width": 2.5,
                "stroke_opacity": 0.45,
            },
            x_axis_config={"stroke_color": X_COLOR},
            y_axis_config={"stroke_color": Y_COLOR},
            z_axis_config={"stroke_color": Z_COLOR},
        )
        triad = make_triad()

        # ── 固定在画面上的文字 ──────────────────────────────────────────────
        title    = Text("外旋  X → Y → Z", font_size=34,
                        color=HIGHLIGHT, weight=BOLD)
        subtitle = Text("Extrinsic  X-Y-Z", font_size=22, color=LABEL_COLOR)
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.1)

        step_txt = Text("初始状态", font_size=24, color=STEP_COLOR)
        form_txt = Text("R = I",    font_size=24, color=FORM_COLOR)
        note_txt = Text("世界轴始终固定", font_size=20, color=WORLD_COLOR)

        for mob in (title_group, step_txt, form_txt, note_txt):
            self.add_fixed_in_frame_mobjects(mob)
        title_group.to_corner(UL, buff=0.3)
        step_txt.to_corner(DL, buff=0.3)
        form_txt.to_corner(DR, buff=0.3)
        note_txt.to_edge(DOWN, buff=0.15)

        self.add(world, triad)
        self.wait(0.8)

        # ── 步骤 1：绕固定 X 轴旋转 γ = 60° ────────────────────────────────
        s1 = Text("① 绕固定 X 轴旋转  γ = 60°", font_size=24, color=STEP_COLOR)
        f1 = Text("R₁ = Rx(γ)", font_size=24, color=FORM_COLOR)
        self.remove(step_txt, form_txt)
        self.add_fixed_in_frame_mobjects(s1, f1)
        s1.to_corner(DL, buff=0.3)
        f1.to_corner(DR, buff=0.3)

        self.play(
            Rotate(triad, GAMMA, axis=RIGHT, about_point=ORIGIN),
            run_time=1.6,
        )
        self.wait(0.5)

        # ── 步骤 2：绕固定 Y 轴旋转 β = 30° ────────────────────────────────
        s2 = Text("② 绕固定 Y 轴旋转  β = 30°", font_size=24, color=STEP_COLOR)
        f2 = Text("R₂ = Ry(β)·Rx(γ)", font_size=24, color=FORM_COLOR)
        self.remove(s1, f1)
        self.add_fixed_in_frame_mobjects(s2, f2)
        s2.to_corner(DL, buff=0.3)
        f2.to_corner(DR, buff=0.3)

        self.play(
            Rotate(triad, BETA, axis=UP, about_point=ORIGIN),
            run_time=1.6,
        )
        self.wait(0.5)

        # ── 步骤 3：绕固定 Z 轴旋转 α = 45° ────────────────────────────────
        s3 = Text("③ 绕固定 Z 轴旋转  α = 45°", font_size=24, color=STEP_COLOR)
        f3 = Text("R = Rz(α)·Ry(β)·Rx(γ)", font_size=22, color=FORM_COLOR)
        self.remove(s2, f2)
        self.add_fixed_in_frame_mobjects(s3, f3)
        s3.to_corner(DL, buff=0.3)
        f3.to_corner(DR, buff=0.3)

        self.play(
            Rotate(triad, ALPHA, axis=OUT, about_point=ORIGIN),
            run_time=1.6,
        )
        self.wait(0.5)

        # ── 结尾 ───────────────────────────────────────────────────────────
        done = Text("最终姿态", font_size=24, color=HIGHLIGHT)
        self.remove(s3)
        self.add_fixed_in_frame_mobjects(done)
        done.to_corner(DL, buff=0.3)

        self.begin_ambient_camera_rotation(rate=0.18)
        self.wait(3.5)
        self.stop_ambient_camera_rotation()
        self.wait(0.5)


# ---------------------------------------------------------------------------
# 场景三：等价性对比
# ---------------------------------------------------------------------------

class Equivalence(ThreeDScene):
    """
    并排展示内旋 Z-Y-X 与外旋 X-Y-Z 的终态，
    然后将两个坐标架叠在一起，证明它们完全重合。
    最终显示公式 R_intrinsic = R_extrinsic = Rz·Ry·Rx。
    """

    def _final_triad(self) -> VGroup:
        """
        计算 Rz(α)·Ry(β)·Rx(γ) 后的坐标架终态。
        内旋/外旋终态完全相同，直接计算这个矩阵即可。
        """
        Rz = rodrigues([0, 0, 1], ALPHA)
        Ry = rodrigues([0, 1, 0], BETA)
        Rx = rodrigues([1, 0, 0], GAMMA)
        R_final = Rz @ Ry @ Rx   # = Rz·Ry·Rx

        L = 1.5
        x_end = R_final @ np.array([L, 0, 0])
        y_end = R_final @ np.array([0, L, 0])
        z_end = R_final @ np.array([0, 0, L])

        return VGroup(
            Arrow3D(ORIGIN, x_end, color=X_COLOR, resolution=6),
            Arrow3D(ORIGIN, y_end, color=Y_COLOR, resolution=6),
            Arrow3D(ORIGIN, z_end, color=Z_COLOR, resolution=6),
        )

    def construct(self):
        self.camera.background_color = BG_COLOR
        self.set_camera_orientation(phi=65 * DEGREES, theta=-35 * DEGREES)

        world = world_axes_mob()

        # ── 两个坐标架，各自做完整旋转序列，最终重叠 ─────────────────────
        # 内旋结果（左侧，偏移 -2.2）
        triad_A = make_triad(length=1.4)
        triad_A.shift(LEFT * 2.2)

        # 外旋结果（右侧，偏移 +2.2）
        triad_B = make_triad(length=1.4)
        triad_B.shift(RIGHT * 2.2)

        label_A = Text("内旋 Z-Y-X", font_size=22, color=STEP_COLOR)
        label_B = Text("外旋 X-Y-Z", font_size=22, color=FORM_COLOR)
        self.add_fixed_in_frame_mobjects(label_A, label_B)
        label_A.move_to(LEFT * 3.5 + UP * 3.0)
        label_B.move_to(RIGHT * 3.5 + UP * 3.0)

        title = Text("终态对比", font_size=34, color=HIGHLIGHT, weight=BOLD)
        self.add_fixed_in_frame_mobjects(title)
        title.to_corner(UL, buff=0.3)

        self.add(world, triad_A, triad_B)
        self.wait(0.5)

        # ── 执行内旋 Z-Y-X（左侧 triad_A）─────────────────────────────────
        z_axis   = np.array([0.0, 0.0, 1.0])
        Rz_mat   = rodrigues(z_axis, ALPHA)
        y_prime  = Rz_mat @ np.array([0.0, 1.0, 0.0])
        Ry_prime = rodrigues(y_prime, BETA)
        R2       = Ry_prime @ Rz_mat
        x_pp     = R2 @ np.array([1.0, 0.0, 0.0])

        # 执行外旋 X-Y-Z（右侧 triad_B），三步同时进行
        self.play(
            # 内旋第 1 步：绕 Z
            Rotate(triad_A, ALPHA, axis=z_axis, about_point=triad_A.get_center()),
            # 外旋第 1 步：绕固定 X
            Rotate(triad_B, GAMMA, axis=RIGHT,  about_point=triad_B.get_center()),
            run_time=1.4,
        )
        self.play(
            # 内旋第 2 步：绕 Y'
            Rotate(triad_A, BETA, axis=y_prime, about_point=triad_A.get_center()),
            # 外旋第 2 步：绕固定 Y
            Rotate(triad_B, BETA,  axis=UP,    about_point=triad_B.get_center()),
            run_time=1.4,
        )
        self.play(
            # 内旋第 3 步：绕 X''
            Rotate(triad_A, GAMMA, axis=x_pp,  about_point=triad_A.get_center()),
            # 外旋第 3 步：绕固定 Z
            Rotate(triad_B, ALPHA, axis=OUT,   about_point=triad_B.get_center()),
            run_time=1.4,
        )
        self.wait(0.6)

        # ── 将两个坐标架合拢到原点，展示重合 ──────────────────────────────
        merge_note = Text("两者叠合 → 完全相同", font_size=26, color=HIGHLIGHT)
        self.add_fixed_in_frame_mobjects(merge_note)
        merge_note.to_corner(DL, buff=0.3)

        self.play(
            triad_A.animate.shift(RIGHT * 2.2),
            triad_B.animate.shift(LEFT  * 2.2),
            run_time=1.4,
        )
        self.wait(0.5)

        # ── 显示最终公式 ────────────────────────────────────────────────────
        formula = Text(
            "R_intrinsic = R_extrinsic = Rz(α)·Ry(β)·Rx(γ)",
            font_size=22, color=FORM_COLOR,
        )
        self.add_fixed_in_frame_mobjects(formula)
        formula.to_edge(DOWN, buff=0.3)

        # 缓慢旋转相机展示三维姿态
        self.begin_ambient_camera_rotation(rate=0.18)
        self.wait(4.0)
        self.stop_ambient_camera_rotation()
        self.wait(0.8)
