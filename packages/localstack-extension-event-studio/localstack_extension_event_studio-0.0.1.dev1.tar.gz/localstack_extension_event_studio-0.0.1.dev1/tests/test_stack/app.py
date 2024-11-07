import aws_cdk as cdk
from stack import TestStack

app = cdk.App()

TestStack(app, "TestStack", env=cdk.Environment())

app.synth()
