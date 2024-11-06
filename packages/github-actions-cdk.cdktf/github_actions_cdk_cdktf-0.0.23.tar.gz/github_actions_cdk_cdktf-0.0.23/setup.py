import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "github-actions-cdk.cdktf",
    "version": "0.0.23",
    "description": "A TypeScript library for creating and managing GitHub Actions workflows using Constructs, enabling type-safe and modular CI/CD automation.",
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
        "github_actions_cdk.cdktf",
        "github_actions_cdk.cdktf._jsii"
    ],
    "package_data": {
        "github_actions_cdk.cdktf._jsii": [
            "cdktf@0.0.23.jsii.tgz"
        ],
        "github_actions_cdk.cdktf": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "cdktf>=0.20.9, <0.21.0",
        "constructs>=10.4.2, <11.0.0",
        "github-actions-cdk>=0.0.23, <0.0.24",
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
