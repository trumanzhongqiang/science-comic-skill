---
name: science-comic-skill
description: "给自媒体一键生成科普漫画：选题理解、事实核查、分镜脚本、角色卡锚定一致性、逐格出图、气泡留空后期填字。触发词：'启动科普漫画'、'科普漫画'、'science comic'、'把 XX 做成漫画'，及任何想把科普选题变成漫画的自然语言请求。"
version: 1.2.0
allowed-tools: Bash, Read, Write, Edit
compatibility: Windows/macOS/Linux. Requires WorkBuddy.
metadata:
  emoji: "🎨"
---

# 科普漫画一键生成

收到本 SKILL.md 意味着用户想把一个科普选题变成一套可发布的漫画图片。核心工作流：成本预告 → 选题理解 → 事实核查（含来源冲突） → 两级角色锚定 → 分镜脚本 → 串行逐格出图 → 脚本合成气泡文字 → 装读者四查（须写 delivery-report.md）。

详细执行指令见 `skill/science-comic-skill/SKILL.md`，打包加载请使用根目录的 `science-comic-skill.skill` 文件。

## 快速使用

1. 在 WorkBuddy 中加载 `science-comic-skill.skill`
2. 对助手说「启动科普漫画」或直接给出选题，例如「把『为什么天空是蓝色的』做成 6 格漫画」
3. 助手会依次产出：知识卡 → 角色卡 → 分镜脚本 → 逐格图片 → 用 tools/compose.py 合成的成品 → 四查交付说明
