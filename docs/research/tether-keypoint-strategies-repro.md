# Tether：两种关键点对应策略（GeoAware-SC / MASt3R）与最快复现

> 论文：**Tether: Autonomous Functional Play with Correspondence-Driven Trajectory Warping**  
> 代码：<https://github.com/tether-research/tether>  
> 本文目标：单独拆解论文中“找关键点对应”的两种策略，并给出代码级最快复现路径。

---

## 1. 先说结论：Tether 里两种“找关键点”策略如何分工

在 Tether 代码里（`run_correspondence.py`），两种策略是互补关系，不是二选一：

1. **GeoAware-SC（同视角、跨时刻）**  
   用于把 demo 图像里的锚点，找到 scene 图像中同一相机视角下的语义对应位置。
2. **MASt3R（跨视角、同时刻）**  
   用于 camera1↔camera2 的跨视角对应一致性检查（demo 和 scene 都会做一遍）。

Tether 最终并不是直接拿单个 2D 匹配点做扭曲，而是：

- 先用双目三角化得到 3D 点；
- 再用 correspondence 分数 + 三角化误差联合打分；
- 同时用 MASt3R 的跨视角误差做过滤；
- 最后选最佳候选偏移，生成 `position_delta`。

---

## 2. 代码级拆解：GeoAware-SC 在 Tether 里怎么用

对应文件：`serve_geo_aware.py`、`run_correspondence.py`

### 2.1 特征构建

`serve_geo_aware.py` 里，GeoAware 的特征不是单一 backbone，而是融合了：

- Stable Diffusion 中间层特征（`s3/s4/s5`）；
- DINOv2 token 描述子；
- 然后经 `AggregationNetwork` 聚合并做 L2 归一化。

这一步让特征既有语义信息又有局部几何辨识力。

### 2.2 匹配方式

在 `GeoAware.compute_correspondence(x, y)` 中，流程是：

1. 取 source 点 `(x, y)` 在 source feature map 上的描述子；
2. 与 target feature map 做余弦相似度图；
3. 取相似度最大位置作为对应点；
4. 将 resize 坐标映射回原图坐标，返回 `(xy, score)`。

### 2.3 在 Tether pipeline 的角色

`run_correspondence.py` 中：

- 每个 camera 都会调用 `geo_aware.load_images(source=demo_frame, target=scene_frame)`；
- 对每个候选锚点调用 `geo_aware.compute_correspondence(...)`；
- 产出 `anchor_correspondence_candidates` 与 `anchor_correspondence_scores`。

这一步提供了“**同视角语义锚点迁移**”。

---

## 3. 代码级拆解：MASt3R 在 Tether 里怎么用

对应文件：`serve_mast3r.py`、`run_correspondence.py`

### 3.1 匹配生成

`serve_mast3r.py` 的核心是：

1. `AsymmetricMASt3R.from_pretrained(...)` 加载模型；
2. 对图像对做 `inference`，得到两侧描述子；
3. 用 `fast_reciprocal_NNs(...)` 求互近邻匹配；
4. 过滤掉边界附近不稳定点；
5. 缓存匹配结果（`npz`）。

### 3.2 查询方式

`Mast3r.compute_correspondence(x, y, max_error)` 并不重新推理，而是：

- 在已有 match 集合里找离 `(x, y)` 最近的 matched 点；
- 若最近距离大于 `max_error`（配置里 `mast3r_error_thres`），返回 `None`；
- 否则返回目标视角坐标和误差。

### 3.3 在 Tether pipeline 的角色

`run_correspondence.py` 里 MASt3R 会做两轮：

1. demo 内 camera1→camera2、camera2→camera1；
2. scene 内 camera1→camera2、camera2→camera1。

之后把三角化得到的 3D 点反投影，与 MASt3R 跨视角对应做 pixel-ray distance 比较，构建：

- `crossview_corres_dist_err1`
- `crossview_corres_dist_err2`

若误差大于阈值（代码中常见阈值 0.1），候选会被剔除。  
这一步提供了“**跨视角几何一致性约束**”。

---

## 4. 二者如何融合成最终 warp

`run_correspondence.py` 的关键逻辑可以概括为：

