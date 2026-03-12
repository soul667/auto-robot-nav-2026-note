# 误差状态与扰动模型

为了在流形上进行优化或滤波，需要使用与群运算一致的扰动模型。以下符号与 slambook 中的记号保持一致。

## 左乘与右乘误差

给定真值位姿 $\mathbf{T}$ 与估计 $\hat{\mathbf{T}}$，左乘误差写作

$$
\mathbf{T} = \exp(\boldsymbol{\xi})\,\hat{\mathbf{T}}, \qquad
\boldsymbol{\xi}\in\mathbb{R}^6.
$$

若选择右乘误差，则为 $\mathbf{T} = \hat{\mathbf{T}}\,\exp(\boldsymbol{\xi})$。两者的主要区别在于协方差传播时使用的伴随矩阵：

$$
\operatorname{Ad}_{\hat{\mathbf{T}}} =
\begin{bmatrix}
\hat{\mathbf{R}} & \widehat{\hat{\mathbf{t}}}\,\hat{\mathbf{R}} \\
\mathbf{0} & \hat{\mathbf{R}}
\end{bmatrix},
\qquad
\boldsymbol{\xi}_\text{right} \approx \operatorname{Ad}_{\hat{\mathbf{T}}}^{-1}\boldsymbol{\xi}_\text{left}.
$$

## 线性化残差

观测模型 $\mathbf{z} = h(\mathbf{T}) + \mathbf{n}$ 的一阶展开可写为

$$
\mathbf{r}(\boldsymbol{\xi}) \approx
h(\hat{\mathbf{T}}) + \mathbf{J}\,\boldsymbol{\xi} - \mathbf{z},
\qquad
\mathbf{J} = \left.\frac{\partial h(\exp(\boldsymbol{\xi})\hat{\mathbf{T}})}{\partial \boldsymbol{\xi}}\right|_{\boldsymbol{\xi}=\mathbf{0}}.
$$

使用左乘扰动，雅可比 $\mathbf{J}$ 的前三列对应旋转扰动对残差的影响，后三列对应平移扰动。保持这一排列有助于与 slambook 的推导保持一致。

## 协方差传播

对于离散运动方程 $\mathbf{T}_{k+1} = \mathbf{F}(\mathbf{T}_k,\mathbf{u}_k) \oplus \mathbf{w}_k$，误差状态的传播形式为

$$
\boldsymbol{\xi}_{k+1} \approx \mathbf{F}_k \boldsymbol{\xi}_k + \mathbf{G}_k \mathbf{w}_k,\qquad
\mathbf{P}_{k+1} = \mathbf{F}_k \mathbf{P}_k \mathbf{F}_k^\top + \mathbf{G}_k \mathbf{Q}_k \mathbf{G}_k^\top.
$$

当状态位于李群上时，$\mathbf{F}_k$ 与 $\mathbf{G}_k$ 需要通过对伴随矩阵的一阶近似获得。例如，对左乘误差有

$$
\mathbf{F}_k = \mathbf{I} + \operatorname{ad}_{\bar{\boldsymbol{\xi}}_k},
\qquad
\operatorname{ad}_{\bar{\boldsymbol{\xi}}} =
\begin{bmatrix}
\widehat{\boldsymbol{\phi}} & \widehat{\mathbf{t}} \\
\mathbf{0} & \widehat{\boldsymbol{\phi}}
\end{bmatrix}.
$$

这里 $\operatorname{ad}$ 表示李代数的“ad”算子，其形式与 slambook 第 9 讲的推导完全一致。
