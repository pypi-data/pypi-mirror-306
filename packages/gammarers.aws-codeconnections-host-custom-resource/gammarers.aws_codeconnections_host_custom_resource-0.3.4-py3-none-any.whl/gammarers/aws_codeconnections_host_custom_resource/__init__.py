r'''
# AWS CodeConnections Host Custom Resource

[![GitHub](https://img.shields.io/github/license/gammarers/aws-codeconnections-host-custom-resource?style=flat-square)](https://github.com/gammarers/aws-codeconnections-host-custom-resource/blob/main/LICENSE)
[![npm (scoped)](https://img.shields.io/npm/v/@gammarers/aws-codeconnections-host-custom-resource?style=flat-square)](https://www.npmjs.com/package/@gammarers/aws-codeconnections-host-custom-resource)
[![GitHub Workflow Status (branch)](https://img.shields.io/github/actions/workflow/status/gammarers/aws-codeconnections-host-custom-resource/release.yml?branch=main&label=release&style=flat-square)](https://github.com/gammarers/aws-codeconnections-host-custom-resource/actions/workflows/release.yml)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/gammarers/aws-codeconnections-host-custom-resource?sort=semver&style=flat-square)](https://github.com/gammarers/aws-codeconnections-host-custom-resource/releases)

[![View on Construct Hub](https://constructs.dev/badge?package=@gammarers/aws-codeconnections-host-custom-resource)](https://constructs.dev/packages/@gammarers/aws-codeconnections-host-custom-resource)

This AWS CDK Construct provides a custom resource (Lambda Function) to create a connection host for Self-Managed GitLab, which is not yet supported by CloudFormation. Additionally, even after creating the Host and the connection, authentication must be done via a browser.

## Install

### TypeScript

#### install by npm

```shell
npm install @gammarers/aws-codeconnections-host-custom-resource
```

#### install by yarn

```shell
yarn add @gammarers/aws-codeconnections-host-custom-resource
```

### Python

#### install by pip

```shell
pip install gammarers.aws-budgets-notification
```

## Example

```python
import { CodeConnectionsHostCustomResource, CodeConnectionsHostProviderType } from '@gammarers/aws-codeconnections-host-custom-resource';

const codeConnectionsHostCustomResource = new CodeConnectionsHostCustomResource(this, 'CodeConnectionsHost', {
  name: 'gitlab.example.com', // required, connection host name (Minimum length of 1. Maximum length of 64.)
  providerEndpoint: 'https://gitlab.example.com', // required, your provider endpoint (Minimum length of 1. Maximum length of 512.)
  providerType: CodeConnectionsHostProviderType.GIT_LAB_SELF_MANAGED,
});

// get host arn
const hostArn = gitLabSelfManagedConnectionHostCustomResource.findHostArn();

new codeconnections.CfnConnection(this, 'Connection', {
  connectionName: 'example-gitlab-connection',
  hostArn,
});
```

## How to complete (Update a pending connection)

Deploy completed after being configured in EXAMPLE.
At this point, the status is ‘Pending’ as shown below because authentication has not yet been completed.

<img alt="CodeConnection Setup 01" src="images/CodeConnection-Setup-01.png" width="800" />

Select the ‘Connection’ you have created to display the Connection detail screen.

<img alt="CodeConnection Setup 02" src="images/CodeConnection-Setup-02.png" width="800" />

You will see the ‘Pending’ status as follows. Select ‘Update pending connection’.

<img alt="CodeConnection Setup 03" src="images/CodeConnection-Setup-03.png" width="800" />

A screen to enter the Provide personal access token (pat) will be displayed; the pat should be created in the target host environment (only api should be enabled). Enter the pat and select ‘Continue’.

<img alt="CodeConnection Setup 04" src="images/CodeConnection-Setup-04.png" width="500" />

The host authorisation screen will appear as shown below, select ‘Authorise’ (the screen will pop up).

> If you have not logged in, a login screen will be displayed, please log in.

<img alt="CodeConnection Setup 05" src="images/CodeConnection-Setup-05.png" width="800" />

When completed, the status will change to ‘Available’ as follows. This completes all Connection settings.

## License

This project is licensed under the Apache-2.0 License.
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

import aws_cdk.custom_resources as _aws_cdk_custom_resources_ceddda9d
import constructs as _constructs_77d1e7e8


class CodeConnectionsHostCustomResource(
    _aws_cdk_custom_resources_ceddda9d.AwsCustomResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gammarers/aws-codeconnections-host-custom-resource.CodeConnectionsHostCustomResource",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        provider_endpoint: builtins.str,
        provider_type: "CodeConnectionsHostProviderType",
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param name: 
        :param provider_endpoint: 
        :param provider_type: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93e92fc39e37866f7e6881c8a553116ad11f67a1051166fa67f97f695c92329f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CodeConnectionsHostCustomResourceProps(
            name=name, provider_endpoint=provider_endpoint, provider_type=provider_type
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="findHostArn")
    def find_host_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.invoke(self, "findHostArn", []))


@jsii.data_type(
    jsii_type="@gammarers/aws-codeconnections-host-custom-resource.CodeConnectionsHostCustomResourceProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "provider_endpoint": "providerEndpoint",
        "provider_type": "providerType",
    },
)
class CodeConnectionsHostCustomResourceProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        provider_endpoint: builtins.str,
        provider_type: "CodeConnectionsHostProviderType",
    ) -> None:
        '''
        :param name: 
        :param provider_endpoint: 
        :param provider_type: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__784fa6fe7d14609c195c71c179fa9c4b8deffdef65bb91d227c890fbdca7b022)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument provider_endpoint", value=provider_endpoint, expected_type=type_hints["provider_endpoint"])
            check_type(argname="argument provider_type", value=provider_type, expected_type=type_hints["provider_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "provider_endpoint": provider_endpoint,
            "provider_type": provider_type,
        }

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def provider_endpoint(self) -> builtins.str:
        result = self._values.get("provider_endpoint")
        assert result is not None, "Required property 'provider_endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def provider_type(self) -> "CodeConnectionsHostProviderType":
        result = self._values.get("provider_type")
        assert result is not None, "Required property 'provider_type' is missing"
        return typing.cast("CodeConnectionsHostProviderType", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodeConnectionsHostCustomResourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@gammarers/aws-codeconnections-host-custom-resource.CodeConnectionsHostProviderType"
)
class CodeConnectionsHostProviderType(enum.Enum):
    BIT_BUCKET = "BIT_BUCKET"
    GIT_HUB = "GIT_HUB"
    GIT_HUB_ENTERPRISE_SERVER = "GIT_HUB_ENTERPRISE_SERVER"
    GIT_LAB = "GIT_LAB"
    GIT_LAB_SELF_MANAGED = "GIT_LAB_SELF_MANAGED"


@jsii.enum(
    jsii_type="@gammarers/aws-codeconnections-host-custom-resource.ResponseField"
)
class ResponseField(enum.Enum):
    HOST_ARN = "HOST_ARN"


__all__ = [
    "CodeConnectionsHostCustomResource",
    "CodeConnectionsHostCustomResourceProps",
    "CodeConnectionsHostProviderType",
    "ResponseField",
]

publication.publish()

def _typecheckingstub__93e92fc39e37866f7e6881c8a553116ad11f67a1051166fa67f97f695c92329f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    provider_endpoint: builtins.str,
    provider_type: CodeConnectionsHostProviderType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__784fa6fe7d14609c195c71c179fa9c4b8deffdef65bb91d227c890fbdca7b022(
    *,
    name: builtins.str,
    provider_endpoint: builtins.str,
    provider_type: CodeConnectionsHostProviderType,
) -> None:
    """Type checking stubs"""
    pass
