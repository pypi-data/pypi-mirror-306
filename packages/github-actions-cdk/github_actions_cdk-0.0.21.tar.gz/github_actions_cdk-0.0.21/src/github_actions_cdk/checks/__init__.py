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

from .._jsii import *

import constructs as _constructs_77d1e7e8
from .. import Check as _Check_647e0db9


class ExternalActionVersionCheck(
    _Check_647e0db9,
    metaclass=jsii.JSIIMeta,
    jsii_type="github-actions-cdk.checks.ExternalActionVersionCheck",
):
    '''
    :stability: experimental
    '''

    def __init__(self, level: typing.Optional[builtins.str] = None) -> None:
        '''
        :param level: Default error level.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0f7edf69cedaf35125b48c271c406f2fed30a00271f0831dc0448af3060f2cb)
            check_type(argname="argument level", value=level, expected_type=type_hints["level"])
        jsii.create(self.__class__, self, [level])

    @jsii.member(jsii_name="visit")
    def visit(self, node: _constructs_77d1e7e8.IConstruct) -> None:
        '''(experimental) Abstract visit method to be implemented by subclasses, providing the node to check.

        :param node: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc03f910c0bb47df0017b4e962f350e0e4896b3e9084dfe4b0275e218e0b504b)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "visit", [node]))


__all__ = [
    "ExternalActionVersionCheck",
]

publication.publish()

def _typecheckingstub__d0f7edf69cedaf35125b48c271c406f2fed30a00271f0831dc0448af3060f2cb(
    level: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc03f910c0bb47df0017b4e962f350e0e4896b3e9084dfe4b0275e218e0b504b(
    node: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
