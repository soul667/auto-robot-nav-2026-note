# Homework #1 — Submission Version

> EE5346 Autonomous Robot Navigation, Spring 2026
> Homogeneous Transformations and Quaternions

---

## Q1. Derive and Correct Equation (1.4)

The observation equation for a 2D laser sensor models the range $r$ and bearing $\phi$ from the robot to a landmark.

**Setup.** Landmark: $\mathbf{y}_j = [y_{1,j},\, y_{2,j}]^\mathrm{T}$. Robot pose (position only in 2D): $\mathbf{x}_k = [x_{1,k},\, x_{2,k}]_k^\mathrm{T}$, with heading $\theta_k$. Observation: $\mathbf{z}_{k,j} = [r_{k,j},\, \phi_{k,j}]^\mathrm{T}$.

**Derivation.**

The range is the Euclidean distance:

$$
r_{k,j} = \sqrt{(y_{1,j} - x_{1,k})^2 + (y_{2,j} - x_{2,k})^2}
$$

The bearing is the angle from the robot's heading direction to the landmark:

$$
\phi_{k,j} = \arctan2\!\left(y_{2,j} - x_{2,k},\; y_{1,j} - x_{1,k}\right) - \theta_k
$$

**Corrected Equation (1.4):**

$$
\begin{bmatrix} r_{k,j} \\ \phi_{k,j} \end{bmatrix}
= \begin{bmatrix}
\sqrt{(y_{1,j} - x_{1,k})^2 + (y_{2,j} - x_{2,k})^2} \\
\arctan2(y_{2,j} - x_{2,k},\; y_{1,j} - x_{1,k}) - \theta_k
\end{bmatrix}
+ \mathbf{v}_{k,j}
$$

**Errors in the original Eq. (1.4):**

1. The pose vector $\mathbf{x}_k$ is defined as only $[x_1, x_2]_k^\mathrm{T}$, but a 2D robot pose should include the heading angle $\theta_k$, i.e., $\mathbf{x}_k = [x_1, x_2, \theta]_k^\mathrm{T}$.
2. The bearing angle $\phi_{k,j}$ in the original equation is the **global** angle $\arctan\!\left(\frac{y_{2,j}-x_{2,k}}{y_{1,j}-x_{1,k}}\right)$. The correct sensor observation should be **relative** to the robot heading, so we must subtract $\theta_k$.
3. Using $\arctan2$ is preferred over $\arctan$ to correctly handle all four quadrants.

---

## Q2. Quaternion Rotation Preserves Pure Quaternion

**Claim.** Given a unit quaternion $\mathbf{q} = [s, \mathbf{v}]^\mathrm{T}$ with $\|\mathbf{q}\|=1$ and a pure quaternion $\mathbf{p} = [0, \mathbf{u}]^\mathrm{T}$, the result $\mathbf{p}' = \mathbf{q}\mathbf{p}\mathbf{q}^{-1}$ is still a pure quaternion (real part = 0).

**Proof.**

Since $\mathbf{q}$ is a unit quaternion, $\mathbf{q}^{-1} = \mathbf{q}^* = [s, -\mathbf{v}]^\mathrm{T}$.

First compute $\mathbf{q}\mathbf{p}$ using the quaternion product formula (2.24):

$$
\mathbf{q}\mathbf{p} = [s, \mathbf{v}]^\mathrm{T} \cdot [0, \mathbf{u}]^\mathrm{T}
= \bigl[-\mathbf{v}^\mathrm{T}\mathbf{u},\; s\mathbf{u} + \mathbf{v}\times\mathbf{u}\bigr]^\mathrm{T}
$$

Let $\alpha = -\mathbf{v}^\mathrm{T}\mathbf{u}$ and $\boldsymbol{\beta} = s\mathbf{u} + \mathbf{v}\times\mathbf{u}$. Then $\mathbf{q}\mathbf{p} = [\alpha, \boldsymbol{\beta}]^\mathrm{T}$.

Now compute $(\mathbf{q}\mathbf{p})\mathbf{q}^{-1} = [\alpha, \boldsymbol{\beta}]^\mathrm{T} \cdot [s, -\mathbf{v}]^\mathrm{T}$:

$$
\mathbf{p}' = \bigl[\alpha s - \boldsymbol{\beta}^\mathrm{T}(-\mathbf{v}),\; \alpha(-\mathbf{v}) + s\boldsymbol{\beta} + \boldsymbol{\beta}\times(-\mathbf{v})\bigr]^\mathrm{T}
$$

