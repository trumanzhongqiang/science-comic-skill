# 角色卡：戒烟这件事

**画风描述词（整组统一，嵌在每格提示词最前）**

```
bright flat-vector cartoon, chibi 2-head-tall proportions, thick clean outlines,
flat high-saturation colors with no gradients, simple shapes, white background
```

---

## 主角：小晴

| 字段 | 内容 |
|---|---|
| 定位 | 讲解型主角（呼吸科医生形象，但不画医院场景也能成立） |
| 外观 | 圆脸；黑色齐耳短发，头顶有一撮向右翘起的呆毛；大圆眼；二头身 |
| 配色 | 主色 青蓝 `#2E9BB5`；辅色 米白 `#FFF8E7`；点缀 橙色 `#F2803C` |
| 服饰 | 青蓝色短款立领外套 + 米白圆领内搭；左胸有一枚**白色肺形徽章**（纯图形，不含任何文字） |
| 标志道具 | 一支**银色小手提喇叭**（讲解用） |
| 性格关键词 | 清醒、直给、表面冷静其实很暖 |
| 表情基调 | 笃定、带一点点"我就直说了"的神态 |

**锚定描述词（Anchor Prompt）— 每格逐字复用**

```
a chibi 2-head-tall cartoon doctor named Xiaoqing: round face, short black bob hair
with one cowlick sticking up to the right, large round eyes, wearing a teal-blue
(#2E9BB5) short stand-collar jacket over a cream-white (#FFF8E7) crew-neck top,
a white lung-shaped pin emblem on the left chest (plain white shape, absolutely no
text or letters), holding a small silver hand megaphone, calm confident expression
```

---

## 配角：老周

| 字段 | 内容 |
|---|---|
| 定位 | 提问型配角（50 多岁、刚戒烟半年的老烟民） |
| 外观 | 圆脸；灰白寸头；粗眉；一字小胡子；二头身，比小晴略矮胖 |
| 配色 | 主色 石板灰蓝 `#6B7F94`；辅色 浅卡其 `#E8DCC8` |
| 服饰 | 石板灰蓝拉链夹克 + 浅卡其内搭 |
| 标志道具 | 手里常攥着一张大号胸部 CT 片（黑底白影的胶片，**胶片上不出现任何文字**） |
| 性格关键词 | 心急、直率、有点委屈 |
| 表情基调 | 困惑、着急、后来恍然大悟 |

**锚定描述词（Anchor Prompt）— 每格逐字复用**

```
a chibi 2-head-tall cartoon middle-aged man named Laozhou: round face, short grey
crew-cut hair, thick eyebrows, a small neat moustache, slightly shorter and
chubbier than the doctor, wearing a slate-grey (#6B7F94) zip jacket over a light
khaki (#E8DCC8) shirt, holding a large chest CT film (plain black-and-white film
with no text or letters on it), worried impatient expression
```

---

## 多角色同框时的写法规则

在每格提示词里，**角色名前必须重复其关键特征**，防止模型把两人混成一个：

- `the teal-blue-jacketed doctor Xiaoqing with the lung pin and silver megaphone`
- `the slate-grey-jacketed grey-haired man Laozhou with the CT film`

## 文字策略（红线）

- 所有气泡、标题、旁白一律写成 **`blank white speech bubble` / `empty title banner`**
- 提示词中显式加约束：`no text, no letters, no words, no numbers, no watermark anywhere in the image`
- 中文全部由阶段 6 用 Pillow 后期合成，模型不渲染任何字符
