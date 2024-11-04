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
from .. import (
    Action as _Action_64902b3f, CommonActionProps as _CommonActionProps_7122e708
)


class AwsCloudFormationGitHubDeployV1(
    _Action_64902b3f,
    metaclass=jsii.JSIIMeta,
    jsii_type="github-actions-cdk.actions.AwsCloudFormationGitHubDeployV1",
):
    '''(experimental) Deploy CloudFormation Stack action for GitHub Actions workflows.

    :stability: experimental
    :remarks:

    Allows deployment of a CloudFormation stack with configuration options for
    capabilities, parameters, rollback behavior, and notification settings.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        stack_name: builtins.str,
        template: builtins.str,
        capabilities: typing.Optional[builtins.str] = None,
        change_set_name: typing.Optional[builtins.str] = None,
        disable_rollback: typing.Optional[builtins.str] = None,
        http_proxy: typing.Optional[builtins.str] = None,
        no_delete_failed_changeset: typing.Optional[builtins.str] = None,
        no_execute_changeset: typing.Optional[builtins.str] = None,
        no_fail_on_empty_changeset: typing.Optional[builtins.str] = None,
        notification_arns: typing.Optional[builtins.str] = None,
        parameter_overrides: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[builtins.str] = None,
        termination_protection: typing.Optional[builtins.str] = None,
        timeout_in_minutes: typing.Optional[jsii.Number] = None,
        version: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Initializes a new instance of the CloudFormation Deploy action.

        :param scope: - The scope in which to define this construct.
        :param id: - Unique identifier for the action.
        :param stack_name: (experimental) The name of the CloudFormation stack.
        :param template: (experimental) Path or URL to the CloudFormation template.
        :param capabilities: (experimental) Comma-delimited list of template capabilities to acknowledge. Default: "CAPABILITY_IAM"
        :param change_set_name: (experimental) Name of the change set to create. Default: "-CS"
        :param disable_rollback: (experimental) Disable rollback if stack creation fails. Default: "0"
        :param http_proxy: (experimental) Proxy for AWS SDK agent.
        :param no_delete_failed_changeset: (experimental) Skip deletion of failed change sets. Default: "0"
        :param no_execute_changeset: (experimental) Set to skip executing the change set for review. Default: "0"
        :param no_fail_on_empty_changeset: (experimental) Skip failure if the change set is empty. Default: "0"
        :param notification_arns: (experimental) Comma-delimited list of SNS topic ARNs for stack-related events.
        :param parameter_overrides: (experimental) Parameters to override in the stack inputs.
        :param role_arn: (experimental) ARN of IAM role for CloudFormation actions.
        :param tags: (experimental) Key-value pairs as JSON for stack tags.
        :param termination_protection: (experimental) Enable termination protection for the stack. Default: "0"
        :param timeout_in_minutes: (experimental) Timeout for stack creation in minutes.
        :param version: (experimental) Specifies the version of the action to use.
        :param name: (experimental) Display name for the action, shown in GitHub workflow logs for better readability.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f33009cee36a7c9ceccab9957a36ae5b2f05c84cc7915b65aec817c79c1a847d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AwsCloudFormationGitHubDeployV1Props(
            stack_name=stack_name,
            template=template,
            capabilities=capabilities,
            change_set_name=change_set_name,
            disable_rollback=disable_rollback,
            http_proxy=http_proxy,
            no_delete_failed_changeset=no_delete_failed_changeset,
            no_execute_changeset=no_execute_changeset,
            no_fail_on_empty_changeset=no_fail_on_empty_changeset,
            notification_arns=notification_arns,
            parameter_overrides=parameter_overrides,
            role_arn=role_arn,
            tags=tags,
            termination_protection=termination_protection,
            timeout_in_minutes=timeout_in_minutes,
            version=version,
            name=name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="IDENTIFIER")
    def IDENTIFIER(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "IDENTIFIER"))

    @builtins.property
    @jsii.member(jsii_name="outputs")
    def outputs(self) -> "AwsCloudFormationGitHubDeployV1Outputs":
        '''(experimental) Retrieves outputs of the CloudFormation Deploy action.

        :return: ``AwsCloudFormationGitHubDeployV1Outputs`` with the ``stackId`` and additional stack outputs.

        :stability: experimental
        '''
        return typing.cast("AwsCloudFormationGitHubDeployV1Outputs", jsii.get(self, "outputs"))

    @builtins.property
    @jsii.member(jsii_name="stackName")
    def stack_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "stackName"))

    @builtins.property
    @jsii.member(jsii_name="template")
    def template(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "template"))

    @builtins.property
    @jsii.member(jsii_name="capabilities")
    def capabilities(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "capabilities"))

    @builtins.property
    @jsii.member(jsii_name="changeSetName")
    def change_set_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "changeSetName"))

    @builtins.property
    @jsii.member(jsii_name="disableRollback")
    def disable_rollback(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "disableRollback"))

    @builtins.property
    @jsii.member(jsii_name="httpProxy")
    def http_proxy(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpProxy"))

    @builtins.property
    @jsii.member(jsii_name="noDeleteFailedChangeset")
    def no_delete_failed_changeset(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "noDeleteFailedChangeset"))

    @builtins.property
    @jsii.member(jsii_name="noExecuteChangeset")
    def no_execute_changeset(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "noExecuteChangeset"))

    @builtins.property
    @jsii.member(jsii_name="noFailOnEmptyChangeset")
    def no_fail_on_empty_changeset(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "noFailOnEmptyChangeset"))

    @builtins.property
    @jsii.member(jsii_name="notificationArns")
    def notification_arns(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notificationArns"))

    @builtins.property
    @jsii.member(jsii_name="parameterOverrides")
    def parameter_overrides(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parameterOverrides"))

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArn"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="terminationProtection")
    def termination_protection(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "terminationProtection"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInMinutes")
    def timeout_in_minutes(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInMinutes"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "version"))


@jsii.data_type(
    jsii_type="github-actions-cdk.actions.AwsCloudFormationGitHubDeployV1Outputs",
    jsii_struct_bases=[],
    name_mapping={"stack_id": "stackId"},
)
class AwsCloudFormationGitHubDeployV1Outputs:
    def __init__(self, *, stack_id: builtins.str) -> None:
        '''(experimental) Output structure for the CloudFormation Deploy action.

        :param stack_id: (experimental) The ID of the deployed CloudFormation stack.

        :stability: experimental
        :remarks:

        This interface defines the specific outputs provided by the CloudFormation
        Deploy action, including the ``stackId`` which is the identifier of the deployed stack.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9be8722b9c2c30737bd11aa1e091049660b5489c48cc4ccecdd739db5ee974db)
            check_type(argname="argument stack_id", value=stack_id, expected_type=type_hints["stack_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "stack_id": stack_id,
        }

    @builtins.property
    def stack_id(self) -> builtins.str:
        '''(experimental) The ID of the deployed CloudFormation stack.

        :stability: experimental
        '''
        result = self._values.get("stack_id")
        assert result is not None, "Required property 'stack_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsCloudFormationGitHubDeployV1Outputs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="github-actions-cdk.actions.AwsCloudFormationGitHubDeployV1Props",
    jsii_struct_bases=[_CommonActionProps_7122e708],
    name_mapping={
        "name": "name",
        "stack_name": "stackName",
        "template": "template",
        "capabilities": "capabilities",
        "change_set_name": "changeSetName",
        "disable_rollback": "disableRollback",
        "http_proxy": "httpProxy",
        "no_delete_failed_changeset": "noDeleteFailedChangeset",
        "no_execute_changeset": "noExecuteChangeset",
        "no_fail_on_empty_changeset": "noFailOnEmptyChangeset",
        "notification_arns": "notificationArns",
        "parameter_overrides": "parameterOverrides",
        "role_arn": "roleArn",
        "tags": "tags",
        "termination_protection": "terminationProtection",
        "timeout_in_minutes": "timeoutInMinutes",
        "version": "version",
    },
)
class AwsCloudFormationGitHubDeployV1Props(_CommonActionProps_7122e708):
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        stack_name: builtins.str,
        template: builtins.str,
        capabilities: typing.Optional[builtins.str] = None,
        change_set_name: typing.Optional[builtins.str] = None,
        disable_rollback: typing.Optional[builtins.str] = None,
        http_proxy: typing.Optional[builtins.str] = None,
        no_delete_failed_changeset: typing.Optional[builtins.str] = None,
        no_execute_changeset: typing.Optional[builtins.str] = None,
        no_fail_on_empty_changeset: typing.Optional[builtins.str] = None,
        notification_arns: typing.Optional[builtins.str] = None,
        parameter_overrides: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[builtins.str] = None,
        termination_protection: typing.Optional[builtins.str] = None,
        timeout_in_minutes: typing.Optional[jsii.Number] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Configuration properties for the CloudFormation Deploy action in a GitHub Actions workflow.

        :param name: (experimental) Display name for the action, shown in GitHub workflow logs for better readability.
        :param stack_name: (experimental) The name of the CloudFormation stack.
        :param template: (experimental) Path or URL to the CloudFormation template.
        :param capabilities: (experimental) Comma-delimited list of template capabilities to acknowledge. Default: "CAPABILITY_IAM"
        :param change_set_name: (experimental) Name of the change set to create. Default: "-CS"
        :param disable_rollback: (experimental) Disable rollback if stack creation fails. Default: "0"
        :param http_proxy: (experimental) Proxy for AWS SDK agent.
        :param no_delete_failed_changeset: (experimental) Skip deletion of failed change sets. Default: "0"
        :param no_execute_changeset: (experimental) Set to skip executing the change set for review. Default: "0"
        :param no_fail_on_empty_changeset: (experimental) Skip failure if the change set is empty. Default: "0"
        :param notification_arns: (experimental) Comma-delimited list of SNS topic ARNs for stack-related events.
        :param parameter_overrides: (experimental) Parameters to override in the stack inputs.
        :param role_arn: (experimental) ARN of IAM role for CloudFormation actions.
        :param tags: (experimental) Key-value pairs as JSON for stack tags.
        :param termination_protection: (experimental) Enable termination protection for the stack. Default: "0"
        :param timeout_in_minutes: (experimental) Timeout for stack creation in minutes.
        :param version: (experimental) Specifies the version of the action to use.

        :stability: experimental
        :remarks: Defines various options for deploying a CloudFormation stack, including stack configuration, parameters, and rollback options.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a728f859f09227f2f94bce8cb1caca1952b0ef45f0b144edf9fda98c10f9de6)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument stack_name", value=stack_name, expected_type=type_hints["stack_name"])
            check_type(argname="argument template", value=template, expected_type=type_hints["template"])
            check_type(argname="argument capabilities", value=capabilities, expected_type=type_hints["capabilities"])
            check_type(argname="argument change_set_name", value=change_set_name, expected_type=type_hints["change_set_name"])
            check_type(argname="argument disable_rollback", value=disable_rollback, expected_type=type_hints["disable_rollback"])
            check_type(argname="argument http_proxy", value=http_proxy, expected_type=type_hints["http_proxy"])
            check_type(argname="argument no_delete_failed_changeset", value=no_delete_failed_changeset, expected_type=type_hints["no_delete_failed_changeset"])
            check_type(argname="argument no_execute_changeset", value=no_execute_changeset, expected_type=type_hints["no_execute_changeset"])
            check_type(argname="argument no_fail_on_empty_changeset", value=no_fail_on_empty_changeset, expected_type=type_hints["no_fail_on_empty_changeset"])
            check_type(argname="argument notification_arns", value=notification_arns, expected_type=type_hints["notification_arns"])
            check_type(argname="argument parameter_overrides", value=parameter_overrides, expected_type=type_hints["parameter_overrides"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument termination_protection", value=termination_protection, expected_type=type_hints["termination_protection"])
            check_type(argname="argument timeout_in_minutes", value=timeout_in_minutes, expected_type=type_hints["timeout_in_minutes"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "stack_name": stack_name,
            "template": template,
        }
        if name is not None:
            self._values["name"] = name
        if capabilities is not None:
            self._values["capabilities"] = capabilities
        if change_set_name is not None:
            self._values["change_set_name"] = change_set_name
        if disable_rollback is not None:
            self._values["disable_rollback"] = disable_rollback
        if http_proxy is not None:
            self._values["http_proxy"] = http_proxy
        if no_delete_failed_changeset is not None:
            self._values["no_delete_failed_changeset"] = no_delete_failed_changeset
        if no_execute_changeset is not None:
            self._values["no_execute_changeset"] = no_execute_changeset
        if no_fail_on_empty_changeset is not None:
            self._values["no_fail_on_empty_changeset"] = no_fail_on_empty_changeset
        if notification_arns is not None:
            self._values["notification_arns"] = notification_arns
        if parameter_overrides is not None:
            self._values["parameter_overrides"] = parameter_overrides
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if tags is not None:
            self._values["tags"] = tags
        if termination_protection is not None:
            self._values["termination_protection"] = termination_protection
        if timeout_in_minutes is not None:
            self._values["timeout_in_minutes"] = timeout_in_minutes
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Display name for the action, shown in GitHub workflow logs for better readability.

        :stability: experimental

        Example::

            "Checkout Repository"
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stack_name(self) -> builtins.str:
        '''(experimental) The name of the CloudFormation stack.

        :stability: experimental
        '''
        result = self._values.get("stack_name")
        assert result is not None, "Required property 'stack_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def template(self) -> builtins.str:
        '''(experimental) Path or URL to the CloudFormation template.

        :stability: experimental
        '''
        result = self._values.get("template")
        assert result is not None, "Required property 'template' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def capabilities(self) -> typing.Optional[builtins.str]:
        '''(experimental) Comma-delimited list of template capabilities to acknowledge.

        :default: "CAPABILITY_IAM"

        :stability: experimental
        '''
        result = self._values.get("capabilities")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def change_set_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the change set to create.

        :default: "-CS"

        :stability: experimental
        '''
        result = self._values.get("change_set_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_rollback(self) -> typing.Optional[builtins.str]:
        '''(experimental) Disable rollback if stack creation fails.

        :default: "0"

        :stability: experimental
        '''
        result = self._values.get("disable_rollback")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_proxy(self) -> typing.Optional[builtins.str]:
        '''(experimental) Proxy for AWS SDK agent.

        :stability: experimental
        '''
        result = self._values.get("http_proxy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def no_delete_failed_changeset(self) -> typing.Optional[builtins.str]:
        '''(experimental) Skip deletion of failed change sets.

        :default: "0"

        :stability: experimental
        '''
        result = self._values.get("no_delete_failed_changeset")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def no_execute_changeset(self) -> typing.Optional[builtins.str]:
        '''(experimental) Set to skip executing the change set for review.

        :default: "0"

        :stability: experimental
        '''
        result = self._values.get("no_execute_changeset")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def no_fail_on_empty_changeset(self) -> typing.Optional[builtins.str]:
        '''(experimental) Skip failure if the change set is empty.

        :default: "0"

        :stability: experimental
        '''
        result = self._values.get("no_fail_on_empty_changeset")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_arns(self) -> typing.Optional[builtins.str]:
        '''(experimental) Comma-delimited list of SNS topic ARNs for stack-related events.

        :stability: experimental
        '''
        result = self._values.get("notification_arns")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameter_overrides(self) -> typing.Optional[builtins.str]:
        '''(experimental) Parameters to override in the stack inputs.

        :stability: experimental
        '''
        result = self._values.get("parameter_overrides")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) ARN of IAM role for CloudFormation actions.

        :stability: experimental
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[builtins.str]:
        '''(experimental) Key-value pairs as JSON for stack tags.

        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def termination_protection(self) -> typing.Optional[builtins.str]:
        '''(experimental) Enable termination protection for the stack.

        :default: "0"

        :stability: experimental
        '''
        result = self._values.get("termination_protection")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout_in_minutes(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Timeout for stack creation in minutes.

        :stability: experimental
        '''
        result = self._values.get("timeout_in_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies the version of the action to use.

        :stability: experimental
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsCloudFormationGitHubDeployV1Props(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CheckoutV4(
    _Action_64902b3f,
    metaclass=jsii.JSIIMeta,
    jsii_type="github-actions-cdk.actions.CheckoutV4",
):
    '''(experimental) Checkout action for GitHub Actions workflows, configuring a Git repository checkout.

    :stability: experimental
    :remarks:

    This class allows configuration of the Checkout action, supporting
    additional parameters for authentication, repository reference, and
    clone behavior.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        clean: typing.Optional[builtins.bool] = None,
        fetch_depth: typing.Optional[jsii.Number] = None,
        fetch_tags: typing.Optional[builtins.bool] = None,
        filter: typing.Optional[builtins.str] = None,
        github_server_url: typing.Optional[builtins.str] = None,
        lfs: typing.Optional[builtins.bool] = None,
        path: typing.Optional[builtins.str] = None,
        persist_credentials: typing.Optional[builtins.bool] = None,
        ref: typing.Optional[builtins.str] = None,
        repository: typing.Optional[builtins.str] = None,
        set_safe_directory: typing.Optional[builtins.bool] = None,
        show_progress: typing.Optional[builtins.bool] = None,
        sparse_checkout: typing.Optional[typing.Sequence[builtins.str]] = None,
        sparse_checkout_cone_mode: typing.Optional[builtins.bool] = None,
        ssh_key: typing.Optional[builtins.str] = None,
        ssh_known_hosts: typing.Optional[builtins.str] = None,
        ssh_strict: typing.Optional[builtins.bool] = None,
        ssh_user: typing.Optional[builtins.str] = None,
        submodules: typing.Optional[typing.Union[builtins.bool, builtins.str]] = None,
        token: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Initializes a new instance of the Checkout action.

        :param scope: - The scope in which to define this construct.
        :param id: - Unique identifier for the action.
        :param clean: (experimental) Specifies if ``git clean`` and ``git reset`` are run before fetching. Default: true
        :param fetch_depth: (experimental) Number of commits to fetch (``0`` for full history). Default: 1
        :param fetch_tags: (experimental) Fetches tags if ``fetchDepth`` is greater than ``0``. Default: false
        :param filter: (experimental) A filter for partially cloning the repository.
        :param github_server_url: (experimental) Base URL for cloning from GitHub instance.
        :param lfs: (experimental) Downloads Git LFS files. Default: false
        :param path: (experimental) Directory under ``$GITHUB_WORKSPACE`` where the repository is checked out.
        :param persist_credentials: (experimental) Determines if credentials should persist in the local git configuration. Default: true
        :param ref: (experimental) The branch, tag, or SHA to checkout. Defaults to the triggering event's reference or SHA, or the default branch if unspecified.
        :param repository: (experimental) Repository name with owner, in the format ``owner/repo``. Default: github.repository
        :param set_safe_directory: (experimental) Adds the repository path to ``safe.directory`` in Git global config. Default: true
        :param show_progress: (experimental) Displays fetch progress in logs. Default: true
        :param sparse_checkout: (experimental) Patterns for sparse checkout.
        :param sparse_checkout_cone_mode: (experimental) Enables cone mode during sparse checkout. Default: true
        :param ssh_key: (experimental) SSH key for authenticated Git commands.
        :param ssh_known_hosts: (experimental) SSH hosts to add to the configuration, retrieved via ``ssh-keyscan``.
        :param ssh_strict: (experimental) Enables or disables strict host key checking for SSH. Default: true
        :param ssh_user: (experimental) Username for SSH host connection. Default: "git"
        :param submodules: (experimental) Determines if submodules should be checked out. Default: false
        :param token: (experimental) Personal Access Token (PAT) used for authenticated Git commands. Default: github.token
        :param version: (experimental) Specifies the version of the action to use.
        :param name: (experimental) Display name for the action, shown in GitHub workflow logs for better readability.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea038e71ccd09ea5713bc2dfca9f90de69d57ba876065a9b834ff5b9b7b9bc87)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CheckoutV4Props(
            clean=clean,
            fetch_depth=fetch_depth,
            fetch_tags=fetch_tags,
            filter=filter,
            github_server_url=github_server_url,
            lfs=lfs,
            path=path,
            persist_credentials=persist_credentials,
            ref=ref,
            repository=repository,
            set_safe_directory=set_safe_directory,
            show_progress=show_progress,
            sparse_checkout=sparse_checkout,
            sparse_checkout_cone_mode=sparse_checkout_cone_mode,
            ssh_key=ssh_key,
            ssh_known_hosts=ssh_known_hosts,
            ssh_strict=ssh_strict,
            ssh_user=ssh_user,
            submodules=submodules,
            token=token,
            version=version,
            name=name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="IDENTIFIER")
    def IDENTIFIER(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "IDENTIFIER"))

    @builtins.property
    @jsii.member(jsii_name="outputs")
    def outputs(self) -> "CheckoutV4Outputs":
        '''(experimental) Retrieves outputs of the Checkout action.

        :return: ``CheckoutV4Outputs`` containing ``ref`` and ``commit`` for further use.

        :stability: experimental
        '''
        return typing.cast("CheckoutV4Outputs", jsii.get(self, "outputs"))

    @builtins.property
    @jsii.member(jsii_name="clean")
    def clean(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "clean"))

    @builtins.property
    @jsii.member(jsii_name="fetchDepth")
    def fetch_depth(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "fetchDepth"))

    @builtins.property
    @jsii.member(jsii_name="fetchTags")
    def fetch_tags(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "fetchTags"))

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filter"))

    @builtins.property
    @jsii.member(jsii_name="githubServerUrl")
    def github_server_url(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "githubServerUrl"))

    @builtins.property
    @jsii.member(jsii_name="lfs")
    def lfs(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "lfs"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "path"))

    @builtins.property
    @jsii.member(jsii_name="persistCredentials")
    def persist_credentials(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "persistCredentials"))

    @builtins.property
    @jsii.member(jsii_name="ref")
    def ref(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ref"))

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repository"))

    @builtins.property
    @jsii.member(jsii_name="setSafeDirectory")
    def set_safe_directory(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "setSafeDirectory"))

    @builtins.property
    @jsii.member(jsii_name="showProgress")
    def show_progress(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "showProgress"))

    @builtins.property
    @jsii.member(jsii_name="sparseCheckout")
    def sparse_checkout(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sparseCheckout"))

    @builtins.property
    @jsii.member(jsii_name="sparseCheckoutConeMode")
    def sparse_checkout_cone_mode(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "sparseCheckoutConeMode"))

    @builtins.property
    @jsii.member(jsii_name="sshKey")
    def ssh_key(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sshKey"))

    @builtins.property
    @jsii.member(jsii_name="sshKnownHosts")
    def ssh_known_hosts(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sshKnownHosts"))

    @builtins.property
    @jsii.member(jsii_name="sshStrict")
    def ssh_strict(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "sshStrict"))

    @builtins.property
    @jsii.member(jsii_name="sshUser")
    def ssh_user(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sshUser"))

    @builtins.property
    @jsii.member(jsii_name="submodules")
    def submodules(self) -> typing.Optional[typing.Union[builtins.bool, builtins.str]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, builtins.str]], jsii.get(self, "submodules"))

    @builtins.property
    @jsii.member(jsii_name="token")
    def token(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "token"))