The real part is:

$$
\alpha s + \boldsymbol{\beta}^\mathrm{T}\mathbf{v}
= (-\mathbf{v}^\mathrm{T}\mathbf{u})s + (s\mathbf{u} + \mathbf{v}\times\mathbf{u})^\mathrm{T}\mathbf{v}
$$

$$
= -s(\mathbf{v}^\mathrm{T}\mathbf{u}) + s(\mathbf{u}^\mathrm{T}\mathbf{v}) + (\mathbf{v}\times\mathbf{u})^\mathrm{T}\mathbf{v}
$$

Note that $\mathbf{v}^\mathrm{T}\mathbf{u} = \mathbf{u}^\mathrm{T}\mathbf{v}$, so the first two terms cancel. For the third term, $(\mathbf{v}\times\mathbf{u})$ is perpendicular to both $\mathbf{v}$ and $\mathbf{u}$, so $(\mathbf{v}\times\mathbf{u})^\mathrm{T}\mathbf{v} = 0$.

Therefore, the real part of $\mathbf{p}'$ is $0$, confirming $\mathbf{p}'$ is a pure quaternion. $\blacksquare$

---

## Q3. Rotation of Point by $\mathrm{Rot}_z(60°)$

**Given:** $\mathbf{p} = [2, 1, 0]^\mathrm{T}$ in the reference frame. The local frame is defined by $\mathbf{R} = \mathrm{Rot}_z(60°)$ with respect to the reference frame. Find $\mathbf{p}$ in the local frame.

Since the **local frame** is rotated by $\mathbf{R}$ relative to the reference frame, a point's coordinates in the local frame are:

$$
\mathbf{p}_{\text{local}} = \mathbf{R}^\mathrm{T} \mathbf{p} = \mathbf{R}^{-1} \mathbf{p}
$$

### (a) Using Rotation Matrix

$$
\mathrm{Rot}_z(60°) = \begin{bmatrix} \cos 60° & -\sin 60° & 0 \\ \sin 60° & \cos 60° & 0 \\ 0 & 0 & 1 \end{bmatrix}
= \begin{bmatrix} 1/2 & -\sqrt{3}/2 & 0 \\ \sqrt{3}/2 & 1/2 & 0 \\ 0 & 0 & 1 \end{bmatrix}
$$

$$
\mathbf{p}_{\text{local}} = \mathbf{R}^\mathrm{T}\mathbf{p}
= \begin{bmatrix} 1/2 & \sqrt{3}/2 & 0 \\ -\sqrt{3}/2 & 1/2 & 0 \\ 0 & 0 & 1 \end{bmatrix}
\begin{bmatrix} 2 \\ 1 \\ 0 \end{bmatrix}
= \begin{bmatrix} 1 + \sqrt{3}/2 \\ -\sqrt{3} + 1/2 \\ 0 \end{bmatrix}
\approx \begin{bmatrix} 1.866 \\ -1.232 \\ 0 \end{bmatrix}
$$

### (b) Using Quaternion

The quaternion for $\mathrm{Rot}_z(60°)$ is:

$$
\mathbf{q} = \left[\cos 30°,\; \sin 30° \cdot (0,0,1)\right]^\mathrm{T}
= \left[\frac{\sqrt{3}}{2},\; 0,\; 0,\; \frac{1}{2}\right]^\mathrm{T}
$$

The inverse rotation uses $\mathbf{q}^{-1} = \mathbf{q}^* = \left[\frac{\sqrt{3}}{2},\; 0,\; 0,\; -\frac{1}{2}\right]^\mathrm{T}$.

Extend $\mathbf{p}$ to a pure quaternion: $\tilde{\mathbf{p}} = [0, 2, 1, 0]^\mathrm{T}$.

Compute $\mathbf{p}_{\text{local}} = \mathbf{q}^* \tilde{\mathbf{p}} (\mathbf{q}^*)^{-1} = \mathbf{q}^* \tilde{\mathbf{p}} \mathbf{q}$.

**Step 1:** $\mathbf{q}^* \tilde{\mathbf{p}}$:

Using $[s_1, \mathbf{v}_1] \cdot [s_2, \mathbf{v}_2] = [s_1 s_2 - \mathbf{v}_1^\mathrm{T}\mathbf{v}_2,\; s_1\mathbf{v}_2 + s_2\mathbf{v}_1 + \mathbf{v}_1 \times \mathbf{v}_2]$

