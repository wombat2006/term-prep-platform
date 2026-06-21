# Terraform — term-prep-platform

Status:
**スキャフォールドのみ** — `.tf` は Phase 0.5（S3 + IAM）から追加予定。

方針の詳細: [docs/IAC.md](../../docs/IAC.md)

---

## 予定モジュール

| モジュール | Phase | 内容 |
|---|---|---|
| `s3-mirror` | 0.5 | corpus / prep バケット |
| `iam-prep-batch` | 0.5 | S3 最小権限ロール |
| `kms-secrets` | 0.5 | KMS + Secrets Manager リソース |
| `ec2-spot` | 3+ ops | launch template · Spot |
| `ecs-prep` | 3+ ops | task definition · EventBridge |
| `api-prep-trigger` | 3+（任意） | API Gateway — HTTP トリガー要件時のみ |
| `prep-notify` | 3+ | Lambda · EventBridge · LINE Webhook URL（Secrets） |
| `ses-notify` | 3+（任意） | SES domain/DKIM — メール必須時のみ |

---

## 使い方（実装後）

```bash
cd infra/terraform/environments/dev
terraform init
terraform plan
terraform apply
```

リモート state（S3 backend + DynamoDB lock）は本番 apply 前に設定する — [docs/IAC.md](../../docs/IAC.md)。
