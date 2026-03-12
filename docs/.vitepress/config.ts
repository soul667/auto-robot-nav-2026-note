import { defineConfig } from 'vitepress'
import footnote from 'markdown-it-footnote'

export default defineConfig({
  lang: 'zh-CN',
  title: 'Robotics Notebook',
  description: 'SLAM 与自主导航的讲义式笔记',
  base: '/auto-robot-nav-2026-note/',
  lastUpdated: true,
  cleanUrls: true,
  appearance: true,
  head: [
    ['meta', { name: 'theme-color', content: '#1f2937' }],
    ['link', { rel: 'icon', href: '/favicon.svg' }]
  ],
  markdown: {
    math: {
      type: 'mathjax',
      options: {
        tex: {
          tags: 'all',
          tagSide: 'right',
          tagIndent: '0.8em'
        }
      }
    },
    config: (md) => {
      md.use(footnote)
    }
  },
  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      {
        text: '基础与代数',
        items: [
          { text: '李群与李代数', link: '/articles/lie-group-primer' },
          { text: '误差状态与扰动模型', link: '/articles/perturbation-model' }
        ]
      },
      {
        text: '估计与优化',
        items: [
          { text: '最小二乘与BA', link: '/articles/least-squares-ba' },
          { text: 'EKF-SLAM', link: '/articles/ekf-slam' }
        ]
      },
      {
        text: '参考资料',
        items: [
          { text: '教材 PDF（slambook）', link: '/textbook/slambook-en.pdf' },
          { text: 'Markdown 语法示例', link: '/markdown-examples' },
          { text: 'API 示例', link: '/api-examples' }
        ]
      }
    ],
    sidebar: {
      '/articles/': [
        {
          text: '基础与代数',
          items: [
            { text: '李群与李代数', link: '/articles/lie-group-primer' },
            { text: '误差状态与扰动模型', link: '/articles/perturbation-model' }
          ]
        },
        {
          text: '估计与优化',
          items: [
            { text: '最小二乘与 BA', link: '/articles/least-squares-ba' },
            { text: 'EKF-SLAM', link: '/articles/ekf-slam' }
          ]
        }
      ],
      '/': [
        {
          text: '入门',
          items: [
            { text: '首页', link: '/' },
            { text: 'Markdown 示例', link: '/markdown-examples' },
            { text: 'API 示例', link: '/api-examples' }
          ]
        }
      ]
    },
    socialLinks: [
      { icon: 'github', link: 'https://github.com/soul667/auto-robot-nav-2026-note' }
    ],
    footer: {
      message: '基于 VitePress 打造的学术型笔记，与 LaTeX 视觉保持一致性。',
      copyright: 'CC BY-SA 4.0'
    },
    outline: 'deep'
  }
})
