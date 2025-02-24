from aws_cdk import (
    Stack,
    Duration,
    aws_ec2 as ec2,
    aws_rds as rds,
    aws_iam as iam,
    aws_secretsmanager as secretsmanager,
    CfnOutput,
)
from constructs import Construct

class AwsBigdataStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # VPC を作成
        self.vpc = self.create_vpc()
        self.add_cfn_output("BigDataVPCId", self.vpc.vpc_id)

        # プライベートサブネットを取得（異なる AZ に 2 つ作成）
        self.private_subnets = self.get_private_subnets(self.vpc)
        self.add_cfn_output("PrivateSubnet1Id", self.private_subnets[0].subnet_id)
        self.add_cfn_output("PrivateSubnet2Id", self.private_subnets[1].subnet_id)

        # Aurora MySQL クラスターを作成
        self.aurora_cluster = self.create_aurora_cluster()
        self.add_cfn_output("AuroraClusterEndpoint", self.aurora_cluster.cluster_endpoint.hostname)

        # 作業用EC2インスタンスを作成
        self.work_instance = self.create_work_instance()
        self.add_cfn_output("WorkInstancePrivateIp", self.work_instance.instance_private_ip)

    def create_vpc(self) -> ec2.Vpc:
        """パブリックサブネットなし、VPC エンドポイントを利用"""
        vpc = ec2.Vpc(
            self, "BigDataVPC",
            ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16"),
            max_azs=2,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="PrivateSubnet",
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,  # NATなしのプライベートサブネット
                    cidr_mask=24
                )
            ]
        )

        # VPC エンドポイントの追加（SSM 用）
        vpc.add_interface_endpoint(
            "SSMEndpoint",
            service=ec2.InterfaceVpcEndpointAwsService.SSM
        )
        vpc.add_interface_endpoint(
            "EC2MessagesEndpoint",
            service=ec2.InterfaceVpcEndpointAwsService.EC2_MESSAGES
        )
        vpc.add_interface_endpoint(
            "SSMMessagesEndpoint",
            service=ec2.InterfaceVpcEndpointAwsService.SSM_MESSAGES
        )

        return vpc

    def get_private_subnets(self, vpc: ec2.Vpc) -> list:
        """異なる AZ の 2 つのプライベートサブネットを取得するメソッド"""
        return vpc.isolated_subnets[:2]  # 2つの AZ に配置

    def create_aurora_cluster(self) -> rds.DatabaseCluster:
        """Aurora MySQL クラスターを作成するメソッド"""
        security_group = ec2.SecurityGroup(
            self, "AuroraSecurityGroup",
            vpc=self.vpc,
            description="Security group for Aurora MySQL",
        )

        credentials = rds.Credentials.from_generated_secret("admin")

        cluster = rds.DatabaseCluster(
            self, "AuroraMySQLCluster",
            engine=rds.DatabaseClusterEngine.aurora_mysql(version=rds.AuroraMysqlEngineVersion.VER_3_05_2),
            instance_identifier_base="aurora-instance",
            credentials=credentials,
            security_groups=[security_group],
            default_database_name="aws_bigdata",
            writer=rds.ClusterInstance.provisioned(
                "AuroraWriter",
                instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE4_GRAVITON, ec2.InstanceSize.MEDIUM),
            ),
            readers=[],  # 読み取り専用レプリカなし
            vpc=self.vpc,
            vpc_subnets=ec2.SubnetSelection(subnets=self.private_subnets),  # Aurora クラスターのサブネット指定
            backup=rds.BackupProps(retention=Duration.days(1)),
        )

        return cluster

    def create_work_instance(self) -> ec2.Instance:
        """作業用EC2インスタンスを作成するメソッド"""
        work_sg = ec2.SecurityGroup(
            self, "WorkInstanceSecurityGroup",
            vpc=self.vpc,
            description="Security group for Work Instance",
        )

        # Aurora へのアクセスを許可
        self.aurora_cluster.connections.allow_from(work_sg, ec2.Port.tcp(3306), "Allow MySQL access from Work Instance")

        # IAM ロールを作成（SSM 用）
        work_role = iam.Role(
            self, "WorkInstanceRole",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com")
        )

        # SSM のポリシーをアタッチ
        work_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"))

        # インスタンスプロファイルを作成
        work_instance = ec2.Instance(
            self, "WorkInstance",
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MICRO),
            machine_image=ec2.MachineImage.latest_amazon_linux(),
            vpc=self.vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED),
            security_group=work_sg,
            role=work_role,  # IAM ロールを指定
        )

        return work_instance

    def add_cfn_output(self, name: str, value: str):
        """CloudFormation の出力を追加するメソッド"""
        CfnOutput(self, name, value=value)
