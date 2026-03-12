# Homework #1 — 解题思路引导版

> EE5346 Autonomous Robot Navigation, Spring 2026
> 齐次变换与四元数

这份文档不是直接给答案——它带你**一步一步**看见每道题背后藏的结构。你会发现，当你真正"看懂"问题时，计算其实只是收尾。

---

## Q1：纠正观测方程 (1.4)

### 🔍 先盯着题看一会儿

题目给了一个 2D 激光雷达的观测方程。激光测量两个东西：到地标的**距离** $r$ 和**角度** $\phi$。

原方程定义的 pose 是 $\mathbf{x}_k = [x_1, x_2]_k^\mathrm{T}$——等等，一个二维平面上的机器人，pose 只有两个分量？

> 💡 **第一个嗅觉**：平面机器人的 pose 应该是 $(x, y, \theta)$——位置加朝向。只有 $(x, y)$ 的话，你怎么知道机器人"面朝哪里"？

### 🧩 距离 $r$ 没什么问题

$$
r_{k,j} = \sqrt{(y_{1,j} - x_{1,k})^2 + (y_{2,j} - x_{2,k})^2}
$$

这就是欧氏距离，纯几何，没争议。

### 🧩 角度 $\phi$ 有问题

原文的角度是：

$$
\phi_{k,j} = \arctan\left(\frac{y_{2,j} - x_{2,k}}{y_{1,j} - x_{1,k}}\right)
$$

你仔细想：这个 $\arctan$ 算出来的是什么？是从**世界坐标系**的 x 轴到地标方向的角度。但激光传感器是装在机器人身上的——它测的 $\phi$ 应该是相对于**机器人朝向**的角度！

> 💡 **这一步很妙**：观测是传感器"看到"的东西，它是机器人视角的。所以正确的角度应该减去机器人朝向 $\theta_k$。

另外，$\arctan$ 在 $x < 0$ 时会出象限错误，用 $\arctan2$ 更安全。

### ✅ 修正后的方程

$$
\begin{bmatrix} r_{k,j} \\ \phi_{k,j} \end{bmatrix}
= \begin{bmatrix}
\sqrt{(y_{1,j}-x_{1,k})^2 + (y_{2,j}-x_{2,k})^2} \\
\arctan2(y_{2,j}-x_{2,k},\; y_{1,j}-x_{1,k}) - \theta_k
\end{bmatrix} + \mathbf{v}_{k,j}
$$

**总结错误**：① pose 应包含 $\theta_k$；② 角度需减去机器人朝向；③ $\arctan$ 应替换为 $\arctan2$。

---

## Q2：四元数旋转保持纯虚性

### 🔍 这道题在问什么？

四元数旋转公式 (2.33) 说：

$$
\mathbf{p}' = \mathbf{q}\,\mathbf{p}\,\mathbf{q}^{-1}
$$

其中 $\mathbf{p} = [0, x, y, z]^\mathrm{T}$ 是纯虚四元数（实部为零）。题目要验证：$\mathbf{p}'$ 的实部也是零。

> 💡 这很重要——如果旋转后的结果不是纯虚四元数，那它就不对应一个三维空间点了。这是四元数旋转能"work"的核心保障。

### 🧩 思路：直接算实部

设 $\mathbf{q} = [s, \mathbf{v}]^\mathrm{T}$，$\mathbf{p} = [0, \mathbf{u}]^\mathrm{T}$。单位四元数满足 $\mathbf{q}^{-1} = \mathbf{q}^* = [s, -\mathbf{v}]^\mathrm{T}$。

**第一步**：用四元数乘法公式 (2.24) 算 $\mathbf{q}\mathbf{p}$：

$$
\mathbf{q}\mathbf{p} = [s,\mathbf{v}]\cdot[0,\mathbf{u}] = [-\mathbf{v}^\mathrm{T}\mathbf{u},\; s\mathbf{u}+\mathbf{v}\times\mathbf{u}]
$$

记 $\alpha = -\mathbf{v}^\mathrm{T}\mathbf{u}$，$\boldsymbol{\beta} = s\mathbf{u}+\mathbf{v}\times\mathbf{u}$。

**第二步**：算 $[\alpha, \boldsymbol{\beta}]\cdot[s, -\mathbf{v}]$，取实部：