$\mathbf{q}^* = [\frac{\sqrt{3}}{2},\; (0,0,-\frac{1}{2})]$, $\tilde{\mathbf{p}} = [0,\; (2,1,0)]$

- Real: $\frac{\sqrt{3}}{2}\cdot 0 - (0,0,-\frac{1}{2})\cdot(2,1,0) = 0$
- Vector: $\frac{\sqrt{3}}{2}(2,1,0) + 0\cdot(0,0,-\frac{1}{2}) + (0,0,-\frac{1}{2})\times(2,1,0)$
  $= (\sqrt{3}, \frac{\sqrt{3}}{2}, 0) + (0,0,0) + \left(\frac{1}{2},\; -1,\; 0\right)$

Computing cross product $(0,0,-\frac{1}{2})\times(2,1,0) = (0\cdot 0 - (-\frac{1}{2})\cdot 1,\; (-\frac{1}{2})\cdot 2 - 0\cdot 0,\; 0\cdot 1 - 0\cdot 2) = (\frac{1}{2}, -1, 0)$

So vector $= (\sqrt{3}+\frac{1}{2},\; \frac{\sqrt{3}}{2}-1,\; 0)$

$\mathbf{q}^*\tilde{\mathbf{p}} = [0,\; (\sqrt{3}+\frac{1}{2},\; \frac{\sqrt{3}}{2}-1,\; 0)]$

**Step 2:** $(\mathbf{q}^*\tilde{\mathbf{p}})\cdot\mathbf{q}$:

$[0,\; \boldsymbol{\beta}] \cdot [\frac{\sqrt{3}}{2},\; (0,0,\frac{1}{2})]$ where $\boldsymbol{\beta} = (\sqrt{3}+\frac{1}{2},\; \frac{\sqrt{3}}{2}-1,\; 0)$

- Real: $0\cdot\frac{\sqrt{3}}{2} - \boldsymbol{\beta}\cdot(0,0,\frac{1}{2}) = 0$
- Vector: $0\cdot(0,0,\frac{1}{2}) + \frac{\sqrt{3}}{2}\boldsymbol{\beta} + \boldsymbol{\beta}\times(0,0,\frac{1}{2})$

$\boldsymbol{\beta}\times(0,0,\frac{1}{2}) = ((\frac{\sqrt{3}}{2}-1)\cdot\frac{1}{2} - 0,\; 0 - (\sqrt{3}+\frac{1}{2})\cdot\frac{1}{2},\; 0)$
$= (\frac{\sqrt{3}/2-1}{2},\; -\frac{\sqrt{3}+1/2}{2},\; 0)$
$= (\frac{\sqrt{3}-2}{4},\; \frac{-(2\sqrt{3}+1)}{4},\; 0)$

Vector $= \frac{\sqrt{3}}{2}(\sqrt{3}+\frac{1}{2},\; \frac{\sqrt{3}}{2}-1,\; 0) + (\frac{\sqrt{3}-2}{4},\; \frac{-(2\sqrt{3}+1)}{4},\; 0)$

$x: \frac{\sqrt{3}}{2}(\sqrt{3}+\frac{1}{2}) + \frac{\sqrt{3}-2}{4} = \frac{3+\frac{\sqrt{3}}{2}}{2} + \frac{\sqrt{3}-2}{4} = \frac{6+\sqrt{3}}{4} + \frac{\sqrt{3}-2}{4} = \frac{4+2\sqrt{3}}{4} = 1+\frac{\sqrt{3}}{2}$

$y: \frac{\sqrt{3}}{2}(\frac{\sqrt{3}}{2}-1) + \frac{-(2\sqrt{3}+1)}{4} = \frac{3/2 - \sqrt{3}}{2} + \frac{-(2\sqrt{3}+1)}{4} = \frac{3-2\sqrt{3}}{4} + \frac{-(2\sqrt{3}+1)}{4} = \frac{2-4\sqrt{3}}{4} = \frac{1}{2}-\sqrt{3}$

$$
\boxed{\mathbf{p}_{\text{local}} = \left[1+\frac{\sqrt{3}}{2},\; \frac{1}{2}-\sqrt{3},\; 0\right]^\mathrm{T} \approx [1.866,\; -1.232,\; 0]^\mathrm{T}}
$$

