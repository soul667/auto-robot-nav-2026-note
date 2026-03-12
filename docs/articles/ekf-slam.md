# EKF-SLAM

滤波式 SLAM 的关键在于正确建模误差状态并保持协方差的一致性。本节使用左乘误差与 slambook 的符号，推导离散 EKF 的两大步骤。

## 状态与噪声

状态包含机器人位姿 $\mathbf{T}\in\mathrm{SE}(3)$ 和若干路标 $\mathbf{p}_j$：

$$
\mathbf{x} = \left[\mathbf{T}, \mathbf{p}_1^\top,\dots,\mathbf{p}_n^\top\right]^\top,\qquad
\delta\mathbf{x} = [\delta\boldsymbol{\xi}^\top,\delta\mathbf{p}_1^\top,\dots]^\top.
\tag{1}
$$

控制输入为里程计或 IMU 积分得到的位移 $\mathbf{u}_k$，其噪声协方差为 $\mathbf{Q}_k$。

## 预测步骤

利用运动模型 $\mathbf{T}_{k+1} = \exp(\boldsymbol{\omega}_k,\mathbf{v}_k)\,\mathbf{T}_k$，

$$
\hat{\mathbf{x}}_{k+1|k} = f(\hat{\mathbf{x}}_{k|k}, \mathbf{u}_k), \qquad
\mathbf{P}_{k+1|k} = \mathbf{F}_k \mathbf{P}_{k|k} \mathbf{F}_k^\top + \mathbf{G}_k \mathbf{Q}_k \mathbf{G}_k^\top.
\tag{2}
$$

雅可比 $\mathbf{F}_k$ 由伴随矩阵决定。例如位姿部分

$$
\mathbf{F}_k^{TT} = \operatorname{Ad}_{\exp(\hat{\boldsymbol{\xi}}_u)}\,,
\tag{3}
$$

体现了群结构对误差传播的影响。

## 更新步骤

假设观测模型为相机重投影，残差定义为

$$
\mathbf{r}_k = \mathbf{z}_k - h(\hat{\mathbf{x}}_{k|k-1}),
\tag{4}
$$

线性化得到 $\mathbf{r}_k \approx \mathbf{H}_k \delta\mathbf{x} + \mathbf{n}_k$，其中 $\mathbf{H}_k$ 按照“姿态在前、路标在后”的顺序拼接。增益与更新公式为

$$
\mathbf{K}_k = \mathbf{P}_{k|k-1}\mathbf{H}_k^\top
\left(\mathbf{H}_k\mathbf{P}_{k|k-1}\mathbf{H}_k^\top + \mathbf{R}_k\right)^{-1},
\tag{5}
$$

$$
\delta\mathbf{x}_k = \mathbf{K}_k \mathbf{r}_k,\qquad
\mathbf{P}_{k|k} = (\mathbf{I} - \mathbf{K}_k \mathbf{H}_k)\mathbf{P}_{k|k-1}.
\tag{6}
$$

最后通过左乘扰动将位姿回写到群上：

$$
\hat{\mathbf{T}}_{k|k} = \exp(\delta\boldsymbol{\xi}_k)\,\hat{\mathbf{T}}_{k|k-1},\qquad
\hat{\mathbf{p}}_{j,k|k} = \hat{\mathbf{p}}_{j,k|k-1} + \delta\mathbf{p}_{j,k}.
\tag{7}
$$

## 稳定性提示

1. **观测选择**：保持路标的视差与基线，避免近远景混杂导致的数值病态。
2. **零空间处理**：首次观测新路标时，使用逆深度或锚点姿态初始化，可降低状态维度间的强耦合。
3. **协方差对称化**：数值误差会破坏协方差的对称性，必要时令 $\mathbf{P}\leftarrow \tfrac{1}{2}(\mathbf{P}+\mathbf{P}^\top)$ 保持正定。
