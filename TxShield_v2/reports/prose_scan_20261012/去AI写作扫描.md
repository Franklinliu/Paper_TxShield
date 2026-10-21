# 本轮修改内容的去 AI 写作扫描

日期：2026-10-12。**仅扫描，未修改正文、图表、数据或 PDF。**

使用 `general-de-defensive` 的分层检查、`general-confident-prose-pass` 的 C1–C7 / AT 检查及 SE/Security overlay。检查对象是我修改的六个章节及相关图表说明；原稿未改段落不列为本轮问题。行号对应扫描时的 LaTeX 源文件。

## 总体判断

上一轮主要清理了表面的日志词汇，尚未充分处理论文的论证组织。当前主要问题是：**配置指代不清、表格复述、反复解释比较边界，以及缺少具体意义的总结句**。这些是可定位的写作问题，不是对文字是否由 AI 生成的鉴定。

在六个文件的 53 个 `\Blue{}` 标记片段中，configuration/configurations 共出现 37 次；JSON、CSV、export、supplied、checkpoint 均为 0。前者不是禁用词或自动缺陷，但两处 “reference configuration” 和三处 “price-manipulation configuration” 未给出足够明确的论文内指代，说明日志用语部分被换成了抽象代称。

以下共 12 项：3 项优先处理，9 项一般问题。建议不改变实验数值，不删除模型、表格或原图，也不重建已按用户要求删除的 6.6 节。

## 优先处理

### 1. 用抽象配置名称掩盖了未定义的实验对象

- **位置**：`sections/evaluation.tex:103,136,283,294`；`sections/introduction.tex:35`。
- **原文**：“the price-manipulation configuration”；“a category-level analysis of the reference configuration”。
- **分类**：AT8 私有语境泄露；Readability 指代不明。
- **问题**：读者只看论文，无法知道 reference 指的是哪一个骨干及设置。将“原结果”换成“reference configuration”并没有完成论文式表达。
- **建议**：在实验设置中一次定义能确认的实验配置，后文使用同一名称。若现有记录不足以指明骨干，应直接写具体实验对象，例如 “the PriceAttackBench evaluation”，不要虚构一个定义完整的配置，也不要猜填模型名。类别分析同理，需要明确其指代，不能只靠换词解决。
- **边界**：保留价格攻击与 Kimi 主实验的区别；不更改原数据，不重复新增披露章节。

### 2. 由单个对照推导“组件交互”的语气偏强

- **位置**：`sections/evaluation.tex:168`；`sections/conclusion.tex:7`；相关表述见 `sections/abstract.tex:6`。
- **原文**：“showing that its benefit depends on the surrounding pipeline”；“highlighting interactions between retrieval and decision refinement”。
- **分类**：L0 claim 校准；C6 缩小结论范围。
- **问题**：已给出的直接观察是：无 XGBoost 时，两阶段检索提高 precision，却降低 recall/F1。这足以支持该条件下的权衡；单凭这一对照，尚不能量化检索与过滤之间的交互效应。“interactions”让读者期待更完整的交叉消融。
- **建议**：直接停在可观测结果。例如：
  > Without XGBoost, two-stage retrieval increases precision but reduces recall and F1.
  在 RQ2 保留原指标和数值。若要声称交互效应，需相应实验支持，不能通过语气润色扩大结论。

### 3. 对比较边界的解释仍像上一轮对话的回应

- **位置**：`sections/evaluation.tex:158,161,163,165,174,200`。
- **原文**：“rather than counts of candidates rejected within a single filtering stage”；“cannot be attributed to retrieval refinement alone”；“These backbone comparisons complement the fixed-Kimi ablation in RQ2”。
- **分类**：C1 重复限定；C7 多轮回应材料积累。
- **问题**：这些区别有实际意义，但现在每个结果后都要再解释“这个比较是什么、不是什​​么”，使正文像对修改争议逐条答复。尤其 filtering stage 的否定句承接了此前助手误解方法的对话背景。
- **建议**：在 RQ2 设置和表注中一次明确：比较的是完整与消融配置的独立运行；联合移除两项组件。随后正文集中解释结果。同样，把跨骨干比较与固定骨干消融的区别放在一个合适位置，不在图注、正文、总结中反复提醒。
- **边界**：保留必要实验范围；不能把不同运行之间的变化改写为同次过滤前后变化。