Both methods agree. ✓

---

## Q4. Quaternion to Rotation Matrix via Eq. (2.39)

**Given:** $\mathbf{q} = \left[\cos\frac{\theta}{2},\; \sin\frac{\theta}{2}(0,0,1)\right]^\mathrm{T}$

So $s = \cos\frac{\theta}{2}$, $\mathbf{v} = (0, 0, \sin\frac{\theta}{2})$.

**Formula (2.39):**

$$
\mathbf{R} = \mathbf{v}\mathbf{v}^\mathrm{T} + s^2\mathbf{I} + 2s\mathbf{v}^\wedge + (\mathbf{v}^\wedge)^2
$$

**Compute each term:**

Let $c = \cos\frac{\theta}{2}$, $s_h = \sin\frac{\theta}{2}$.

$$
\mathbf{v}\mathbf{v}^\mathrm{T} = \begin{bmatrix}0\\0\\s_h\end{bmatrix}\begin{bmatrix}0&0&s_h\end{bmatrix}
= \begin{bmatrix}0&0&0\\0&0&0\\0&0&s_h^2\end{bmatrix}
$$

$$
s^2\mathbf{I} = c^2\begin{bmatrix}1&0&0\\0&1&0\\0&0&1\end{bmatrix}
$$

$$
\mathbf{v}^\wedge = \begin{bmatrix}0&-s_h&0\\s_h&0&0\\0&0&0\end{bmatrix},\quad
2s\mathbf{v}^\wedge = 2c\begin{bmatrix}0&-s_h&0\\s_h&0&0\\0&0&0\end{bmatrix}
= \begin{bmatrix}0&-2cs_h&0\\2cs_h&0&0\\0&0&0\end{bmatrix}
$$

$$
(\mathbf{v}^\wedge)^2 = \begin{bmatrix}0&-s_h&0\\s_h&0&0\\0&0&0\end{bmatrix}^2
= \begin{bmatrix}-s_h^2&0&0\\0&-s_h^2&0\\0&0&0\end{bmatrix}
$$

**Sum:**

$$
\mathbf{R} = \begin{bmatrix}
c^2 - s_h^2 & -2cs_h & 0 \\
2cs_h & c^2 - s_h^2 & 0 \\
0 & 0 & c^2 + s_h^2
\end{bmatrix}
$$

Using double angle identities: $c^2 - s_h^2 = \cos\theta$, $2cs_h = \sin\theta$, $c^2+s_h^2 = 1$:

$$
\boxed{\mathbf{R} = \begin{bmatrix}\cos\theta & -\sin\theta & 0 \\ \sin\theta & \cos\theta & 0 \\ 0 & 0 & 1\end{bmatrix} = \mathrm{Rot}_z(\theta)}
$$

---

## Q5. Unit Quaternion to Rotation Vector

**Given:** $\mathbf{q} = [0.8,\; (0.35355, 0.35355, 0.35355)]^\mathrm{T}$

**Step 1.** Rotation angle from Eq. (2.43):

$$
\theta = 2\arccos(q_0) = 2\arccos(0.8) \approx 2 \times 0.6435 \approx 1.2870 \;\text{rad} \approx 73.74°
$$

**Step 2.** Rotation axis from Eq. (2.44):

$$
\begin{aligned}
\mathbf{n} &= \frac{[q_1, q_2, q_3]^\mathrm{T}}{\sin(\theta/2)} \\
&= \frac{(0.35355, 0.35355, 0.35355)^\mathrm{T}}{\sin(0.6435)} \\
&= \frac{(0.35355, 0.35355, 0.35355)^\mathrm{T}}{0.6} \\
&\approx (0.5893, 0.5893, 0.5893)^\mathrm{T}
\end{aligned}
$$

Normalizing: $\|\mathbf{n}\| = 0.5893\sqrt{3} \approx 1.0206$, so $\hat{\mathbf{n}} \approx \left(\frac{1}{\sqrt{3}}, \frac{1}{\sqrt{3}}, \frac{1}{\sqrt{3}}\right)^\mathrm{T}$.

**Step 3.** Rotation vector:

$$
\boxed{\boldsymbol{\phi} = \theta\,\hat{\mathbf{n}} \approx 1.287 \times \left(\frac{1}{\sqrt{3}}, \frac{1}{\sqrt{3}}, \frac{1}{\sqrt{3}}\right)^\mathrm{T} \approx (0.7432, 0.7432, 0.7432)^\mathrm{T}}
$$

