个人项目，作数学建模作业之用。

分析GitHub上的COVID-19数据集，统计以下内容：

- 全球各国

  1. 总确诊人数
  2. 总治愈人数
  3. 总死亡人数
  4. 每日确诊人数
  5. 每日治愈人数
  6. 每日死亡人数

- 重点国家

  应题目要求，选择意大利和美国两个国家。

  - 意大利  疫情防控较好
  - 美国  疫情防控较差

作出以下定义：

- 小拐点(tiny inflection point): 每日确诊人数 - 每日治愈人数
- 大拐点(obvious inflection point): 每日确诊人数 - 每日治愈人数 - 每日死亡人数

- 疫情的四个时期：
  1. 前疫情期(pre epidemic period)  当前拐点 ≈ 0，拐点平缓
  2. 疫情爆发期(the outbreak period)  当前拐点 > 0，拐点上升
  3. 全民抗疫期(the resistance period) 当前拐点 > 0，拐点下降
  4. 后疫情期(post epidemic period)  当前拐点 < 0，拐点上升或平缓