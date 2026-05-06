# KhmerX P2P 砍头息利率矩阵与试算接口（V1）

## 1. 利率矩阵规则（普通用户）

| 期限 | A级 | B级 | C级 | D级 |
|---|---:|---:|---:|---:|
| 7天 | 8% | 9% | 10% | 12% |
| 14天 | 15% | 17% | 18% | 20% |
| 30天 | 25% | 28% | 30% | 35% |

## 2. PostgreSQL 建表与种子数据

文件：[khmerx-interest-rate-matrix.sql](file:///d:/projects/khmerx/docs/khmerx-interest-rate-matrix.sql)

## 3. 砍头息试算口径

输入：本金 `principal`、期限 `term_days`、名义利率 `rate_percent`。

- 利息：`interest = principal * rate_percent / 100`
- 到手：`received_amount = principal - interest`
- 到期还：`repay_amount = principal`
- 实际利率：`real_rate_percent = interest / received_amount * 100`
- 年化 APR：`apr_percent = interest / received_amount * (365 / term_days) * 100`

金额统一四舍五入到 2 位小数。

## 4. 试算示例：借 100 美金

| 期限 | 等级 | 利率 | 利息 | 到手 | 到期还 |
|---|---|---:|---:|---:|---:|
| 7天 | C | 10% | $10 | $90 | $100 |
| 14天 | C | 18% | $18 | $82 | $100 |
| 30天 | C | 30% | $30 | $70 | $100 |

## 5. API：POST `/p2p/calculate`

请求：

```json
{
  "amount": 100,
  "term_days": 7,
  "credit_level": "C"
}
```

返回：

```json
{
  "principal": 100,
  "term_days": 7,
  "rate_percent": 10,
  "interest": 10,
  "received_amount": 90,
  "repay_amount": 100,
  "real_rate_percent": 11.11,
  "apr_percent": 579.37,
  "mode": "cut_interest"
}
```

约束：

- `term_days` 仅支持 `7/14/30`
- `credit_level` 仅支持 `A/B/C/D`