1. 构造多个锚点偏移候选（`anchor_offsets`）；
2. GeoAware 给每个候选做 demo→scene 同视角匹配；
3. MASt3R 给候选做 cross-view 一致性校验（demo/scene 各一遍）；
4. 双目三角化得到 anchor/corres 3D 点；
5. 计算打分：
   - `correspondence_score = score_cam1 + score_cam2`
   - `distance_score = -corres_dist_err`
   - `score = 1.0 * correspondence_score + 10.0 * distance_score`
6. 过滤：
   - 三角化误差超阈值 -> reject
   - cross-view 误差超阈值 -> reject
   - OOB -> reject
7. 选 best candidate，写入 `warp_response.json`（`position_delta`）。

所以这套系统不是“只拼语义相似度”，而是语义+几何双重筛选。

---

## 5. 最快复现（按“最快拿到可运行结果”组织）

下面分成三个层级，从快到慢：

## 5.1 Level-0：最快确认代码链路（不跑真实机器人）

目标：先让代码结构跑通到“可读、可改”的程度。

1. 克隆仓库并建环境：

```bash
git clone https://github.com/tether-research/tether.git
cd tether
conda create -n tether python=3.10 -y
conda activate tether
pip install -r requirements.txt
```

2. 按官方文档分别准备 GeoAware-SC 与 MASt3R 环境；
3. 启动服务端脚本：
   - `python serve_geo_aware.py`
   - `python serve_mast3r.py`

这一步的意义是先确保 “对应服务可启动 + BaseManager 可连通”。

## 5.2 Level-1：最快看到 correspondence 输出（推荐）

目标：在不完整闭环执行前，先拿到 `warp_response.json` 和可视化中间产物。

1. 准备最小 demo/scene 数据（至少两相机图像 + 轨迹 + 标定）；
2. 配置 `conf/config.yaml`（API key 可先留空，只跑 correspondence 时不必依赖完整 VLM 路径）；
3. 配置 `conf/setting/real.yaml`：
   - 两个 camera id；
   - `image_crop`；
   - `oob_bounds`；
   - `mast3r_error_thres`。
4. 执行单次路径（推荐从 `mode=single` 入手）：

```bash
python runner.py mode=single action="<你在 real.yaml 中配置的一个动作文本>"
```

该流程会经过 `extract_keypoint_trajectory -> run_correspondence -> warp_trajectory`，  
只要你把机器人发送阶段替换成 mock，依然能验证关键点对应与扭曲逻辑。

## 5.3 Level-2：完整论文式自动 play 复现

目标：跑 `mode=cycle`，得到多轮自主交互数据增长。

1. 需要真实机器人接口（默认 `utils/robot_utils.py` 使用 zerorpc + rsync 到远端 Eva 机）；
2. 配置 Gemini key（`conf/config.yaml` 的 `api_key_smart/fast`）；
3. 准备初始 demonstrations 到 `data_real/demos/...`；
4. 跑循环：

```bash
python runner.py mode=cycle
```

若硬件链路没接通，最快做法是先改 `utils/robot_utils.py`：

- `collect_scene_image()` 改为本地读取静态 scene；
- `send_trajectory()` 改为保存轨迹并返回伪 rollout 路径；

这样可以先把算法/数据流验证完，再接真实机器人。

---

## 6. 我建议的“最快成功”复现顺序

1. **先通服务**：`serve_geo_aware.py`、`serve_mast3r.py`；
2. **先通 correspondence**：确保 `warp_response.json` 产出；
3. **再通 single**：一次动作全链路；
4. **最后再跑 cycle**：长时间自治 play。

这能最大化定位效率：每层失败都能快速缩小问题范围。

---

## 7. 关于“帮你 fork 仓库”

我在这个受限环境里不能直接替你在 GitHub 账户下执行 fork 动作（平台权限限制）。  
你可以手动 10 秒完成：

1. 打开：<https://github.com/tether-research/tether>
2. 右上角点击 **Fork**
3. 选择你的账号创建 fork

然后把你的 fork 地址发我，我可以继续按你的 fork 结构给出定制化复现脚本与目录规划。

