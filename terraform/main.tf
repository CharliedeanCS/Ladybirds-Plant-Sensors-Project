terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region  = "eu-west-2"
}

data "aws_iam_role" "ecs_task_execution_role" {
  name = "ecsTaskExecutionRole"
}

resource "aws_ecs_task_definition" "c9-ladybirds-pipeline-task" {
  family                   = "c9-ladybirds-pipeline-task"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 1024
  memory                   = 2048
  execution_role_arn       = "${data.aws_iam_role.ecs_task_execution_role.arn}"
  container_definitions    = <<TASK_DEFINITION
[
  {
    "environment": [
      {"name": "DATABASE_IP", "value": "${var.database_ip}"},
      {"name": "DATABASE_NAME", "value": "${var.database_name}"},
      {"name": "DATABASE_PASSWORD", "value": "${var.database_password}"},
      {"name": "DATABASE_PORT", "value": "${var.database_port}"},
      {"name": "DATABASE_USERNAME", "value": "${var.database_username}"}
    ],
    "name": "c9-ladybirds-pipeline",
    "image": "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c9-ladybirds-pipeline:latest",
    "essential": true
  }
]
TASK_DEFINITION

  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture        = "X86_64"
  }
}

resource "null_resource" "c9-ladybirds-pipeline-task" {
  depends_on = [
    aws_ecs_task_definition.c9-ladybirds-pipeline-task    
  ]

  provisioner "local-exec" {
    command = <<EOF
    aws ecs run-task \
      --region eu-west-2 \
      --cluster arn:aws:ecs:eu-west-2:129033205317:cluster/c9-ecs-cluster \
      --task-definition c9-ladybirds-pipeline-task \
      --count 1 --launch-type FARGATE \
      --network-configuration '{    
      "awsvpcConfiguration": {
      "assignPublicIp":"ENABLED",
      "subnets": ["subnet-0d0b16e76e68cf51b","subnet-081c7c419697dec52","subnet-02a00c7be52b00368"]
      }
      }'
EOF
  }
}