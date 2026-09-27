# 项目清理方案 — 废弃/冗余代码全量识别

> 日期：2026-09-27
> 方法：全量引用追踪（grep -r 引用计数）+ git 跟踪状态核查
> 原则：只删「零引用 + 零 git 价值」的项；不动业务代码

---

## 一、废弃文件/目录（删除）

### A. 未被 git 跟踪的本地垃圾（约 1.6 GB + 12 MB）

| 项 | 大小 | 判定依据 | 风险 |
|----|------|---------|------|
| `target/`（根目录） | 1.6 GB | 历史遗留：曾从根目录跑 cargo，产物已由 `src-tauri/target/` 取代；未被 git 跟踪 | 无 |
| `release/` | 4.5 MB | 旧打包产物（`Hello-Tauri-0.1.0-x64.exe`），已被 `build/日志解析工具-*.exe` 流程取代；未跟踪 | 无 |
| `dist/`（根目录） | 1.5 MB | 旧 Vite 产物（输出目录早已改为 `build/web`）；未跟踪 | 无 |
| `Hello-Tauri-Log-Parser/` | 12 MB | **整份项目副本**（含自己的 src/package.json，无 node_modules），零引用零跟踪 | 无 |

### B. git 跟踪中的零引用死代码

| 项 | 引用数 | 判定依据 | 风险 |
|----|--------|---------|------|
| `src/components/public-bar/GlobalStats.vue` | **0 处** | 无任何 import（含 e2e） | 无 |
| `src/components/property-panel/ConfigForm.vue` | **0 处** | 无任何 import | 无 |
| `src/api/.gitkeep` | — | 空目录占位，目录从未使用 | 无 |
| `src/assets/logo.png` + `logo.svg` | **0 处** | 无引用（Logo 已由 `AppLogo.vue` SVG 组件实现） | 无 |
| `vitest.debug.config.ts` | 0 处 | 自述「临时调试脚本」，console.log 探测 `__dirname` | 无 |
| `vitest.minimal.config.ts` | 0 处 | 仅指向 `_minimal.test.ts` | 无 |
| `src/__tests__/_minimal.test.ts` | — | 冒烟占位测试，随 minimal 配置一起废弃 | 无 |

## 二、依赖优化（package.json）

| 依赖 | 判定 | 动作 |
|------|------|------|
| `vue-draggable-plus` | **全项目零 import**（src/ e2e/ 均无） | 移除（AGENTS.md 文档同步删除） |
| `splitpanes` | 在用（`CsvTableTreeView` → `SplitView` → main.ts 引 CSS） | **保留** |

## 三、代码级优化建议（本次不动，仅记录）

1. `index-B2oSRxVO.js` 主 chunk 790 KB —— 后续可做路由级/渲染器级动态 import 拆包
2. `src/styles/theme.ts` 中 `themeColorLabels` 先 const 后 export（两段声明），可合并——纯风格问题，不值得动
3. `data/` 测试样本（含 2 个 zip、万行 CSV）—— e2e 测试数据，保留

## 四、执行与验证

- 删除方式：git 跟踪项走 `git rm`；本地垃圾目录用 `cmd rmdir`（绕开 node fs 垫片坑）
- 验证四连：`typecheck` → `test`（531 基线）→ `build` → `build:exe`（单文件产物冒烟）
- 提交：`chore: 清理废弃代码与冗余产物目录`
