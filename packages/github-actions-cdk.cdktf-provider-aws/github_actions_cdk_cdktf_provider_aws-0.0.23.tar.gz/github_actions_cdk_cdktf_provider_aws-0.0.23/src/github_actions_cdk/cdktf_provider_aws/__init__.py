r'''
[![View on Construct Hub](https://constructs.dev/badge?package=%40github-actions-cdk%2Fcdktf-provider-aws)](https://constructs.dev/packages/@github-actions-cdk/cdktf-provider-aws)

# @github-actions-cdk/cdktf-provider-aws

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

import cdktf_cdktf_provider_aws.iam_role as _cdktf_cdktf_provider_aws_iam_role_0cbe8a87
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="@github-actions-cdk/cdktf-provider-aws.GitHubActionsOpenIdConnectProviderProps",
    jsii_struct_bases=[],
    name_mapping={"thumbprints": "thumbprints"},
)
class GitHubActionsOpenIdConnectProviderProps:
    def __init__(
        self,
        *,
        thumbprints: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Properties for configuring the GitHub Actions OpenID Connect provider.

        :param thumbprints: (experimental) Optional thumbprints to verify GitHub's certificates. Default is the predefined thumbprints.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3710eeda3c9fcd7b95cd5bad44282c48af6e9ff9dba195298e3801917c945fac)
            check_type(argname="argument thumbprints", value=thumbprints, expected_type=type_hints["thumbprints"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if thumbprints is not None:
            self._values["thumbprints"] = thumbprints

    @builtins.property
    def thumbprints(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Optional thumbprints to verify GitHub's certificates.

        Default is the predefined thumbprints.

        :stability: experimental
        '''
        result = self._values.get("thumbprints")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitHubActionsOpenIdConnectProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GitHubActionsRole(
    _cdktf_cdktf_provider_aws_iam_role_0cbe8a87.IamRole,
    metaclass=jsii.JSIIMeta,
    jsii_type="@github-actions-cdk/cdktf-provider-aws.GitHubActionsRole",
):
    '''(experimental) Creates an IAM Role for GitHub Actions workflows using an OpenID Connect provider.

    The role includes policies allowing the assumption of bootstrap roles and access to ECR authorization.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        provider: "IOpenIdConnectProvider",
        inline_policy: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_aws_iam_role_0cbe8a87.IamRoleInlinePolicy, typing.Dict[builtins.str, typing.Any]]]] = None,
        repos: typing.Optional[typing.Sequence[builtins.str]] = None,
        role_name: typing.Optional[builtins.str] = None,
        subject_claims: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Constructs a new instance of ``GitHubActionsRole``.

        :param scope: - The construct scope to define the role within.
        :param id: - The unique identifier for this role.
        :param provider: (experimental) The OpenID Connect provider that GitHub Actions will use to assume this role.
        :param inline_policy: (experimental) Inline policies that define the permissions for the IAM role. This allows configuring the role with specific policies.
        :param repos: (experimental) A list of GitHub repositories that are permitted to assume this role. Each repository should be formatted as ``owner/repo``.
        :param role_name: (experimental) The name for the GitHub Actions IAM role. Default: - "GitHubActionsRole"
        :param subject_claims: (experimental) Additional custom subject claims to allow for the role. Each claim should conform to the format used in GitHub OIDC conditions.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f368ad9e1c006c78397f77b800b7ed7cfb7d365060c0888e49712afb9596227d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GitHubActionsRoleProps(
            provider=provider,
            inline_policy=inline_policy,
            repos=repos,
            role_name=role_name,
            subject_claims=subject_claims,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@github-actions-cdk/cdktf-provider-aws.GitHubActionsRoleProps",
    jsii_struct_bases=[],
    name_mapping={
        "provider": "provider",
        "inline_policy": "inlinePolicy",
        "repos": "repos",
        "role_name": "roleName",
        "subject_claims": "subjectClaims",
    },
)
class GitHubActionsRoleProps:
    def __init__(
        self,
        *,
        provider: "IOpenIdConnectProvider",
        inline_policy: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_aws_iam_role_0cbe8a87.IamRoleInlinePolicy, typing.Dict[builtins.str, typing.Any]]]] = None,
        repos: typing.Optional[typing.Sequence[builtins.str]] = None,
        role_name: typing.Optional[builtins.str] = None,
        subject_claims: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Properties for creating a GitHub Actions IAM role.

        :param provider: (experimental) The OpenID Connect provider that GitHub Actions will use to assume this role.
        :param inline_policy: (experimental) Inline policies that define the permissions for the IAM role. This allows configuring the role with specific policies.
        :param repos: (experimental) A list of GitHub repositories that are permitted to assume this role. Each repository should be formatted as ``owner/repo``.
        :param role_name: (experimental) The name for the GitHub Actions IAM role. Default: - "GitHubActionsRole"
        :param subject_claims: (experimental) Additional custom subject claims to allow for the role. Each claim should conform to the format used in GitHub OIDC conditions.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a19ae08d7542a4acc332750835d37f92fb790d7376f1c5e14830273dd2eb1760)
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument inline_policy", value=inline_policy, expected_type=type_hints["inline_policy"])
            check_type(argname="argument repos", value=repos, expected_type=type_hints["repos"])
            check_type(argname="argument role_name", value=role_name, expected_type=type_hints["role_name"])
            check_type(argname="argument subject_claims", value=subject_claims, expected_type=type_hints["subject_claims"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "provider": provider,
        }
        if inline_policy is not None:
            self._values["inline_policy"] = inline_policy
        if repos is not None:
            self._values["repos"] = repos
        if role_name is not None:
            self._values["role_name"] = role_name
        if subject_claims is not None:
            self._values["subject_claims"] = subject_claims

    @builtins.property
    def provider(self) -> "IOpenIdConnectProvider":
        '''(experimental) The OpenID Connect provider that GitHub Actions will use to assume this role.

        :stability: experimental
        '''
        result = self._values.get("provider")
        assert result is not None, "Required property 'provider' is missing"
        return typing.cast("IOpenIdConnectProvider", result)

    @builtins.property
    def inline_policy(
        self,
    ) -> typing.Optional[typing.List[_cdktf_cdktf_provider_aws_iam_role_0cbe8a87.IamRoleInlinePolicy]]:
        '''(experimental) Inline policies that define the permissions for the IAM role.

        This allows configuring the role with specific policies.

        :stability: experimental
        '''
        result = self._values.get("inline_policy")
        return typing.cast(typing.Optional[typing.List[_cdktf_cdktf_provider_aws_iam_role_0cbe8a87.IamRoleInlinePolicy]], result)

    @builtins.property
    def repos(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of GitHub repositories that are permitted to assume this role.

        Each repository should be formatted as ``owner/repo``.

        :stability: experimental
        '''
        result = self._values.get("repos")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def role_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name for the GitHub Actions IAM role.

        :default: - "GitHubActionsRole"

        :stability: experimental
        '''
        result = self._values.get("role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subject_claims(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Additional custom subject claims to allow for the role.

        Each claim should conform to the format used in GitHub OIDC conditions.

        :stability: experimental
        '''
        result = self._values.get("subject_claims")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitHubActionsRoleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(
    jsii_type="@github-actions-cdk/cdktf-provider-aws.IOpenIdConnectProvider"
)
class IOpenIdConnectProvider(typing_extensions.Protocol):
    '''(experimental) Interface for an OpenID Connect (OIDC) provider that GitHub Actions can use.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="providerArn")
    def provider_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the OIDC provider.

        :stability: experimental
        '''
        ...


