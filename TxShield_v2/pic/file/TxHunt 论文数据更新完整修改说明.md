
# TxHunt 论文数据更新完整修改说明

**更新原因**：更换主力 LLM 骨干模型（默认使用 Kimi_k3），重新跑通 DeFiAttackBench 全量实验及消融实验，同步更新开销数据 
**影响范围**：摘要、引言、第6章全部 RQ、表1 / 表4 / 表5、结论、数据可用性声明 
**默认主结果**：以 **Kimi_k3** 作为完整 TxHunt 的官方结果  

[tx-anomaly-predict/data at main · limumus/tx-anomaly-predict](https://github.com/limumus/tx-anomaly-predict/blob/main/data)

---

## 1. 总体变更摘要

| 关键指标 | 原数值（GPT-4.1-mini） | 新数值（Kimi_k3） | 变化幅度 |
|----------|------------------------|-------------------|----------|
| Accuracy | 0.838 / 83.8% | **93.27%** | +9.47 pp |
| Precision | 0.832 / 83.2% | **97.87%** | +14.67 pp |
| Recall | 0.846 / 84.6% | **88.46%** | +3.86 pp |
| F1-Score | 0.839 / 83.9% | **92.93%** | +9.03 pp |
| 消融 RAG 增益 | 0.601 | **17.59 pp** | 大幅上升 |
| 主力模型成本（728样本） | $3.86 | **¥74.05** | 计价体系变化 |

---

## 2. 表格更新对照及对应修改说明

### 2.1 Table 1：Performance comparison on DeFiAttackBench  
**原文件位置**：第13页 Table 1

#### 原表格

| Tool | TP | FP | TN | FN | Accuracy | Precision | Recall | F1-Score | Avg. Time |
|------|----|----|----|----|----------|-----------|--------|----------|-----------|
| Txspector | 117 | 117 | 128 | 88 | 0.544 | 0.500 | 0.571 | 0.533 | ∼hours |
| TrxGNNBERT | 288 | 91 | 264 | 85 | 0.759 | 0.760 | 0.773 | 0.766 | ∼5 min |
| Blockscan | 255 | 12 | 352 | 109 | 0.834 | 0.955 | 0.701 | 0.810 | 25 s |
| ~~TxHunt(Ours)~~ | ~~308~~ | ~~62~~ | ~~302~~ | ~~56~~ | ~~0.838~~ | ~~0.832~~ | ~~0.846~~ | ~~0.839~~ | ~~15.02 s~~ |

#### 更新后完整表格（更新部分加粗）

| Tool / Model | TP | FP | TN | FN | Samples | Accuracy | Precision | Recall | F1-Score | Notes |
|--------------|----|----|----|----|---------|----------|-----------|--------|----------|-------|
| Txspector | 117 | 117 | 128 | 88 | 450 | 0.544 | 0.500 | 0.571 | 0.533 | 原结果保留 |
| TrxGNNBERT | 288 | 91 | 264 | 85 | 728 | 0.759 | 0.760 | 0.773 | 0.766 | 原结果保留 |
| Blockscan | 255 | 12 | 352 | 109 | 728 | 0.834 | 0.955 | 0.701 | 0.810 | 原结果保留 |
| **TxHunt (Kimi_k3)** | **322** | **7** | **357** | **42** | **728** | **93.27%** | **97.87%** | **88.46%** | **92.93%** | **主结果** |
| Deepseek-v4-pro | 325 | 24 | 340 | 39 | 728 | 91.35% | 93.12% | 89.29% | 91.16% | 新增对比 |
| GPT-5.6-luna | 318 | 28 | 335 | 46 | 727 | 89.82% | 91.91% | 87.36% | 89.58% | 新增对比 |
| ~~Qwen3_8B~~ | ~~293~~ | ~~97~~ | ~~162~~ | ~~36~~ | ~~588~~ | ~~77.38%~~ | ~~75.13%~~ | ~~89.06%~~ | ~~81.50%~~ | ~~样本不完整（作为参考）~~ |

source: `data/defiattack_with_xgboost_728.csv`

之前的数据仅供参考：`data/defiattack_original_noxgboost_728.csv`

**本表对应结论变化标注与修改后参考段落**：

- 主结果 F1 从 **83.9%** 提升至 **92.93%**（+9.03 pp），已大幅领先所有原基线。
- 原“F1 0.824/0.839”“TxHunt achieves an F1-score of 0.839”等表述必须全部同步修改，否则结论与数据严重矛盾。
- Qwen3_8B 样本仅 588，建议在表格中明确标注“样本不完整，仅作参考”。
- 原“20× faster than TrxGNNBERT”等效率对比可保留。

**修改后参考段落（建议替换原 6.1 节 RQ1 回答）**：

**中文**： 
在 DeFiAttackBench 上，以 Kimi_k3 为骨干的 TxHunt 取得 **93.27%** 准确率和 **92.93%** F1 分数（TP=322, FP=7, TN=357, FN=42），显著优于原报告的 GPT-4.1-mini 结果以及所有基线方法。Deepseek-v4-pro 和 GPT-5.6-luna 分别取得 91.16% 和 89.58% 的 F1，验证了框架在不同 LLM 上的稳健性。Qwen3_8B 因样本不完整（588 条）仅作参考。
On the DeFiAttackBench dataset, TxHunt with the Kimi_k3 backbone achieves an accuracy of **93.27%** and an F1-score of **92.93%** (TP=322, FP=7, TN=357, FN=42), substantially outperforming the previously reported GPT-4.1-mini results as well as all baseline methods. Deepseek-v4-pro and GPT-5.6-luna obtain F1-scores of 91.16% and 89.58%, respectively, confirming the robustness of the framework across different LLM backbones. Qwen3_8B is reported only for reference due to incomplete samples (588).

---

### 2.2 Table 4：Ablation study  
**原文件位置**：第14页 Table 4 
**说明**：以 Kimi_k3 完整系统作为 Full TxHunt 基准。

#### 原表格

| Configuration | Accuracy | Precision | Recall | F1-Score |
|---------------|----------|-----------|--------|----------|
| ~~TxHunt~~ | ~~0.838~~ | ~~0.832~~ | ~~0.846~~ | ~~0.839~~ |
| ~~w/o XGBoost classifier~~ | ~~0.812~~ | ~~0.774~~ | ~~0.882~~ | ~~0.824~~ |
| ~~w/o XGBoost & Two-Stage Retrieval~~ | ~~0.779~~ | ~~0.743~~ | ~~0.852~~ | ~~0.794~~ |
| ~~w/o RAG Framework~~ | ~~0.551~~ | ~~0.785~~ | ~~0.140~~ | ~~0.238~~ |

#### 更新后完整表格（）

| Configuration | TN | TP | FN | FP | Samples | Accuracy | Precision | Recall | F1-Score |
|---------------|----|----|----|----|---------|----------|-----------|--------|----------|
| **TxHunt (Full, Kimi_k3)** | **357** | **322** | **42** | **7** | **728** | **93.27%** | **97.87%** | **88.46%** | **92.93%** |
| w/o XGBoost classifier | **266** | **295** | **69** | **98** | **728** | **77.06%** | **75.06%** | **81.04%** | **77.94%** |
| w/o XGBoost & Two-Stage Retrieval | **254** | **315** | **49** | **110** | **728** | **78.16%** | **74.12%** | **86.54%** | **79.85%** |
| w/o RAG Framework | **266** | **278** | **84** | **98** | **726** | **74.93%** | **73.94%** | **76.80%** | **75.34%** |

source: `data/ablation_study_kimi_k3.csv`

**消融增益计算（新）**：

- RAG 贡献：92.93% − 75.34% = **+17.59 pp**
- 两阶段检索贡献：92.93% − 79.85% = **+13.08 pp**
- XGBoost 贡献：92.93% − 77.94% = **+14.99 pp**

#### 各模块贡献结论变化对比

| 模块               | 原 GPT-4.1-mini 贡献（绝对 F1） | 新 Kimi_k3 贡献（绝对 F1）                                   | 变化说明                                    |
| ------------------ | ------------------------------- | ------------------------------------------------------------ | ------------------------------------------- |
| **RAG 框架**       | +0.601（从 0.238 → 0.839）      | **+17.59 pp**（92.93% → 75.34%）                             | 仍然是最大贡献源                            |
| **两阶段检索**     | +0.030                          | 约 **+13 pp** 量级（结合 w/o XGBoost & Two-Stage 数据）      | 贡献明显放大                                |
| **XGBoost 分类器** | 无                              | **+14.99 pp**（92.93% → 77.94%）                             | 从几乎可忽略变为与 RAG 接近的重要精度提升器 |
| **整体层次**       | RAG 绝对主导                    | RAG 仍最大，但 XGBoost 与两阶段检索的贡献都大幅上升，三者更均衡 | 系统对后处理与检索质量更敏感                |

**本表对应结论变化标注与修改后参考段落**：

- RAG 绝对贡献从原来的 0.601 变为约 **17.59 个百分点**，仍然是最大贡献源。
- 原“RAG 贡献 0.586/0.601”“absolute F1 gain of 0.601”等表述必须全部同步修改，否则结论与数据严重矛盾。
- 两阶段检索与 XGBoost 的边际贡献数值也需同步更新。

**修改后参考段落（建议替换原 6.2 节 RQ2 回答）**：

**中文**： 
消融实验以 Kimi_k3 完整系统为基准。移除 RAG 框架后，F1 分数从 92.93% 降至 75.34%，绝对下降 17.59 个百分点，仍是性能的最大贡献源。移除 XGBoost 分类器后，F1 降至 77.94%（下降 14.99 个百分点）；同时移除两阶段检索后，F1 为 79.85%。结果表明，在更强的 LLM 骨干下，检索增强依然核心，但两阶段过滤与 XGBoost 后处理的贡献显著提升，三者共同构成稳健的检测性能。
Ablation studies are conducted with the full Kimi_k3 system as the baseline. Removing the RAG framework drops the F1-score from 92.93% to 75.34%, an absolute decrease of 17.59 percentage points, remaining the largest contributor. Removing the XGBoost classifier reduces F1 to 77.94% (a drop of 14.99 percentage points); further removing the two-stage retrieval yields 79.85%. These results show that while retrieval augmentation remains central, the contributions of two-stage filtering and the XGBoost post-processor become substantially larger under a stronger LLM backbone, jointly forming a more balanced and robust detection pipeline.

---

### 2.3 Table 5：Runtime & Cost  
**原文件位置**：第17页 Table 5

#### 原表格

| Model                        | Tokens | Cost($) | Avg. Time(s) |
| ---------------------------- | ------ | ------- | ------------ |
| GPT-4.1-mini                 | 8.62M  | 3.86    | 15.02        |
| Llama-3.1-8B-Instruct        | 8.28M  | 0.26    | 11.82        |
| 百度 ERNIE-Speed-128k        | 11.62M | FREE    | 12.66        |
| InternLM3-8B-Instruct        | 8.2M   | FREE    | 12.70        |
| DeepSeek-R1-Distill-Qwen-14B | 7.7M   | FREE    | 32.31        |
| Qwen3-8B                     | 8.15M  | FREE    | 37.54        |

#### 更新后完整表格（在原表格基础上追加新结果）

| Model                 | Tokens    | Cost                                               | Avg. Time | Notes      |
| --------------------- | --------- | -------------------------------------------------- | --------- | ---------- |
| GPT-4.1-mini          | 8.62M     | $3.86                                              | 15.02s    | 原结果保留 |
| Llama-3.1-8B-Instruct | 8.28M     | $0.26                                              | 11.82s    | 原结果保留 |
| **Kimi_k3**           | **7.6M**  | **¥73.67（推理）+ ¥0.38（缓存）≈ ¥74.05 ≈ $11.03** | 20.06s    | 全量一轮   |
| **Deepseek-v4-pro**   | **6.49M** | **¥34.87（夜间运行） ≈ $5.20 **                    | 45.74s    | 全量一轮   |
| **GPT-5.6-luna**      | ≈         | ≈ **$3.04**                                        | 10.21s    | 全量一轮   |

- 原“20× faster than TrxGNNBERT”等效率对比可保留，但成本数字需同步更新。

## 

## 【参考】其他需要同步修改的位置清单

| 位置 | 原内容关键词 | 建议动作 |
|------|--------------|----------|
| 摘要 | F1-score of 0.824 / 0.839 | 改为 **92.93%**，并更新 RAG 增益描述 |
| 引言最后 | F1 score of 0.824 | 同步修改 |
| 6.1 节正文 | 0.838 / 0.839 | 全部替换为新表数字 |
| 6.2 节正文 | 0.601 / 0.030 / 0.015 | 按新消融增益重写 |
| 6.3 节（敏感性） | GPT-4.1-mini 最高 | 改为 Kimi_k3 最高，补充新模型对比 |
| 6.4 节（效率） | $3.86 / $0.26 | 增加 Kimi 与 Deepseek 成本 |
| 结论 | 0.824 / 0.586 | 全部同步为新数字 |



## 6. 未更新部分说明（RQ4 与横向基线对比）

**RQ4（效率与成本分析）**： 
本来预期对 RQ4 进行更新，但未能找回之前实验中使用的样本划分结果。由于该部分主要报告检出率进行分析，所以 RQ4 正文暂保持原有表述，未做实质性修改。source：`data/history_knowledge.csv`，但有知识库的攻击类型分类

**其他 Benchmark & 基线对比**（包括 TrxGNNBERT、Blockscan、TxSpector、DeFiScope、DeFort、DeFiRanger 等）： 
相关对比结果在之前文本中已存在，但原始中间数据文件暂未找到，且本次未对上述基线方法重新run。因此未进行更新。

