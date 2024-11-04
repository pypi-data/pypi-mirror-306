import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "github-actions-cdk.aws-cdk",
    "version": "0.0.20",
    "description": "A TypeScript library for building GitHub Actions pipelines specifically for AWS CDK applications. This library allows developers to define, structure, and automate CI/CD workflows tailored to CDK projects, making it easy to deploy infrastructure through GitHub Actions in a type-safe and modular way.",
    "license": "MIT",
    "url": "https://github.com/hupe1980/github-actions-cdk.git",
    "long_description_content_type": "text/markdown",
    "author": "hupe1980",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/hupe1980/github-actions-cdk.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "github_actions_cdk.aws_cdk",
        "github_actions_cdk.aws_cdk._jsii"
    ],
    "package_data": {
        "github_actions_cdk.aws_cdk._jsii": [
            "aws-cdk@0.0.20.jsii.tgz"
        ],
        "github_actions_cdk.aws_cdk": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.164.1, <3.0.0",
        "constructs>=10.4.2, <11.0.0",
        "github-actions-cdk>=0.0.20, <0.0.21",
        "jsii>=1.104.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard>=2.13.3,<4.3.0"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