class _IOpenIdConnectProviderProxy:
    '''(experimental) Interface for an OpenID Connect (OIDC) provider that GitHub Actions can use.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@github-actions-cdk/cdktf-provider-aws.IOpenIdConnectProvider"

    @builtins.property
    @jsii.member(jsii_name="providerArn")
    def provider_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the OIDC provider.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "providerArn"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IOpenIdConnectProvider).__jsii_proxy_class__ = lambda : _IOpenIdConnectProviderProxy


@jsii.implements(IOpenIdConnectProvider)
class GitHubActionsOpenIdConnectProvider(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@github-actions-cdk/cdktf-provider-aws.GitHubActionsOpenIdConnectProvider",
):
    '''(experimental) Represents an OpenID Connect (OIDC) provider for GitHub Actions.

    This construct creates an IAM OIDC provider that allows GitHub Actions
    to assume roles using web identity federation.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        thumbprints: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Constructs a new instance of ``GitHubActionsOpenIdConnectProvider``.

        :param scope: - The construct scope to define the provider within.
        :param id: - The unique identifier for this provider.
        :param thumbprints: (experimental) Optional thumbprints to verify GitHub's certificates. Default is the predefined thumbprints.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6197172237b968849f5c72a24e1e48a1d3031abab1cc9f29d5c76e5ae7c9c1b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GitHubActionsOpenIdConnectProviderProps(thumbprints=thumbprints)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromGitHubActionsOpenIdConnectProvider")
    @builtins.classmethod
    def from_git_hub_actions_open_id_connect_provider(
        cls,
        scope: _constructs_77d1e7e8.Construct,
    ) -> IOpenIdConnectProvider:
        '''(experimental) Imports an existing GitHub Actions OpenID Connect provider by ARN.

        :param scope: - The construct scope to define the provider within.

        :return: An object that implements ``IOpenIdConnectProvider``.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf60e764df68069cb2a27c3c8a7378c9c6f83045957c4fe37b8a409f9cd31820)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(IOpenIdConnectProvider, jsii.sinvoke(cls, "fromGitHubActionsOpenIdConnectProvider", [scope]))

    @builtins.property
    @jsii.member(jsii_name="providerArn")
    def provider_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the created OpenID Connect provider.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "providerArn"))


__all__ = [
    "GitHubActionsOpenIdConnectProvider",
    "GitHubActionsOpenIdConnectProviderProps",
    "GitHubActionsRole",
    "GitHubActionsRoleProps",
    "IOpenIdConnectProvider",
]

publication.publish()

def _typecheckingstub__3710eeda3c9fcd7b95cd5bad44282c48af6e9ff9dba195298e3801917c945fac(
    *,
    thumbprints: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f368ad9e1c006c78397f77b800b7ed7cfb7d365060c0888e49712afb9596227d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    provider: IOpenIdConnectProvider,
    inline_policy: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_aws_iam_role_0cbe8a87.IamRoleInlinePolicy, typing.Dict[builtins.str, typing.Any]]]] = None,
    repos: typing.Optional[typing.Sequence[builtins.str]] = None,
    role_name: typing.Optional[builtins.str] = None,
    subject_claims: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a19ae08d7542a4acc332750835d37f92fb790d7376f1c5e14830273dd2eb1760(
    *,
    provider: IOpenIdConnectProvider,
    inline_policy: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_aws_iam_role_0cbe8a87.IamRoleInlinePolicy, typing.Dict[builtins.str, typing.Any]]]] = None,
    repos: typing.Optional[typing.Sequence[builtins.str]] = None,
    role_name: typing.Optional[builtins.str] = None,
    subject_claims: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6197172237b968849f5c72a24e1e48a1d3031abab1cc9f29d5c76e5ae7c9c1b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    thumbprints: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf60e764df68069cb2a27c3c8a7378c9c6f83045957c4fe37b8a409f9cd31820(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass
