---
name: setup-terraform
description: Create production-ready Terraform modules for AWS/GCP/Azure with remote state, workspaces, and CI/CD
---

# Setup Terraform

Creates complete Infrastructure as Code with:
- Modular Terraform structure
- Remote state with S3 + DynamoDB locking
- Multi-environment workspaces
- VPC, ECS/EKS, RDS, ElastiCache
- IAM least-privilege roles
- GitHub Actions CI/CD integration

## Usage
```
#setup-terraform <cloud-provider>
```

## Project Structure
```
infrastructure/
├── modules/
│   ├── vpc/
│   ├── ecs/
│   ├── rds/
│   └── redis/
├── environments/
│   ├── dev/
│   ├── staging/
│   └── prod/
├── main.tf
├── variables.tf
├── outputs.tf
└── backend.tf
```

## Core Files

### backend.tf
```hcl
terraform {
  required_version = ">= 1.6"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "{{ PROJECT }}-terraform-state"
    key            = "{{ ENV }}/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "{{ PROJECT }}-terraform-locks"
  }
}
```

### modules/vpc/main.tf
```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "${var.project}-${var.environment}"
  cidr = var.vpc_cidr

  azs             = data.aws_availability_zones.available.names
  private_subnets = var.private_subnet_cidrs
  public_subnets  = var.public_subnet_cidrs
  database_subnets = var.database_subnet_cidrs

  enable_nat_gateway     = true
  single_nat_gateway     = var.environment != "prod"
  enable_dns_hostnames   = true
  enable_dns_support     = true

  enable_flow_log                      = true
  create_flow_log_cloudwatch_iam_role  = true
  create_flow_log_cloudwatch_log_group = true

  tags = local.common_tags
}
```

### modules/rds/main.tf
```hcl
module "db" {
  source  = "terraform-aws-modules/rds/aws"
  version = "~> 6.0"

  identifier = "${var.project}-${var.environment}"

  engine               = "postgres"
  engine_version       = "16"
  instance_class       = var.instance_class
  allocated_storage    = var.allocated_storage
  max_allocated_storage = var.max_allocated_storage

  db_name  = var.db_name
  username = var.db_username
  port     = 5432

  multi_az               = var.environment == "prod"
  db_subnet_group_name   = module.vpc.database_subnet_group
  vpc_security_group_ids = [aws_security_group.rds.id]

  backup_retention_period = var.environment == "prod" ? 30 : 7
  deletion_protection     = var.environment == "prod"
  skip_final_snapshot     = var.environment != "prod"

  performance_insights_enabled = true
  monitoring_interval          = 60

  parameters = [
    { name = "log_connections", value = "1" },
    { name = "log_min_duration_statement", value = "1000" },
  ]

  tags = local.common_tags
}
```

### GitHub Actions CI
```yaml
# .github/workflows/terraform.yml
name: Terraform

on:
  push:
    branches: [main]
    paths: ['infrastructure/**']
  pull_request:
    paths: ['infrastructure/**']

jobs:
  terraform:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
      pull-requests: write

    steps:
      - uses: actions/checkout@v4

      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: us-east-1

      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: "1.6"

      - name: Terraform Format
        run: terraform fmt -check -recursive
        working-directory: infrastructure

      - name: Terraform Init
        run: terraform init
        working-directory: infrastructure/environments/${{ github.ref == 'refs/heads/main' && 'prod' || 'dev' }}

      - name: Terraform Validate
        run: terraform validate

      - name: Terraform Plan
        run: terraform plan -out=tfplan
        id: plan

      - name: Comment PR
        uses: actions/github-script@v7
        if: github.event_name == 'pull_request'
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '```\n${{ steps.plan.outputs.stdout }}\n```'
            })

      - name: Terraform Apply
        if: github.ref == 'refs/heads/main'
        run: terraform apply -auto-approve tfplan
```
