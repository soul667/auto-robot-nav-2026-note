# 李群与李代数

本节对齐 slambook 的符号系统，重点呈现 $\mathrm{SO}(3)$、$\mathrm{SE}(3)$ 与指数映射的严谨推导。

## 基本符号

- 旋转矩阵 $\mathbf{R}\in \mathrm{SO}(3)$ 满足 $\mathbf{R}^\top \mathbf{R} = \mathbf{I}$ 且 $\det(\mathbf{R}) = 1$。
- 反对称矩阵使用“帽”算子表示：对角速度向量 $\boldsymbol{\omega}=[\omega_x,\omega_y,\omega_z]^\top$，

  $$
  \widehat{\boldsymbol{\omega}} =
  \begin{bmatrix}
  0 & -\omega_z & \omega_y \\
  \omega_z & 0 & -\omega_x \\
  -\omega_y & \omega_x & 0
  \end{bmatrix},\qquad
  \boldsymbol{\omega} = \operatorname{vee}(\widehat{\boldsymbol{\omega}}).
  \tag{1}
  $$

- $\boldsymbol{\xi} = (\boldsymbol{\phi},\mathbf{t}) \in \mathbb{R}^6$ 表示 $\mathrm{se}(3)$ 元素，其中 $\boldsymbol{\phi}$ 为旋转扰动，$\mathbf{t}$ 为平移扰动。

## 指数映射

轴角 $\boldsymbol{\phi}$ 的范数 $\theta=\lVert \boldsymbol{\phi}\rVert$ 对应的指数映射为

$$
\exp(\widehat{\boldsymbol{\phi}})=
\mathbf{I}+\frac{\sin\theta}{\theta}\widehat{\boldsymbol{\phi}}
+\frac{1-\cos\theta}{\theta^2}\widehat{\boldsymbol{\phi}}^2.
\tag{2}
$$

当 $\theta\rightarrow 0$，利用泰勒展开可得到近似 $\exp(\widehat{\boldsymbol{\phi}})\approx \mathbf{I}+\widehat{\boldsymbol{\phi}}$，这在求解小扰动的雅可比时尤为常用。

## 对数映射

若已知旋转矩阵 $\mathbf{R}$，其对数映射为

$$
\operatorname{Log}(\mathbf{R})=
\frac{\theta}{2\sin\theta}(\mathbf{R}-\mathbf{R}^\top),
\qquad \theta = \arccos\frac{\operatorname{tr}(\mathbf{R})-1}{2}.
\tag{3}
$$

该形式保证 $\operatorname{Log}(\mathbf{R})$ 落在 $\mathrm{so}(3)$，并与上式的指数映射互为逆变换。

## $\mathrm{SE}(3)$ 的左乘扰动

在优化与滤波中，位姿的误差通常放置在左侧：

$$
\mathbf{T} \oplus \delta\boldsymbol{\xi}
= \exp\!\left(
\begin{bmatrix}
\widehat{\delta\boldsymbol{\phi}} & \delta\mathbf{t} \\
\mathbf{0}^\top & 0
\end{bmatrix}
\right)\mathbf{T}.
\tag{4}
$$

其中 $\mathbf{T}\in \mathrm{SE}(3)$，$\delta\boldsymbol{\xi}$ 表示小扰动。左乘扰动与李代数的指数映射组合，保持了群结构的封闭性和一阶线性化的正确性[^book]。

## BCH 展开要点

对于两个小扰动 $\boldsymbol{a},\boldsymbol{b}\in\mathrm{se}(3)$，

$$
\log(\exp(\boldsymbol{a})\exp(\boldsymbol{b}))
=\boldsymbol{a}+\boldsymbol{b}+\tfrac{1}{2}[\boldsymbol{a},\boldsymbol{b}]
+ \mathcal{O}(\lVert\boldsymbol{a}\rVert\lVert\boldsymbol{b}\rVert).
\tag{5}
$$

其中李括号 $[\boldsymbol{a},\boldsymbol{b}]$ 体现了非交换性。忽略高阶项可以获得一阶组合扰动，这在推导迭代更新或先验传播时会频繁出现。

[^book]: 高翔，《视觉 SLAM 十四讲：从理论到实践》，电子工业出版社，2021。为了方便查阅，教材 PDF 已附在站点的 `textbook/` 目录。