@jsii.data_type(
    jsii_type="github-actions-cdk.actions.CheckoutV4Outputs",
    jsii_struct_bases=[],
    name_mapping={"commit": "commit", "ref": "ref"},
)
class CheckoutV4Outputs:
    def __init__(self, *, commit: builtins.str, ref: builtins.str) -> None:
        '''(experimental) Output structure for the Checkout action.

        :param commit: (experimental) The commit hash of the checked-out version.
        :param ref: (experimental) The reference (branch, tag, or SHA) that was checked out.

        :stability: experimental
        :remarks:

        This interface defines specific outputs provided by the Checkout action,
        including the ``ref`` and ``commit`` properties, which indicate the reference
        and commit hash of the checked-out repository, respectively.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54616a2166aa05511f4ce80de3d19df7e9b2ad2a82723fe69c4d1511171c40e0)
            check_type(argname="argument commit", value=commit, expected_type=type_hints["commit"])
            check_type(argname="argument ref", value=ref, expected_type=type_hints["ref"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "commit": commit,
            "ref": ref,
        }

    @builtins.property
    def commit(self) -> builtins.str:
        '''(experimental) The commit hash of the checked-out version.

        :stability: experimental

        Example::

            "e5e8c1a..."
        '''
        result = self._values.get("commit")
        assert result is not None, "Required property 'commit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ref(self) -> builtins.str:
        '''(experimental) The reference (branch, tag, or SHA) that was checked out.

        :stability: experimental

        Example::

            "main"
        '''
        result = self._values.get("ref")
        assert result is not None, "Required property 'ref' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CheckoutV4Outputs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="github-actions-cdk.actions.CheckoutV4Props",
    jsii_struct_bases=[_CommonActionProps_7122e708],
    name_mapping={
        "name": "name",
        "clean": "clean",
        "fetch_depth": "fetchDepth",
        "fetch_tags": "fetchTags",
        "filter": "filter",
        "github_server_url": "githubServerUrl",
        "lfs": "lfs",
        "path": "path",
        "persist_credentials": "persistCredentials",
        "ref": "ref",
        "repository": "repository",
        "set_safe_directory": "setSafeDirectory",
        "show_progress": "showProgress",
        "sparse_checkout": "sparseCheckout",
        "sparse_checkout_cone_mode": "sparseCheckoutConeMode",
        "ssh_key": "sshKey",
        "ssh_known_hosts": "sshKnownHosts",
        "ssh_strict": "sshStrict",
        "ssh_user": "sshUser",
        "submodules": "submodules",
        "token": "token",
        "version": "version",
    },
)
class CheckoutV4Props(_CommonActionProps_7122e708):
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        clean: typing.Optional[builtins.bool] = None,
        fetch_depth: typing.Optional[jsii.Number] = None,
        fetch_tags: typing.Optional[builtins.bool] = None,
        filter: typing.Optional[builtins.str] = None,
        github_server_url: typing.Optional[builtins.str] = None,
        lfs: typing.Optional[builtins.bool] = None,
        path: typing.Optional[builtins.str] = None,
        persist_credentials: typing.Optional[builtins.bool] = None,
        ref: typing.Optional[builtins.str] = None,
        repository: typing.Optional[builtins.str] = None,
        set_safe_directory: typing.Optional[builtins.bool] = None,
        show_progress: typing.Optional[builtins.bool] = None,
        sparse_checkout: typing.Optional[typing.Sequence[builtins.str]] = None,
        sparse_checkout_cone_mode: typing.Optional[builtins.bool] = None,
        ssh_key: typing.Optional[builtins.str] = None,
        ssh_known_hosts: typing.Optional[builtins.str] = None,
        ssh_strict: typing.Optional[builtins.bool] = None,
        ssh_user: typing.Optional[builtins.str] = None,
        submodules: typing.Optional[typing.Union[builtins.bool, builtins.str]] = None,
        token: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Configuration properties for the Checkout action in a GitHub Actions workflow.

        :param name: (experimental) Display name for the action, shown in GitHub workflow logs for better readability.
        :param clean: (experimental) Specifies if ``git clean`` and ``git reset`` are run before fetching. Default: true
        :param fetch_depth: (experimental) Number of commits to fetch (``0`` for full history). Default: 1
        :param fetch_tags: (experimental) Fetches tags if ``fetchDepth`` is greater than ``0``. Default: false
        :param filter: (experimental) A filter for partially cloning the repository.
        :param github_server_url: (experimental) Base URL for cloning from GitHub instance.
        :param lfs: (experimental) Downloads Git LFS files. Default: false
        :param path: (experimental) Directory under ``$GITHUB_WORKSPACE`` where the repository is checked out.
        :param persist_credentials: (experimental) Determines if credentials should persist in the local git configuration. Default: true
        :param ref: (experimental) The branch, tag, or SHA to checkout. Defaults to the triggering event's reference or SHA, or the default branch if unspecified.
        :param repository: (experimental) Repository name with owner, in the format ``owner/repo``. Default: github.repository
        :param set_safe_directory: (experimental) Adds the repository path to ``safe.directory`` in Git global config. Default: true
        :param show_progress: (experimental) Displays fetch progress in logs. Default: true
        :param sparse_checkout: (experimental) Patterns for sparse checkout.
        :param sparse_checkout_cone_mode: (experimental) Enables cone mode during sparse checkout. Default: true
        :param ssh_key: (experimental) SSH key for authenticated Git commands.
        :param ssh_known_hosts: (experimental) SSH hosts to add to the configuration, retrieved via ``ssh-keyscan``.
        :param ssh_strict: (experimental) Enables or disables strict host key checking for SSH. Default: true
        :param ssh_user: (experimental) Username for SSH host connection. Default: "git"
        :param submodules: (experimental) Determines if submodules should be checked out. Default: false
        :param token: (experimental) Personal Access Token (PAT) used for authenticated Git commands. Default: github.token
        :param version: (experimental) Specifies the version of the action to use.

        :stability: experimental
        :remarks:

        ``CheckoutV4Props`` defines the various options available for the Checkout action,
        including authentication, repository reference, and checkout behavior.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__793e1f4d94ca6fd3f7e196da09f67c9aa4acaf68fd9a2b0264d3d18b68dc78d2)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument clean", value=clean, expected_type=type_hints["clean"])
            check_type(argname="argument fetch_depth", value=fetch_depth, expected_type=type_hints["fetch_depth"])
            check_type(argname="argument fetch_tags", value=fetch_tags, expected_type=type_hints["fetch_tags"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument github_server_url", value=github_server_url, expected_type=type_hints["github_server_url"])
            check_type(argname="argument lfs", value=lfs, expected_type=type_hints["lfs"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument persist_credentials", value=persist_credentials, expected_type=type_hints["persist_credentials"])
            check_type(argname="argument ref", value=ref, expected_type=type_hints["ref"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument set_safe_directory", value=set_safe_directory, expected_type=type_hints["set_safe_directory"])
            check_type(argname="argument show_progress", value=show_progress, expected_type=type_hints["show_progress"])
            check_type(argname="argument sparse_checkout", value=sparse_checkout, expected_type=type_hints["sparse_checkout"])
            check_type(argname="argument sparse_checkout_cone_mode", value=sparse_checkout_cone_mode, expected_type=type_hints["sparse_checkout_cone_mode"])
            check_type(argname="argument ssh_key", value=ssh_key, expected_type=type_hints["ssh_key"])
            check_type(argname="argument ssh_known_hosts", value=ssh_known_hosts, expected_type=type_hints["ssh_known_hosts"])
            check_type(argname="argument ssh_strict", value=ssh_strict, expected_type=type_hints["ssh_strict"])
            check_type(argname="argument ssh_user", value=ssh_user, expected_type=type_hints["ssh_user"])
            check_type(argname="argument submodules", value=submodules, expected_type=type_hints["submodules"])
            check_type(argname="argument token", value=token, expected_type=type_hints["token"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if clean is not None:
            self._values["clean"] = clean
        if fetch_depth is not None:
            self._values["fetch_depth"] = fetch_depth
        if fetch_tags is not None:
            self._values["fetch_tags"] = fetch_tags
        if filter is not None:
            self._values["filter"] = filter
        if github_server_url is not None:
            self._values["github_server_url"] = github_server_url
        if lfs is not None:
            self._values["lfs"] = lfs
        if path is not None:
            self._values["path"] = path
        if persist_credentials is not None:
            self._values["persist_credentials"] = persist_credentials
        if ref is not None:
            self._values["ref"] = ref
        if repository is not None:
            self._values["repository"] = repository
        if set_safe_directory is not None:
            self._values["set_safe_directory"] = set_safe_directory
        if show_progress is not None:
            self._values["show_progress"] = show_progress
        if sparse_checkout is not None:
            self._values["sparse_checkout"] = sparse_checkout
        if sparse_checkout_cone_mode is not None:
            self._values["sparse_checkout_cone_mode"] = sparse_checkout_cone_mode
        if ssh_key is not None:
            self._values["ssh_key"] = ssh_key
        if ssh_known_hosts is not None:
            self._values["ssh_known_hosts"] = ssh_known_hosts
        if ssh_strict is not None:
            self._values["ssh_strict"] = ssh_strict
        if ssh_user is not None:
            self._values["ssh_user"] = ssh_user
        if submodules is not None:
            self._values["submodules"] = submodules
        if token is not None:
            self._values["token"] = token
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Display name for the action, shown in GitHub workflow logs for better readability.

        :stability: experimental

        Example::

            "Checkout Repository"
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def clean(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies if ``git clean`` and ``git reset`` are run before fetching.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("clean")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def fetch_depth(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Number of commits to fetch (``0`` for full history).

        :default: 1

        :stability: experimental
        '''
        result = self._values.get("fetch_depth")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def fetch_tags(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Fetches tags if ``fetchDepth`` is greater than ``0``.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("fetch_tags")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def filter(self) -> typing.Optional[builtins.str]:
        '''(experimental) A filter for partially cloning the repository.

        :stability: experimental
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def github_server_url(self) -> typing.Optional[builtins.str]:
        '''(experimental) Base URL for cloning from GitHub instance.

        :stability: experimental
        '''
        result = self._values.get("github_server_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lfs(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Downloads Git LFS files.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("lfs")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''(experimental) Directory under ``$GITHUB_WORKSPACE`` where the repository is checked out.

        :stability: experimental
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def persist_credentials(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Determines if credentials should persist in the local git configuration.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("persist_credentials")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ref(self) -> typing.Optional[builtins.str]:
        '''(experimental) The branch, tag, or SHA to checkout.

        Defaults to the triggering event's reference
        or SHA, or the default branch if unspecified.

        :stability: experimental
        '''
        result = self._values.get("ref")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository(self) -> typing.Optional[builtins.str]:
        '''(experimental) Repository name with owner, in the format ``owner/repo``.

        :default: github.repository

        :stability: experimental
        '''
        result = self._values.get("repository")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def set_safe_directory(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Adds the repository path to ``safe.directory`` in Git global config.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("set_safe_directory")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def show_progress(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Displays fetch progress in logs.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("show_progress")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def sparse_checkout(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Patterns for sparse checkout.

        :stability: experimental
        '''
        result = self._values.get("sparse_checkout")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sparse_checkout_cone_mode(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables cone mode during sparse checkout.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("sparse_checkout_cone_mode")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ssh_key(self) -> typing.Optional[builtins.str]:
        '''(experimental) SSH key for authenticated Git commands.

        :stability: experimental
        '''
        result = self._values.get("ssh_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssh_known_hosts(self) -> typing.Optional[builtins.str]:
        '''(experimental) SSH hosts to add to the configuration, retrieved via ``ssh-keyscan``.

        :stability: experimental
        '''
        result = self._values.get("ssh_known_hosts")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssh_strict(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables or disables strict host key checking for SSH.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("ssh_strict")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ssh_user(self) -> typing.Optional[builtins.str]:
        '''(experimental) Username for SSH host connection.

        :default: "git"

        :stability: experimental
        '''
        result = self._values.get("ssh_user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def submodules(self) -> typing.Optional[typing.Union[builtins.bool, builtins.str]]:
        '''(experimental) Determines if submodules should be checked out.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("submodules")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, builtins.str]], result)

    @builtins.property
    def token(self) -> typing.Optional[builtins.str]:
        '''(experimental) Personal Access Token (PAT) used for authenticated Git commands.

        :default: github.token

        :stability: experimental
        '''
        result = self._values.get("token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies the version of the action to use.

        :stability: experimental
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CheckoutV4Props(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ConfigureAwsCredentialsV4(
    _Action_64902b3f,
    metaclass=jsii.JSIIMeta,
    jsii_type="github-actions-cdk.actions.ConfigureAwsCredentialsV4",
):
    '''(experimental) Configure AWS Credentials action for GitHub Actions.

    Enables AWS credentials setup via access keys, session tokens, and role assumption, allowing
    workflow steps to interact with AWS services.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        aws_region: builtins.str,
        aws_access_key_id: typing.Optional[builtins.str] = None,
        aws_secret_access_key: typing.Optional[builtins.str] = None,
        aws_session_token: typing.Optional[builtins.str] = None,
        output_credentials: typing.Optional[builtins.bool] = None,
        role_duration_seconds: typing.Optional[builtins.str] = None,
        role_external_id: typing.Optional[builtins.str] = None,
        role_session_name: typing.Optional[builtins.str] = None,
        role_to_assume: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
        web_identity_token_file: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Initializes a new instance of the Configure AWS Credentials action.

        :param scope: - Construct scope in which this action is defined.
        :param id: - Unique identifier for the action within a workflow.
        :param aws_region: (experimental) AWS region to use for the action. Must be a valid AWS region.
        :param aws_access_key_id: (experimental) AWS access key ID to use for credentials.
        :param aws_secret_access_key: (experimental) AWS secret access key associated with the access key ID.
        :param aws_session_token: (experimental) Session token for temporary AWS credentials.
        :param output_credentials: (experimental) If true, outputs the credentials for use in later steps.
        :param role_duration_seconds: (experimental) Duration, in seconds, for the assumed role session.
        :param role_external_id: 
        :param role_session_name: (experimental) Name for the assumed role session.
        :param role_to_assume: (experimental) Optional role ARN to assume for the AWS session.
        :param version: (experimental) Specifies the version of the action to use.
        :param web_identity_token_file: (experimental) Path to a file containing a web identity token, used for assuming a role.
        :param name: (experimental) Display name for the action, shown in GitHub workflow logs for better readability.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f723b68cc5060feca0773e3504ec3cab637cd329d1fc9cbabb7e4cdce4bbb843)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ConfigureAwsCredentialsV4Props(
            aws_region=aws_region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token,
            output_credentials=output_credentials,
            role_duration_seconds=role_duration_seconds,
            role_external_id=role_external_id,
            role_session_name=role_session_name,
            role_to_assume=role_to_assume,
            version=version,
            web_identity_token_file=web_identity_token_file,
            name=name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="IDENTIFIER")
    def IDENTIFIER(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "IDENTIFIER"))

    @builtins.property
    @jsii.member(jsii_name="awsRegion")
    def aws_region(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "awsRegion"))

    @builtins.property
    @jsii.member(jsii_name="outputs")
    def outputs(self) -> "ConfigureAwsCredentialsV4Outputs":
        '''(experimental) Retrieves the outputs of the Configure AWS Credentials action, accessible for use in subsequent workflow steps.

        :return: AWS credentials outputs including account ID, access key, secret key, and session token.

        :stability: experimental
        '''
        return typing.cast("ConfigureAwsCredentialsV4Outputs", jsii.get(self, "outputs"))

    @builtins.property
    @jsii.member(jsii_name="awsAccessKeyId")
    def aws_access_key_id(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsAccessKeyId"))

    @builtins.property
    @jsii.member(jsii_name="awsSecretAccessKey")
    def aws_secret_access_key(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsSecretAccessKey"))

    @builtins.property
    @jsii.member(jsii_name="awsSessionToken")
    def aws_session_token(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsSessionToken"))

    @builtins.property
    @jsii.member(jsii_name="outputCredentials")
    def output_credentials(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "outputCredentials"))

    @builtins.property
    @jsii.member(jsii_name="roleDurationSeconds")
    def role_duration_seconds(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleDurationSeconds"))

    @builtins.property
    @jsii.member(jsii_name="roleSessionName")
    def role_session_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleSessionName"))

    @builtins.property
    @jsii.member(jsii_name="roleToAssume")
    def role_to_assume(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleToAssume"))

    @builtins.property
    @jsii.member(jsii_name="webIdentityTokenFile")
    def web_identity_token_file(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "webIdentityTokenFile"))


@jsii.data_type(
    jsii_type="github-actions-cdk.actions.ConfigureAwsCredentialsV4Outputs",
    jsii_struct_bases=[],
    name_mapping={
        "aws_access_key_id": "awsAccessKeyId",
        "aws_account_id": "awsAccountId",
        "aws_secret_access_key": "awsSecretAccessKey",
        "aws_session_token": "awsSessionToken",
    },
)
class ConfigureAwsCredentialsV4Outputs:
    def __init__(
        self,
        *,
        aws_access_key_id: builtins.str,
        aws_account_id: builtins.str,
        aws_secret_access_key: builtins.str,
        aws_session_token: builtins.str,
    ) -> None:
        '''(experimental) Output structure for the Configure AWS Credentials action.

        Provides outputs such as AWS account ID, access keys, and session tokens, enabling
        subsequent steps in the workflow to use AWS credentials securely.

        :param aws_access_key_id: (experimental) The AWS Access Key ID that allows programmatic access to AWS services. This key should be handled securely and kept confidential.
        :param aws_account_id: (experimental) The AWS account ID associated with the configured credentials. This is typically the 12-digit account number linked to the credentials used.
        :param aws_secret_access_key: (experimental) The AWS Secret Access Key paired with the AWS Access Key ID. This secret is used to authenticate and authorize requests to AWS. It must be protected to prevent unauthorized access to AWS resources.
        :param aws_session_token: (experimental) A temporary session token associated with the AWS credentials, provided when using temporary security credentials, such as those obtained through role assumption. This token must accompany requests along with the Access Key ID and Secret Access Key.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d918670eac1bc925c8ff150989e850a95d733be7100fde7739a6de34b65fe343)
            check_type(argname="argument aws_access_key_id", value=aws_access_key_id, expected_type=type_hints["aws_access_key_id"])
            check_type(argname="argument aws_account_id", value=aws_account_id, expected_type=type_hints["aws_account_id"])
            check_type(argname="argument aws_secret_access_key", value=aws_secret_access_key, expected_type=type_hints["aws_secret_access_key"])
            check_type(argname="argument aws_session_token", value=aws_session_token, expected_type=type_hints["aws_session_token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "aws_access_key_id": aws_access_key_id,
            "aws_account_id": aws_account_id,
            "aws_secret_access_key": aws_secret_access_key,
            "aws_session_token": aws_session_token,
        }

    @builtins.property
    def aws_access_key_id(self) -> builtins.str:
        '''(experimental) The AWS Access Key ID that allows programmatic access to AWS services.

        This key should be handled securely and kept confidential.

        :stability: experimental
        '''
        result = self._values.get("aws_access_key_id")
        assert result is not None, "Required property 'aws_access_key_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aws_account_id(self) -> builtins.str:
        '''(experimental) The AWS account ID associated with the configured credentials.

        This is typically the 12-digit account number linked to the credentials used.

        :stability: experimental
        '''
        result = self._values.get("aws_account_id")
        assert result is not None, "Required property 'aws_account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aws_secret_access_key(self) -> builtins.str:
        '''(experimental) The AWS Secret Access Key paired with the AWS Access Key ID.

        This secret is used to authenticate and authorize requests to AWS.
        It must be protected to prevent unauthorized access to AWS resources.

        :stability: experimental
        '''
        result = self._values.get("aws_secret_access_key")
        assert result is not None, "Required property 'aws_secret_access_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aws_session_token(self) -> builtins.str:
        '''(experimental) A temporary session token associated with the AWS credentials, provided when using temporary security credentials, such as those obtained through role assumption.

        This token must accompany requests along with the Access Key ID and Secret Access Key.

        :stability: experimental
        '''
        result = self._values.get("aws_session_token")
        assert result is not None, "Required property 'aws_session_token' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConfigureAwsCredentialsV4Outputs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="github-actions-cdk.actions.ConfigureAwsCredentialsV4Props",
    jsii_struct_bases=[_CommonActionProps_7122e708],
    name_mapping={
        "name": "name",
        "aws_region": "awsRegion",
        "aws_access_key_id": "awsAccessKeyId",
        "aws_secret_access_key": "awsSecretAccessKey",
        "aws_session_token": "awsSessionToken",
        "output_credentials": "outputCredentials",
        "role_duration_seconds": "roleDurationSeconds",
        "role_external_id": "roleExternalId",
        "role_session_name": "roleSessionName",
        "role_to_assume": "roleToAssume",
        "version": "version",
        "web_identity_token_file": "webIdentityTokenFile",
    },
)
class ConfigureAwsCredentialsV4Props(_CommonActionProps_7122e708):
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        aws_region: builtins.str,
        aws_access_key_id: typing.Optional[builtins.str] = None,
        aws_secret_access_key: typing.Optional[builtins.str] = None,
        aws_session_token: typing.Optional[builtins.str] = None,
        output_credentials: typing.Optional[builtins.bool] = None,
        role_duration_seconds: typing.Optional[builtins.str] = None,
        role_external_id: typing.Optional[builtins.str] = None,
        role_session_name: typing.Optional[builtins.str] = None,
        role_to_assume: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
        web_identity_token_file: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for configuring the AWS credentials setup within a GitHub Actions workflow.

        Extends CommonActionProps to allow AWS-specific options, including access key IDs,
        session tokens, and optional role assumption parameters.

        :param name: (experimental) Display name for the action, shown in GitHub workflow logs for better readability.
        :param aws_region: (experimental) AWS region to use for the action. Must be a valid AWS region.
        :param aws_access_key_id: (experimental) AWS access key ID to use for credentials.
        :param aws_secret_access_key: (experimental) AWS secret access key associated with the access key ID.
        :param aws_session_token: (experimental) Session token for temporary AWS credentials.
        :param output_credentials: (experimental) If true, outputs the credentials for use in later steps.
        :param role_duration_seconds: (experimental) Duration, in seconds, for the assumed role session.
        :param role_external_id: 
        :param role_session_name: (experimental) Name for the assumed role session.
        :param role_to_assume: (experimental) Optional role ARN to assume for the AWS session.
        :param version: (experimental) Specifies the version of the action to use.
        :param web_identity_token_file: (experimental) Path to a file containing a web identity token, used for assuming a role.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3c951820ed9d0fac84354bff07728164b63ce96b9a0b7074d1fd679131f013f)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument aws_region", value=aws_region, expected_type=type_hints["aws_region"])
            check_type(argname="argument aws_access_key_id", value=aws_access_key_id, expected_type=type_hints["aws_access_key_id"])
            check_type(argname="argument aws_secret_access_key", value=aws_secret_access_key, expected_type=type_hints["aws_secret_access_key"])
            check_type(argname="argument aws_session_token", value=aws_session_token, expected_type=type_hints["aws_session_token"])
            check_type(argname="argument output_credentials", value=output_credentials, expected_type=type_hints["output_credentials"])
            check_type(argname="argument role_duration_seconds", value=role_duration_seconds, expected_type=type_hints["role_duration_seconds"])
            check_type(argname="argument role_external_id", value=role_external_id, expected_type=type_hints["role_external_id"])
            check_type(argname="argument role_session_name", value=role_session_name, expected_type=type_hints["role_session_name"])
            check_type(argname="argument role_to_assume", value=role_to_assume, expected_type=type_hints["role_to_assume"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument web_identity_token_file", value=web_identity_token_file, expected_type=type_hints["web_identity_token_file"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "aws_region": aws_region,
        }
        if name is not None:
            self._values["name"] = name
        if aws_access_key_id is not None:
            self._values["aws_access_key_id"] = aws_access_key_id
        if aws_secret_access_key is not None:
            self._values["aws_secret_access_key"] = aws_secret_access_key
        if aws_session_token is not None:
            self._values["aws_session_token"] = aws_session_token
        if output_credentials is not None:
            self._values["output_credentials"] = output_credentials
        if role_duration_seconds is not None:
            self._values["role_duration_seconds"] = role_duration_seconds
        if role_external_id is not None:
            self._values["role_external_id"] = role_external_id
        if role_session_name is not None:
            self._values["role_session_name"] = role_session_name
        if role_to_assume is not None:
            self._values["role_to_assume"] = role_to_assume
        if version is not None:
            self._values["version"] = version
        if web_identity_token_file is not None:
            self._values["web_identity_token_file"] = web_identity_token_file

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Display name for the action, shown in GitHub workflow logs for better readability.

        :stability: experimental

        Example::

            "Checkout Repository"
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def aws_region(self) -> builtins.str:
        '''(experimental) AWS region to use for the action.

        Must be a valid AWS region.

        :stability: experimental
        '''
        result = self._values.get("aws_region")
        assert result is not None, "Required property 'aws_region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aws_access_key_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) AWS access key ID to use for credentials.

        :stability: experimental
        '''
        result = self._values.get("aws_access_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def aws_secret_access_key(self) -> typing.Optional[builtins.str]:
        '''(experimental) AWS secret access key associated with the access key ID.

        :stability: experimental
        '''
        result = self._values.get("aws_secret_access_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def aws_session_token(self) -> typing.Optional[builtins.str]:
        '''(experimental) Session token for temporary AWS credentials.

        :stability: experimental
        '''
        result = self._values.get("aws_session_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output_credentials(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If true, outputs the credentials for use in later steps.

        :stability: experimental
        '''
        result = self._values.get("output_credentials")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def role_duration_seconds(self) -> typing.Optional[builtins.str]:
        '''(experimental) Duration, in seconds, for the assumed role session.

        :stability: experimental
        '''
        result = self._values.get("role_duration_seconds")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_external_id(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("role_external_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_session_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name for the assumed role session.

        :stability: experimental
        '''
        result = self._values.get("role_session_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_to_assume(self) -> typing.Optional[builtins.str]:
        '''(experimental) Optional role ARN to assume for the AWS session.

        :stability: experimental
        '''
        result = self._values.get("role_to_assume")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies the version of the action to use.

        :stability: experimental
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def web_identity_token_file(self) -> typing.Optional[builtins.str]:
        '''(experimental) Path to a file containing a web identity token, used for assuming a role.

        :stability: experimental
        '''
        result = self._values.get("web_identity_token_file")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConfigureAwsCredentialsV4Props(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DownloadArtifactV4(
    _Action_64902b3f,
    metaclass=jsii.JSIIMeta,
    jsii_type="github-actions-cdk.actions.DownloadArtifactV4",
):
    '''(experimental) Download action for GitHub Actions workflows, configuring a download of build artifacts.

    :stability: experimental
    :remarks:

    This class allows configuration of the Download action with options for specifying
    the artifact name, download path, pattern matching, and GitHub API authentication.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        artifact_name: typing.Optional[builtins.str] = None,
        github_token: typing.Optional[builtins.str] = None,
        merge_multiple: typing.Optional[builtins.bool] = None,
        path: typing.Optional[builtins.str] = None,
        pattern: typing.Optional[builtins.str] = None,
        repository: typing.Optional[builtins.str] = None,
        run_id: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Initializes a new instance of the Download action.

        :param scope: - The scope in which to define this construct.
        :param id: - Unique identifier for the action.
        :param artifact_name: (experimental) Name of the artifact to download. If unspecified, all artifacts for the run are downloaded.
        :param github_token: (experimental) GitHub token for authenticating with the GitHub API when downloading from a different repository or workflow.
        :param merge_multiple: (experimental) Determines whether multiple matched artifacts are merged into the same directory. Default: "false"
        :param path: (experimental) Destination path for the downloaded artifact. Defaults to ``$GITHUB_WORKSPACE``.
        :param pattern: (experimental) A glob pattern to match artifacts to download. Ignored if ``name`` is specified.
        :param repository: (experimental) Repository from which to download artifacts, specified as ``owner/repo``. Default: "${{ github.repository }}"
        :param run_id: (experimental) Workflow run ID from which artifacts are downloaded. Relevant if ``githubToken`` is provided. Default: "${{ github.run_id }}"
        :param version: (experimental) Specifies the version of the action to use. Default: "v4"
        :param name: (experimental) Display name for the action, shown in GitHub workflow logs for better readability.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75ddbcb870cc3986303a27a9f386945450807cc25d331c2c74d4604252866c3e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DownloadArtifactV4Props(
            artifact_name=artifact_name,
            github_token=github_token,
            merge_multiple=merge_multiple,
            path=path,
            pattern=pattern,
            repository=repository,
            run_id=run_id,
            version=version,
            name=name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="IDENTIFIER")
    def IDENTIFIER(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "IDENTIFIER"))

    @builtins.property
    @jsii.member(jsii_name="outputs")
    def outputs(self) -> "DownloadArtifactV4Outputs":
        '''(experimental) Retrieves outputs of the Download action.

        :return: ``DownloadArtifactV4Outputs`` containing ``downloadPath`` for further use.

        :stability: experimental
        '''
        return typing.cast("DownloadArtifactV4Outputs", jsii.get(self, "outputs"))

    @builtins.property
    @jsii.member(jsii_name="artifactName")
    def artifact_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "artifactName"))

    @builtins.property
    @jsii.member(jsii_name="githubToken")
    def github_token(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "githubToken"))

    @builtins.property
    @jsii.member(jsii_name="mergeMultiple")
    def merge_multiple(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "mergeMultiple"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "path"))

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pattern"))

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repository"))

    @builtins.property
    @jsii.member(jsii_name="runId")
    def run_id(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runId"))


@jsii.data_type(
    jsii_type="github-actions-cdk.actions.DownloadArtifactV4Outputs",
    jsii_struct_bases=[],
    name_mapping={"download_path": "downloadPath"},
)
class DownloadArtifactV4Outputs:
    def __init__(self, *, download_path: builtins.str) -> None:
        '''(experimental) Output structure for the Download action.

        :param download_path: (experimental) Path where the artifact was downloaded.

        :stability: experimental
        :remarks:

        This interface defines the specific output provided by the Download action,
        including the ``downloadPath`` property which indicates where the artifact was downloaded.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__630f831b0e35891deec9d936b23d192524aaee9f92ef964bb2dbf490a404e085)
            check_type(argname="argument download_path", value=download_path, expected_type=type_hints["download_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "download_path": download_path,
        }

    @builtins.property
    def download_path(self) -> builtins.str:
        '''(experimental) Path where the artifact was downloaded.

        :stability: experimental
        '''
        result = self._values.get("download_path")
        assert result is not None, "Required property 'download_path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DownloadArtifactV4Outputs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="github-actions-cdk.actions.DownloadArtifactV4Props",
    jsii_struct_bases=[_CommonActionProps_7122e708],
    name_mapping={
        "name": "name",
        "artifact_name": "artifactName",
        "github_token": "githubToken",
        "merge_multiple": "mergeMultiple",
        "path": "path",
        "pattern": "pattern",
        "repository": "repository",
        "run_id": "runId",
        "version": "version",
    },
)
class DownloadArtifactV4Props(_CommonActionProps_7122e708):
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        artifact_name: typing.Optional[builtins.str] = None,
        github_token: typing.Optional[builtins.str] = None,
        merge_multiple: typing.Optional[builtins.bool] = None,
        path: typing.Optional[builtins.str] = None,
        pattern: typing.Optional[builtins.str] = None,
        repository: typing.Optional[builtins.str] = None,
        run_id: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Configuration properties for the Download action in a GitHub Actions workflow.

        :param name: (experimental) Display name for the action, shown in GitHub workflow logs for better readability.
        :param artifact_name: (experimental) Name of the artifact to download. If unspecified, all artifacts for the run are downloaded.
        :param github_token: (experimental) GitHub token for authenticating with the GitHub API when downloading from a different repository or workflow.
        :param merge_multiple: (experimental) Determines whether multiple matched artifacts are merged into the same directory. Default: "false"
        :param path: (experimental) Destination path for the downloaded artifact. Defaults to ``$GITHUB_WORKSPACE``.
        :param pattern: (experimental) A glob pattern to match artifacts to download. Ignored if ``name`` is specified.
        :param repository: (experimental) Repository from which to download artifacts, specified as ``owner/repo``. Default: "${{ github.repository }}"
        :param run_id: (experimental) Workflow run ID from which artifacts are downloaded. Relevant if ``githubToken`` is provided. Default: "${{ github.run_id }}"
        :param version: (experimental) Specifies the version of the action to use. Default: "v4"

        :stability: experimental
        :remarks:

        ``DownloadArtifactProps`` defines the various options available for the Download action,
        including artifact naming, paths, patterns, and authentication settings.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e538a875e1d66d457ed6169280daa9f036b8abe5e7c691a77f7b40b8b0a382b)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument artifact_name", value=artifact_name, expected_type=type_hints["artifact_name"])
            check_type(argname="argument github_token", value=github_token, expected_type=type_hints["github_token"])
            check_type(argname="argument merge_multiple", value=merge_multiple, expected_type=type_hints["merge_multiple"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument run_id", value=run_id, expected_type=type_hints["run_id"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if artifact_name is not None:
            self._values["artifact_name"] = artifact_name
        if github_token is not None:
            self._values["github_token"] = github_token
        if merge_multiple is not None:
            self._values["merge_multiple"] = merge_multiple
        if path is not None:
            self._values["path"] = path
        if pattern is not None:
            self._values["pattern"] = pattern
        if repository is not None:
            self._values["repository"] = repository
        if run_id is not None:
            self._values["run_id"] = run_id
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Display name for the action, shown in GitHub workflow logs for better readability.

        :stability: experimental

        Example::

            "Checkout Repository"
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def artifact_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the artifact to download.

        If unspecified, all artifacts for the run are downloaded.

        :stability: experimental
        '''
        result = self._values.get("artifact_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def github_token(self) -> typing.Optional[builtins.str]:
        '''(experimental) GitHub token for authenticating with the GitHub API when downloading from a different repository or workflow.

        :stability: experimental
        '''
        result = self._values.get("github_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def merge_multiple(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Determines whether multiple matched artifacts are merged into the same directory.

        :default: "false"

        :stability: experimental
        '''
        result = self._values.get("merge_multiple")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''(experimental) Destination path for the downloaded artifact.

        Defaults to ``$GITHUB_WORKSPACE``.

        :stability: experimental
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pattern(self) -> typing.Optional[builtins.str]:
        '''(experimental) A glob pattern to match artifacts to download.

        Ignored if ``name`` is specified.

        :stability: experimental
        '''
        result = self._values.get("pattern")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository(self) -> typing.Optional[builtins.str]:
        '''(experimental) Repository from which to download artifacts, specified as ``owner/repo``.

        :default: "${{ github.repository }}"

        :stability: experimental
        '''
        result = self._values.get("repository")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def run_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) Workflow run ID from which artifacts are downloaded.

        Relevant if ``githubToken`` is provided.

        :default: "${{ github.run_id }}"

        :stability: experimental
        '''
        result = self._values.get("run_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies the version of the action to use.

        :default: "v4"

        :stability: experimental
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DownloadArtifactV4Props(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SetupGoV5(
    _Action_64902b3f,
    metaclass=jsii.JSIIMeta,
    jsii_type="github-actions-cdk.actions.SetupGoV5",
):
    '''(experimental) Class representing the Setup Go action in a GitHub Actions workflow.

    This action supports Go version setup, dependency caching, and architecture targeting.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        go_version: builtins.str,
        architecture: typing.Optional[builtins.str] = None,
        cache: typing.Optional[builtins.bool] = None,
        cache_dependency_path: typing.Optional[builtins.str] = None,
        check_latest: typing.Optional[builtins.bool] = None,
        go_version_file: typing.Optional[builtins.str] = None,
        token: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Initializes a new instance of the ``SetupGo`` action with the specified properties.

        :param scope: - Scope in which this construct is defined.
        :param id: - Unique identifier for the action within a workflow.
        :param go_version: (experimental) The version range or exact version of Go to use. If not specified, the action will read the version from the ``go-version`` file if it exists.
        :param architecture: (experimental) Target architecture of the Go interpreter. Supported values include "amd64", "arm64", etc.
        :param cache: (experimental) A boolean indicating whether to cache Go dependencies. Default: true
        :param cache_dependency_path: (experimental) Path to dependency files for caching. Supports wildcards or a list of file names. This allows caching of multiple dependencies efficiently.
        :param check_latest: (experimental) If true, the action will check for the latest available version that satisfies the specified version. Default: false
        :param go_version_file: (experimental) Optional file containing the Go version to use. Typically this would be ``go-version``.
        :param token: (experimental) Token used for authentication when fetching Go distributions from the repository.
        :param version: (experimental) Specifies the version of the action to use.
        :param name: (experimental) Display name for the action, shown in GitHub workflow logs for better readability.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d098cb52550887ce4e35792740ea36a97eef44d2539af13aa4d53349f22ee9f2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SetupGoV5Props(
            go_version=go_version,
            architecture=architecture,
            cache=cache,
            cache_dependency_path=cache_dependency_path,
            check_latest=check_latest,
            go_version_file=go_version_file,
            token=token,
            version=version,
            name=name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="IDENTIFIER")
    def IDENTIFIER(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "IDENTIFIER"))

    @builtins.property
    @jsii.member(jsii_name="cache")
    def cache(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "cache"))

    @builtins.property
    @jsii.member(jsii_name="checkLatest")
    def check_latest(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "checkLatest"))

    @builtins.property
    @jsii.member(jsii_name="goVersion")
    def go_version(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "goVersion"))

    @builtins.property
    @jsii.member(jsii_name="outputs")
    def outputs(self) -> "SetupGoV5Outputs":
        '''(experimental) Retrieves outputs from the Setup Go action.

        This method returns an object containing output values that can be referenced in subsequent
        steps of the workflow, including the installed Go version and cache status.

        :return: Go setup outputs, including the installed Go version and cache status.

        :stability: experimental
        '''
        return typing.cast("SetupGoV5Outputs", jsii.get(self, "outputs"))

    @builtins.property
    @jsii.member(jsii_name="architecture")
    def architecture(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "architecture"))

    @builtins.property
    @jsii.member(jsii_name="cacheDependencyPath")
    def cache_dependency_path(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cacheDependencyPath"))

    @builtins.property
    @jsii.member(jsii_name="goVersionFile")
    def go_version_file(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "goVersionFile"))

    @builtins.property
    @jsii.member(jsii_name="token")
    def token(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "token"))


@jsii.data_type(
    jsii_type="github-actions-cdk.actions.SetupGoV5Outputs",
    jsii_struct_bases=[],
    name_mapping={"cache_hit": "cacheHit", "go_version": "goVersion"},
)
class SetupGoV5Outputs:
    def __init__(self, *, cache_hit: builtins.str, go_version: builtins.str) -> None:
        '''(experimental) Output structure for the Setup Go action.

        Provides outputs related to the Go setup process, such as
        the installed Go version and cache hit status.

        :param cache_hit: (experimental) A boolean value indicating whether a cache entry was found during the setup.
        :param go_version: (experimental) The version of Go that has been installed.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb32ebe9fe1e7aa81e60daf556e177c2bc27c7167c6ac87223b7efc7b74d9080)
            check_type(argname="argument cache_hit", value=cache_hit, expected_type=type_hints["cache_hit"])
            check_type(argname="argument go_version", value=go_version, expected_type=type_hints["go_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cache_hit": cache_hit,
            "go_version": go_version,
        }

    @builtins.property
    def cache_hit(self) -> builtins.str:
        '''(experimental) A boolean value indicating whether a cache entry was found during the setup.

        :stability: experimental
        '''
        result = self._values.get("cache_hit")
        assert result is not None, "Required property 'cache_hit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def go_version(self) -> builtins.str:
        '''(experimental) The version of Go that has been installed.

        :stability: experimental
        '''
        result = self._values.get("go_version")
        assert result is not None, "Required property 'go_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SetupGoV5Outputs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="github-actions-cdk.actions.SetupGoV5Props",
    jsii_struct_bases=[_CommonActionProps_7122e708],
    name_mapping={
        "name": "name",
        "go_version": "goVersion",
        "architecture": "architecture",
        "cache": "cache",
        "cache_dependency_path": "cacheDependencyPath",
        "check_latest": "checkLatest",
        "go_version_file": "goVersionFile",
        "token": "token",
        "version": "version",
    },
)
class SetupGoV5Props(_CommonActionProps_7122e708):
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        go_version: builtins.str,
        architecture: typing.Optional[builtins.str] = None,
        cache: typing.Optional[builtins.bool] = None,
        cache_dependency_path: typing.Optional[builtins.str] = None,
        check_latest: typing.Optional[builtins.bool] = None,
        go_version_file: typing.Optional[builtins.str] = None,
        token: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for configuring the Setup Go action.

        This interface defines the specific options for Go setup, including
        version, caching, and target architecture.

        :param name: (experimental) Display name for the action, shown in GitHub workflow logs for better readability.
        :param go_version: (experimental) The version range or exact version of Go to use. If not specified, the action will read the version from the ``go-version`` file if it exists.
        :param architecture: (experimental) Target architecture of the Go interpreter. Supported values include "amd64", "arm64", etc.
        :param cache: (experimental) A boolean indicating whether to cache Go dependencies. Default: true
        :param cache_dependency_path: (experimental) Path to dependency files for caching. Supports wildcards or a list of file names. This allows caching of multiple dependencies efficiently.
        :param check_latest: (experimental) If true, the action will check for the latest available version that satisfies the specified version. Default: false
        :param go_version_file: (experimental) Optional file containing the Go version to use. Typically this would be ``go-version``.
        :param token: (experimental) Token used for authentication when fetching Go distributions from the repository.
        :param version: (experimental) Specifies the version of the action to use.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__193f087c7324cb14bfe6c01d286db48a15756f5b2e6a66f682f341f23bffb800)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument go_version", value=go_version, expected_type=type_hints["go_version"])
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
            check_type(argname="argument cache", value=cache, expected_type=type_hints["cache"])
            check_type(argname="argument cache_dependency_path", value=cache_dependency_path, expected_type=type_hints["cache_dependency_path"])
            check_type(argname="argument check_latest", value=check_latest, expected_type=type_hints["check_latest"])
            check_type(argname="argument go_version_file", value=go_version_file, expected_type=type_hints["go_version_file"])
            check_type(argname="argument token", value=token, expected_type=type_hints["token"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "go_version": go_version,
        }
        if name is not None:
            self._values["name"] = name
        if architecture is not None:
            self._values["architecture"] = architecture
        if cache is not None:
            self._values["cache"] = cache
        if cache_dependency_path is not None:
            self._values["cache_dependency_path"] = cache_dependency_path
        if check_latest is not None:
            self._values["check_latest"] = check_latest
        if go_version_file is not None:
            self._values["go_version_file"] = go_version_file
        if token is not None:
            self._values["token"] = token
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Display name for the action, shown in GitHub workflow logs for better readability.

        :stability: experimental

        Example::

            "Checkout Repository"
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def go_version(self) -> builtins.str:
        '''(experimental) The version range or exact version of Go to use.

        If not specified, the action will read the version from the ``go-version`` file if it exists.

        :stability: experimental
        '''
        result = self._values.get("go_version")
        assert result is not None, "Required property 'go_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def architecture(self) -> typing.Optional[builtins.str]:
        '''(experimental) Target architecture of the Go interpreter.

        Supported values include "amd64", "arm64", etc.

        :stability: experimental
        '''
        result = self._values.get("architecture")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cache(self) -> typing.Optional[builtins.bool]:
        '''(experimental) A boolean indicating whether to cache Go dependencies.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("cache")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cache_dependency_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) Path to dependency files for caching.

        Supports wildcards or a list of file names.
        This allows caching of multiple dependencies efficiently.

        :stability: experimental
        '''
        result = self._values.get("cache_dependency_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def check_latest(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If true, the action will check for the latest available version that satisfies the specified version.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("check_latest")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def go_version_file(self) -> typing.Optional[builtins.str]:
        '''(experimental) Optional file containing the Go version to use.

        Typically this would be ``go-version``.

        :stability: experimental
        '''
        result = self._values.get("go_version_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token(self) -> typing.Optional[builtins.str]:
        '''(experimental) Token used for authentication when fetching Go distributions from the repository.

        :stability: experimental
        '''
        result = self._values.get("token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies the version of the action to use.

        :stability: experimental
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SetupGoV5Props(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SetupNodeV4(
    _Action_64902b3f,
    metaclass=jsii.JSIIMeta,
    jsii_type="github-actions-cdk.actions.SetupNodeV4",
):
    '''(experimental) Class representing the Setup Node.js action in a GitHub Actions workflow.

    This action configures Node.js version, caching, registry settings, and more to facilitate builds.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        node_version: builtins.str,
        always_auth: typing.Optional[builtins.bool] = None,
        architecture: typing.Optional[builtins.str] = None,
        cache: typing.Optional[builtins.str] = None,
        cache_dependency_path: typing.Optional[builtins.str] = None,
        check_latest: typing.Optional[builtins.bool] = None,
        node_version_file: typing.Optional[builtins.str] = None,
        npm_package_scope: typing.Optional[builtins.str] = None,
        registry_url: typing.Optional[builtins.str] = None,
        token: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Initializes a new instance of the Setup Node.js action.

        :param scope: - Scope in which this construct is defined.
        :param id: - A unique identifier for the action instance.
        :param node_version: (experimental) The version of Node.js to use, specified as a version range or exact version.
        :param always_auth: (experimental) If true, forces authentication to the npm registry even when installing public packages.
        :param architecture: (experimental) The target architecture for the Node.js installation (e.g., ``x64`` or ``arm64``).
        :param cache: (experimental) The package manager to use for caching (``npm``, ``yarn``, or ``pnpm``).
        :param cache_dependency_path: (experimental) Optional path to dependency files for caching. This allows caching of multiple dependencies efficiently.
        :param check_latest: (experimental) If true, checks for the latest version matching the specified version. Default: false
        :param node_version_file: (experimental) Optional path to a file containing the Node.js version to use. This is useful for dynamically specifying versions.
        :param npm_package_scope: (experimental) Scope for the npm packages, useful for scoped packages in the registry.
        :param registry_url: (experimental) The URL of the npm registry to authenticate against.
        :param token: (experimental) Token for authentication with the npm registry.
        :param version: (experimental) Specifies the version of the action to use.
        :param name: (experimental) Display name for the action, shown in GitHub workflow logs for better readability.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1ab7f5eb53c65e0b1962e11c2c602fff9b8e83df00b3c3369bcca6895bfd876)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SetupNodeV4Props(
            node_version=node_version,
            always_auth=always_auth,
            architecture=architecture,
            cache=cache,
            cache_dependency_path=cache_dependency_path,
            check_latest=check_latest,
            node_version_file=node_version_file,
            npm_package_scope=npm_package_scope,
            registry_url=registry_url,
            token=token,
            version=version,
            name=name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="IDENTIFIER")
    def IDENTIFIER(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "IDENTIFIER"))

    @builtins.property
    @jsii.member(jsii_name="checkLatest")
    def check_latest(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "checkLatest"))

    @builtins.property
    @jsii.member(jsii_name="nodeVersion")
    def node_version(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "nodeVersion"))

    @builtins.property
    @jsii.member(jsii_name="outputs")
    def outputs(self) -> "SetupNodeV4Outputs":
        '''(experimental) Retrieves outputs from the Setup Node.js action for use in subsequent workflow steps.

        :return: The Setup Node.js action's outputs, including ``cacheHit`` and ``nodeVersion``.

        :stability: experimental
        '''
        return typing.cast("SetupNodeV4Outputs", jsii.get(self, "outputs"))

    @builtins.property
    @jsii.member(jsii_name="alwaysAuth")
    def always_auth(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "alwaysAuth"))

    @builtins.property
    @jsii.member(jsii_name="architecture")
    def architecture(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "architecture"))

    @builtins.property
    @jsii.member(jsii_name="cache")
    def cache(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cache"))

    @builtins.property
    @jsii.member(jsii_name="cacheDependencyPath")
    def cache_dependency_path(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cacheDependencyPath"))

    @builtins.property
    @jsii.member(jsii_name="nodeVersionFile")
    def node_version_file(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeVersionFile"))

    @builtins.property
    @jsii.member(jsii_name="npmPackageScope")
    def npm_package_scope(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "npmPackageScope"))

    @builtins.property
    @jsii.member(jsii_name="registryUrl")
    def registry_url(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "registryUrl"))

    @builtins.property
    @jsii.member(jsii_name="token")
    def token(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "token"))


