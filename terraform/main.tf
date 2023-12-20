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
      {"name": "DB_HOST", "value": "${var.database_ip}"},
      {"name": "DB_NAME", "value": "${var.database_name}"},
      {"name": "DB_PASSWORD", "value": "${var.database_password}"},
      {"name": "DB_PORT", "value": "${var.database_port}"},
      {"name": "DB_USERNAME", "value": "${var.database_username}"}
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

resource "aws_ecs_service" "c9-ladybirds-pipeline" {
  name            = "c9-ladybirds-pipeline"
  cluster         = "c9-ecs-cluster"
  task_definition = aws_ecs_task_definition.c9-ladybirds-pipeline-task.arn
  desired_count   = 1
  launch_type     = "FARGATE"
  force_new_deployment = true 
  depends_on = [aws_ecs_task_definition.c9-ladybirds-pipeline-task]

network_configuration {
    security_groups = ["sg-020697b6514174b72"]
    subnets         = ["subnet-0d0b16e76e68cf51b","subnet-081c7c419697dec52","subnet-02a00c7be52b00368"]
    assign_public_ip = true
  }
}



resource "aws_ecs_task_definition" "c9-ladybirds-load-old-data-task" {
  family                   = "c9-ladybirds-load-old-data-task"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 1024
  memory                   = 2048
  execution_role_arn       = "${data.aws_iam_role.ecs_task_execution_role.arn}"
  container_definitions    = <<TASK_DEFINITION
[
  {
    "environment": [
      {"name": "DB_HOST", "value": "${var.database_ip}"},
      {"name": "DB_NAME", "value": "${var.database_name}"},
      {"name": "DB_PASSWORD", "value": "${var.database_password}"},
      {"name": "DB_PORT", "value": "${var.database_port}"},
      {"name": "DB_USERNAME", "value": "${var.database_username}"},
      {"name": "AWS_ACCESS_KEY_ID", "value": "${var.aws_access_key_id}"},
      {"name": "AWS_SECRET_ACCESS_KEY", "value": "${var.aws_secret_access_key}"}
    ],
    "name": "c9-ladybirds-load-old-data",
    "image": "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c9-ladybirds-load-old-data:latest",
    "essential": true
  }
]
TASK_DEFINITION

  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture        = "X86_64"
  }
}