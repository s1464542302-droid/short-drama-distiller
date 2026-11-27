# 短剧解说蒸馏器

一个 WorkBuddy Skill：把爆款短剧解说拆解成可复用的结构模板，再基于用户自己的观点生成合规的原创解说脚本。

**核心原则：蒸馏结构，不蒸馏内容。**

## 它能做什么

- 拆解爆款：钩子类型、情绪曲线、节奏参数、选题角度
- 蒸馏模板：钩子公式 + 情绪时间轴 + 节奏参数表 + 选题清单
- 原创脚本：基于目标短剧生成口播稿，观点内容占比 ≥ 50%
- 合规自检：自动检测剧透结局、替代式解说、照搬与导流风险

## 为什么需要它

2026 年平台查重与版权治理升级，搬运式二创基本没有生存空间。这个 skill 把"学爆款"和"抄爆款"严格分开：只提取可迁移的结构，输出必须是有观点增量的原创内容，并内置合规红线检查。

## 安装

下载 `dist/short-drama-distiller.zip`，解压后放到：

- 用户级：`~/.workbuddy/skills/short-drama-distiller/`
- 项目级：`<项目>/.workbuddy/skills/short-drama-distiller/`

重启 WorkBuddy 后即可通过「蒸馏这条短剧解说」等指令触发。

## 目录结构

```
short-drama-distiller/
├── SKILL.md                           # 工作流与核心原则
├── references/
│   ├── deconstruction-framework.md    # 拆解框架
│   ├── hook-library.md                # 钩子类型库与填空公式
│   ├── compliance-boundaries.md       # 版权红线与合规做法
│   └── platform-profiles.md           # 平台差异速查
├── scripts/
│   └── compliance_check.py            # 脚本合规自检
└── assets/
    ├── deconstruction-template.md     # 拆解报告模板
    └── script-template.md             # 原创脚本模板
```

## 合规自检

```bash
python scripts/compliance_check.py <脚本文件路径>
```

输出分「高风险 / 提示」两级。命中"代替原作"或"剧透结局"必须修改后重跑。自动检查不能替代人工复核，素材授权与引用占比仍需人工确认。

## 使用示例

- 「帮我拆解这 3 条爆款短剧解说的结构」
- 「把这类解说的钩子公式和情绪曲线蒸馏出来」
- 「用蒸馏出的模板，给我这个短剧写一版原创解说脚本」
- 「检查我这份脚本有没有剧透和搬运风险」

## 许可

MIT