## 一般问题

### 4. 摘要实验段过于像压缩后的实验目录

- **位置**：`sections/abstract.tex:6`。
- **原文**：连续列出 728/364/364、P/R/F1、直接分类差值、无 XGBoost 差值、检索消融的两组 F1。
- **分类**：AT7 报告式铺陈；Readability 数字负担；Arc 主线分散。
- **问题**：每一句分别对应一个实验，却没有突出最主要的结果：后过滤框架在降低误报方面的价值。读者需要记忆太多数值才到达段尾。
- **建议**：摘要优先保留主结果和直接 baseline 对比；检索消融若在摘要保留，可压缩为一句有明确范围的发现。全部原始数值继续在表格和 RQ2 保留，不删除实验数据。
- **示例主句**：
  > With Kimi-k3, TxShield achieves 92.93% F1 and reduces false positives from 60 to 7 compared with XGBoost-only.
  这是段落主线示例，不是要求将整个摘要换成一句话。

### 5. 引言与结论重复同一组完整指标，缺少章节分工

- **位置**：`sections/introduction.tex:35`；`sections/conclusion.tex:7`。
- **原文**：两处均完整重复 93.27% accuracy、97.87% precision、88.46% recall、92.93% F1，随后重复 baseline 和消融数字。
- **分类**：AT7 表格转述；Arc。
- **问题**：引言像结果表的目录，结论像再次播放结果表。数字复述挤占了“这项方法解决了什么问题”的表达。
- **建议**：引言用主要发现建立贡献；完整指标放主表；结论总结已证实的能力及适用条件，只保留支撑这一总结的关键数字。数字仍存在论文中，不要求删表或删模型。

### 6. 贡献句描述“做了哪些工作”，没有突出研究产出

- **位置**：`sections/introduction.tex:41`。
- **原文**：“We combine two-stage retrieval, adaptive prompting, and XGBoost post-filtering, and evaluate their configuration-dependent effects…”
- **分类**：AT7 任务清单；AT6 抽象修饰。
- **问题**：“combine … and evaluate …”既像实现清单，又像实验计划；“configuration-dependent effects”没有说明具体产出。相邻一条贡献已经负责实验评价，二者职责重叠。
- **建议**：这一条只写方法设计，让下一条负责实验。示例：
  > We design a detection pipeline that retrieves historical attack evidence for LLM reasoning and applies XGBoost to filter the resulting attack candidates.
  不补未经验证的创新性或普遍有效性断言。

### 7. 方法段在相邻位置重复同一执行流程

- **位置**：`sections/approach.tex:21,317,346`。
- **原文**：“first … produces an initial decision”；“subsequently pass through the XGBoost filter”；“first analyzes … then checked”。
- **分类**：AT7 说明书感；Readability 重复。
- **问题**：概述、输出定义、XGBoost 小节都重新讲“LLM 后接过滤”，但小节并未比概述多解释多少过滤的作用。
- **建议**：概述保留一句流程；输出段只定义初始标签与最终标签；XGBoost 小节聚焦判别依据及其为何补充语义推理。不要再增加同义流程句，也不要编造阈值或融合公式。

### 8. 特征与参数长清单缺少组织，接近配置说明

- **位置**：`sections/approach.tex:348`；`sections/evaluation.tex:42`。
- **原文**：“The 14 candidate features comprise …”；“Its hyperparameters are maximum depth 3, learning rate 0.02 …”。
- **分类**：AT7 技术说明书感；Readability 长句。
- **问题**：特征段一次塞入 14 项，baseline 段把方法定义、样本划分、7 项参数、AUC 和表格导航混在一起。列表本身合法，问题在于读者难以识别每类信息的作用。
- **建议**：特征按调用结构、操作标志、调用 value/签名概括后列出细项；参数集中到设置表或紧凑的设置句，保留全部参数值。将 AUC 放结果语境而非夹在 baseline 定义与实现设置之间。
- **边界**：不推断某项特征最重要，也不把调用 value 写成完整代币资金流。

