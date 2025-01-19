from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    CfnOutput,
)
from constructs import Construct

class AwsBigdataStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # VPC を作成
        self.vpc = self.create_vpc()
        self.add_cfn_output("BigDataVPCId", self.vpc.vpc_id)

        # プライベートサブネットを取得
        self.private_subnet = self.get_private_subnet(self.vpc)
        self.add_cfn_output("PrivateSubnetId", self.private_subnet.subnet_id)

    def create_vpc(self) -> ec2.Vpc:
        """VPC を作成するメソッド"""
        return ec2.Vpc(
            self, "BigDataVPC",
            ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16"),
            max_azs=1,  # シングルAZ
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="PrivateSubnet",
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,  # 完全プライベート（NATなし）
                    cidr_mask=24
                )
            ]
        )

    def get_private_subnet(self, vpc: ec2.Vpc) -> ec2.Subnet:
        """プライベートサブネットを取得するメソッド"""
        return vpc.isolated_subnets[0] # エラー: vpc.private_subnets[0]


    def add_cfn_output(self, name: str, value: str):
        """CloudFormation の出力を追加するヘルパーメソッド"""
        from aws_cdk import CfnOutput
        CfnOutput(self, name, value=value)
