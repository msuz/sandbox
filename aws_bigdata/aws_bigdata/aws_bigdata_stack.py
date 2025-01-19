from aws_cdk import (
    Stack,
    Duration,
    aws_ec2 as ec2,
    aws_rds as rds,
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

    def create_vpc(self) -> ec2.Vpc:
        """VPC を作成するメソッド"""
        return ec2.Vpc(
            self, "BigDataVPC",
            ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16"),
            max_azs=2,  # 2つのAZを使用
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="PrivateSubnet",
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                    cidr_mask=24
                )
            ]
        )

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

    def add_cfn_output(self, name: str, value: str):
        """CloudFormation の出力を追加するメソッド"""
        CfnOutput(self, name, value=value)