### 9. RQ1 与 RQ2 有明显的“把表格念一遍”问题

- **位置**：`sections/evaluation.tex:55,161`。
- **原文**：“679 of 728 … 322 attacks and 357 benign … 7 false positives and 42 false negatives”；“93 … two … 39 … 12 … 91 … 27 …”。
- **分类**：AT7 实验记录感；Readability 信息密度。
- **问题**：正文逐项重述混淆矩阵及转换计数。读者需自己从数字堆中提取观察；主结果表已含完整混淆矩阵。
- **建议**：正文以“误报下降、召回变化”组织证据。混淆矩阵继续留表中；配对转换计数若需要全部保留，可集中为一行或独立小表，避免逐个口述。不要把这些计数解读为过滤器的同次运行直接贡献。

### 10. RQ3 先列九个名字，后给结论，段落重点埋得太深

- **位置**：`sections/evaluation.tex:181`。
- **原文**：“compares nine backbone configurations, spanning GPT-4.1-mini, Baidu …”。
- **分类**：Readability buried lede；AT7 清点式写法。
- **问题**：Fig. 5 已完整列出九模型，正文再次枚举占据开头；真正有价值的发现直到第三句才出现。
- **建议**：以 Kimi 和 DeepSeek 的错误类型差异开头，随后引用 Fig. 5 和表 5。示例：
  > Among the three complete post-filtered evaluations, Kimi-k3 yields the fewest false positives, while DeepSeek-v4-pro detects the most attacks.
- **边界**：全部九个模型和各自数值仍在图中。这里删的是正文的重复枚举，不是模型或数据。

### 11. 多处段尾只重复结论或泛化为“价值/未来交互”

- **位置**：`sections/abstract.tex:6`；`sections/evaluation.tex:165,200,222`；`sections/conclusion.tex:7`。
- **原文**：“while motivating further study of interactions…”；“This comparison uses a common sample set and measures the difference…”；“These backbone comparisons complement…”；“Together, these results show the value…”。
- **分类**：AT3/AT5 模板化收尾；Readability 低信息句。
- **问题**：有的句子只是重复上一句，有的泛泛指向 future work 或 method value，没有增加研究含义。
- **建议**：对每个段尾做删除测试：删掉后若不丢信息，就删重复句；若需要收束，则写具体发现，例如哪一种错误减少、哪种取舍出现。不要为了每段都“升华”而补一句空泛总结。

### 12. Data Availability 已去掉流水账，但仍重复方法摘要

- **位置**：`sections/data_availability.tex:3,5`。
- **原文**：“The framework combines historical attack knowledge, two-stage retrieval, adaptive LLM prompting, and XGBoost post-filtering.”
- **分类**：AT7 栏目功能错位；Arc。
- **问题**：该栏目应该让读者找到资源，末句却再次介绍系统组成。样本构成也已在实验设置出现，这里无需再完整复述。
- **建议**：保留数据集名称、可定位的来源与实现仓库；删方法组成句。不要换成新一轮 JSON/CSV 清单，也不要在未核实的情况下扩大“全部公开”的承诺。

## 哪些内容不应为了“去 AI”而删掉

- 726/728、588/728 等有效样本数及 coverage：影响指标含义。
- XGBoost-only 与 LLM 后过滤的区别：它们回答不同研究问题。
- 无 XGBoost 时检索消融的真实方向：不能改成始终提升 F1。
- Fig. 5 原六模型和新三模型：全部保留，统一坐标轴。
- RQ4 与主结果的骨干区别：保留一次清楚的范围说明，压缩重复提醒。
- 数据表、真实计数、引用：扫描不改；后续润色应保留。

## 建议处理顺序

1. 先处理指代不清和过度解释（问题 1、2），确定各句实际能说什么。
2. 合并重复范围说明（问题 3），不新增独立披露章节。
3. 重新安排摘要、贡献、RQ3 的主句（问题 4、5、6、10）。
4. 压缩流程复述、特征/参数铺陈和数字口述（问题 7、8、9）。
5. 删除低信息段尾和 Data Availability 的栏目外内容（问题 11、12）。

当前源文件和 PDF 未改动。建议英文仅用于说明修改方向，不构成已实施修改。
