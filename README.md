# 科普漫画 science-comic-skill 🎨

![version](https://img.shields.io/badge/version-1.1.0-blue)
![license](https://img.shields.io/badge/license-MIT-green)
![platform](https://img.shields.io/badge/platform-WorkBuddy-orange)

> 给自媒体一键生成科普漫画的 Agent Skill：选题理解、事实核查、分镜脚本、角色卡锚定一致性、逐格出图、气泡留空后期填字。
>
> One-click science comics for content creators: topic analysis, fact-checking, storyboard scripting, character-card anchoring for cross-panel consistency, and panel-by-panel publishable comic images. [English README](#english-readme)

只需提供一个选题，自动完成从「为什么天空是蓝色的」到一整套可发布漫画图片的全过程：事实准确、角色跨格一致、气泡文字清晰。

## 功能特性

- **选题理解**：接收选题或一段科普文案，提炼核心知识点，规划「悬念开场 → 层层拆解 → 总结升华」的叙事节奏
- **事实核查优先**：生成脚本前先检索核对知识点，来源可溯；检索不到的说法点名缺口、交用户决定，不写成「科学家认为」式的泛话
- **分镜脚本**：逐格输出画面描述、旁白与气泡对话，先给你确认再出图
- **角色卡锚定一致性**：先固化角色外观、配色（具体色值）与画风描述词，压缩成锚定提示词原样嵌入每一格，跨格、跨连载期数形象不漂移
- **逐格出图**：自动生成每格图像提示词，处理多角色构图、表情与肢体动作
- **智能文字策略**：图像模型中文渲染不可靠，气泡与标题一律留空，后期精准填字，不错字、可修改

## 快速开始

**WorkBuddy 用户：**

1. 下载本仓库的 [`science-comic-skill.skill`](./science-comic-skill.skill) 文件
2. 在 WorkBuddy 中加载该 `.skill` 文件
3. 对助手说「启动科普漫画」，或直接给出选题：

   > 把「为什么天空是蓝色的」做成 6 格漫画

4. 助手依次产出：知识卡 → 角色卡 → 分镜脚本（给你确认）→ 逐格图片 → 合成成品

**其他支持 SKILL.md 规范的助手：** 直接让助手读取 [`skill/science-comic-skill/SKILL.md`](./skill/science-comic-skill/SKILL.md) 并按其中的指令工作即可。

## 演示示例

想看看产出的中间产物长什么样？[`examples/demo-comic.md`](./examples/demo-comic.md) 里有一份完整演示：从选题到知识卡、角色卡锚定词、分镜脚本节选、单格出图提示词的全链路。

## 它是怎么工作的

```
选题分析 → 事实核查（知识卡，来源可溯）
        → 角色卡锚定（外观/色值/画风固化为锚定词）
        → 分镜脚本（每格一个知识点，先确认再出图）
        → 逐格图像生成（锚定词逐字嵌入每格）
        → 气泡文字后期合成（模型不碰文字）
```

三条核心设计原则：**科学准确性优先**（核查不过的知识点不进脚本）、**角色一致性是生命线**（锚定词逐字复用）、**同一张角色卡可复用到整个连载系列**。

## 质量保证

发布前必须通过「装读者四查」（[`skill/science-comic-skill/references/quality-checklist.md`](./skill/science-comic-skill/references/quality-checklist.md)）——假装自己是一个刷到这条漫画的读者，逐项核对：知识可溯 / 角色一致 / 文字清晰 / 节奏，任一查不过不交付。

## 目录结构

```
science-comic-skill/
├── README.md                  # 本文件
├── LICENSE                    # MIT License
├── SKILL.md                   # 根级 Skill 说明（WorkBuddy 规范 frontmatter）
├── science-comic-skill.skill  # 打包文件（WorkBuddy 直接加载）
├── examples/
│   └── demo-comic.md          # 演示：选题 → 知识卡 → 角色卡 → 分镜 → 出图提示词
└── skill/
    └── science-comic-skill/
        ├── SKILL.md           # 核心执行指令（工作流 + 归因式红线）
        └── references/
            ├── character-card-template.md   # 角色卡模板与锚定描述词规范
            ├── storyboard-template.md       # 分镜脚本模板与 6 格示例
            └── quality-checklist.md         # 发布前「装读者四查」质检清单
```

## 常见问题

**Q：气泡文字为什么是后期填的，不让模型直接画？**
图像生成模型渲染中文必然出现乱码错字，且无法无痕修复只能整格重画。留空白气泡 + 后期填字，文字清晰、可改、可换字体。

**Q：能做连载吗？**
可以。角色卡是核心资产——同一张角色卡复用到每一期，形象不漂移；新增配角补建角色卡即可。

**Q：医疗、法律这类专业选题能做吗？**
能，但漫画中会保留「科普仅供参考」提示；事实核查阶段对强专业内容会更严格，核查不过的知识点不进入脚本。

## License

[MIT](LICENSE) © 2026 Zhongqiang Wang

---

## English README

**science-comic-skill** turns a science topic into a publishable comic strip for content creators — with fact-checking before creation and character consistency across every panel.

### How it works

1. Load `science-comic-skill.skill` in WorkBuddy (or point any AI assistant at `skill/science-comic-skill/SKILL.md`)
2. Say "启动科普漫画" or give a topic: "把『为什么天空是蓝色的』做成 6 格漫画"
3. The pipeline runs: topic analysis → **fact-checking first** (knowledge cards with traceable sources; unverifiable claims are flagged, never papered over) → **character card** (appearance, hex colors, art style compressed into an anchor prompt reused verbatim in every panel) → storyboard (approved by you before any image) → panel-by-panel image generation (bubbles left blank — image models can't render Chinese text reliably) → text composited in post

### Key properties

- **Facts before art**: unverified knowledge points never enter the script — a beautiful comic with wrong science spreads the error wider
- **Consistency anchoring**: the same anchor prompt is embedded verbatim in every panel and every episode of a series
- **Text in post**: all bubbles and titles are composited afterward — no garbled characters, editable forever
- **Reader-perspective QA**: a four-point "as a reader" checklist (traceable facts / consistent characters / clean text / pacing) gates every delivery

See `examples/demo-comic.md` for a full demo from topic to panel prompts.

License: [MIT](LICENSE) © 2026 Zhongqiang Wang