---

## Q6. Rotation Matrix to Euler Angles, Angle-Axis, Quaternion

**Given:**

$$
\mathbf{R} = \begin{bmatrix}0&0&1\\-1&0&0\\0&-1&0\end{bmatrix}
$$

### (a) Roll-Pitch-Yaw Euler Angles (ZYX convention)

For ZYX Euler angles, $\mathbf{R} = \mathrm{Rot}_z(\text{yaw})\,\mathrm{Rot}_y(\text{pitch})\,\mathrm{Rot}_x(\text{roll})$.

Standard ZYX extraction formulas (reading from the matrix entries):

$$
R = \begin{bmatrix}c_y c_p & c_y s_p s_r - s_y c_r & c_y s_p c_r + s_y s_r \\ s_y c_p & s_y s_p s_r + c_y c_r & s_y s_p c_r - c_y s_r \\ -s_p & c_p s_r & c_p c_r\end{bmatrix}
$$

From $R_{20} = -\sin p = 0$: $p = 0°$.

From $R_{00} = \cos y \cos p = 0$ and $R_{10} = \sin y \cos p = -1$: since $\cos p = 1$, we get $\sin y = -1$, so $y = -90°$.

From $R_{21} = \cos p \sin r = -1$ and $R_{22} = \cos p \cos r = 0$: $\sin r = -1$, so $r = -90°$.

**Verification:** $\mathrm{Rot}_z(-90°)\,\mathrm{Rot}_y(0°)\,\mathrm{Rot}_x(-90°)$:

$$
\begin{bmatrix}0&1&0\\-1&0&0\\0&0&1\end{bmatrix}\begin{bmatrix}1&0&0\\0&0&1\\0&-1&0\end{bmatrix}
= \begin{bmatrix}0&0&1\\-1&0&0\\0&-1&0\end{bmatrix} = \mathbf{R} \;\checkmark
$$

$$
\boxed{\text{yaw}=-90°,\quad \text{pitch}=0°,\quad \text{roll}=-90°}
$$

### (b) Rotation Vector (Angle-Axis)

**Angle** via Eq. (2.17):

$$
\theta = \arccos\!\left(\frac{\mathrm{tr}(\mathbf{R})-1}{2}\right) = \arccos\!\left(\frac{0-1}{2}\right) = \arccos(-0.5) = 120°  = \frac{2\pi}{3}
$$

**Axis** via $\mathbf{R}\mathbf{n} = \mathbf{n}$ and sign from $\mathbf{R}-\mathbf{R}^\mathrm{T} = 2\sin\theta\,\mathbf{n}^\wedge$:

First, from the null space of $(\mathbf{R}-\mathbf{I})$:

$$
\begin{bmatrix}-1&0&1\\-1&-1&0\\0&-1&-1\end{bmatrix}\mathbf{n}=\mathbf{0}
\implies \mathbf{n} \propto (1, -1, 1)^\mathrm{T}
$$

To determine the correct sign, use $\mathbf{R}-\mathbf{R}^\mathrm{T} = 2\sin\theta\,\mathbf{n}^\wedge$:

$$
\mathbf{R}-\mathbf{R}^\mathrm{T} = \begin{bmatrix}0&1&1\\-1&0&1\\-1&-1&0\end{bmatrix}
$$

Extracting $\mathbf{n}$ from the skew-symmetric matrix ($n_1 = [\mathbf{n}^\wedge]_{32}$, etc.), divided by $2\sin 120° = \sqrt{3}$:

$$
\mathbf{n} = \frac{1}{\sqrt{3}}(-1, 1, -1)^\mathrm{T}
$$

$$
\boxed{\theta = 120° = \frac{2\pi}{3}, \quad \mathbf{n} = \frac{1}{\sqrt{3}}(-1,1,-1)^\mathrm{T}}
$$

### (c) Quaternion

From Eq. (2.44) reversed:

$$
q_0 = \cos\frac{\theta}{2} = \cos 60° = \frac{1}{2}
$$

$$
(q_1, q_2, q_3)^\mathrm{T} = \sin\frac{\theta}{2}\,\mathbf{n} = \frac{\sqrt{3}}{2}\cdot\frac{1}{\sqrt{3}}(-1,1,-1)^\mathrm{T} = \frac{1}{2}(-1,1,-1)^\mathrm{T}
$$