@jsii.data_type(
    jsii_type="github-actions-cdk.actions.SetupNodeV4Outputs",
    jsii_struct_bases=[],
    name_mapping={"cache_hit": "cacheHit", "node_version": "nodeVersion"},
)
class SetupNodeV4Outputs:
    def __init__(self, *, cache_hit: builtins.str, node_version: builtins.str) -> None:
        '''(experimental) Outputs from the Setup Node.js action.

        This interface includes key output values such as the Node.js version installed and whether a cache was used.

        :param cache_hit: (experimental) Indicates if a cache was successfully hit during the action.
        :param node_version: (experimental) The version of Node.js that was installed.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33f67a423382aad4c4a76bd53e1f611bf55398796e7444cb580a0b3201f380d6)
            check_type(argname="argument cache_hit", value=cache_hit, expected_type=type_hints["cache_hit"])
            check_type(argname="argument node_version", value=node_version, expected_type=type_hints["node_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cache_hit": cache_hit,
            "node_version": node_version,
        }

    @builtins.property
    def cache_hit(self) -> builtins.str:
        '''(experimental) Indicates if a cache was successfully hit during the action.

        :stability: experimental
        '''
        result = self._values.get("cache_hit")
        assert result is not None, "Required property 'cache_hit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def node_version(self) -> builtins.str:
        '''(experimental) The version of Node.js that was installed.

        :stability: experimental
        '''
        result = self._values.get("node_version")
        assert result is not None, "Required property 'node_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SetupNodeV4Outputs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="github-actions-cdk.actions.SetupNodeV4Props",
    jsii_struct_bases=[_CommonActionProps_7122e708],
    name_mapping={
        "name": "name",
        "node_version": "nodeVersion",
        "always_auth": "alwaysAuth",
        "architecture": "architecture",
        "cache": "cache",
        "cache_dependency_path": "cacheDependencyPath",
        "check_latest": "checkLatest",
        "node_version_file": "nodeVersionFile",
        "npm_package_scope": "npmPackageScope",
        "registry_url": "registryUrl",
        "token": "token",
        "version": "version",
    },
)
class SetupNodeV4Props(_CommonActionProps_7122e708):
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        node_version: builtins.str,
        always_auth: typing.Optional[builtins.bool] = None,
        architecture: typing.Optional[builtins.str] = None,
        cache: typing.Optional[builtins.str] = None,
        cache_dependency_path: typing.Optional[builtins.str] = None,
        check_latest: typing.Optional[builtins.bool] = None,
        node_version_file: typing.Optional[builtins.str] = None,
        npm_package_scope: typing.Optional[builtins.str] = None,
        registry_url: typing.Optional[builtins.str] = None,
        token: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for configuring the Setup Node.js action within a GitHub Actions workflow.

        This interface extends common action properties to include options specific to Node.js setup,
        such as versioning, caching, and registry authentication.

        :param name: (experimental) Display name for the action, shown in GitHub workflow logs for better readability.
        :param node_version: (experimental) The version of Node.js to use, specified as a version range or exact version.
        :param always_auth: (experimental) If true, forces authentication to the npm registry even when installing public packages.
        :param architecture: (experimental) The target architecture for the Node.js installation (e.g., ``x64`` or ``arm64``).
        :param cache: (experimental) The package manager to use for caching (``npm``, ``yarn``, or ``pnpm``).
        :param cache_dependency_path: (experimental) Optional path to dependency files for caching. This allows caching of multiple dependencies efficiently.
        :param check_latest: (experimental) If true, checks for the latest version matching the specified version. Default: false
        :param node_version_file: (experimental) Optional path to a file containing the Node.js version to use. This is useful for dynamically specifying versions.
        :param npm_package_scope: (experimental) Scope for the npm packages, useful for scoped packages in the registry.
        :param registry_url: (experimental) The URL of the npm registry to authenticate against.
        :param token: (experimental) Token for authentication with the npm registry.
        :param version: (experimental) Specifies the version of the action to use.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e4e0c57ce9902ca546bf42cba9e59263c8b6849e1ae751d5faae0046e308e5b)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument node_version", value=node_version, expected_type=type_hints["node_version"])
            check_type(argname="argument always_auth", value=always_auth, expected_type=type_hints["always_auth"])
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
            check_type(argname="argument cache", value=cache, expected_type=type_hints["cache"])
            check_type(argname="argument cache_dependency_path", value=cache_dependency_path, expected_type=type_hints["cache_dependency_path"])
            check_type(argname="argument check_latest", value=check_latest, expected_type=type_hints["check_latest"])
            check_type(argname="argument node_version_file", value=node_version_file, expected_type=type_hints["node_version_file"])
            check_type(argname="argument npm_package_scope", value=npm_package_scope, expected_type=type_hints["npm_package_scope"])
            check_type(argname="argument registry_url", value=registry_url, expected_type=type_hints["registry_url"])
            check_type(argname="argument token", value=token, expected_type=type_hints["token"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "node_version": node_version,
        }
        if name is not None:
            self._values["name"] = name
        if always_auth is not None:
            self._values["always_auth"] = always_auth
        if architecture is not None:
            self._values["architecture"] = architecture
        if cache is not None:
            self._values["cache"] = cache
        if cache_dependency_path is not None:
            self._values["cache_dependency_path"] = cache_dependency_path
        if check_latest is not None:
            self._values["check_latest"] = check_latest
        if node_version_file is not None:
            self._values["node_version_file"] = node_version_file
        if npm_package_scope is not None:
            self._values["npm_package_scope"] = npm_package_scope
        if registry_url is not None:
            self._values["registry_url"] = registry_url
        if token is not None:
            self._values["token"] = token
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Display name for the action, shown in GitHub workflow logs for better readability.

        :stability: experimental

        Example::

            "Checkout Repository"
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_version(self) -> builtins.str:
        '''(experimental) The version of Node.js to use, specified as a version range or exact version.

        :stability: experimental
        '''
        result = self._values.get("node_version")
        assert result is not None, "Required property 'node_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def always_auth(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If true, forces authentication to the npm registry even when installing public packages.

        :stability: experimental
        '''
        result = self._values.get("always_auth")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def architecture(self) -> typing.Optional[builtins.str]:
        '''(experimental) The target architecture for the Node.js installation (e.g., ``x64`` or ``arm64``).

        :stability: experimental
        '''
        result = self._values.get("architecture")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cache(self) -> typing.Optional[builtins.str]:
        '''(experimental) The package manager to use for caching (``npm``, ``yarn``, or ``pnpm``).

        :stability: experimental
        '''
        result = self._values.get("cache")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cache_dependency_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) Optional path to dependency files for caching.

        This allows caching of multiple dependencies efficiently.

        :stability: experimental
        '''
        result = self._values.get("cache_dependency_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def check_latest(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If true, checks for the latest version matching the specified version.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("check_latest")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def node_version_file(self) -> typing.Optional[builtins.str]:
        '''(experimental) Optional path to a file containing the Node.js version to use. This is useful for dynamically specifying versions.

        :stability: experimental
        '''
        result = self._values.get("node_version_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def npm_package_scope(self) -> typing.Optional[builtins.str]:
        '''(experimental) Scope for the npm packages, useful for scoped packages in the registry.

        :stability: experimental
        '''
        result = self._values.get("npm_package_scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def registry_url(self) -> typing.Optional[builtins.str]:
        '''(experimental) The URL of the npm registry to authenticate against.

        :stability: experimental
        '''
        result = self._values.get("registry_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token(self) -> typing.Optional[builtins.str]:
        '''(experimental) Token for authentication with the npm registry.

        :stability: experimental
        '''
        result = self._values.get("token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies the version of the action to use.

        :stability: experimental
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SetupNodeV4Props(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SetupPythonV5(
    _Action_64902b3f,
    metaclass=jsii.JSIIMeta,
    jsii_type="github-actions-cdk.actions.SetupPythonV5",
):
    '''(experimental) Action class to configure Python within a GitHub Actions workflow.

    This action supports version specification, dependency caching, environment updates, and more.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        python_version: builtins.str,
        allow_prereleases: typing.Optional[builtins.bool] = None,
        architecture: typing.Optional[builtins.str] = None,
        cache: typing.Optional[builtins.str] = None,
        cache_dependency_path: typing.Optional[builtins.str] = None,
        check_latest: typing.Optional[builtins.bool] = None,
        python_version_file: typing.Optional[builtins.str] = None,
        token: typing.Optional[builtins.str] = None,
        update_environment: typing.Optional[builtins.bool] = None,
        version: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Initializes the SetupPython action instance.

        :param scope: - Scope in which this construct is defined.
        :param id: - Unique identifier for the action instance.
        :param python_version: (experimental) The version of Python to install, specified as a version range or exact version.
        :param allow_prereleases: (experimental) If true, allows pre-release versions of Python to be installed. Default: false
        :param architecture: (experimental) The target architecture for the Python installation (e.g., ``x64`` or ``arm64``).
        :param cache: (experimental) The package manager to use for caching dependencies (``pip``, ``pipenv``, or ``poetry``).
        :param cache_dependency_path: (experimental) Optional path to dependency files for caching.
        :param check_latest: (experimental) If true, checks for the latest version matching the specified version. Default: false
        :param python_version_file: (experimental) Optional path to a file containing the Python version to use. This is useful for dynamically specifying versions.
        :param token: (experimental) Token for authentication with package registries.
        :param update_environment: (experimental) If true, updates the environment with the installed Python version. Default: true
        :param version: (experimental) Specifies the version of the action to use.
        :param name: (experimental) Display name for the action, shown in GitHub workflow logs for better readability.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__958e586a89ee54a9c090bb32c57ad50f30fba363ab082ac4f248508f8130f2eb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SetupPythonV5Props(
            python_version=python_version,
            allow_prereleases=allow_prereleases,
            architecture=architecture,
            cache=cache,
            cache_dependency_path=cache_dependency_path,
            check_latest=check_latest,
            python_version_file=python_version_file,
            token=token,
            update_environment=update_environment,
            version=version,
            name=name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="IDENTIFIER")
    def IDENTIFIER(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "IDENTIFIER"))

    @builtins.property
    @jsii.member(jsii_name="allowPrereleases")
    def allow_prereleases(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "allowPrereleases"))

    @builtins.property
    @jsii.member(jsii_name="checkLatest")
    def check_latest(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "checkLatest"))

    @builtins.property
    @jsii.member(jsii_name="outputs")
    def outputs(self) -> "SetupPythonV5Outputs":
        '''(experimental) Retrieves the output parameters from the Setup Python action for use in subsequent workflow steps.

        :return: Outputs object containing ``pythonVersion``, ``cacheHit``, and ``pythonPath``.

        :stability: experimental
        '''
        return typing.cast("SetupPythonV5Outputs", jsii.get(self, "outputs"))

    @builtins.property
    @jsii.member(jsii_name="pythonVersion")
    def python_version(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "pythonVersion"))

    @builtins.property
    @jsii.member(jsii_name="updateEnvironment")
    def update_environment(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "updateEnvironment"))

    @builtins.property
    @jsii.member(jsii_name="architecture")
    def architecture(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "architecture"))

    @builtins.property
    @jsii.member(jsii_name="cache")
    def cache(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cache"))

    @builtins.property
    @jsii.member(jsii_name="cacheDependencyPath")
    def cache_dependency_path(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cacheDependencyPath"))

    @builtins.property
    @jsii.member(jsii_name="pythonVersionFile")
    def python_version_file(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pythonVersionFile"))

    @builtins.property
    @jsii.member(jsii_name="token")
    def token(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "token"))


@jsii.data_type(
    jsii_type="github-actions-cdk.actions.SetupPythonV5Outputs",
    jsii_struct_bases=[],
    name_mapping={
        "cache_hit": "cacheHit",
        "python_path": "pythonPath",
        "python_version": "pythonVersion",
    },
)
class SetupPythonV5Outputs:
    def __init__(
        self,
        *,
        cache_hit: builtins.str,
        python_path: builtins.str,
        python_version: builtins.str,
    ) -> None:
        '''(experimental) Outputs from the Setup Python action.

        This interface provides access to the installed Python version, cache hit status,
        and the path to the Python executable, which can be referenced in subsequent workflow steps.

        :param cache_hit: (experimental) Indicates if a cache was successfully hit during the action.
        :param python_path: (experimental) The file path to the Python executable.
        :param python_version: (experimental) The version of Python that was installed.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc9d10ab2d490988a3db6f4b674474936fad585c7466ddcd70c2d8fcc283cdf1)
            check_type(argname="argument cache_hit", value=cache_hit, expected_type=type_hints["cache_hit"])
            check_type(argname="argument python_path", value=python_path, expected_type=type_hints["python_path"])
            check_type(argname="argument python_version", value=python_version, expected_type=type_hints["python_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cache_hit": cache_hit,
            "python_path": python_path,
            "python_version": python_version,
        }

    @builtins.property
    def cache_hit(self) -> builtins.str:
        '''(experimental) Indicates if a cache was successfully hit during the action.

        :stability: experimental
        '''
        result = self._values.get("cache_hit")
        assert result is not None, "Required property 'cache_hit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def python_path(self) -> builtins.str:
        '''(experimental) The file path to the Python executable.

        :stability: experimental
        '''
        result = self._values.get("python_path")
        assert result is not None, "Required property 'python_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def python_version(self) -> builtins.str:
        '''(experimental) The version of Python that was installed.

        :stability: experimental
        '''
        result = self._values.get("python_version")
        assert result is not None, "Required property 'python_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SetupPythonV5Outputs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="github-actions-cdk.actions.SetupPythonV5Props",
    jsii_struct_bases=[_CommonActionProps_7122e708],
    name_mapping={
        "name": "name",
        "python_version": "pythonVersion",
        "allow_prereleases": "allowPrereleases",
        "architecture": "architecture",
        "cache": "cache",
        "cache_dependency_path": "cacheDependencyPath",
        "check_latest": "checkLatest",
        "python_version_file": "pythonVersionFile",
        "token": "token",
        "update_environment": "updateEnvironment",
        "version": "version",
    },
)
class SetupPythonV5Props(_CommonActionProps_7122e708):
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        python_version: builtins.str,
        allow_prereleases: typing.Optional[builtins.bool] = None,
        architecture: typing.Optional[builtins.str] = None,
        cache: typing.Optional[builtins.str] = None,
        cache_dependency_path: typing.Optional[builtins.str] = None,
        check_latest: typing.Optional[builtins.bool] = None,
        python_version_file: typing.Optional[builtins.str] = None,
        token: typing.Optional[builtins.str] = None,
        update_environment: typing.Optional[builtins.bool] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Configuration options for the Setup Python action within a GitHub Actions workflow.

        This interface extends common action properties to include options specific to Python setup,
        such as version specifications, caching, and environment updates.

        :param name: (experimental) Display name for the action, shown in GitHub workflow logs for better readability.
        :param python_version: (experimental) The version of Python to install, specified as a version range or exact version.
        :param allow_prereleases: (experimental) If true, allows pre-release versions of Python to be installed. Default: false
        :param architecture: (experimental) The target architecture for the Python installation (e.g., ``x64`` or ``arm64``).
        :param cache: (experimental) The package manager to use for caching dependencies (``pip``, ``pipenv``, or ``poetry``).
        :param cache_dependency_path: (experimental) Optional path to dependency files for caching.
        :param check_latest: (experimental) If true, checks for the latest version matching the specified version. Default: false
        :param python_version_file: (experimental) Optional path to a file containing the Python version to use. This is useful for dynamically specifying versions.
        :param token: (experimental) Token for authentication with package registries.
        :param update_environment: (experimental) If true, updates the environment with the installed Python version. Default: true
        :param version: (experimental) Specifies the version of the action to use.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9b4a72547007e73d31693a92bcd0d96c49b0372ce094263860c6185c8c4c439)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument python_version", value=python_version, expected_type=type_hints["python_version"])
            check_type(argname="argument allow_prereleases", value=allow_prereleases, expected_type=type_hints["allow_prereleases"])
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
            check_type(argname="argument cache", value=cache, expected_type=type_hints["cache"])
            check_type(argname="argument cache_dependency_path", value=cache_dependency_path, expected_type=type_hints["cache_dependency_path"])
            check_type(argname="argument check_latest", value=check_latest, expected_type=type_hints["check_latest"])
            check_type(argname="argument python_version_file", value=python_version_file, expected_type=type_hints["python_version_file"])
            check_type(argname="argument token", value=token, expected_type=type_hints["token"])
            check_type(argname="argument update_environment", value=update_environment, expected_type=type_hints["update_environment"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "python_version": python_version,
        }
        if name is not None:
            self._values["name"] = name
        if allow_prereleases is not None:
            self._values["allow_prereleases"] = allow_prereleases
        if architecture is not None:
            self._values["architecture"] = architecture
        if cache is not None:
            self._values["cache"] = cache
        if cache_dependency_path is not None:
            self._values["cache_dependency_path"] = cache_dependency_path
        if check_latest is not None:
            self._values["check_latest"] = check_latest
        if python_version_file is not None:
            self._values["python_version_file"] = python_version_file
        if token is not None:
            self._values["token"] = token
        if update_environment is not None:
            self._values["update_environment"] = update_environment
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Display name for the action, shown in GitHub workflow logs for better readability.

        :stability: experimental

        Example::

            "Checkout Repository"
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def python_version(self) -> builtins.str:
        '''(experimental) The version of Python to install, specified as a version range or exact version.

        :stability: experimental
        '''
        result = self._values.get("python_version")
        assert result is not None, "Required property 'python_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_prereleases(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If true, allows pre-release versions of Python to be installed.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("allow_prereleases")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def architecture(self) -> typing.Optional[builtins.str]:
        '''(experimental) The target architecture for the Python installation (e.g., ``x64`` or ``arm64``).

        :stability: experimental
        '''
        result = self._values.get("architecture")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cache(self) -> typing.Optional[builtins.str]:
        '''(experimental) The package manager to use for caching dependencies (``pip``, ``pipenv``, or ``poetry``).

        :stability: experimental
        '''
        result = self._values.get("cache")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cache_dependency_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) Optional path to dependency files for caching.

        :stability: experimental
        '''
        result = self._values.get("cache_dependency_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def check_latest(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If true, checks for the latest version matching the specified version.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("check_latest")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def python_version_file(self) -> typing.Optional[builtins.str]:
        '''(experimental) Optional path to a file containing the Python version to use.

        This is useful for dynamically specifying versions.

        :stability: experimental
        '''
        result = self._values.get("python_version_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token(self) -> typing.Optional[builtins.str]:
        '''(experimental) Token for authentication with package registries.

        :stability: experimental
        '''
        result = self._values.get("token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update_environment(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If true, updates the environment with the installed Python version.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("update_environment")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies the version of the action to use.

        :stability: experimental
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SetupPythonV5Props(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UploadArtifactV4(
    _Action_64902b3f,
    metaclass=jsii.JSIIMeta,
    jsii_type="github-actions-cdk.actions.UploadArtifactV4",
):
    '''(experimental) Upload action for GitHub Actions workflows, uploading a build artifact for use in later steps.

    :stability: experimental
    :remarks:

    This class allows configuration of the Upload action, supporting
    additional parameters for naming, paths, and artifact retention.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        path: builtins.str,
        artifact_name: typing.Optional[builtins.str] = None,
        compression_level: typing.Optional[jsii.Number] = None,
        if_no_files_found: typing.Optional[builtins.str] = None,
        include_hidden_files: typing.Optional[builtins.bool] = None,
        overwrite: typing.Optional[builtins.bool] = None,
        retention_days: typing.Optional[jsii.Number] = None,
        version: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Initializes a new instance of the Upload action.

        :param scope: - The scope in which to define this construct.
        :param id: - Unique identifier for the action.
        :param path: (experimental) The path or pattern describing files to upload.
        :param artifact_name: (experimental) Name of the artifact to upload. Default: "artifact"
        :param compression_level: (experimental) Compression level for artifact archiving, from 0 (no compression) to 9 (best compression). Default: 6
        :param if_no_files_found: (experimental) Behavior when no files match the provided path. Options: - "warn": Output a warning but do not fail the action. - "error": Fail the action with an error message. - "ignore": Do not output warnings or errors. Default: "warn"
        :param include_hidden_files: (experimental) If true, includes hidden files in the artifact. Default: false
        :param overwrite: (experimental) If true, deletes an existing artifact with the same name before uploading. Default: false
        :param retention_days: (experimental) Days after which the artifact will expire.
        :param version: (experimental) Specifies the version of the action to use.
        :param name: (experimental) Display name for the action, shown in GitHub workflow logs for better readability.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84bef44550bdaded7d55aa46e3d588426d424729cf0b4d79585f682d0d633496)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = UploadArtifactV4Props(
            path=path,
            artifact_name=artifact_name,
            compression_level=compression_level,
            if_no_files_found=if_no_files_found,
            include_hidden_files=include_hidden_files,
            overwrite=overwrite,
            retention_days=retention_days,
            version=version,
            name=name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="IDENTIFIER")
    def IDENTIFIER(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "IDENTIFIER"))

    @builtins.property
    @jsii.member(jsii_name="outputs")
    def outputs(self) -> "UploadArtifactV4Outputs":
        '''(experimental) Retrieves outputs of the Upload action.

        :return: ``UploadArtifactV4Outputs`` containing ``artifactId`` and ``artifactUrl`` for further use.

        :stability: experimental
        '''
        return typing.cast("UploadArtifactV4Outputs", jsii.get(self, "outputs"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @builtins.property
    @jsii.member(jsii_name="artifactName")
    def artifact_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "artifactName"))

    @builtins.property
    @jsii.member(jsii_name="compressionLevel")
    def compression_level(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "compressionLevel"))

    @builtins.property
    @jsii.member(jsii_name="ifNoFilesFound")
    def if_no_files_found(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ifNoFilesFound"))

    @builtins.property
    @jsii.member(jsii_name="includeHiddenFiles")
    def include_hidden_files(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "includeHiddenFiles"))

    @builtins.property
    @jsii.member(jsii_name="overwrite")
    def overwrite(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "overwrite"))

    @builtins.property
    @jsii.member(jsii_name="retentionDays")
    def retention_days(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retentionDays"))


@jsii.data_type(
    jsii_type="github-actions-cdk.actions.UploadArtifactV4Outputs",
    jsii_struct_bases=[],
    name_mapping={"artifact_id": "artifactId", "artifact_url": "artifactUrl"},
)
class UploadArtifactV4Outputs:
    def __init__(
        self,
        *,
        artifact_id: builtins.str,
        artifact_url: builtins.str,
    ) -> None:
        '''(experimental) Output structure for the Upload action.

        :param artifact_id: (experimental) Unique identifier for the uploaded artifact.
        :param artifact_url: (experimental) Download URL for the uploaded artifact.

        :stability: experimental
        :remarks:

        This interface defines specific outputs provided by the Upload action,
        including the ``artifactId`` and ``artifactUrl`` properties, which allow for
        retrieval of the artifact's identifier and URL.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9f68a38f6216910e5863804b1b3eb290f3e0f432a9c8077cde684f43f66db78)
            check_type(argname="argument artifact_id", value=artifact_id, expected_type=type_hints["artifact_id"])
            check_type(argname="argument artifact_url", value=artifact_url, expected_type=type_hints["artifact_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "artifact_id": artifact_id,
            "artifact_url": artifact_url,
        }

    @builtins.property
    def artifact_id(self) -> builtins.str:
        '''(experimental) Unique identifier for the uploaded artifact.

        :stability: experimental
        '''
        result = self._values.get("artifact_id")
        assert result is not None, "Required property 'artifact_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def artifact_url(self) -> builtins.str:
        '''(experimental) Download URL for the uploaded artifact.

        :stability: experimental
        '''
        result = self._values.get("artifact_url")
        assert result is not None, "Required property 'artifact_url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UploadArtifactV4Outputs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="github-actions-cdk.actions.UploadArtifactV4Props",
    jsii_struct_bases=[_CommonActionProps_7122e708],
    name_mapping={
        "name": "name",
        "path": "path",
        "artifact_name": "artifactName",
        "compression_level": "compressionLevel",
        "if_no_files_found": "ifNoFilesFound",
        "include_hidden_files": "includeHiddenFiles",
        "overwrite": "overwrite",
        "retention_days": "retentionDays",
        "version": "version",
    },
)
class UploadArtifactV4Props(_CommonActionProps_7122e708):
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        path: builtins.str,
        artifact_name: typing.Optional[builtins.str] = None,
        compression_level: typing.Optional[jsii.Number] = None,
        if_no_files_found: typing.Optional[builtins.str] = None,
        include_hidden_files: typing.Optional[builtins.bool] = None,
        overwrite: typing.Optional[builtins.bool] = None,
        retention_days: typing.Optional[jsii.Number] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Configuration properties for the Upload action in a GitHub Actions workflow.

        :param name: (experimental) Display name for the action, shown in GitHub workflow logs for better readability.
        :param path: (experimental) The path or pattern describing files to upload.
        :param artifact_name: (experimental) Name of the artifact to upload. Default: "artifact"
        :param compression_level: (experimental) Compression level for artifact archiving, from 0 (no compression) to 9 (best compression). Default: 6
        :param if_no_files_found: (experimental) Behavior when no files match the provided path. Options: - "warn": Output a warning but do not fail the action. - "error": Fail the action with an error message. - "ignore": Do not output warnings or errors. Default: "warn"
        :param include_hidden_files: (experimental) If true, includes hidden files in the artifact. Default: false
        :param overwrite: (experimental) If true, deletes an existing artifact with the same name before uploading. Default: false
        :param retention_days: (experimental) Days after which the artifact will expire.
        :param version: (experimental) Specifies the version of the action to use.

        :stability: experimental
        :remarks:

        ``UploadArtifactProps`` defines the various options available for the Upload action,
        including artifact naming, paths, retention, and compression settings.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ef506776442c01f09c83b5508dfa959639842220e35b2fc6757efb8d1617433)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument artifact_name", value=artifact_name, expected_type=type_hints["artifact_name"])
            check_type(argname="argument compression_level", value=compression_level, expected_type=type_hints["compression_level"])
            check_type(argname="argument if_no_files_found", value=if_no_files_found, expected_type=type_hints["if_no_files_found"])
            check_type(argname="argument include_hidden_files", value=include_hidden_files, expected_type=type_hints["include_hidden_files"])
            check_type(argname="argument overwrite", value=overwrite, expected_type=type_hints["overwrite"])
            check_type(argname="argument retention_days", value=retention_days, expected_type=type_hints["retention_days"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
        }
        if name is not None:
            self._values["name"] = name
        if artifact_name is not None:
            self._values["artifact_name"] = artifact_name
        if compression_level is not None:
            self._values["compression_level"] = compression_level
        if if_no_files_found is not None:
            self._values["if_no_files_found"] = if_no_files_found
        if include_hidden_files is not None:
            self._values["include_hidden_files"] = include_hidden_files
        if overwrite is not None:
            self._values["overwrite"] = overwrite
        if retention_days is not None:
            self._values["retention_days"] = retention_days
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Display name for the action, shown in GitHub workflow logs for better readability.

        :stability: experimental

        Example::

            "Checkout Repository"
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> builtins.str:
        '''(experimental) The path or pattern describing files to upload.

        :stability: experimental
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def artifact_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the artifact to upload.

        :default: "artifact"

        :stability: experimental
        '''
        result = self._values.get("artifact_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compression_level(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Compression level for artifact archiving, from 0 (no compression) to 9 (best compression).

        :default: 6

        :stability: experimental
        '''
        result = self._values.get("compression_level")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def if_no_files_found(self) -> typing.Optional[builtins.str]:
        '''(experimental) Behavior when no files match the provided path.

        Options:

        - "warn": Output a warning but do not fail the action.
        - "error": Fail the action with an error message.
        - "ignore": Do not output warnings or errors.

        :default: "warn"

        :stability: experimental
        '''
        result = self._values.get("if_no_files_found")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def include_hidden_files(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If true, includes hidden files in the artifact.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("include_hidden_files")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def overwrite(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If true, deletes an existing artifact with the same name before uploading.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("overwrite")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def retention_days(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Days after which the artifact will expire.

        :stability: experimental
        :remarks: 0 uses the repository default. Minimum 1 day, maximum 90 days.
        '''
        result = self._values.get("retention_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies the version of the action to use.

        :stability: experimental
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UploadArtifactV4Props(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AwsCloudFormationGitHubDeployV1",
    "AwsCloudFormationGitHubDeployV1Outputs",
    "AwsCloudFormationGitHubDeployV1Props",
    "CheckoutV4",
    "CheckoutV4Outputs",
    "CheckoutV4Props",
    "ConfigureAwsCredentialsV4",
    "ConfigureAwsCredentialsV4Outputs",
    "ConfigureAwsCredentialsV4Props",
    "DownloadArtifactV4",
    "DownloadArtifactV4Outputs",
    "DownloadArtifactV4Props",
    "SetupGoV5",
    "SetupGoV5Outputs",
    "SetupGoV5Props",
    "SetupNodeV4",
    "SetupNodeV4Outputs",
    "SetupNodeV4Props",
    "SetupPythonV5",
    "SetupPythonV5Outputs",
    "SetupPythonV5Props",
    "UploadArtifactV4",
    "UploadArtifactV4Outputs",
    "UploadArtifactV4Props",
]

publication.publish()

def _typecheckingstub__f33009cee36a7c9ceccab9957a36ae5b2f05c84cc7915b65aec817c79c1a847d(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    stack_name: builtins.str,
    template: builtins.str,
    capabilities: typing.Optional[builtins.str] = None,
    change_set_name: typing.Optional[builtins.str] = None,
    disable_rollback: typing.Optional[builtins.str] = None,
    http_proxy: typing.Optional[builtins.str] = None,
    no_delete_failed_changeset: typing.Optional[builtins.str] = None,
    no_execute_changeset: typing.Optional[builtins.str] = None,
    no_fail_on_empty_changeset: typing.Optional[builtins.str] = None,
    notification_arns: typing.Optional[builtins.str] = None,
    parameter_overrides: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[builtins.str] = None,
    termination_protection: typing.Optional[builtins.str] = None,
    timeout_in_minutes: typing.Optional[jsii.Number] = None,
    version: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9be8722b9c2c30737bd11aa1e091049660b5489c48cc4ccecdd739db5ee974db(
    *,
    stack_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a728f859f09227f2f94bce8cb1caca1952b0ef45f0b144edf9fda98c10f9de6(
    *,
    name: typing.Optional[builtins.str] = None,
    stack_name: builtins.str,
    template: builtins.str,
    capabilities: typing.Optional[builtins.str] = None,
    change_set_name: typing.Optional[builtins.str] = None,
    disable_rollback: typing.Optional[builtins.str] = None,
    http_proxy: typing.Optional[builtins.str] = None,
    no_delete_failed_changeset: typing.Optional[builtins.str] = None,
    no_execute_changeset: typing.Optional[builtins.str] = None,
    no_fail_on_empty_changeset: typing.Optional[builtins.str] = None,
    notification_arns: typing.Optional[builtins.str] = None,
    parameter_overrides: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[builtins.str] = None,
    termination_protection: typing.Optional[builtins.str] = None,
    timeout_in_minutes: typing.Optional[jsii.Number] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea038e71ccd09ea5713bc2dfca9f90de69d57ba876065a9b834ff5b9b7b9bc87(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    clean: typing.Optional[builtins.bool] = None,
    fetch_depth: typing.Optional[jsii.Number] = None,
    fetch_tags: typing.Optional[builtins.bool] = None,
    filter: typing.Optional[builtins.str] = None,
    github_server_url: typing.Optional[builtins.str] = None,
    lfs: typing.Optional[builtins.bool] = None,
    path: typing.Optional[builtins.str] = None,
    persist_credentials: typing.Optional[builtins.bool] = None,
    ref: typing.Optional[builtins.str] = None,
    repository: typing.Optional[builtins.str] = None,
    set_safe_directory: typing.Optional[builtins.bool] = None,
    show_progress: typing.Optional[builtins.bool] = None,
    sparse_checkout: typing.Optional[typing.Sequence[builtins.str]] = None,
    sparse_checkout_cone_mode: typing.Optional[builtins.bool] = None,
    ssh_key: typing.Optional[builtins.str] = None,
    ssh_known_hosts: typing.Optional[builtins.str] = None,
    ssh_strict: typing.Optional[builtins.bool] = None,
    ssh_user: typing.Optional[builtins.str] = None,
    submodules: typing.Optional[typing.Union[builtins.bool, builtins.str]] = None,
    token: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54616a2166aa05511f4ce80de3d19df7e9b2ad2a82723fe69c4d1511171c40e0(
    *,
    commit: builtins.str,
    ref: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__793e1f4d94ca6fd3f7e196da09f67c9aa4acaf68fd9a2b0264d3d18b68dc78d2(
    *,
    name: typing.Optional[builtins.str] = None,
    clean: typing.Optional[builtins.bool] = None,
    fetch_depth: typing.Optional[jsii.Number] = None,
    fetch_tags: typing.Optional[builtins.bool] = None,
    filter: typing.Optional[builtins.str] = None,
    github_server_url: typing.Optional[builtins.str] = None,
    lfs: typing.Optional[builtins.bool] = None,
    path: typing.Optional[builtins.str] = None,
    persist_credentials: typing.Optional[builtins.bool] = None,
    ref: typing.Optional[builtins.str] = None,
    repository: typing.Optional[builtins.str] = None,
    set_safe_directory: typing.Optional[builtins.bool] = None,
    show_progress: typing.Optional[builtins.bool] = None,
    sparse_checkout: typing.Optional[typing.Sequence[builtins.str]] = None,
    sparse_checkout_cone_mode: typing.Optional[builtins.bool] = None,
    ssh_key: typing.Optional[builtins.str] = None,
    ssh_known_hosts: typing.Optional[builtins.str] = None,
    ssh_strict: typing.Optional[builtins.bool] = None,
    ssh_user: typing.Optional[builtins.str] = None,
    submodules: typing.Optional[typing.Union[builtins.bool, builtins.str]] = None,
    token: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f723b68cc5060feca0773e3504ec3cab637cd329d1fc9cbabb7e4cdce4bbb843(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    aws_region: builtins.str,
    aws_access_key_id: typing.Optional[builtins.str] = None,
    aws_secret_access_key: typing.Optional[builtins.str] = None,
    aws_session_token: typing.Optional[builtins.str] = None,
    output_credentials: typing.Optional[builtins.bool] = None,
    role_duration_seconds: typing.Optional[builtins.str] = None,
    role_external_id: typing.Optional[builtins.str] = None,
    role_session_name: typing.Optional[builtins.str] = None,
    role_to_assume: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
    web_identity_token_file: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d918670eac1bc925c8ff150989e850a95d733be7100fde7739a6de34b65fe343(
    *,
    aws_access_key_id: builtins.str,
    aws_account_id: builtins.str,
    aws_secret_access_key: builtins.str,
    aws_session_token: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3c951820ed9d0fac84354bff07728164b63ce96b9a0b7074d1fd679131f013f(
    *,
    name: typing.Optional[builtins.str] = None,
    aws_region: builtins.str,
    aws_access_key_id: typing.Optional[builtins.str] = None,
    aws_secret_access_key: typing.Optional[builtins.str] = None,
    aws_session_token: typing.Optional[builtins.str] = None,
    output_credentials: typing.Optional[builtins.bool] = None,
    role_duration_seconds: typing.Optional[builtins.str] = None,
    role_external_id: typing.Optional[builtins.str] = None,
    role_session_name: typing.Optional[builtins.str] = None,
    role_to_assume: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
    web_identity_token_file: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75ddbcb870cc3986303a27a9f386945450807cc25d331c2c74d4604252866c3e(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    artifact_name: typing.Optional[builtins.str] = None,
    github_token: typing.Optional[builtins.str] = None,
    merge_multiple: typing.Optional[builtins.bool] = None,
    path: typing.Optional[builtins.str] = None,
    pattern: typing.Optional[builtins.str] = None,
    repository: typing.Optional[builtins.str] = None,
    run_id: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__630f831b0e35891deec9d936b23d192524aaee9f92ef964bb2dbf490a404e085(
    *,
    download_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e538a875e1d66d457ed6169280daa9f036b8abe5e7c691a77f7b40b8b0a382b(
    *,
    name: typing.Optional[builtins.str] = None,
    artifact_name: typing.Optional[builtins.str] = None,
    github_token: typing.Optional[builtins.str] = None,
    merge_multiple: typing.Optional[builtins.bool] = None,
    path: typing.Optional[builtins.str] = None,
    pattern: typing.Optional[builtins.str] = None,
    repository: typing.Optional[builtins.str] = None,
    run_id: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d098cb52550887ce4e35792740ea36a97eef44d2539af13aa4d53349f22ee9f2(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    go_version: builtins.str,
    architecture: typing.Optional[builtins.str] = None,
    cache: typing.Optional[builtins.bool] = None,
    cache_dependency_path: typing.Optional[builtins.str] = None,
    check_latest: typing.Optional[builtins.bool] = None,
    go_version_file: typing.Optional[builtins.str] = None,
    token: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb32ebe9fe1e7aa81e60daf556e177c2bc27c7167c6ac87223b7efc7b74d9080(
    *,
    cache_hit: builtins.str,
    go_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__193f087c7324cb14bfe6c01d286db48a15756f5b2e6a66f682f341f23bffb800(
    *,
    name: typing.Optional[builtins.str] = None,
    go_version: builtins.str,
    architecture: typing.Optional[builtins.str] = None,
    cache: typing.Optional[builtins.bool] = None,
    cache_dependency_path: typing.Optional[builtins.str] = None,
    check_latest: typing.Optional[builtins.bool] = None,
    go_version_file: typing.Optional[builtins.str] = None,
    token: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1ab7f5eb53c65e0b1962e11c2c602fff9b8e83df00b3c3369bcca6895bfd876(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    node_version: builtins.str,
    always_auth: typing.Optional[builtins.bool] = None,
    architecture: typing.Optional[builtins.str] = None,
    cache: typing.Optional[builtins.str] = None,
    cache_dependency_path: typing.Optional[builtins.str] = None,
    check_latest: typing.Optional[builtins.bool] = None,
    node_version_file: typing.Optional[builtins.str] = None,
    npm_package_scope: typing.Optional[builtins.str] = None,
    registry_url: typing.Optional[builtins.str] = None,
    token: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33f67a423382aad4c4a76bd53e1f611bf55398796e7444cb580a0b3201f380d6(
    *,
    cache_hit: builtins.str,
    node_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e4e0c57ce9902ca546bf42cba9e59263c8b6849e1ae751d5faae0046e308e5b(
    *,
    name: typing.Optional[builtins.str] = None,
    node_version: builtins.str,
    always_auth: typing.Optional[builtins.bool] = None,
    architecture: typing.Optional[builtins.str] = None,
    cache: typing.Optional[builtins.str] = None,
    cache_dependency_path: typing.Optional[builtins.str] = None,
    check_latest: typing.Optional[builtins.bool] = None,
    node_version_file: typing.Optional[builtins.str] = None,
    npm_package_scope: typing.Optional[builtins.str] = None,
    registry_url: typing.Optional[builtins.str] = None,
    token: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__958e586a89ee54a9c090bb32c57ad50f30fba363ab082ac4f248508f8130f2eb(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    python_version: builtins.str,
    allow_prereleases: typing.Optional[builtins.bool] = None,
    architecture: typing.Optional[builtins.str] = None,
    cache: typing.Optional[builtins.str] = None,
    cache_dependency_path: typing.Optional[builtins.str] = None,
    check_latest: typing.Optional[builtins.bool] = None,
    python_version_file: typing.Optional[builtins.str] = None,
    token: typing.Optional[builtins.str] = None,
    update_environment: typing.Optional[builtins.bool] = None,
    version: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc9d10ab2d490988a3db6f4b674474936fad585c7466ddcd70c2d8fcc283cdf1(
    *,
    cache_hit: builtins.str,
    python_path: builtins.str,
    python_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9b4a72547007e73d31693a92bcd0d96c49b0372ce094263860c6185c8c4c439(
    *,
    name: typing.Optional[builtins.str] = None,
    python_version: builtins.str,
    allow_prereleases: typing.Optional[builtins.bool] = None,
    architecture: typing.Optional[builtins.str] = None,
    cache: typing.Optional[builtins.str] = None,
    cache_dependency_path: typing.Optional[builtins.str] = None,
    check_latest: typing.Optional[builtins.bool] = None,
    python_version_file: typing.Optional[builtins.str] = None,
    token: typing.Optional[builtins.str] = None,
    update_environment: typing.Optional[builtins.bool] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84bef44550bdaded7d55aa46e3d588426d424729cf0b4d79585f682d0d633496(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    path: builtins.str,
    artifact_name: typing.Optional[builtins.str] = None,
    compression_level: typing.Optional[jsii.Number] = None,
    if_no_files_found: typing.Optional[builtins.str] = None,
    include_hidden_files: typing.Optional[builtins.bool] = None,
    overwrite: typing.Optional[builtins.bool] = None,
    retention_days: typing.Optional[jsii.Number] = None,
    version: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9f68a38f6216910e5863804b1b3eb290f3e0f432a9c8077cde684f43f66db78(
    *,
    artifact_id: builtins.str,
    artifact_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ef506776442c01f09c83b5508dfa959639842220e35b2fc6757efb8d1617433(
    *,
    name: typing.Optional[builtins.str] = None,
    path: builtins.str,
    artifact_name: typing.Optional[builtins.str] = None,
    compression_level: typing.Optional[jsii.Number] = None,
    if_no_files_found: typing.Optional[builtins.str] = None,
    include_hidden_files: typing.Optional[builtins.bool] = None,
    overwrite: typing.Optional[builtins.bool] = None,
    retention_days: typing.Optional[jsii.Number] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
