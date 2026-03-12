# 最小二乘与 BA

本节参考 slambook 的符号，对 bundle adjustment (BA) 的二次型近似与舒尔补求解过程进行梳理。

## 代价函数

设观测为像素坐标 $\mathbf{z}_{ij}$，相机姿态为 $\mathbf{T}_i \in \mathrm{SE}(3)$，路标为 $\mathbf{p}_j\in\mathbb{R}^3$。重投影误差

$$
\mathbf{r}_{ij} = \pi\!\left(\mathbf{T}_i\,\mathbf{p}_j\right) - \mathbf{z}_{ij},
\label{eq:reproj}
$$

其中 $\pi(\cdot)$ 为针孔相机投影。总的最小二乘问题为

$$
\min_{\{\mathbf{T}_i,\mathbf{p}_j\}}
\sum_{(i,j)\in\mathcal{O}} \left\|\mathbf{r}_{ij}\right\|_{\Sigma_{ij}}^2,
\label{eq:ls}
$$

$\Sigma_{ij}$ 为测量协方差。

## 一阶线性化

对姿态和路标在当前估计处进行一阶展开：

$$
\mathbf{r}_{ij}(\delta\boldsymbol{\xi}_i,\delta\mathbf{p}_j)
\approx \mathbf{r}_{ij}^0 + \mathbf{J}_{ij}^{T}\delta\boldsymbol{\xi}_i + \mathbf{J}_{ij}^{P}\delta\mathbf{p}_j,
\label{eq:linearization}
$$

其中 $\delta\boldsymbol{\xi}_i$ 为位姿扰动（按李代数顺序旋转在前，平移在后）。将所有残差堆叠，可写成标准二次型

$$
\tfrac{1}{2}\delta\mathbf{x}^\top \mathbf{H}\,\delta\mathbf{x} - \mathbf{b}^\top\delta\mathbf{x},
\label{eq:quadratic}
$$

其中 Hessian 的块结构为

$$
\mathbf{H}=
\begin{bmatrix}
\mathbf{H}_{TT} & \mathbf{H}_{TP} \\
\mathbf{H}_{PT} & \mathbf{H}_{PP}
\end{bmatrix},\qquad
\mathbf{b} = \begin{bmatrix}\mathbf{b}_T \\ \mathbf{b}_P\end{bmatrix}.
\label{eq:hessian}
$$

## 舒尔补

消元路标后得到只含位姿的简化系统：

$$
\left(\mathbf{H}_{TT} - \mathbf{H}_{TP}\mathbf{H}_{PP}^{-1}\mathbf{H}_{PT}\right)\delta\mathbf{x}_T
=
\mathbf{b}_T - \mathbf{H}_{TP}\mathbf{H}_{PP}^{-1}\mathbf{b}_P.
\label{eq:schur}
$$

计算量集中在分块求逆上。利用稀疏性可按观测逐项累加，而不必显式构造大矩阵。求得位姿更新后，再利用回代

$$
\delta\mathbf{p}_j = \mathbf{H}_{PP}^{-1}\left(\mathbf{b}_P - \mathbf{H}_{PT}\delta\mathbf{x}_T\right)
\label{eq:backsub}
$$

即可获得路标增量。

## 阻尼与信赖域

为提升收敛性，可采用 LM 或 Dogleg 策略。在 Hessian 对角线添加阻尼项

$$
\mathbf{H}_{\lambda} = \mathbf{H} + \lambda\,\operatorname{diag}(\mathbf{H})
\label{eq:damping}
$$

能够抑制迭代中出现的奇异方向，同时保持与 Gauss–Newton 一致的近似。当 $\rho$ 大于阈值时减小 $\lambda$，否则加大阻尼并重新线性化，这是与 slambook 第 6 讲保持一致的经验做法。