$$
\text{Re}(\mathbf{p}') = \alpha s + \boldsymbol{\beta}^\mathrm{T}\mathbf{v}
$$

代入展开：

$$
= (-\mathbf{v}^\mathrm{T}\mathbf{u})\cdot s + (s\mathbf{u}+\mathbf{v}\times\mathbf{u})^\mathrm{T}\mathbf{v}
$$

$$
= -s(\mathbf{v}^\mathrm{T}\mathbf{u}) + s(\mathbf{u}^\mathrm{T}\mathbf{v}) + (\mathbf{v}\times\mathbf{u})^\mathrm{T}\mathbf{v}
$$

> 💡 **看出来了吗？** 前两项 $-s(\mathbf{v}^\mathrm{T}\mathbf{u}) + s(\mathbf{u}^\mathrm{T}\mathbf{v})$ 是完全一样的，对消为零。第三项 $(\mathbf{v}\times\mathbf{u})^\mathrm{T}\mathbf{v}$ 呢？叉积的结果垂直于 $\mathbf{v}$ 和 $\mathbf{u}$，所以它和 $\mathbf{v}$ 的点积天然为零。

三项全为零 → 实部 = 0 → $\mathbf{p}'$ 是纯虚四元数。✓

> 🤓 整个证明的美在于：你不需要知道 $\mathbf{q}$ 具体是什么旋转，只需要用代数结构就能得出结论。这就是四元数的设计之精妙。

---

## Q3：用 $\mathrm{Rot}_z(60°)$ 变换坐标

### 🔍 先理清楚方向

**关键问题**：参考系中的点 $\mathbf{p}$，变换到一个**旋转过的局部坐标系**中，坐标怎么变？

> 💡 很多人在这里搞反方向。记住：如果局部坐标系相对参考系旋转了 $\mathbf{R}$，那么同一个点在局部坐标系中的坐标是 $\mathbf{p}_{\text{local}} = \mathbf{R}^{-1}\mathbf{p} = \mathbf{R}^\mathrm{T}\mathbf{p}$。

直觉：坐标系往左转了 $60°$，那点在新坐标系里"看起来"就像往右转了 $60°$。

### (a) 旋转矩阵法

$$
\mathrm{Rot}_z(60°) = \begin{bmatrix}\frac{1}{2} & -\frac{\sqrt{3}}{2} & 0 \\ \frac{\sqrt{3}}{2} & \frac{1}{2} & 0 \\ 0 & 0 & 1\end{bmatrix}
$$

转置（因为正交矩阵的逆就是转置）：

$$
\mathbf{R}^\mathrm{T} = \begin{bmatrix}\frac{1}{2} & \frac{\sqrt{3}}{2} & 0 \\ -\frac{\sqrt{3}}{2} & \frac{1}{2} & 0 \\ 0 & 0 & 1\end{bmatrix}
$$

$$
\mathbf{p}_{\text{local}} = \mathbf{R}^\mathrm{T}\begin{bmatrix}2\\1\\0\end{bmatrix}
= \begin{bmatrix}\frac{1}{2}\cdot 2 + \frac{\sqrt{3}}{2}\cdot 1 \\ -\frac{\sqrt{3}}{2}\cdot 2 + \frac{1}{2}\cdot 1 \\ 0\end{bmatrix}
= \begin{bmatrix}1+\frac{\sqrt{3}}{2} \\ \frac{1}{2}-\sqrt{3} \\ 0\end{bmatrix}
\approx \begin{bmatrix}1.866 \\ -1.232 \\ 0\end{bmatrix}
$$

### (b) 四元数法

绕 z 轴旋转 $60°$ 的四元数：

$$
\mathbf{q} = \left[\cos 30°,\; \sin 30°(0,0,1)\right]^\mathrm{T} = \left[\frac{\sqrt{3}}{2}, 0, 0, \frac{1}{2}\right]^\mathrm{T}
$$

> 💡 注意：四元数表示旋转角度的**一半**！所以 $60°$ 的旋转用 $\cos 30°$ 和 $\sin 30°$。

逆旋转用 $\mathbf{q}^*$（共轭）：

$$
\mathbf{q}^* = \left[\frac{\sqrt{3}}{2}, 0, 0, -\frac{1}{2}\right]^\mathrm{T}
$$

把 $\mathbf{p}$ 扩展为纯虚四元数 $\tilde{\mathbf{p}} = [0, 2, 1, 0]^\mathrm{T}$，然后计算：

$$
\mathbf{p}_{\text{local}} = \mathbf{q}^* \tilde{\mathbf{p}} \mathbf{q}
$$

**第一步**：$\mathbf{q}^*\tilde{\mathbf{p}} = [\frac{\sqrt{3}}{2}, (0,0,-\frac{1}{2})] \cdot [0, (2,1,0)]$

用 $[s_1,\mathbf{v}_1]\cdot[s_2,\mathbf{v}_2] = [s_1 s_2 - \mathbf{v}_1\cdot\mathbf{v}_2,\; s_1\mathbf{v}_2+s_2\mathbf{v}_1+\mathbf{v}_1\times\mathbf{v}_2]$：

- 实部：$\frac{\sqrt{3}}{2}\cdot 0 - (0,0,-\frac{1}{2})\cdot(2,1,0) = 0$
- 虚部：$\frac{\sqrt{3}}{2}(2,1,0) + 0\cdot(0,0,-\frac{1}{2}) + (0,0,-\frac{1}{2})\times(2,1,0)$

叉积 $(0,0,-\frac{1}{2})\times(2,1,0)$：

$$
= \begin{vmatrix}\mathbf{i}&\mathbf{j}&\mathbf{k}\\0&0&-\frac{1}{2}\\2&1&0\end{vmatrix}
= \left(\frac{1}{2}, -1, 0\right)
$$

所以虚部 $= (\sqrt{3}+\frac{1}{2},\; \frac{\sqrt{3}}{2}-1,\; 0)$

$\mathbf{q}^*\tilde{\mathbf{p}} = [0,\; (\sqrt{3}+\frac{1}{2},\;\frac{\sqrt{3}}{2}-1,\;0)]$

**第二步**：结果乘以 $\mathbf{q}$。设 $\boldsymbol{\beta} = (\sqrt{3}+\frac{1}{2},\;\frac{\sqrt{3}}{2}-1,\;0)$。

$[0, \boldsymbol{\beta}]\cdot[\frac{\sqrt{3}}{2}, (0,0,\frac{1}{2})]$：
- 实部：$0 - \boldsymbol{\beta}\cdot(0,0,\frac{1}{2}) = 0$ ✓（果然还是纯虚的！）
- 虚部：$\frac{\sqrt{3}}{2}\boldsymbol{\beta} + \boldsymbol{\beta}\times(0,0,\frac{1}{2})$

经过计算（过程见提交版），最终得到：

$$
\mathbf{p}_{\text{local}} = \left[1+\frac{\sqrt{3}}{2},\;\frac{1}{2}-\sqrt{3},\;0\right]^\mathrm{T} \approx [1.866,\;-1.232,\;0]^\mathrm{T}
$$

> 🤓 两种方法得到完全一样的结果——这种一致性检查是你确认自己没算错的最好方式。

---

## Q4：用公式 (2.39) 从四元数推旋转矩阵

### 🔍 这道题的结构

给的四元数是 $\mathbf{q} = [\cos\frac{\theta}{2},\;\sin\frac{\theta}{2}(0,0,1)]^\mathrm{T}$——这是一个**绕 z 轴旋转 $\theta$** 的四元数。

公式 (2.39)：

$$
\mathbf{R} = \mathbf{v}\mathbf{v}^\mathrm{T} + s^2\mathbf{I} + 2s\mathbf{v}^\wedge + (\mathbf{v}^\wedge)^2
$$

> 💡 关键观察：$\mathbf{v} = (0,0,\sin\frac{\theta}{2})$，所以 $\mathbf{v}\mathbf{v}^\mathrm{T}$ 是一个只有右下角有值的矩阵——这大大简化了计算。

### 🧩 分块计算

设 $c = \cos\frac{\theta}{2}$，$s_h = \sin\frac{\theta}{2}$。

$$
\mathbf{v}\mathbf{v}^\mathrm{T} = \begin{bmatrix}0&0&0\\0&0&0\\0&0&s_h^2\end{bmatrix},\quad
s^2\mathbf{I} = \begin{bmatrix}c^2&0&0\\0&c^2&0\\0&0&c^2\end{bmatrix}
$$

$$
\mathbf{v}^\wedge = \begin{bmatrix}0&-s_h&0\\s_h&0&0\\0&0&0\end{bmatrix}
$$

> 💡 **反对称矩阵** $\mathbf{v}^\wedge$ 就是叉积的矩阵形式。对于 $\mathbf{v} = (0,0,v_3)$，它的结构特别简单。

$$
2s\mathbf{v}^\wedge = \begin{bmatrix}0&-2cs_h&0\\2cs_h&0&0\\0&0&0\end{bmatrix}
$$

$$
(\mathbf{v}^\wedge)^2 = \begin{bmatrix}-s_h^2&0&0\\0&-s_h^2&0\\0&0&0\end{bmatrix}
$$

### ✅ 加起来

$$
\mathbf{R} = \begin{bmatrix}
c^2-s_h^2 & -2cs_h & 0 \\
2cs_h & c^2-s_h^2 & 0 \\
0 & 0 & 1
\end{bmatrix}
$$

> 💡 **妙的来了**——用二倍角公式：$c^2 - s_h^2 = \cos^2\frac{\theta}{2} - \sin^2\frac{\theta}{2} = \cos\theta$，$2cs_h = \sin\theta$。

$$
\mathbf{R} = \begin{bmatrix}\cos\theta & -\sin\theta & 0 \\ \sin\theta & \cos\theta & 0 \\ 0 & 0 & 1\end{bmatrix} = \mathrm{Rot}_z(\theta)
$$

> 🤓 绕 z 轴旋转的四元数，通过公式 (2.39) 正好还原出 $\mathrm{Rot}_z(\theta)$。整个推导没有任何"意外"——这说明公式是自洽的。

---

## Q5：单位四元数转旋转向量

### 🔍 题目给了什么

$$
\mathbf{q} = [0.8,\;(0.35355, 0.35355, 0.35355)]^\mathrm{T}
$$

> 💡 注意三个虚部分量相等——这暗示旋转轴在 $(1,1,1)$ 方向（空间对角线）。

### 🧩 公式 (2.43) 和 (2.44)

**角度**：

$$
\theta = 2\arccos(q_0) = 2\arccos(0.8) \approx 2 \times 36.87° \approx 73.74° \approx 1.287\;\text{rad}
$$

**轴**：

$$
\mathbf{n} = \frac{(q_1, q_2, q_3)^\mathrm{T}}{\sin(\theta/2)} = \frac{(0.35355, 0.35355, 0.35355)^\mathrm{T}}{\sin(36.87°)} = \frac{(0.35355, 0.35355, 0.35355)^\mathrm{T}}{0.6}
$$

$$
\approx (0.5893, 0.5893, 0.5893)^\mathrm{T}
$$

归一化后确实是 $\hat{\mathbf{n}} = \frac{1}{\sqrt{3}}(1,1,1)^\mathrm{T}$，跟我们的直觉一致。✓

**旋转向量**：

$$
\boldsymbol{\phi} = \theta\hat{\mathbf{n}} \approx 1.287 \times \frac{1}{\sqrt{3}}(1,1,1)^\mathrm{T} \approx (0.743, 0.743, 0.743)^\mathrm{T}
$$

> 🤓 旋转向量的方向就是旋转轴，长度就是旋转角度。简洁、优雅。

---

## Q6：旋转矩阵的三种等价表示

### 🔍 先感受一下这个矩阵

$$
\mathbf{R} = \begin{bmatrix}0&0&1\\-1&0&0\\0&-1&0\end{bmatrix}
$$

> 💡 每一列其实是新坐标轴在原坐标系中的方向。第一列 $(0,-1,0)^\mathrm{T}$ 说明新的 x 轴指向原来的 -y 方向。第二列 $(0,0,-1)^\mathrm{T}$ 说明新的 y 轴指向原来的 -z 方向。第三列 $(1,0,0)^\mathrm{T}$ 说明新的 z 轴指向原来的 x 方向。

验证一下 $\mathbf{R}^\mathrm{T}\mathbf{R} = \mathbf{I}$ 和 $\det(\mathbf{R}) = 1$：✓

### (a) ZYX 欧拉角 (yaw-pitch-roll)

$\mathrm{tr}(\mathbf{R}) = 0$，说明旋转角度是 $120°$——不小。

对于 ZYX 顺序 $\mathbf{R} = R_z(y)R_y(p)R_x(r)$，标准提取公式中各矩阵元素对应为：

$$
R_{20} = -\sin p,\quad R_{00} = \cos y\cos p,\quad R_{10} = \sin y\cos p
$$

$$
R_{21} = \cos p\sin r,\quad R_{22} = \cos p\cos r
$$

代入：
- $R_{20} = 0 \Rightarrow \sin p = 0 \Rightarrow p = 0°$
- $R_{00} = 0,\; R_{10} = -1 \Rightarrow \cos y = 0,\;\sin y = -1 \Rightarrow y = -90°$
- $R_{21} = -1,\; R_{22} = 0 \Rightarrow \sin r = -1 \Rightarrow r = -90°$

> 💡 这次没有 Gimbal lock（pitch ≠ ±90°），可以唯一确定三个角度。

验证：$R_z(-90°)R_y(0°)R_x(-90°) = \mathbf{R}$ ✓

$$
\text{yaw} = -90°,\quad \text{pitch} = 0°,\quad \text{roll} = -90°
$$

### (b) 旋转向量 (angle-axis)

**角度**：

$$
\theta = \arccos\frac{\mathrm{tr}(\mathbf{R})-1}{2} = \arccos\frac{-1}{2} = 120° = \frac{2\pi}{3}
$$

**轴**：解 $(\mathbf{R}-\mathbf{I})\mathbf{n} = \mathbf{0}$：

$$
\begin{bmatrix}-1&0&1\\-1&-1&0\\0&-1&-1\end{bmatrix}\mathbf{n} = \mathbf{0}
$$

> 💡 从第一行：$n_3 = n_1$。从第二行：$n_2 = -n_1$。所以 $\mathbf{n} \propto (1,-1,1)^\mathrm{T}$。

但这只给了轴的**方向**，还有正负号的问题。用 $\mathbf{R}-\mathbf{R}^\mathrm{T} = 2\sin\theta\,\mathbf{n}^\wedge$ 来确定：

$$
\mathbf{R}-\mathbf{R}^\mathrm{T} = \begin{bmatrix}0&1&1\\-1&0&1\\-1&-1&0\end{bmatrix}
$$

从反对称矩阵中提取 $\mathbf{n}$（除以 $2\sin 120° = \sqrt{3}$）：

$$
\mathbf{n} = \frac{1}{\sqrt{3}}(-1,1,-1)^\mathrm{T}
$$

> 🤓 注意：虽然 $(1,-1,1)$ 和 $(-1,1,-1)$ 都是特征值 1 的特征向量，但只有 $(-1,1,-1)/\sqrt{3}$ 才与 $\theta=120°$ 按右手定则一致。

$$
\theta = 120°,\quad \mathbf{n} = \frac{1}{\sqrt{3}}(-1,1,-1)^\mathrm{T}
$$

### (c) 四元数

从旋转向量直接转：

$$
q_0 = \cos 60° = \frac{1}{2}
$$

$$
(q_1,q_2,q_3)^\mathrm{T} = \sin 60° \cdot \mathbf{n} = \frac{\sqrt{3}}{2}\cdot\frac{1}{\sqrt{3}}(-1,1,-1)^\mathrm{T} = \frac{1}{2}(-1,1,-1)^\mathrm{T}
$$

$$
\mathbf{q} = \left[\frac{1}{2},\;-\frac{1}{2},\;\frac{1}{2},\;-\frac{1}{2}\right]^\mathrm{T}
$$

> 🤓 验证：$\|\mathbf{q}\|^2 = \frac{1}{4}\times 4 = 1$ ✓。一个漂亮的单位四元数。

---

## Q7：四元数群的单位元

### 🔍 群的四个要素

单位四元数在乘法下构成群，需要满足：封闭性、结合律、单位元、逆元。

题目问的是单位元是什么。

> 💡 单位元 $\mathbf{q}_e$ 的定义：对所有 $\mathbf{q}$，$\mathbf{q}_e\mathbf{q} = \mathbf{q}\mathbf{q}_e = \mathbf{q}$。

### 🧩 验证

$\mathbf{q}_e = [1, 0, 0, 0]^\mathrm{T} = [1, \mathbf{0}]^\mathrm{T}$

$$
\mathbf{q}_e\mathbf{q} = [1,\mathbf{0}]\cdot[s,\mathbf{v}] = [1\cdot s - \mathbf{0}\cdot\mathbf{v},\; 1\cdot\mathbf{v}+s\cdot\mathbf{0}+\mathbf{0}\times\mathbf{v}] = [s,\mathbf{v}] = \mathbf{q}
$$

同理 $\mathbf{q}\mathbf{q}_e = \mathbf{q}$。

> 🤓 几何意义：$\mathbf{q}_e$ 对应的旋转角度是 $\theta = 2\arccos(1) = 0$，即"不旋转"。这完美对应了单位元"什么都不做"的语义。

---

## Q8：KITTI 车辆的齐次变换

### 🔍 先读图

这道题需要从 KITTI 车辆的实际传感器布局推导出齐次变换矩阵。

> 💡 **建立坐标系**是第一步，也是最容易出错的一步。

**假设**（题目需要我们声明）：
- 右手坐标系：X-前方（车头方向），Y-左侧，Z-向上
- 两个坐标系的朝向一致（只有平移，没有旋转）

### 🧩 读尺寸

| 关系 | 数值 |
|------|------|
| 相机比 GPS/IMU 高 | $1.65 - 0.93 = 0.72$ m |
| 相机在 Velodyne 前方 | $0.81$ m |
| Velodyne 在 GPS/IMU 前方 | $0.30$ m |
| 相机侧向偏移 | $0.32$ m |

所以相机在 GPS/IMU 坐标系中的位置：
- X (前方)：$0.81 + 0.30 = 1.11$ m
- Y (左侧)：$0.32$ m
- Z (上方)：$0.72$ m

### $\mathbf{A}_c^g$（相机在 GPS/IMU 中的表示）

$$
\mathbf{A}_c^g = \begin{bmatrix}\mathbf{R} & \mathbf{t} \\ \mathbf{0}^\mathrm{T} & 1\end{bmatrix}
= \begin{bmatrix}1&0&0&1.11\\0&1&0&0.32\\0&0&1&0.72\\0&0&0&1\end{bmatrix}
$$

> $\mathbf{R} = \mathbf{I}$ 因为我们假设两个坐标系朝向一致。

### $\mathbf{A}_g^c$（GPS/IMU 在相机中的表示）

#### (a) 通过观察图片

从相机的角度看 GPS/IMU：在后方、右侧、下方。

$$
\mathbf{A}_g^c = \begin{bmatrix}1&0&0&-1.11\\0&1&0&-0.32\\0&0&1&-0.72\\0&0&0&1\end{bmatrix}
$$

#### (b) 通过齐次变换的逆公式

$$
\mathbf{T}^{-1} = \begin{bmatrix}\mathbf{R}^\mathrm{T} & -\mathbf{R}^\mathrm{T}\mathbf{t}\\\mathbf{0}^\mathrm{T}&1\end{bmatrix}
$$

当 $\mathbf{R} = \mathbf{I}$ 时：

$$
\mathbf{A}_g^c = \begin{bmatrix}\mathbf{I} & -\mathbf{t}\\\mathbf{0}^\mathrm{T}&1\end{bmatrix}
= \begin{bmatrix}1&0&0&-1.11\\0&1&0&-0.32\\0&0&1&-0.72\\0&0&0&1\end{bmatrix}
$$

> 🤓 两种方法的结果一致——当 $\mathbf{R}=\mathbf{I}$ 时，逆变换就是简单取反平移向量。但如果有旋转，直接取反是**不对**的，必须用 $-\mathbf{R}^\mathrm{T}\mathbf{t}$。这个区别很重要！

---

## 📝 解题方法总结

1. **先看结构，再算数字**：每道题都有内在的对称性或简化结构，找到它再动手。
2. **方向要清楚**：坐标变换中最常见的错误是搞反方向。$\mathbf{R}$ 是从哪个系到哪个系？
3. **交叉验证**：能用两种方法做的题，两种都做，互相验证。
4. **物理直觉 + 代数验证**：先用直觉猜答案的量级和方向，再用公式精确计算。
5. **注意退化情况**：Gimbal lock、$\arctan$ 象限问题等边界情况是考点。
