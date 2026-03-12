import DefaultTheme from 'vitepress/theme'
import type { Theme } from 'vitepress'

import './style.css'
import 'katex/dist/katex.min.css'

export default {
  extends: DefaultTheme
} satisfies Theme
