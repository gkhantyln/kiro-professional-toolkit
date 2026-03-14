---
inclusion: fileMatch
fileMatchPattern: "**/*.{tf,tfvars,hcl,pulumi,cdk}"
---

# Infrastructure as Code — İleri Seviye (Terraform / Pulumi / CDK)

## Terraform — Module Yapısı

```hcl
# ✅ Module yapısı
# modules/
#   ├── vpc/
#   ├── eks/
#   ├── rds/
#   └── app-service/
# environments/
#   ├── dev/
#   ├── staging/
#   └── prod/

# modules/rds/main.tf
resource "aws_db_instance" "main" {
  identifier        = "${var.project}-${var.environment}-db"
  engine            = "postgres"
  engine_version    = var.postgres_version
  instance_class    = var.instance_class
  allocated_storage = var.allocated_storage

  db_name  = var.database_name
  username = var.database_username
  password = random_password.db.result  # ❌ hardcode etme

  # ✅ Güvenlik
  storage_encrypted       = true
  deletion_protection     = var.environment == "prod"
  skip_final_snapshot     = var.environment != "prod"
  backup_retention_period = var.environment == "prod" ? 30 : 7
  multi_az                = var.environment == "prod"

  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name

  performance_insights_enabled = true
  monitoring_interval          = 60

  tags = local.common_tags
}

resource "random_password" "db" {
  length  = 32
  special = true
}

# ✅ Secret'ı Secrets Manager'a kaydet
resource "aws_secretsmanager_secret_version" "db" {
  secret_id = aws_secretsmanager_secret.db.id
  secret_string = jsonencode({
    username = var.database_username
    password = random_password.db.result
    host     = aws_db_instance.main.address
    port     = aws_db_instance.main.port
    dbname   = var.database_name
  })
}
```

## Terraform — Variables & Outputs

```hcl
# variables.tf
variable "environment" {
  type        = string
  description = "Deployment environment"
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "instance_class" {
  type        = string
  default     = "db.t3.micro"
  description = "RDS instance class"
}

# locals.tf
locals {
  common_tags = {
    Project     = var.project
    Environment = var.environment
    ManagedBy   = "terraform"
    Owner       = var.team
  }
  is_prod = var.environment == "prod"
}

# outputs.tf
output "db_secret_arn" {
  value       = aws_secretsmanager_secret.db.arn
  description = "ARN of the database credentials secret"
  sensitive   = false  # ARN güvenli, credentials değil
}
```

## Terraform — Remote State + Locking

```hcl
# backend.tf
terraform {
  backend "s3" {
    bucket         = "mycompany-terraform-state"
    key            = "prod/app/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  required_version = ">= 1.6.0"
}
```

## Pulumi — TypeScript

```typescript
import * as aws from "@pulumi/aws";
import * as pulumi from "@pulumi/pulumi";

const config = new pulumi.Config();
const env = pulumi.getStack(); // dev | staging | prod
const isProd = env === "prod";

// ✅ Component resource — reusable
class AppDatabase extends pulumi.ComponentResource {
  public readonly endpoint: pulumi.Output<string>;
  public readonly secretArn: pulumi.Output<string>;

  constructor(name: string, opts?: pulumi.ComponentResourceOptions) {
    super("myapp:index:AppDatabase", name, {}, opts);

    const password = new aws.secretsmanager.Secret(`${name}-password`, {}, { parent: this });

    const db = new aws.rds.Instance(`${name}-db`, {
      engine: "postgres",
      engineVersion: "16.1",
      instanceClass: isProd ? "db.r6g.large" : "db.t3.micro",
      allocatedStorage: isProd ? 100 : 20,
      storageEncrypted: true,
      deletionProtection: isProd,
      backupRetentionPeriod: isProd ? 30 : 7,
      multiAz: isProd,
    }, { parent: this });

    this.endpoint = db.endpoint;
    this.secretArn = password.arn;
    this.registerOutputs({ endpoint: this.endpoint, secretArn: this.secretArn });
  }
}
```

## AWS CDK — TypeScript

```typescript
import * as cdk from "aws-cdk-lib";
import * as ec2 from "aws-cdk-lib/aws-ec2";
import * as rds from "aws-cdk-lib/aws-rds";

export class DatabaseStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props: DatabaseStackProps) {
    super(scope, id, props);

    const isProd = props.env === "prod";

    const db = new rds.DatabaseInstance(this, "Database", {
      engine: rds.DatabaseInstanceEngine.postgres({
        version: rds.PostgresEngineVersion.VER_16,
      }),
      instanceType: isProd
        ? ec2.InstanceType.of(ec2.InstanceClass.R6G, ec2.InstanceSize.LARGE)
        : ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MICRO),
      vpc: props.vpc,
      vpcSubnets: { subnetType: ec2.SubnetType.PRIVATE_ISOLATED },
      storageEncrypted: true,
      deletionProtection: isProd,
      backupRetention: cdk.Duration.days(isProd ? 30 : 7),
      multiAz: isProd,
      removalPolicy: isProd ? cdk.RemovalPolicy.RETAIN : cdk.RemovalPolicy.DESTROY,
    });

    // ✅ Rotation
    db.addRotationSingleUser({ automaticallyAfter: cdk.Duration.days(30) });
  }
}
```

## Kurallar

- State'i remote backend'de tut (S3 + DynamoDB lock)
- Secret'ları hardcode etme — Secrets Manager / Parameter Store kullan
- `deletion_protection = true` prod'da zorunlu
- Module'leri environment'a göre parametrize et
- `common_tags` ile tüm resource'lara tag ekle
- `terraform plan` çıktısını PR'da review et
- `terraform validate` + `tflint` CI'da çalıştır
- Prod ve non-prod için ayrı state dosyaları kullan
