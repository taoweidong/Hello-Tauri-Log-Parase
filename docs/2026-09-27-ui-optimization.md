# 前端界面优化方案 — 现代 / 流畅 / SVG 化

> 日期：2026-09-27
> 范围：UI 层（组件 + 样式），不改业务逻辑与数据流
> 技术约束：Vue 3 + Naive UI + Tailwind v4，图标全部内联 SVG（零 CDN、零新依赖）

---

## 一、设计方向

**关键词：桌面工具级 Modern Utility（工业实用风）**

面向开发者的本地日志分析工具，界面应当：信息密度高、反馈即时、动效克制但精准。参考 VS Code / Linear 的工具气质 —— 不做营销页的浮夸动效，聚焦三类动作：

1. **状态反馈**：hover / active / 拖放 有可感知的即时响应
2. **入场编排**：首次渲染的组件有 100~200ms 级交错入场，营造「加载完成」的确定感
3. **状态语义**：运行中呼吸动画、错误轻震动、成功轻脉冲，动画即信息

### 动效规范（全局 token）

| Token | 值 | 用途 |
|-------|-----|------|
| `--ease-out-quart` | `cubic-bezier(0.25, 1, 0.5, 1)` | 通用自然减速（默认） |
| `--ease-out-expo` | `cubic-bezier(0.16, 1, 0.3, 1)` | 面板/抽屉类大位移 |
| `--duration-fast` | `120ms` | 按钮按压、开关反馈 |
| `--duration-base` | `200ms` | hover、色彩过渡 |
| `--duration-smooth` | `320ms` | 面板宽度、入场编排 |
| `--motion-breathe` | keyframes | 运行状态呼吸（2.4s 循环） |

所有动效遵循 `prefers-reduced-motion: reduce` 降级为 0.01ms。

---

## 二、改动清单

### A. 全局层（main.css / theme.ts）

| 项 | 现状 | 改为 |
|----|------|------|
| 缓动/时长 token | 各组件硬编码 `duration-200` 等 | `@theme` 内统一 token，组件引用 |
| 滚动条 hover | 直切颜色 | 增加 `transition` |
| 减少动效支持 | 无 | 新增全局 `@media (prefers-reduced-motion: reduce)` 规则 |

### B. 图标系统（新组件 `src/components/shared/AppIcon.vue`）

- 收敛全部内联 SVG 为单一组件（24×24 viewBox，`name` prop 分发）
- 覆盖图标：`upload / search / file / clock / folder / chevron-left/right/down / close / sun / moon / help / github / issue / pin / arrow-up / trash / retry / warning / check / batch(操作)`
- Props：`name`、`size`（默认 16）、`strokeWidth`（默认 2）
- 继承 `currentColor`，尺寸走 `em` 实现随字号缩放

### C. AppLayout（顶栏）

| 项 | 现状 | 改为 |
|----|------|------|
| 主题切换图标 | Unicode 字符 ☽ / ☼（跨平台字形不一致） | 精细 SVG sun / moon，保留旋转+缩放切换动画 |
| 主题色下拉 | 纯文字「蓝色/绿色…」 | 每项带色点 swatch（用 `h()` 渲染） |
| 帮助/菜单图标 | 内联 SVG 已合格 | 迁移到 AppIcon，消除重复 |
| 拖放遮罩 | 已有淡入 | 上传图标加轻浮动动画，增强「可放置」暗示 |
| Logo 区 | drop-shadow 发光 | 保留（品牌锚点，克制） |

### D. TabBar（标签栏）

| 项 | 现状 | 改为 |
|----|------|------|
| 溢出渐隐 | 无（内容突然被裁切） | 左右两端 `mask-image` 线性渐隐 |
| 标签入场 | 无（瞬间出现） | 120ms fade + translateY 交错入场 |
| 关闭按钮 | hover 直切红色 | 先 `scale(0)→1` 显示，hover 放大 1.1 |
| 活动标签 | 底部 2px 色条 | 色条改为顶部渐变发光条 + 字重提升 |
| 滚动箭头 | hover 直切色 | 保持，但加 `mask` 后箭头可省（保留兜底） |

### E. WelcomePage（欢迎页）

| 项 | 现状 | 改为 |
|----|------|------|
| 卡片入场 | 无 | 100ms 交错 stagger 入场（`animation-delay: calc()`） |
| 卡片 hover | 仅边框变色 | 边框变色 + `translateY(-1px)` 微上浮 + 阴影加深 |
| kbd 快捷键 | 样式可用 | 统一 kbd 全局样式：阴影下边框模拟键帽 |

### F. StatusBar（状态栏）

| 项 | 现状 | 改为 |
|----|------|------|
| 字号滑块 | 原生 `<input range>`（样式割裂） | 自定义 webkit-slider 样式：细轨道 + 圆形 thumb + hover 放大 |
| 状态信息 | 纯文字 | 保持（信息密度优先，不加噪音） |

### G. ArchiveCard / UploadZone / StatusIndicator

| 项 | 现状 | 改为 |
|----|------|------|
| 状态点 | NTag 静态标签 | 解压中：进度条加条纹流动动画（`background-position` 位移动画）；completed: 无动画 |
| 失败错误行 | 纯文字 | 错误图标 + 文字，背景轻红 |
| 上传区拖入 | 边框变色 | 边框变色 + 图标上浮动效 + 边框虚线滚动（dash offset 动画） |

### H. 文档与验证

- 方案文档：`docs/2026-09-27-ui-optimization.md`（本文件）
- 验证：`npm run typecheck` + `npm test` + `npm run build`
- 提交：中文 commit message，`feat` 前缀

---

## 三、验收标准

| # | 检查项 | 标准 |
|---|--------|------|
| 1 | 图标 | 全应用无 Unicode 字符图标；无 CDN 引用；无新增 npm 依赖 |
| 2 | 动效 | hover/入场/状态动画符合时长 token；`prefers-reduced-motion` 生效 |
| 3 | 类型 | `vue-tsc --noEmit` 通过 |
| 4 | 测试 | `vitest run` 全绿（不新增 UI 快照断言，避免脆弱测试） |
| 5 | 构建 | `vite build` 成功 |
| 6 | 兼容 | 深色/浅色主题切换后所有新样式正常 |

---

## 四、风险与边界

- **不改**：路由/状态管理/composables 数据流、渲染器组件内部逻辑、Rust 侧
- TabBar 溢出 mask 与滚动箭头并存：箭头仍保留（无滚动条时的兜底操作），mask 让裁切不生硬
- 所有动画只动 `transform / opacity / background-position / color`，不触发布局重排
- stagger 入场使用 CSS `animation-delay` 索引计算，避免 JS 编排
