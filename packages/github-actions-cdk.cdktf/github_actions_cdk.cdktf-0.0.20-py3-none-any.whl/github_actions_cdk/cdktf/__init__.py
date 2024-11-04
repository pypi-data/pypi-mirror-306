r'''
# @github-actions-cdk/cdktf

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING.md](../../CONTRIBUTING.md) for details on how to get involved.

## License

This project is licensed under the MIT License. See the [LICENSE](../../LICENCE) file for more information.
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from ._jsii import *

import constructs as _constructs_77d1e7e8
import github_actions_cdk as _github_actions_cdk_5328d874


class CdktfAdapter(
    _github_actions_cdk_5328d874.Project,
    metaclass=jsii.JSIIMeta,
    jsii_type="@github-actions-cdk/cdktf.CdktfAdapter",
):
    '''(experimental) Adapter to integrate CDKTF (Cloud Development Kit for Terraform) projects with GitHub Actions.

    This class extends the base ``Project`` class and allows for GitHub Actions workflow generation with annotation handling and validation.

    :stability: experimental
    '''

    def __init__(
        self,
        aws_cdk_scope: _constructs_77d1e7e8.Construct,
        *,
        additional_checks: typing.Optional[builtins.bool] = None,
        continue_on_error_annotations: typing.Optional[builtins.bool] = None,
        outdir: typing.Optional[builtins.str] = None,
        skip_validation: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Initializes a new instance of the CdktfAdapter.

        :param aws_cdk_scope: - The scope of the AWS CDK project.
        :param additional_checks: 
        :param continue_on_error_annotations: 
        :param outdir: 
        :param skip_validation: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a07e6c0ea47e438c3e00b7c13060b9628822bacab1806eaa624698ae719aa0d)
            check_type(argname="argument aws_cdk_scope", value=aws_cdk_scope, expected_type=type_hints["aws_cdk_scope"])
        props = _github_actions_cdk_5328d874.ProjectProps(
            additional_checks=additional_checks,
            continue_on_error_annotations=continue_on_error_annotations,
            outdir=outdir,
            skip_validation=skip_validation,
        )

        jsii.create(self.__class__, self, [aws_cdk_scope, props])

    @jsii.member(jsii_name="finalizeSynthesis")
    def _finalize_synthesis(self) -> None:
        '''(experimental) Finalizes the synthesis process by adding annotations based on workflow metadata.

        Adds informational, warning, and error messages to the AWS CDK scope and handles whether synthesis should continue on error annotations.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "finalizeSynthesis", []))

    @jsii.member(jsii_name="handleSynthesisError")
    def _handle_synthesis_error(self, error: typing.Any) -> None:
        '''(experimental) Handles errors occurring during the synthesis process, particularly validation errors.

        Adds validation error messages as annotations to the CDK scope node.

        :param error: - The error encountered during synthesis.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5116fe47e6d12b1d0cd8a6b1f9e9d429fdc1ed0d7fdc243f53e53b5ac47f297)
            check_type(argname="argument error", value=error, expected_type=type_hints["error"])
        return typing.cast(None, jsii.invoke(self, "handleSynthesisError", [error]))


__all__ = [
    "CdktfAdapter",
]

publication.publish()

def _typecheckingstub__4a07e6c0ea47e438c3e00b7c13060b9628822bacab1806eaa624698ae719aa0d(
    aws_cdk_scope: _constructs_77d1e7e8.Construct,
    *,
    additional_checks: typing.Optional[builtins.bool] = None,
    continue_on_error_annotations: typing.Optional[builtins.bool] = None,
    outdir: typing.Optional[builtins.str] = None,
    skip_validation: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5116fe47e6d12b1d0cd8a6b1f9e9d429fdc1ed0d7fdc243f53e53b5ac47f297(
    error: typing.Any,
) -> None:
    """Type checking stubs"""
    pass
