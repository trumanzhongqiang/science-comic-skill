# 演示：从一个选题到一格出图提示词

> 这是文字链路示例，没有真实出图。要看测评成品，打开 [`samples/lung-cancer-quit/preview.html`](samples/lung-cancer-quit/preview.html)。


> 本演示完整呈现 science-comic-skill 的中间产物链路：选题 → 知识卡 → 角色卡锚定词 → 分镜脚本（节选）→ 单格出图提示词。
> 示例选题：「为什么天空是蓝色的」。

---

## 1. 知识卡（阶段 2：事实核查）

| 编号 | 一句话结论 | 来源 | 类比/可视化建议 |
|------|-----------|------|----------------|
| K1 | 天空呈现蓝色是阳光被大气散射的结果 | 大学物理教材·光学 | 阳光穿过「空气滤网」 |
| K2 | 阳光由多种颜色的光组成（可分解为七色） | 初中物理·光的色散 | 「彩虹全家桶」 |
| K3 | 蓝光波长短，被空气分子散射得最强（瑞利散射，强度 ∝ 1/λ⁴） | 百科·瑞利散射词条 | 小颗粒弹小球，蓝光被弹得到处都是 |
| K4 | 傍晚太阳斜射，光路变长，蓝光散失多，红光直达眼睛 | 同上 | 长跑比赛，蓝光先「累倒」 |

**纪律可见**：每个知识点一句话结论 + 可溯来源 + 画面化建议；核查不过的知识点不进脚本。

## 2. 角色卡与锚定描述词（阶段 3）

角色卡（节选）：

| 字段 | 小盐（讲解型主角） |
|------|------------------|
| 外观 | 圆脸、黑色齐耳短发、大眼睛 |
| 配色 | 主色番茄红 #FF6347，辅色米白 #FFF8E7 |
| 服饰 | 红色连帽衫 + 米色围裙，胸口白色盐粒图案 |
| 画风 | 明快扁平卡通，粗描边，二头身 Q 版 |

锚定描述词（抽象风格级 + 具象形态级，之后每一格原样嵌入）：

```
chibi 2-head-tall cartoon, thick outlines, flat bright colors,
extremely large round head, tiny stubby body, very short thick limbs,
warm beige skin #F6D7B8,
round face, short black bob haircut, big eyes,
wearing a tomato-red hoodie (#FF6347) and cream apron (#FFF8E7),
a tiny white salt-grain emblem on the chest,
holding a wand-like stirring stick,
cheerful curious expression, clean vector style
```

## 3. 分镜脚本（阶段 4，节选两格）

```markdown
## P1｜全景｜情绪：疑问
- 画面：小海躺在草地上指着天空，小盐站在旁边。天空大面积留白，顶部预留空白标题位。
- 旁白：（留空，后期填「天空为什么是蓝色的？」）
- 气泡：小海：「天为啥是蓝的？」
- 知识点：K1（现象）

## P3｜中景｜情绪：演示
- 画面：小盐用手把一束光「拆」成七色，空中留白气泡。
- 气泡：小盐：「小颗粒把光拦住了。」
- 知识点：K3（瑞利散射）
```

**纪律可见**：每格只讲透一个知识点；每格标注对应知识卡编号，保证事实有出处；气泡是一句能听懂的口语，解释和数字放文字卡；标题与旁白位置留空待后期填字。

## 4. 单格出图提示词（阶段 5，P3 示例）

```
chibi 2-head-tall cartoon, thick outlines, flat bright colors,
extremely large round head, tiny stubby body, very short thick limbs,
warm beige skin #F6D7B8,
round face, short black bob haircut, big eyes,
wearing a tomato-red hoodie (#FF6347) and cream apron (#FFF8E7),
a tiny white salt-grain emblem on the chest,
holding a wand-like stirring stick,
cheerful curious expression, clean vector style,
splitting a beam of sunlight into a rainbow of seven colors with both hands,
medium shot, plain light background, a large wide blank white speech bubble, inner width at least 40% of the panel, above
```

**纪律可见**：锚定词逐字嵌入在最前；多角色同框时角色名前重复关键特征防混淆；气泡写 `blank white speech bubble`——模型只画空白气泡，一个中文字都不许渲染。

---

出图后进入阶段 6（文字后期合成）与发布前「装读者四查」。完整工作流与红线见 [`skill/science-comic-skill/SKILL.md`](../skill/science-comic-skill/SKILL.md)。