$$
\boxed{\mathbf{q} = \left[\frac{1}{2},\; -\frac{1}{2},\; \frac{1}{2},\; -\frac{1}{2}\right]^\mathrm{T}}
$$

---

## Q7. Identity of the Unit Quaternion Group

**Claim.** The identity quaternion is $\mathbf{q}_e = [1, 0, 0, 0]^\mathrm{T}$.

**Justification.** For any unit quaternion $\mathbf{q} = [s, \mathbf{v}]^\mathrm{T}$:

$$
\mathbf{q}_e \mathbf{q} = [1, \mathbf{0}]^\mathrm{T} \cdot [s, \mathbf{v}]^\mathrm{T}
= [1\cdot s - \mathbf{0}^\mathrm{T}\mathbf{v},\; 1\cdot\mathbf{v} + s\cdot\mathbf{0} + \mathbf{0}\times\mathbf{v}]^\mathrm{T}
= [s, \mathbf{v}]^\mathrm{T} = \mathbf{q}
$$

Similarly $\mathbf{q}\mathbf{q}_e = \mathbf{q}$. Therefore $\mathbf{q}_e = [1,0,0,0]^\mathrm{T}$ is the identity.

Geometrically, this corresponds to a rotation of angle $\theta = 2\arccos(1) = 0$, i.e., no rotation at all. $\blacksquare$

---

## Q8. Homogeneous Transformation (KITTI Vehicle)

**Setup & Assumptions:**
- We use a right-handed coordinate system with **X-forward, Y-left, Z-up**.
- GPS/IMU frame $\{g\}$: origin at GPS/IMU location.
- Camera frame $\{c\}$: origin at camera location.
- The cameras are located: $0.81\,\text{m}$ forward, $0.32\,\text{m}$ lateral (left), and $0.72\,\text{m}$ above the GPS/IMU (height: $1.65 - 0.93 = 0.72\,\text{m}$).

**No rotation** between the two frames is assumed (both frames aligned with vehicle axes).

### $\mathbf{A}_c^g$ (Camera frame w.r.t. GPS/IMU frame)

The translation from GPS/IMU to camera in the GPS/IMU frame is:

$$
\mathbf{t}_c^g = \begin{bmatrix}0.81+0.30\\0.32\\0.72\end{bmatrix} = \begin{bmatrix}1.11\\0.32\\0.72\end{bmatrix}
$$

(The camera is $0.81\,\text{m}$ in front of Velodyne, and Velodyne is $0.30\,\text{m}$ in front of GPS/IMU, so camera is $1.11\,\text{m}$ forward.)

$$
\mathbf{A}_c^g = \begin{bmatrix}\mathbf{I}_{3\times3} & \mathbf{t}_c^g \\ \mathbf{0}^\mathrm{T} & 1\end{bmatrix}
= \begin{bmatrix}1&0&0&1.11\\0&1&0&0.32\\0&0&1&0.72\\0&0&0&1\end{bmatrix}
$$

### $\mathbf{A}_g^c$ — (a) By Inspection

From the camera's perspective, the GPS/IMU is: $1.11\,\text{m}$ behind (−X), $0.32\,\text{m}$ to the right (−Y), and $0.72\,\text{m}$ below (−Z):

$$
\mathbf{A}_g^c = \begin{bmatrix}1&0&0&-1.11\\0&1&0&-0.32\\0&0&1&-0.72\\0&0&0&1\end{bmatrix}
$$

### $\mathbf{A}_g^c$ — (b) By Closed-Form Inverse

Using Eq. (2.14): $\mathbf{T}^{-1} = \begin{bmatrix}\mathbf{R}^\mathrm{T} & -\mathbf{R}^\mathrm{T}\mathbf{t}\\\mathbf{0}^\mathrm{T}&1\end{bmatrix}$

Since $\mathbf{R}=\mathbf{I}$:

$$
\mathbf{A}_g^c = \begin{bmatrix}\mathbf{I} & -\mathbf{t}_c^g \\ \mathbf{0}^\mathrm{T} & 1\end{bmatrix}
= \begin{bmatrix}1&0&0&-1.11\\0&1&0&-0.32\\0&0&1&-0.72\\0&0&0&1\end{bmatrix}
$$

Both methods yield the same result. ✓
