---
layout: home

hero:
  name: Robotics Notebook
  text: "一套 LaTeX 质感的 SLAM / 自动驾驶课堂笔记"
  tagline: "紧贴 slambook 的推导与符号，注重公式的可读性与严谨度。"
  image:
    src: /preview.png
    alt: "站点预览截图"
  actions:
    - theme: brand
      text: 李群与扰动模型
      link: /articles/lie-group-primer
    - theme: alt
      text: 最小二乘与 BA
      link: /articles/least-squares-ba
    - theme: alt
      text: EKF-SLAM
      link: /articles/ekf-slam

features:
  - title: 严谨的公式排版
    details: 启用 KaTeX 与 LaTeX 风格字体，确保推导、证明和矩阵表达保持课堂级清晰度。
  - title: 学术化的版式
    details: 纸张质感的背景、柔和的色彩和高可读性的排版，适合长时间阅读与批注。
  - title: 可复用的结构
    details: 导航、侧边栏和章节组织与 slambook 相呼应，便于扩展更多几何与滤波内容。
  - title: 直接可部署
    details: 随附 GitHub Pages 工作流，提交后自动构建并发布。
---

## 快速导览

- 若想理解李群、指数映射与扰动模型，从 [李群与李代数](/articles/lie-group-primer) 开始。
- 需要在视觉 SLAM 中求解位姿与路标，请查看 [最小二乘与 BA](/articles/least-squares-ba)。
- 对滤波式 SLAM 感兴趣，可阅读 [EKF-SLAM](/articles/ekf-slam)。
- 原版教材可在 [slambook PDF](/textbook/slambook-en.pdf) 中查阅，本站排版与符号遵循其约定。

> 这些示例章节聚焦推导思路与符号一致性，便于你直接扩展课程讲义、作业和实验记录。
