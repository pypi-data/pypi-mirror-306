r'''
# 🚧 GitHub Actions CDK

**github-actions-cdk** is a TypeScript library that simplifies the creation and management of GitHub Actions workflows using Constructs. With this library, developers can define workflows in a structured and type-safe manner, making it easier to automate CI/CD pipelines on GitHub. It also includes Python bindings for developers who prefer working in Python.

## Features

* **Type-Safe Workflows**: Leverage TypeScript's strong typing to define your GitHub Actions workflows and ensure correctness.
* **Python Bindings**: Access the same powerful constructs and features in Python, allowing seamless integration for Python developers.
* **Modular Design**: Easily create and manage jobs, triggers, and options for your workflows.

## Installation

To get started with `github-actions-cdk`, install the package using npm or yarn for TypeScript, or pip for Python:

### TypeScript

```bash
npm install github-actions-cdk
```

or

```bash
yarn add github-actions-cdk
```

### Python

```bash
pip install github-actions-cdk
```

## Getting Started

### Basic Usage (TypeScript)

Here's a simple example of how to create a GitHub Actions workflow using `github-actions-cdk` in TypeScript::

```python
import { PermissionLevel, Project, actions } from 'github-actions-cdk';

const project = new Project({
  //additionalChecks: true,
});

const workflow = project.addWorkflow("build", {
  name: "Build",
  triggers: {
    push: { branches: ["main"] },
    workflowDispatch: {},
  },
  permissions: {
    contents: PermissionLevel.READ,
  },
});

const job = workflow.addJob("build", {
  env: {
    CI: "true",
  },
});

new actions.CheckoutV4(job, "checkout", {
  name: "Checkout Code",
});

const setupNode = new actions.SetupNodeV4(job, "setup-node", {
  name: "Set up Node.js",
  nodeVersion: "20.x",
});

job.addOutput("node-version", setupNode.outputs.nodeVersion);

project.synth();
```

### Basic Usage (Python)

Here's how to create a GitHub Actions workflow using `github-actions-cdk` in Python:

```python
from github_actions_cdk import Project, PermissionLevel
from github_actions_cdk.actions import CheckoutV4, SetupNodeV4

project = Project(
    #additional_checks=True,
)

workflow = project.add_workflow(
    id="build",
    name="Build",
    triggers={
        "push": {
            "branches": ["main"],
        }
    },
    permissions={
        "contents": PermissionLevel.READ,
    }
)

job = workflow.add_job(
    id="build",
    env={
        "CI": "true",
    },
)

CheckoutV4(
    scope=job,
    id="checkout",
    name="Checkout Code",
)

setup_node = SetupNodeV4(
    scope=job,
    id="setup-node",
    name="Set up Node.js",
    node_version="14.x",
)

job.add_output("node-version", setup_node.outputs.node_version)

project.synth()
```

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


@jsii.enum(jsii_type="github-actions-cdk.AnnotationMetadataEntryType")
class AnnotationMetadataEntryType(enum.Enum):
    '''(experimental) Enumeration of annotation metadata entry types.

    :stability: experimental
    '''

    INFO = "INFO"
    '''
    :stability: experimental
    '''
    WARN = "WARN"
    '''
    :stability: experimental
    '''
    ERROR = "ERROR"
    '''
    :stability: experimental
    '''


class Annotations(metaclass=jsii.JSIIMeta, jsii_type="github-actions-cdk.Annotations"):
    '''(experimental) Manages annotations for a given construct scope, allowing for structured logging of informational, warning, and error messages.

    :stability: experimental
    '''

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, scope: _constructs_77d1e7e8.IConstruct) -> "Annotations":
        '''(experimental) Retrieves an instance of ``Annotations`` for the specified construct scope.

        :param scope: The construct scope for which annotations will be managed.

        :return: An instance of ``Annotations`` associated with the given scope.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41853ff7ac51646114947d7ccb872e1de9083a5c4900057f8d8a456318e444b1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast("Annotations", jsii.sinvoke(cls, "of", [scope]))

    @jsii.member(jsii_name="addError")
    def add_error(self, message: builtins.str) -> None:
        '''(experimental) Adds an error message to the annotations.

        :param message: The message to be logged as an error.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf15371b0b32189247fd2fa5d7da361f441b75c8466eb2d95e290c7c5925e1a5)
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
        return typing.cast(None, jsii.invoke(self, "addError", [message]))

    @jsii.member(jsii_name="addInfo")
    def add_info(self, message: builtins.str) -> None:
        '''(experimental) Adds an informational message to the annotations.

        :param message: The message to be logged as information.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cd7b68a0f961ca03a01bb4a2848df3543dd010a8cc04387dae7427a33a274c5)
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
        return typing.cast(None, jsii.invoke(self, "addInfo", [message]))

    @jsii.member(jsii_name="addWarning")
    def add_warning(self, message: builtins.str) -> None:
        '''(experimental) Adds a warning message to the annotations.

        :param message: The message to be logged as a warning.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8fb2edf6217e6883f8480c7c1e3ec856adcc99d2f697a15a82ad4ba3dd9d99e)
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
        return typing.cast(None, jsii.invoke(self, "addWarning", [message]))


class Aspects(metaclass=jsii.JSIIMeta, jsii_type="github-actions-cdk.Aspects"):
    '''(experimental) Manages aspects applied to CDK construct scopes.

    Aspects can modify constructs before they are synthesized.

    :stability: experimental
    '''

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, scope: _constructs_77d1e7e8.IConstruct) -> "Aspects":
        '''(experimental) Retrieves the ``Aspects`` instance associated with a given construct scope.

        If no instance exists, it creates one.

        :param scope: The construct scope for which aspects will be managed.

        :return: The ``Aspects`` instance for the specified scope.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9849ad7742ade5708dc29c2c349592e867841c1351e736e2595c097a43a8a697)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast("Aspects", jsii.sinvoke(cls, "of", [scope]))

    @jsii.member(jsii_name="add")
    def add(self, aspect: "IAspect") -> None:
        '''(experimental) Adds an aspect to be applied to this scope before synthesis.

        :param aspect: The aspect to add.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2cd0e82cb0e76c6e1c9570a01b80475e7d91b7f38af5045f26e006bc742abde)
            check_type(argname="argument aspect", value=aspect, expected_type=type_hints["aspect"])
        return typing.cast(None, jsii.invoke(self, "add", [aspect]))

    @builtins.property
    @jsii.member(jsii_name="all")
    def all(self) -> typing.List["IAspect"]:
        '''(experimental) Retrieves all aspects directly applied to this scope.

        :return: An array of all aspects applied.

        :stability: experimental
        '''
        return typing.cast(typing.List["IAspect"], jsii.get(self, "all"))


@jsii.data_type(
    jsii_type="github-actions-cdk.CheckRunOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class CheckRunOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Options for check run events.

        :param types: (experimental) Activity types to trigger on. Default: - triggers on all activity types

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5072f3495f4b3ba39176b029f0940e9c79221c2d0e31e596908947c243e493d1)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Activity types to trigger on.

        :default: - triggers on all activity types

        :stability: experimental
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CheckRunOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="github-actions-cdk.CheckSuiteOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class CheckSuiteOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Options for check suite events.

        :param types: (experimental) Activity types to trigger on. Default: - triggers on all activity types

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e104de4e65a228ba7996b869572411dc7ad5e1a2a7d6121de1f6ccd55f0e0e0)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Activity types to trigger on.

        :default: - triggers on all activity types

        :stability: experimental
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CheckSuiteOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="github-actions-cdk.CommonActionProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class CommonActionProps:
    def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
        '''(experimental) Base configuration properties shared across GitHub Actions.

        :param name: (experimental) Display name for the action, shown in GitHub workflow logs for better readability.

        :stability: experimental
        :remarks:

        The ``CommonActionProps`` interface defines the basic, reusable properties that can be used across various
        GitHub Actions, including a customizable ``name`` for the action.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c2457d2237bc9a4fbe495a7ad14440d0b2d6772b6a04f06098aa85b34837ac3)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Display name for the action, shown in GitHub workflow logs for better readability.

        :stability: experimental

        Example::

            "Checkout Repository"
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CommonActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="github-actions-cdk.CommonStepProps",
    jsii_struct_bases=[],
    name_mapping={
        "condition": "condition",
        "continue_on_error": "continueOnError",
        "env": "env",
        "name": "name",
        "timeout_minutes": "timeoutMinutes",
    },
)
class CommonStepProps:
    def __init__(
        self,
        *,
        condition: typing.Optional[builtins.str] = None,
        continue_on_error: typing.Optional[builtins.bool] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        timeout_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Common properties for all step types in a GitHub Actions workflow job.

        :param condition: (experimental) Conditional expression to determine if the step should run (equivalent to ``if`` in GitHub Actions). Supports GitHub Actions expressions, e.g., ``${{ success() }}``.
        :param continue_on_error: (experimental) Whether the job should continue if this step fails. Default: false
        :param env: (experimental) Environment variables specific to this step, overriding job-level or workflow-level variables.
        :param name: (experimental) A descriptive name for the step, displayed in the GitHub Actions UI.
        :param timeout_minutes: (experimental) Maximum execution time for the step, in minutes.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4461e91974812e072653647f48469feee51054f06cb5f13a7cad6c2175e8290b)
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument continue_on_error", value=continue_on_error, expected_type=type_hints["continue_on_error"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument timeout_minutes", value=timeout_minutes, expected_type=type_hints["timeout_minutes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if condition is not None:
            self._values["condition"] = condition
        if continue_on_error is not None:
            self._values["continue_on_error"] = continue_on_error
        if env is not None:
            self._values["env"] = env
        if name is not None:
            self._values["name"] = name
        if timeout_minutes is not None:
            self._values["timeout_minutes"] = timeout_minutes

    @builtins.property
    def condition(self) -> typing.Optional[builtins.str]:
        '''(experimental) Conditional expression to determine if the step should run (equivalent to ``if`` in GitHub Actions).

        Supports GitHub Actions expressions, e.g., ``${{ success() }}``.

        :stability: experimental

        Example::

            "${{ github.event_name == 'push' }}"
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def continue_on_error(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the job should continue if this step fails.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("continue_on_error")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Environment variables specific to this step, overriding job-level or workflow-level variables.

        :stability: experimental

        Example::

            { "NODE_ENV": "production" }
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A descriptive name for the step, displayed in the GitHub Actions UI.

        :stability: experimental

        Example::

            "Install dependencies"
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout_minutes(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Maximum execution time for the step, in minutes.

        :stability: experimental

        Example::

            10
        '''
        result = self._values.get("timeout_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CommonStepProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Component(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="github-actions-cdk.Component",
):
    '''(experimental) Abstract class representing a GitHub Actions CDK Component.

    :stability: experimental
    :remarks:

    The ``Component`` class is a foundational construct for defining reusable elements in
    GitHub Actions workflows. It extends the base ``Construct`` class, adding unique
    identifiers, type metadata, and markers for internal component identification.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Initializes a new ``Component`` instance.

        :param scope: - The construct scope in which this component is defined.
        :param id: - The unique identifier for this component. If not provided, an auto-generated ID based on the component name and scope will be used.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cead5b79c90c5d033e0e67c6a4b6ab32d75b9b25a356a33e670e380460cbd641)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [scope, id])

    @jsii.member(jsii_name="isComponent")
    @builtins.classmethod
    def is_component(cls, x: typing.Any) -> builtins.bool:
        '''(experimental) Checks if an object is an instance of ``Component``.

        :param x: - The object to check.

        :return: ``true`` if ``x`` is a ``Component``; otherwise, ``false``.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fdef1626108471936d90bdb773b97c0ad75e293b12de823502fcf8c725662c2)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isComponent", [x]))

    @jsii.member(jsii_name="addOverride")
    def add_override(self, path: builtins.str, value: typing.Any) -> None:
        '''(experimental) Adds or updates an override to the component configuration at a specified path.

        :param path: - Dot-separated path specifying where the override should be applied.
        :param value: - The value to set at the specified path.

        :stability: experimental
        :throws: Error if the provided path is an empty or non-string value.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2447762264aa67d0f00dbe099516e25b1326d1e83c0df0016a54fd25b6de84ac)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "addOverride", [path, value]))

    @builtins.property
    @jsii.member(jsii_name="rawOverrides")
    def _raw_overrides(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''(experimental) Holds overrides for properties, allowing deep customization of component configuration.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "rawOverrides"))


class _ComponentProxy(Component):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, Component).__jsii_proxy_class__ = lambda : _ComponentProxy


@jsii.data_type(
    jsii_type="github-actions-cdk.ConcurrencyOptions",
    jsii_struct_bases=[],
    name_mapping={"group": "group", "cancel_in_progress": "cancelInProgress"},
)
class ConcurrencyOptions:
    def __init__(
        self,
        *,
        group: builtins.str,
        cancel_in_progress: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options for job concurrency control in GitHub Actions workflows.

        GitHub Actions concurrency allows you to limit and control the number of jobs or workflows
        that can run simultaneously within a specified concurrency group. When concurrency is enabled,
        GitHub will cancel or queue jobs to avoid duplicate or conflicting runs, ensuring that only
        one job from the group runs at a time.

        For further details, see the GitHub Actions concurrency documentation:

        :param group: (experimental) The concurrency group to use for the job. The ``group`` property defines a unique identifier for the concurrency group. Only one job or workflow within the same concurrency group will run at a time. This group can be a simple string or a dynamically generated value using expressions.
        :param cancel_in_progress: (experimental) Specifies whether to cancel any currently running jobs or workflows in the same concurrency group. If set to ``true``, any currently running jobs or workflows within the same concurrency group will be canceled in favor of the latest job. If set to ``false`` or not provided, jobs will be queued to wait until any currently running jobs in the group complete. Default: false

        :see: https://docs.github.com/en/actions/using-jobs/using-concurrency
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b13408e5c019460595cf165919cb1c57a2410148d6fb00d9d9defcb7d65e776)
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
            check_type(argname="argument cancel_in_progress", value=cancel_in_progress, expected_type=type_hints["cancel_in_progress"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "group": group,
        }
        if cancel_in_progress is not None:
            self._values["cancel_in_progress"] = cancel_in_progress

    @builtins.property
    def group(self) -> builtins.str:
        '''(experimental) The concurrency group to use for the job.

        The ``group`` property defines a unique identifier for the concurrency group. Only one job
        or workflow within the same concurrency group will run at a time. This group can be a
        simple string or a dynamically generated value using expressions.

        :stability: experimental

        Example::

            // Use an expression to create a dynamic group for each branch
            group: "${{ github.ref }}"
        '''
        result = self._values.get("group")
        assert result is not None, "Required property 'group' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cancel_in_progress(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether to cancel any currently running jobs or workflows in the same concurrency group.

        If set to ``true``, any currently running jobs or workflows within the same concurrency group
        will be canceled in favor of the latest job. If set to ``false`` or not provided, jobs will
        be queued to wait until any currently running jobs in the group complete.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("cancel_in_progress")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConcurrencyOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="github-actions-cdk.ContainerCredentials",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "username": "username"},
)
class ContainerCredentials:
    def __init__(self, *, password: builtins.str, username: builtins.str) -> None:
        '''(experimental) Credentials for authenticating with Docker registries.

        :param password: (experimental) Docker registry password.
        :param username: (experimental) Docker registry username.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5997eadaf75d9e6cd05815d9747672927e15adfd92719380a1dbbd3e31d9ec3)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "password": password,
            "username": username,
        }

    @builtins.property
    def password(self) -> builtins.str:
        '''(experimental) Docker registry password.

        :stability: experimental
        '''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''(experimental) Docker registry username.

        :stability: experimental
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="github-actions-cdk.ContainerOptions",
    jsii_struct_bases=[],
    name_mapping={
        "image": "image",
        "credentials": "credentials",
        "env": "env",
        "options": "options",
        "ports": "ports",
        "volumes": "volumes",
    },
)
class ContainerOptions:
    def __init__(
        self,
        *,
        image: builtins.str,
        credentials: typing.Optional[typing.Union[ContainerCredentials, typing.Dict[builtins.str, typing.Any]]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        options: typing.Optional[typing.Sequence[builtins.str]] = None,
        ports: typing.Optional[typing.Sequence[jsii.Number]] = None,
        volumes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Configuration options for a Docker container used in the job.

        :param image: (experimental) Docker image to run within the job.
        :param credentials: (experimental) Credentials for container registry authentication.
        :param env: (experimental) Environment variables set within the container.
        :param options: (experimental) Additional Docker options for the container. Refer to Docker's documentation for a list of supported options.
        :param ports: (experimental) Ports exposed by the container.
        :param volumes: (experimental) Volumes attached to the container, enabling data sharing. Each entry specifies a ``<source>:<destinationPath>`` mapping.

        :stability: experimental
        '''
        if isinstance(credentials, dict):
            credentials = ContainerCredentials(**credentials)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5f7e57053d743d397fc21ea95452cce83840076921ca452abe46d7200ba007e)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument options", value=options, expected_type=type_hints["options"])
            check_type(argname="argument ports", value=ports, expected_type=type_hints["ports"])
            check_type(argname="argument volumes", value=volumes, expected_type=type_hints["volumes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image": image,
        }
        if credentials is not None:
            self._values["credentials"] = credentials
        if env is not None:
            self._values["env"] = env
        if options is not None:
            self._values["options"] = options
        if ports is not None:
            self._values["ports"] = ports
        if volumes is not None:
            self._values["volumes"] = volumes

    @builtins.property
    def image(self) -> builtins.str:
        '''(experimental) Docker image to run within the job.

        :stability: experimental
        '''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def credentials(self) -> typing.Optional[ContainerCredentials]:
        '''(experimental) Credentials for container registry authentication.

        :stability: experimental
        '''
        result = self._values.get("credentials")
        return typing.cast(typing.Optional[ContainerCredentials], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Environment variables set within the container.

        :stability: experimental
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def options(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Additional Docker options for the container.

        Refer to Docker's documentation for a list of supported options.

        :see: https://docs.docker.com/engine/reference/commandline/create/#options
        :stability: experimental
        '''
        result = self._values.get("options")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ports(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''(experimental) Ports exposed by the container.

        :stability: experimental
        '''
        result = self._values.get("ports")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def volumes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Volumes attached to the container, enabling data sharing.

        Each entry specifies a ``<source>:<destinationPath>`` mapping.

        :stability: experimental
        '''
        result = self._values.get("volumes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Cron(metaclass=jsii.JSIIMeta, jsii_type="github-actions-cdk.Cron"):
    '''(experimental) The Cron class provides a structure to define, validate, and manipulate cron expressions.

    It includes pre-defined schedules and supports custom cron expressions.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        day: typing.Optional[builtins.str] = None,
        hour: typing.Optional[builtins.str] = None,
        minute: typing.Optional[builtins.str] = None,
        month: typing.Optional[builtins.str] = None,
        week_day: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Constructs a Cron instance with each field defaulting to '*' if not specified.

        :param day: 
        :param hour: 
        :param minute: 
        :param month: 
        :param week_day: 

        :stability: experimental
        '''
        options = CronOptions(
            day=day, hour=hour, minute=minute, month=month, week_day=week_day
        )

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="fromExpression")
    @builtins.classmethod
    def from_expression(cls, expression: builtins.str) -> "Cron":
        '''(experimental) Parses a cron expression string into a Cron instance.

        Supports standard POSIX format and special strings like "@hourly".

        :param expression: A valid cron expression string (5 fields or predefined like "@hourly").

        :return: A new Cron instance.

        :stability: experimental
        :throws: Error if the expression does not have exactly 5 fields and is not a recognized special string.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__421e7476c56b104ee34b40b641f796adb4f6ed1124a2b669faba030276256f6c)
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
        return typing.cast("Cron", jsii.sinvoke(cls, "fromExpression", [expression]))

    @jsii.member(jsii_name="fromFields")
    @builtins.classmethod
    def from_fields(
        cls,
        *,
        day: typing.Optional[builtins.str] = None,
        hour: typing.Optional[builtins.str] = None,
        minute: typing.Optional[builtins.str] = None,
        month: typing.Optional[builtins.str] = None,
        week_day: typing.Optional[builtins.str] = None,
    ) -> "Cron":
        '''(experimental) Creates a Cron instance from provided cron options.

        :param day: 
        :param hour: 
        :param minute: 
        :param month: 
        :param week_day: 

        :return: A new Cron instance with the specified options.

        :stability: experimental
        '''
        options = CronOptions(
            day=day, hour=hour, minute=minute, month=month, week_day=week_day
        )

        return typing.cast("Cron", jsii.sinvoke(cls, "fromFields", [options]))

    @jsii.member(jsii_name="isValidExpression")
    @builtins.classmethod
    def is_valid_expression(cls, expression: builtins.str) -> builtins.bool:
        '''(experimental) Validates a POSIX cron expression string, checking adherence to constraints for each field.

        :param expression: A cron expression string to validate (5 fields).

        :return: True if the cron expression is valid, otherwise false.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a72dec72fc7f64420284eadcea6911406a89268b4330d95e815b45a734008dbd)
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isValidExpression", [expression]))

    @jsii.member(jsii_name="toJSON")
    def to_json(self) -> builtins.str:
        '''(experimental) Converts the cron expression to a JSON-compatible string.

        :return: The cron expression in string format, suitable for JSON.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toJSON", []))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Returns the cron expression as a single string in standard cron format.

        :return: The cron expression string.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DAILY")
    def DAILY(cls) -> "Cron":
        '''(experimental) A cron expression that triggers every day, at midnight.

        Expression: ``0 0 * * *`` - This will run every day at 00:00.

        :stability: experimental
        '''
        return typing.cast("Cron", jsii.sget(cls, "DAILY"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="HOURLY")
    def HOURLY(cls) -> "Cron":
        '''(experimental) A cron expression that triggers every hour, at the start of the hour.

        Expression: ``0 * * * *`` - This will run at 00:00, 01:00, 02:00, etc.

        :stability: experimental
        '''
        return typing.cast("Cron", jsii.sget(cls, "HOURLY"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MONTHLY")
    def MONTHLY(cls) -> "Cron":
        '''(experimental) A cron expression that triggers on the first day of every month at midnight.

        Expression: ``0 0 1 * *`` - This will run on the first day of every month at 00:00.

        :stability: experimental
        '''
        return typing.cast("Cron", jsii.sget(cls, "MONTHLY"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="WEEKLY")
    def WEEKLY(cls) -> "Cron":
        '''(experimental) A cron expression that triggers every week, on Sunday at midnight.

        Expression: ``0 0 * * 0`` - This will run every Sunday at 00:00.

        :stability: experimental
        '''
        return typing.cast("Cron", jsii.sget(cls, "WEEKLY"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="YEARLY")
    def YEARLY(cls) -> "Cron":
        '''(experimental) A cron expression that triggers once a year, on January 1st at midnight.

        Expression: ``0 0 1 1 *`` - This will run on January 1st every year at 00:00.

        :stability: experimental
        '''
        return typing.cast("Cron", jsii.sget(cls, "YEARLY"))

    @builtins.property
    @jsii.member(jsii_name="day")
    def day(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "day"))

    @builtins.property
    @jsii.member(jsii_name="hour")
    def hour(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "hour"))

    @builtins.property
    @jsii.member(jsii_name="minute")
    def minute(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "minute"))

    @builtins.property
    @jsii.member(jsii_name="month")
    def month(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "month"))

    @builtins.property
    @jsii.member(jsii_name="weekDay")
    def week_day(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "weekDay"))


@jsii.data_type(
    jsii_type="github-actions-cdk.CronOptions",
    jsii_struct_bases=[],
    name_mapping={
        "day": "day",
        "hour": "hour",
        "minute": "minute",
        "month": "month",
        "week_day": "weekDay",
    },
)
class CronOptions:
    def __init__(
        self,
        *,
        day: typing.Optional[builtins.str] = None,
        hour: typing.Optional[builtins.str] = None,
        minute: typing.Optional[builtins.str] = None,
        month: typing.Optional[builtins.str] = None,
        week_day: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) CronOptions interface defines the structure for specifying cron fields.

        Each field is optional and, if omitted, defaults to '*'.

        :param day: 
        :param hour: 
        :param minute: 
        :param month: 
        :param week_day: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f87d77789ba0ef97f504cc1ff5b1ad08e4c6aaf974d775c90a3fa4d819bc2d9)
            check_type(argname="argument day", value=day, expected_type=type_hints["day"])
            check_type(argname="argument hour", value=hour, expected_type=type_hints["hour"])
            check_type(argname="argument minute", value=minute, expected_type=type_hints["minute"])
            check_type(argname="argument month", value=month, expected_type=type_hints["month"])
            check_type(argname="argument week_day", value=week_day, expected_type=type_hints["week_day"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if day is not None:
            self._values["day"] = day
        if hour is not None:
            self._values["hour"] = hour
        if minute is not None:
            self._values["minute"] = minute
        if month is not None:
            self._values["month"] = month
        if week_day is not None:
            self._values["week_day"] = week_day

    @builtins.property
    def day(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("day")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hour(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("hour")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def minute(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("minute")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def month(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("month")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def week_day(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("week_day")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CronOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="github-actions-cdk.CronScheduleOptions",
    jsii_struct_bases=[],
    name_mapping={"cron": "cron"},
)
class CronScheduleOptions:
    def __init__(self, *, cron: Cron) -> None:
        '''(experimental) Options for configuring CRON schedule.

        :param cron: (experimental) CRON expression to define workflow schedule.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__199600a8fe0c62df3cbff7bfcacbbf2f8e629df37768f92e7958220548d6dd60)
            check_type(argname="argument cron", value=cron, expected_type=type_hints["cron"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cron": cron,
        }

    @builtins.property
    def cron(self) -> Cron:
        '''(experimental) CRON expression to define workflow schedule.

        :see: https://pubs.opengroup.org/onlinepubs/9699919799/utilities/crontab.html#tag_20_25_07
        :stability: experimental
        '''
        result = self._values.get("cron")
        assert result is not None, "Required property 'cron' is missing"
        return typing.cast(Cron, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CronScheduleOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="github-actions-cdk.Defaults",
    jsii_struct_bases=[],
    name_mapping={"run": "run"},
)
class Defaults:
    def __init__(
        self,
        *,
        run: typing.Optional[typing.Union["RunSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Default settings applied to all steps within a job.

        ``Defaults`` provides a consistent configuration that applies to every step in the job,
        ensuring uniformity in settings like ``shell`` and ``workingDirectory``. These settings
        can be overridden in individual steps as needed.

        :param run: (experimental) Default run settings to apply across all steps in the job. Use ``run`` to define the shell and working directory settings that should be applied to each step, unless overridden at the step level.

        :stability: experimental
        '''
        if isinstance(run, dict):
            run = RunSettings(**run)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37fef6d91b1101241267e5d35cbcd7e3ed2eb1139f4522bfcd355fc98907624f)
            check_type(argname="argument run", value=run, expected_type=type_hints["run"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if run is not None:
            self._values["run"] = run

    @builtins.property
    def run(self) -> typing.Optional["RunSettings"]:
        '''(experimental) Default run settings to apply across all steps in the job.

        Use ``run`` to define the shell and working directory settings that should
        be applied to each step, unless overridden at the step level.

        :stability: experimental
        '''
        result = self._values.get("run")
        return typing.cast(typing.Optional["RunSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Defaults(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="github-actions-cdk.Environment",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "url": "url"},
)
class Environment:
    def __init__(
        self,
        *,
        name: builtins.str,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Github environment with name and url.

        :param name: (experimental) Name of the environment.
        :param url: (experimental) The url for the environment.

        :see: https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#jobsjob_idenvironment
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e00484e77e735ea20fd6f2113bad3b33b25a952640e97df3f6ccb53bf88c5e22)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if url is not None:
            self._values["url"] = url

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) Name of the environment.

        :see: https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#example-using-environment-name-and-url
        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''(experimental) The url for the environment.

        :see: https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#example-using-environment-name-and-url
        :stability: experimental
        '''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Environment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Expression(metaclass=jsii.JSIIMeta, jsii_type="github-actions-cdk.Expression"):
    '''
    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromEnv")
    @builtins.classmethod
    def from_env(cls, name: builtins.str) -> builtins.str:
        '''
        :param name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__652ef72a750362b475687a33b055dad928a1e92d94365a9f021ba54bc2531888)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "fromEnv", [name]))

    @jsii.member(jsii_name="fromGitHub")
    @builtins.classmethod
    def from_git_hub(cls, name: builtins.str) -> builtins.str:
        '''
        :param name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c052e3e0c8198428a3912fd3a6ae477cb8b8713c50b31805c6711109db7b56f)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "fromGitHub", [name]))

    @jsii.member(jsii_name="fromSecrets")
    @builtins.classmethod
    def from_secrets(cls, name: builtins.str) -> builtins.str:
        '''
        :param name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a19e270a038d7235d302888dbc8430c67f616419d9e0d7622fbe25210462244a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "fromSecrets", [name]))


@jsii.interface(jsii_type="github-actions-cdk.IAspect")
class IAspect(typing_extensions.Protocol):
    '''(experimental) Represents an aspect that can visit constructs in the CDK tree.

    :stability: experimental
    '''

    @jsii.member(jsii_name="visit")
    def visit(self, node: _constructs_77d1e7e8.IConstruct) -> None:
        '''(experimental) Visit a specific construct node.

        :param node: The construct to visit.

        :stability: experimental
        '''
        ...


class _IAspectProxy:
    '''(experimental) Represents an aspect that can visit constructs in the CDK tree.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "github-actions-cdk.IAspect"

    @jsii.member(jsii_name="visit")
    def visit(self, node: _constructs_77d1e7e8.IConstruct) -> None:
        '''(experimental) Visit a specific construct node.

        :param node: The construct to visit.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75fc1df357426ae5fccdc448c6418fbf29e128e68fa95bc0e1036a13c512c920)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "visit", [node]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAspect).__jsii_proxy_class__ = lambda : _IAspectProxy


@jsii.interface(jsii_type="github-actions-cdk.IManifest")
class IManifest(typing_extensions.Protocol):
    '''(experimental) Represents the structure of the manifest, containing workflows and their version.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        '''(experimental) The version of the manifest format.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="workflows")
    def workflows(self) -> typing.Mapping[builtins.str, "WorkflowManifest"]:
        '''(experimental) A record mapping workflow IDs to their respective manifest details.

        :stability: experimental
        '''
        ...


class _IManifestProxy:
    '''(experimental) Represents the structure of the manifest, containing workflows and their version.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "github-actions-cdk.IManifest"

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        '''(experimental) The version of the manifest format.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="workflows")
    def workflows(self) -> typing.Mapping[builtins.str, "WorkflowManifest"]:
        '''(experimental) A record mapping workflow IDs to their respective manifest details.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, "WorkflowManifest"], jsii.get(self, "workflows"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IManifest).__jsii_proxy_class__ = lambda : _IManifestProxy


@jsii.interface(jsii_type="github-actions-cdk.ISynthesisSession")
class ISynthesisSession(typing_extensions.Protocol):
    '''(experimental) Represents the session for synthesizing workflows, including output directory and validation options.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="manifest")
    def manifest(self) -> "Manifest":
        '''(experimental) The manifest that records synthesized workflows.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="outdir")
    def outdir(self) -> builtins.str:
        '''(experimental) The output directory where synthesized YAML files will be stored.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="skipValidation")
    def skip_validation(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether to skip validation during synthesis.

        :default: false

        :stability: experimental
        '''
        ...


class _ISynthesisSessionProxy:
    '''(experimental) Represents the session for synthesizing workflows, including output directory and validation options.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "github-actions-cdk.ISynthesisSession"

    @builtins.property
    @jsii.member(jsii_name="manifest")
    def manifest(self) -> "Manifest":
        '''(experimental) The manifest that records synthesized workflows.

        :stability: experimental
        '''
        return typing.cast("Manifest", jsii.get(self, "manifest"))

    @builtins.property
    @jsii.member(jsii_name="outdir")
    def outdir(self) -> builtins.str:
        '''(experimental) The output directory where synthesized YAML files will be stored.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "outdir"))

    @builtins.property
    @jsii.member(jsii_name="skipValidation")
    def skip_validation(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether to skip validation during synthesis.

        :default: false

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "skipValidation"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISynthesisSession).__jsii_proxy_class__ = lambda : _ISynthesisSessionProxy


@jsii.interface(jsii_type="github-actions-cdk.IWorkflowSynthesizer")
class IWorkflowSynthesizer(typing_extensions.Protocol):
    '''(experimental) Interface for synthesizers that handle workflow synthesis.

    :stability: experimental
    '''

    @jsii.member(jsii_name="synthesize")
    def synthesize(self, session: ISynthesisSession) -> None:
        '''(experimental) Synthesizes a workflow into the specified output format.

        :param session: - The synthesis session containing configuration for the synthesis process.

        :stability: experimental
        '''
        ...


class _IWorkflowSynthesizerProxy:
    '''(experimental) Interface for synthesizers that handle workflow synthesis.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "github-actions-cdk.IWorkflowSynthesizer"

    @jsii.member(jsii_name="synthesize")
    def synthesize(self, session: ISynthesisSession) -> None:
        '''(experimental) Synthesizes a workflow into the specified output format.

        :param session: - The synthesis session containing configuration for the synthesis process.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a272dd50f7650140229a9894b3ea042f23351f229dbf6e6bdf63d88290ddd368)
            check_type(argname="argument session", value=session, expected_type=type_hints["session"])
        return typing.cast(None, jsii.invoke(self, "synthesize", [session]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IWorkflowSynthesizer).__jsii_proxy_class__ = lambda : _IWorkflowSynthesizerProxy


@jsii.data_type(
    jsii_type="github-actions-cdk.IssueCommentOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class IssueCommentOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Options for issue comment events.

        :param types: (experimental) Activity types to trigger on. Default: - triggers on all activity types

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9245f610dfdf28f8846ab53cd23fb911806e86522c4cea0c3e62e5529532c5bc)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Activity types to trigger on.

        :default: - triggers on all activity types

        :stability: experimental
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IssueCommentOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="github-actions-cdk.IssuesOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class IssuesOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Options for issue events.

        :param types: (experimental) Activity types to trigger on. Default: - triggers on all activity types

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf87540107a62d8d64ed58e95f8b01db8159513fdd767fdd8c3f30aa87899b9e)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Activity types to trigger on.

        :default: - triggers on all activity types

        :stability: experimental
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IssuesOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Job(Component, metaclass=jsii.JSIIMeta, jsii_type="github-actions-cdk.Job"):
    '''(experimental) Represents a GitHub Actions job, containing configurations, steps, and dependencies.

    Jobs are composed of steps and run within a specified environment with defined
    permissions, environment variables, and strategies.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        container: typing.Optional[typing.Union[ContainerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        continue_on_error: typing.Optional[builtins.bool] = None,
        defaults: typing.Optional[typing.Union[Defaults, typing.Dict[builtins.str, typing.Any]]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        environment: typing.Optional[typing.Union[Environment, typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        needs: typing.Optional[typing.Sequence[builtins.str]] = None,
        outputs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        permissions: typing.Optional[typing.Union[typing.Union["PermissionsEvent", typing.Dict[builtins.str, typing.Any]], builtins.str]] = None,
        required_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
        runner_labels: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
        runs_on: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
        services: typing.Optional[typing.Mapping[builtins.str, typing.Union[ContainerOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        strategy: typing.Optional[typing.Union["Strategy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Initializes a new instance of the ``Job`` class.

        :param scope: - Construct scope for the job.
        :param id: - Unique identifier for the job.
        :param container: (experimental) A container to run any steps in a job that don't already specify a container. If you have steps that use both script and container actions, the container actions will run as sibling containers on the same network with the same volume mounts.
        :param continue_on_error: (experimental) Prevents a workflow run from failing when a job fails. Set to true to allow a workflow run to pass when this job fails.
        :param defaults: (experimental) Default configuration settings for job steps.
        :param env: (experimental) Environment variables for all steps in the job.
        :param environment: (experimental) GitHub environment target for this job.
        :param name: (experimental) Display name for the job.
        :param needs: (experimental) List of job dependencies that must complete before this job starts.
        :param outputs: (experimental) Outputs produced by this job, accessible by downstream jobs.
        :param permissions: (experimental) Permissions granted to the job.
        :param required_checks: (experimental) List of checks required to pass before this job runs.
        :param runner_labels: (experimental) Runner labels for selecting a self-hosted runner.
        :param runs_on: (experimental) Runner environment, e.g., "ubuntu-latest".
        :param services: (experimental) Used to host service containers for a job in a workflow. Service containers are useful for creating databases or cache services like Redis. The runner automatically creates a Docker network and manages the life cycle of the service containers.
        :param strategy: (experimental) Strategy settings, including matrix configuration and concurrency limits.
        :param timeout_minutes: (experimental) Timeout duration for the job, in minutes.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba74ac8c28c96ce71749c13835adfaf0239f2f521dd066f17e0e73c75ff7d315)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = JobProps(
            container=container,
            continue_on_error=continue_on_error,
            defaults=defaults,
            env=env,
            environment=environment,
            name=name,
            needs=needs,
            outputs=outputs,
            permissions=permissions,
            required_checks=required_checks,
            runner_labels=runner_labels,
            runs_on=runs_on,
            services=services,
            strategy=strategy,
            timeout_minutes=timeout_minutes,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="isJob")
    @builtins.classmethod
    def is_job(cls, x: typing.Any) -> builtins.bool:
        '''(experimental) Checks if an object is an instance of ``Job``.

        :param x: - The object to check.

        :return: ``true`` if ``x`` is a ``Job``; otherwise, ``false``.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04102a365a36ddd57481a063efb6b1cd4953a212e6fa1a614385d0a163d9a28c)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isJob", [x]))

    @jsii.member(jsii_name="addDependency")
    def add_dependency(self, job: "Job") -> None:
        '''(experimental) Adds a dependency to another job, which must complete first.

        :param job: - Job to depend on.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__560683b73063a8009cbc4b45624c887259235712969b5f491054f13ca86e6cf2)
            check_type(argname="argument job", value=job, expected_type=type_hints["job"])
        return typing.cast(None, jsii.invoke(self, "addDependency", [job]))

    @jsii.member(jsii_name="addOutput")
    def add_output(self, name: builtins.str, value: builtins.str) -> None:
        '''(experimental) Adds an output accessible by downstream jobs.

        :param name: - Name of the output.
        :param value: - Value for the output.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c84ddb7613f0dc156744978622a36eaccf42eb24f73fb68aadd45210e8a453a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "addOutput", [name, value]))

    @jsii.member(jsii_name="addRegularStep")
    def add_regular_step(
        self,
        id: builtins.str,
        *,
        uses: builtins.str,
        parameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        condition: typing.Optional[builtins.str] = None,
        continue_on_error: typing.Optional[builtins.bool] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        timeout_minutes: typing.Optional[jsii.Number] = None,
    ) -> "RegularStep":
        '''(experimental) Adds a ``RegularStep`` to the job.

        :param id: - Unique ID for the step.
        :param uses: (experimental) GitHub Action to run, identified by repository or Docker image reference.
        :param parameters: (experimental) Input parameters for the action, passed as a key-value map.
        :param condition: (experimental) Conditional expression to determine if the step should run (equivalent to ``if`` in GitHub Actions). Supports GitHub Actions expressions, e.g., ``${{ success() }}``.
        :param continue_on_error: (experimental) Whether the job should continue if this step fails. Default: false
        :param env: (experimental) Environment variables specific to this step, overriding job-level or workflow-level variables.
        :param name: (experimental) A descriptive name for the step, displayed in the GitHub Actions UI.
        :param timeout_minutes: (experimental) Maximum execution time for the step, in minutes.

        :return: Created ``RegularStep`` instance.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af6c992ed1e3551de2bfc926e5e9d43b0d334c8ce844dfdc7a6dfcb6e483c25f)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = RegularStepProps(
            uses=uses,
            parameters=parameters,
            condition=condition,
            continue_on_error=continue_on_error,
            env=env,
            name=name,
            timeout_minutes=timeout_minutes,
        )

        return typing.cast("RegularStep", jsii.invoke(self, "addRegularStep", [id, props]))

    @jsii.member(jsii_name="addRunStep")
    def add_run_step(
        self,
        id: builtins.str,
        *,
        run: typing.Union[builtins.str, typing.Sequence[builtins.str]],
        shell: typing.Optional[builtins.str] = None,
        working_directory: typing.Optional[builtins.str] = None,
        condition: typing.Optional[builtins.str] = None,
        continue_on_error: typing.Optional[builtins.bool] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        timeout_minutes: typing.Optional[jsii.Number] = None,
    ) -> "RunStep":
        '''(experimental) Adds a ``RunStep`` to the job.

        :param id: - Unique ID for the step.
        :param run: (experimental) Commands or scripts to execute in this step.
        :param shell: (experimental) Shell environment for this step, allowing custom shells like ``bash``, ``pwsh``, etc. Default: "bash"
        :param working_directory: (experimental) Directory in which the step's command or action executes. Defaults to the job's working directory if not specified.
        :param condition: (experimental) Conditional expression to determine if the step should run (equivalent to ``if`` in GitHub Actions). Supports GitHub Actions expressions, e.g., ``${{ success() }}``.
        :param continue_on_error: (experimental) Whether the job should continue if this step fails. Default: false
        :param env: (experimental) Environment variables specific to this step, overriding job-level or workflow-level variables.
        :param name: (experimental) A descriptive name for the step, displayed in the GitHub Actions UI.
        :param timeout_minutes: (experimental) Maximum execution time for the step, in minutes.

        :return: Created ``RunStep`` instance.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3f8799500375f858f993c7e31e1600bc24bfdd95ae1cf9e57200e7a867e49a2)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = RunStepProps(
            run=run,
            shell=shell,
            working_directory=working_directory,
            condition=condition,
            continue_on_error=continue_on_error,
            env=env,
            name=name,
            timeout_minutes=timeout_minutes,
        )

        return typing.cast("RunStep", jsii.invoke(self, "addRunStep", [id, props]))

    @jsii.member(jsii_name="hasSteps")
    def has_steps(self) -> builtins.bool:
        '''(experimental) Checks if the current job contains any steps.

        This method iterates through the children of the node associated with
        the job and checks if any of those children are instances of StepBase.
        If at least one child is a step, the method returns true; otherwise, it
        returns false.

        :return: True if the job has one or more steps; otherwise, false.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.invoke(self, "hasSteps", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''(experimental) Retrieves the unique identifier for the job.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="needs")
    def needs(self) -> typing.List[builtins.str]:
        '''(experimental) Retrieves job dependencies.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "needs"))

    @builtins.property
    @jsii.member(jsii_name="runsOn")
    def runs_on(self) -> typing.Union[builtins.str, typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Union[builtins.str, typing.List[builtins.str]], jsii.get(self, "runsOn"))

    @builtins.property
    @jsii.member(jsii_name="container")
    def container(self) -> typing.Optional[ContainerOptions]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[ContainerOptions], jsii.get(self, "container"))

    @builtins.property
    @jsii.member(jsii_name="continueOnError")
    def continue_on_error(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "continueOnError"))

    @builtins.property
    @jsii.member(jsii_name="defaults")
    def defaults(self) -> typing.Optional[Defaults]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[Defaults], jsii.get(self, "defaults"))

    @builtins.property
    @jsii.member(jsii_name="env")
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "env"))

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(self) -> typing.Optional[Environment]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[Environment], jsii.get(self, "environment"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="outputs")
    def outputs(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Retrieves the job's defined outputs, if any.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "outputs"))

    @builtins.property
    @jsii.member(jsii_name="permissions")
    def permissions(
        self,
    ) -> typing.Optional[typing.Union["PermissionsEvent", builtins.str]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union["PermissionsEvent", builtins.str]], jsii.get(self, "permissions"))

    @builtins.property
    @jsii.member(jsii_name="requiredChecks")
    def required_checks(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "requiredChecks"))

    @builtins.property
    @jsii.member(jsii_name="runnerLabels")
    def runner_labels(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, typing.List[builtins.str]]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, typing.List[builtins.str]]], jsii.get(self, "runnerLabels"))

    @builtins.property
    @jsii.member(jsii_name="services")
    def services(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, ContainerOptions]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, ContainerOptions]], jsii.get(self, "services"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def strategy(self) -> typing.Optional["Strategy"]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional["Strategy"], jsii.get(self, "strategy"))

    @builtins.property
    @jsii.member(jsii_name="timeoutMinutes")
    def timeout_minutes(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutMinutes"))


@jsii.data_type(
    jsii_type="github-actions-cdk.JobProps",
    jsii_struct_bases=[],
    name_mapping={
        "container": "container",
        "continue_on_error": "continueOnError",
        "defaults": "defaults",
        "env": "env",
        "environment": "environment",
        "name": "name",
        "needs": "needs",
        "outputs": "outputs",
        "permissions": "permissions",
        "required_checks": "requiredChecks",
        "runner_labels": "runnerLabels",
        "runs_on": "runsOn",
        "services": "services",
        "strategy": "strategy",
        "timeout_minutes": "timeoutMinutes",
    },
)
class JobProps:
    def __init__(
        self,
        *,
        container: typing.Optional[typing.Union[ContainerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        continue_on_error: typing.Optional[builtins.bool] = None,
        defaults: typing.Optional[typing.Union[Defaults, typing.Dict[builtins.str, typing.Any]]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        environment: typing.Optional[typing.Union[Environment, typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        needs: typing.Optional[typing.Sequence[builtins.str]] = None,
        outputs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        permissions: typing.Optional[typing.Union[typing.Union["PermissionsEvent", typing.Dict[builtins.str, typing.Any]], builtins.str]] = None,
        required_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
        runner_labels: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
        runs_on: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
        services: typing.Optional[typing.Mapping[builtins.str, typing.Union[ContainerOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        strategy: typing.Optional[typing.Union["Strategy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Properties for configuring a GitHub Actions job.

        :param container: (experimental) A container to run any steps in a job that don't already specify a container. If you have steps that use both script and container actions, the container actions will run as sibling containers on the same network with the same volume mounts.
        :param continue_on_error: (experimental) Prevents a workflow run from failing when a job fails. Set to true to allow a workflow run to pass when this job fails.
        :param defaults: (experimental) Default configuration settings for job steps.
        :param env: (experimental) Environment variables for all steps in the job.
        :param environment: (experimental) GitHub environment target for this job.
        :param name: (experimental) Display name for the job.
        :param needs: (experimental) List of job dependencies that must complete before this job starts.
        :param outputs: (experimental) Outputs produced by this job, accessible by downstream jobs.
        :param permissions: (experimental) Permissions granted to the job.
        :param required_checks: (experimental) List of checks required to pass before this job runs.
        :param runner_labels: (experimental) Runner labels for selecting a self-hosted runner.
        :param runs_on: (experimental) Runner environment, e.g., "ubuntu-latest".
        :param services: (experimental) Used to host service containers for a job in a workflow. Service containers are useful for creating databases or cache services like Redis. The runner automatically creates a Docker network and manages the life cycle of the service containers.
        :param strategy: (experimental) Strategy settings, including matrix configuration and concurrency limits.
        :param timeout_minutes: (experimental) Timeout duration for the job, in minutes.

        :stability: experimental
        '''
        if isinstance(container, dict):
            container = ContainerOptions(**container)
        if isinstance(defaults, dict):
            defaults = Defaults(**defaults)
        if isinstance(environment, dict):
            environment = Environment(**environment)
        if isinstance(strategy, dict):
            strategy = Strategy(**strategy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20769971cc29ac6695fc59fa70f7ce92e7e4f43121f480d0ffcda1a97016201b)
            check_type(argname="argument container", value=container, expected_type=type_hints["container"])
            check_type(argname="argument continue_on_error", value=continue_on_error, expected_type=type_hints["continue_on_error"])
            check_type(argname="argument defaults", value=defaults, expected_type=type_hints["defaults"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument needs", value=needs, expected_type=type_hints["needs"])
            check_type(argname="argument outputs", value=outputs, expected_type=type_hints["outputs"])
            check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
            check_type(argname="argument required_checks", value=required_checks, expected_type=type_hints["required_checks"])
            check_type(argname="argument runner_labels", value=runner_labels, expected_type=type_hints["runner_labels"])
            check_type(argname="argument runs_on", value=runs_on, expected_type=type_hints["runs_on"])
            check_type(argname="argument services", value=services, expected_type=type_hints["services"])
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
            check_type(argname="argument timeout_minutes", value=timeout_minutes, expected_type=type_hints["timeout_minutes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if container is not None:
            self._values["container"] = container
        if continue_on_error is not None:
            self._values["continue_on_error"] = continue_on_error
        if defaults is not None:
            self._values["defaults"] = defaults
        if env is not None:
            self._values["env"] = env
        if environment is not None:
            self._values["environment"] = environment
        if name is not None:
            self._values["name"] = name
        if needs is not None:
            self._values["needs"] = needs
        if outputs is not None:
            self._values["outputs"] = outputs
        if permissions is not None:
            self._values["permissions"] = permissions
        if required_checks is not None:
            self._values["required_checks"] = required_checks
        if runner_labels is not None:
            self._values["runner_labels"] = runner_labels
        if runs_on is not None:
            self._values["runs_on"] = runs_on
        if services is not None:
            self._values["services"] = services
        if strategy is not None:
            self._values["strategy"] = strategy
        if timeout_minutes is not None:
            self._values["timeout_minutes"] = timeout_minutes

    @builtins.property
    def container(self) -> typing.Optional[ContainerOptions]:
        '''(experimental) A container to run any steps in a job that don't already specify a container.

        If you have steps that use both script and container actions,
        the container actions will run as sibling containers on the same network
        with the same volume mounts.

        :stability: experimental
        '''
        result = self._values.get("container")
        return typing.cast(typing.Optional[ContainerOptions], result)

    @builtins.property
    def continue_on_error(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Prevents a workflow run from failing when a job fails.

        Set to true to
        allow a workflow run to pass when this job fails.

        :stability: experimental
        '''
        result = self._values.get("continue_on_error")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def defaults(self) -> typing.Optional[Defaults]:
        '''(experimental) Default configuration settings for job steps.

        :stability: experimental
        '''
        result = self._values.get("defaults")
        return typing.cast(typing.Optional[Defaults], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Environment variables for all steps in the job.

        :stability: experimental
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def environment(self) -> typing.Optional[Environment]:
        '''(experimental) GitHub environment target for this job.

        :stability: experimental
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[Environment], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Display name for the job.

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def needs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of job dependencies that must complete before this job starts.

        :stability: experimental
        '''
        result = self._values.get("needs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def outputs(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Outputs produced by this job, accessible by downstream jobs.

        :stability: experimental
        '''
        result = self._values.get("outputs")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def permissions(
        self,
    ) -> typing.Optional[typing.Union["PermissionsEvent", builtins.str]]:
        '''(experimental) Permissions granted to the job.

        :stability: experimental
        '''
        result = self._values.get("permissions")
        return typing.cast(typing.Optional[typing.Union["PermissionsEvent", builtins.str]], result)

    @builtins.property
    def required_checks(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of checks required to pass before this job runs.

        :stability: experimental
        '''
        result = self._values.get("required_checks")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def runner_labels(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, typing.List[builtins.str]]]:
        '''(experimental) Runner labels for selecting a self-hosted runner.

        :stability: experimental
        '''
        result = self._values.get("runner_labels")
        return typing.cast(typing.Optional[typing.Union[builtins.str, typing.List[builtins.str]]], result)

    @builtins.property
    def runs_on(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, typing.List[builtins.str]]]:
        '''(experimental) Runner environment, e.g., "ubuntu-latest".

        :stability: experimental
        '''
        result = self._values.get("runs_on")
        return typing.cast(typing.Optional[typing.Union[builtins.str, typing.List[builtins.str]]], result)

    @builtins.property
    def services(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, ContainerOptions]]:
        '''(experimental) Used to host service containers for a job in a workflow.

        Service
        containers are useful for creating databases or cache services like Redis.
        The runner automatically creates a Docker network and manages the life
        cycle of the service containers.

        :stability: experimental
        '''
        result = self._values.get("services")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, ContainerOptions]], result)

    @builtins.property
    def strategy(self) -> typing.Optional["Strategy"]:
        '''(experimental) Strategy settings, including matrix configuration and concurrency limits.

        :stability: experimental
        '''
        result = self._values.get("strategy")
        return typing.cast(typing.Optional["Strategy"], result)

    @builtins.property
    def timeout_minutes(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Timeout duration for the job, in minutes.

        :stability: experimental
        '''
        result = self._values.get("timeout_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="github-actions-cdk.LabelOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class LabelOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Options for label events.

        :param types: (experimental) Activity types to trigger on. Default: - triggers on all activity types

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb9e02a1d086f2f6835ff0ea1688329d1c317ce50ab856b1f80f5638e1cece8f)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Activity types to trigger on.

        :default: - triggers on all activity types

        :stability: experimental
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LabelOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IManifest)
class Manifest(metaclass=jsii.JSIIMeta, jsii_type="github-actions-cdk.Manifest"):
    '''(experimental) Manages the creation of a manifest for synthesized workflows.

    The ``Manifest`` class maintains a record of workflows and provides methods
    to generate a structured manifest output.

    :stability: experimental
    '''

    def __init__(self, version: builtins.str, outdir: builtins.str) -> None:
        '''(experimental) Initializes a new instance of the Manifest class.

        :param version: - The version of the manifest format.
        :param outdir: - The output directory where the synthesized workflow YAML files are saved.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e7cbe59fdc33cb58cca9416f9ec62a26538d9b96aa5706cd8f0189f8d6bf739)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument outdir", value=outdir, expected_type=type_hints["outdir"])
        jsii.create(self.__class__, self, [version, outdir])

    @jsii.member(jsii_name="buildManifest")
    def build_manifest(self) -> IManifest:
        '''(experimental) Builds the complete manifest object for all workflows.

        :return: An object representing the manifest, including version and workflow details.

        :stability: experimental
        '''
        return typing.cast(IManifest, jsii.invoke(self, "buildManifest", []))

    @jsii.member(jsii_name="forWorkflow")
    def for_workflow(self, workflow: "Workflow") -> "WorkflowManifest":
        '''(experimental) Retrieves the manifest details for a specified workflow.

        If the workflow does not already exist in the manifest, it adds a new entry.

        :param workflow: - The workflow instance for which the manifest is generated.

        :return: The ``WorkflowManifest`` for the specified workflow.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dfdec75e2107c3fc50d8e620bb996f0d6bd7375948a2b8613aec4dd9d006d96)
            check_type(argname="argument workflow", value=workflow, expected_type=type_hints["workflow"])
        return typing.cast("WorkflowManifest", jsii.invoke(self, "forWorkflow", [workflow]))

    @jsii.member(jsii_name="hasErrorAnnotation")
    def has_error_annotation(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.invoke(self, "hasErrorAnnotation", []))

    @builtins.property
    @jsii.member(jsii_name="outdir")
    def outdir(self) -> builtins.str:
        '''(experimental) - The output directory where the synthesized workflow YAML files are saved.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "outdir"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        '''(experimental) - The version of the manifest format.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="workflows")
    def workflows(self) -> typing.Mapping[builtins.str, "WorkflowManifest"]:
        '''(experimental) A record mapping workflow IDs to their respective manifest details.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, "WorkflowManifest"], jsii.get(self, "workflows"))


@jsii.data_type(
    jsii_type="github-actions-cdk.Matrix",
    jsii_struct_bases=[],
    name_mapping={"domain": "domain", "exclude": "exclude", "include": "include"},
)
class Matrix:
    def __init__(
        self,
        *,
        domain: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[builtins.str]]] = None,
        exclude: typing.Optional[typing.Sequence[typing.Mapping[builtins.str, builtins.str]]] = None,
        include: typing.Optional[typing.Sequence[typing.Mapping[builtins.str, builtins.str]]] = None,
    ) -> None:
        '''(experimental) Defines a configuration matrix for variations of a job.

        The matrix feature allows setting up multiple configurations in a job, each with
        different parameters. GitHub Actions will create a unique job for each configuration.

        :param domain: (experimental) Key-value pairs for matrix configuration, where each key can contain multiple values, producing unique jobs for each combination.
        :param exclude: (experimental) Specific configurations to exclude from the matrix. Useful for avoiding certain configurations from running.
        :param include: (experimental) Specific configurations to include in the matrix. Each entry is a configuration object added to the job matrix.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03098613492927ce72af982b6409517ead55bde8380b16f202b5570d740d05fc)
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument exclude", value=exclude, expected_type=type_hints["exclude"])
            check_type(argname="argument include", value=include, expected_type=type_hints["include"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if domain is not None:
            self._values["domain"] = domain
        if exclude is not None:
            self._values["exclude"] = exclude
        if include is not None:
            self._values["include"] = include

    @builtins.property
    def domain(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.List[builtins.str]]]:
        '''(experimental) Key-value pairs for matrix configuration, where each key can contain multiple values, producing unique jobs for each combination.

        :stability: experimental
        '''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.List[builtins.str]]], result)

    @builtins.property
    def exclude(
        self,
    ) -> typing.Optional[typing.List[typing.Mapping[builtins.str, builtins.str]]]:
        '''(experimental) Specific configurations to exclude from the matrix.

        Useful for avoiding certain configurations from running.

        :stability: experimental
        '''
        result = self._values.get("exclude")
        return typing.cast(typing.Optional[typing.List[typing.Mapping[builtins.str, builtins.str]]], result)

    @builtins.property
    def include(
        self,
    ) -> typing.Optional[typing.List[typing.Mapping[builtins.str, builtins.str]]]:
        '''(experimental) Specific configurations to include in the matrix.

        Each entry is a configuration object added to the job matrix.

        :stability: experimental
        '''
        result = self._values.get("include")
        return typing.cast(typing.Optional[typing.List[typing.Mapping[builtins.str, builtins.str]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Matrix(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="github-actions-cdk.MilestoneOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class MilestoneOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Options for milestone events.

        :param types: (experimental) Activity types to trigger on. Default: - triggers on all activity types

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de2c4c22ac0039acb049ce3c2e609e65738cb30ba50ee75b76ee87ddb332ad6f)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Activity types to trigger on.

        :default: - triggers on all activity types

        :stability: experimental
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MilestoneOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="github-actions-cdk.PermissionLevel")
class PermissionLevel(enum.Enum):
    '''(experimental) Access levels for specific workflow permission scopes.

    ``PermissionLevel`` defines the different levels of access available for
    each permission scope in a workflow. These levels determine the
    degree of interaction that GitHub Actions workflows have with repository
    resources.

    :stability: experimental
    '''

    READ = "READ"
    '''(experimental) Grants read-only access to the specified scope.

    :stability: experimental
    '''
    WRITE = "WRITE"
    '''(experimental) Grants both read and write access to the specified scope.

    :stability: experimental
    '''
    NONE = "NONE"
    '''(experimental) Explicitly denies all access to the specified scope.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="github-actions-cdk.PermissionsEvent",
    jsii_struct_bases=[],
    name_mapping={
        "actions": "actions",
        "checks": "checks",
        "contents": "contents",
        "deployments": "deployments",
        "discussions": "discussions",
        "id_token": "idToken",
        "issues": "issues",
        "packages": "packages",
        "pull_requests": "pullRequests",
        "repository_projects": "repositoryProjects",
        "security_events": "securityEvents",
        "statuses": "statuses",
    },
)
class PermissionsEvent:
    def __init__(
        self,
        *,
        actions: typing.Optional[PermissionLevel] = None,
        checks: typing.Optional[PermissionLevel] = None,
        contents: typing.Optional[PermissionLevel] = None,
        deployments: typing.Optional[PermissionLevel] = None,
        discussions: typing.Optional[PermissionLevel] = None,
        id_token: typing.Optional[PermissionLevel] = None,
        issues: typing.Optional[PermissionLevel] = None,
        packages: typing.Optional[PermissionLevel] = None,
        pull_requests: typing.Optional[PermissionLevel] = None,
        repository_projects: typing.Optional[PermissionLevel] = None,
        security_events: typing.Optional[PermissionLevel] = None,
        statuses: typing.Optional[PermissionLevel] = None,
    ) -> None:
        '''(experimental) Specifies detailed permission levels for individual GitHub resources in a workflow.

        Each property in ``PermissionsEvent`` represents a specific scope for which
        access can be configured. When any scope is specified, all unspecified scopes
        are set to ``PermissionLevel.NONE``, overriding the default GitHub behavior
        of automatically setting unspecified permissions to ``read`` or ``write``.

        :param actions: (experimental) Permissions for GitHub Actions, affecting access to workflows.
        :param checks: (experimental) Permissions for check runs, enabling read or write access to check details.
        :param contents: (experimental) Permissions for repository contents, controlling file and directory access.
        :param deployments: (experimental) Permissions for deployments, affecting environment deployments in the repository.
        :param discussions: (experimental) Permissions for discussions, enabling interaction with GitHub Discussions.
        :param id_token: (experimental) Permissions for the GitHub OIDC (OpenID Connect) token, allowing secure identity verification.
        :param issues: (experimental) Permissions for managing and interacting with issues in the repository.
        :param packages: (experimental) Permissions for packages in the GitHub Packages registry.
        :param pull_requests: (experimental) Permissions for interacting with pull requests in the repository.
        :param repository_projects: (experimental) Permissions for repository projects, affecting project boards and related assets.
        :param security_events: (experimental) Permissions for security events, such as vulnerability alerts.
        :param statuses: (experimental) Permissions for statuses, affecting commit statuses in the repository.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__250bfcabc87a33880947a3c29504b6eba32fdb6d7ba0d62131a0d5f9b95f3f5a)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument checks", value=checks, expected_type=type_hints["checks"])
            check_type(argname="argument contents", value=contents, expected_type=type_hints["contents"])
            check_type(argname="argument deployments", value=deployments, expected_type=type_hints["deployments"])
            check_type(argname="argument discussions", value=discussions, expected_type=type_hints["discussions"])
            check_type(argname="argument id_token", value=id_token, expected_type=type_hints["id_token"])
            check_type(argname="argument issues", value=issues, expected_type=type_hints["issues"])
            check_type(argname="argument packages", value=packages, expected_type=type_hints["packages"])
            check_type(argname="argument pull_requests", value=pull_requests, expected_type=type_hints["pull_requests"])
            check_type(argname="argument repository_projects", value=repository_projects, expected_type=type_hints["repository_projects"])
            check_type(argname="argument security_events", value=security_events, expected_type=type_hints["security_events"])
            check_type(argname="argument statuses", value=statuses, expected_type=type_hints["statuses"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if actions is not None:
            self._values["actions"] = actions
        if checks is not None:
            self._values["checks"] = checks
        if contents is not None:
            self._values["contents"] = contents
        if deployments is not None:
            self._values["deployments"] = deployments
        if discussions is not None:
            self._values["discussions"] = discussions
        if id_token is not None:
            self._values["id_token"] = id_token
        if issues is not None:
            self._values["issues"] = issues
        if packages is not None:
            self._values["packages"] = packages
        if pull_requests is not None:
            self._values["pull_requests"] = pull_requests
        if repository_projects is not None:
            self._values["repository_projects"] = repository_projects
        if security_events is not None:
            self._values["security_events"] = security_events
        if statuses is not None:
            self._values["statuses"] = statuses

    @builtins.property
    def actions(self) -> typing.Optional[PermissionLevel]:
        '''(experimental) Permissions for GitHub Actions, affecting access to workflows.

        :stability: experimental
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[PermissionLevel], result)

    @builtins.property
    def checks(self) -> typing.Optional[PermissionLevel]:
        '''(experimental) Permissions for check runs, enabling read or write access to check details.

        :stability: experimental
        '''
        result = self._values.get("checks")
        return typing.cast(typing.Optional[PermissionLevel], result)

    @builtins.property
    def contents(self) -> typing.Optional[PermissionLevel]:
        '''(experimental) Permissions for repository contents, controlling file and directory access.

        :stability: experimental
        '''
        result = self._values.get("contents")
        return typing.cast(typing.Optional[PermissionLevel], result)

    @builtins.property
    def deployments(self) -> typing.Optional[PermissionLevel]:
        '''(experimental) Permissions for deployments, affecting environment deployments in the repository.

        :stability: experimental
        '''
        result = self._values.get("deployments")
        return typing.cast(typing.Optional[PermissionLevel], result)

    @builtins.property
    def discussions(self) -> typing.Optional[PermissionLevel]:
        '''(experimental) Permissions for discussions, enabling interaction with GitHub Discussions.

        :stability: experimental
        '''
        result = self._values.get("discussions")
        return typing.cast(typing.Optional[PermissionLevel], result)

    @builtins.property
    def id_token(self) -> typing.Optional[PermissionLevel]:
        '''(experimental) Permissions for the GitHub OIDC (OpenID Connect) token, allowing secure identity verification.

        :stability: experimental
        '''
        result = self._values.get("id_token")
        return typing.cast(typing.Optional[PermissionLevel], result)

    @builtins.property
    def issues(self) -> typing.Optional[PermissionLevel]:
        '''(experimental) Permissions for managing and interacting with issues in the repository.

        :stability: experimental
        '''
        result = self._values.get("issues")
        return typing.cast(typing.Optional[PermissionLevel], result)

    @builtins.property
    def packages(self) -> typing.Optional[PermissionLevel]:
        '''(experimental) Permissions for packages in the GitHub Packages registry.

        :stability: experimental
        '''
        result = self._values.get("packages")
        return typing.cast(typing.Optional[PermissionLevel], result)

    @builtins.property
    def pull_requests(self) -> typing.Optional[PermissionLevel]:
        '''(experimental) Permissions for interacting with pull requests in the repository.

        :stability: experimental
        '''
        result = self._values.get("pull_requests")
        return typing.cast(typing.Optional[PermissionLevel], result)

    @builtins.property
    def repository_projects(self) -> typing.Optional[PermissionLevel]:
        '''(experimental) Permissions for repository projects, affecting project boards and related assets.

        :stability: experimental
        '''
        result = self._values.get("repository_projects")
        return typing.cast(typing.Optional[PermissionLevel], result)

    @builtins.property
    def security_events(self) -> typing.Optional[PermissionLevel]:
        '''(experimental) Permissions for security events, such as vulnerability alerts.

        :stability: experimental
        '''
        result = self._values.get("security_events")
        return typing.cast(typing.Optional[PermissionLevel], result)

    @builtins.property
    def statuses(self) -> typing.Optional[PermissionLevel]:
        '''(experimental) Permissions for statuses, affecting commit statuses in the repository.

        :stability: experimental
        '''
        result = self._values.get("statuses")
        return typing.cast(typing.Optional[PermissionLevel], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PermissionsEvent(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Project(
    _constructs_77d1e7e8.RootConstruct,
    metaclass=jsii.JSIIMeta,
    jsii_type="github-actions-cdk.Project",
):
    '''(experimental) Represents a GitHub Actions project, managing workflows and their output.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        additional_checks: typing.Optional[builtins.bool] = None,
        continue_on_error_annotations: typing.Optional[builtins.bool] = None,
        outdir: typing.Optional[builtins.str] = None,
        skip_validation: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param additional_checks: 
        :param continue_on_error_annotations: 
        :param outdir: 
        :param skip_validation: 

        :stability: experimental
        '''
        props = ProjectProps(
            additional_checks=additional_checks,
            continue_on_error_annotations=continue_on_error_annotations,
            outdir=outdir,
            skip_validation=skip_validation,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="addWorkflow")
    def add_workflow(
        self,
        id: builtins.str,
        *,
        comment_at_top: typing.Optional[builtins.str] = None,
        concurrency: typing.Optional[typing.Union[ConcurrencyOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        defaults: typing.Optional[typing.Union[Defaults, typing.Dict[builtins.str, typing.Any]]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        permissions: typing.Optional[typing.Union[typing.Union[PermissionsEvent, typing.Dict[builtins.str, typing.Any]], builtins.str]] = None,
        run_name: typing.Optional[builtins.str] = None,
        synthesizer: typing.Optional[IWorkflowSynthesizer] = None,
        triggers: typing.Optional[typing.Union["WorkflowTriggers", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> "Workflow":
        '''
        :param id: -
        :param comment_at_top: (experimental) An optional comment that can be included at the top of the generated workflow YAML. This can serve as a note or reminder for users not to modify the generated output directly. Default: "Generated by github-actions-cdk, DO NOT EDIT DIRECTLY!"
        :param concurrency: (experimental) Configuration for concurrency control of workflow runs.
        :param defaults: (experimental) Default configuration settings for jobs in this workflow.
        :param env: (experimental) Environment variables that will be available to all jobs in the workflow.
        :param name: (experimental) The name of the workflow. GitHub displays the names of your workflows under your repository's "Actions" tab. If you omit the name, GitHub displays the workflow file path relative to the root of the repository.
        :param permissions: (experimental) Permissions required by the workflow.
        :param run_name: (experimental) The name for workflow runs generated from the workflow. GitHub displays the workflow run name in the list of workflow runs on your repository's "Actions" tab. If ``run-name`` is omitted or is only whitespace, then the run name is set to event-specific information for the workflow run. For example, for a workflow triggered by a ``push`` or ``pull_request`` event, it is set as the commit message or the title of the pull request. This value can include expressions and can reference the ``github`` and ``inputs`` contexts.
        :param synthesizer: (experimental) Custom synthesizer for rendering the workflow YAML.
        :param triggers: (experimental) Triggers that define when this workflow should run.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f851528c9102c82f6c29bf01ec2c142ebc403fa63d25b0a6e4ede555270f048a)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = WorkflowProps(
            comment_at_top=comment_at_top,
            concurrency=concurrency,
            defaults=defaults,
            env=env,
            name=name,
            permissions=permissions,
            run_name=run_name,
            synthesizer=synthesizer,
            triggers=triggers,
        )

        return typing.cast("Workflow", jsii.invoke(self, "addWorkflow", [id, props]))

    @jsii.member(jsii_name="createSynthesisSession")
    def _create_synthesis_session(self) -> ISynthesisSession:
        '''(experimental) Creates a synthesis session object.

        :stability: experimental
        '''
        return typing.cast(ISynthesisSession, jsii.invoke(self, "createSynthesisSession", []))

    @jsii.member(jsii_name="finalizeSynthesis")
    def _finalize_synthesis(self) -> None:
        '''(experimental) Finalizes the synthesis process, printing annotations and handling error annotations.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "finalizeSynthesis", []))

    @jsii.member(jsii_name="handleSynthesisError")
    def _handle_synthesis_error(self, error: typing.Any) -> None:
        '''(experimental) Handles any errors encountered during synthesis.

        :param error: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb2f842de27922aee627b6c05553006d17dcf8a11e5f292933003092ca075b08)
            check_type(argname="argument error", value=error, expected_type=type_hints["error"])
        return typing.cast(None, jsii.invoke(self, "handleSynthesisError", [error]))

    @jsii.member(jsii_name="prepareOutputDir")
    def _prepare_output_dir(self) -> None:
        '''(experimental) Ensures the output directory exists before synthesis.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "prepareOutputDir", []))

    @jsii.member(jsii_name="synth")
    def synth(self) -> None:
        '''(experimental) Main synthesis process that orchestrates the synthesis steps.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "synth", []))

    @jsii.member(jsii_name="synthesizeWorkflows")
    def _synthesize_workflows(
        self,
        workflows: typing.Sequence["Workflow"],
        session: ISynthesisSession,
    ) -> None:
        '''(experimental) Synthesizes each workflow and applies additional checks if configured.

        :param workflows: - Array of workflows to synthesize.
        :param session: - Synthesis session information.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7b94817da2f841c3520000a4ae8fca0578751c4ec686e7a7db759554fb271e2)
            check_type(argname="argument workflows", value=workflows, expected_type=type_hints["workflows"])
            check_type(argname="argument session", value=session, expected_type=type_hints["session"])
        return typing.cast(None, jsii.invoke(self, "synthesizeWorkflows", [workflows, session]))

    @builtins.property
    @jsii.member(jsii_name="manifest")
    def manifest(self) -> Manifest:
        '''
        :stability: experimental
        '''
        return typing.cast(Manifest, jsii.get(self, "manifest"))

    @builtins.property
    @jsii.member(jsii_name="outdir")
    def outdir(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "outdir"))

    @builtins.property
    @jsii.member(jsii_name="additionalChecks")
    def additional_checks(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "additionalChecks"))

    @builtins.property
    @jsii.member(jsii_name="continueOnErrorAnnotations")
    def continue_on_error_annotations(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "continueOnErrorAnnotations"))

    @builtins.property
    @jsii.member(jsii_name="skipValidation")
    def skip_validation(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "skipValidation"))


@jsii.data_type(
    jsii_type="github-actions-cdk.ProjectCardOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class ProjectCardOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Options for project card events.

        :param types: (experimental) Activity types to trigger on. Default: - triggers on all activity types

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad415eff52b84a055c84337c2805ce9044b826d99699d6689cc01763af6c8119)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Activity types to trigger on.

        :default: - triggers on all activity types

        :stability: experimental
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectCardOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="github-actions-cdk.ProjectColumnOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class ProjectColumnOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Options for project column events.

        :param types: (experimental) Activity types to trigger on. Default: - triggers on all activity types

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c3004989fcc8d55376e3ef3a1db982fc0094ca209aa3573c22b231d6389d9e7)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Activity types to trigger on.

        :default: - triggers on all activity types

        :stability: experimental
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectColumnOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="github-actions-cdk.ProjectOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class ProjectOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Options for project events.

        :param types: (experimental) Activity types to trigger on. Default: - triggers on all activity types

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67d88b3a3d6d856bdf249d58a343a9ef8740ccb7f40fe245ca15140bf5b34fdb)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Activity types to trigger on.

        :default: - triggers on all activity types

        :stability: experimental
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="github-actions-cdk.ProjectProps",
    jsii_struct_bases=[],
    name_mapping={
        "additional_checks": "additionalChecks",
        "continue_on_error_annotations": "continueOnErrorAnnotations",
        "outdir": "outdir",
        "skip_validation": "skipValidation",
    },
)
class ProjectProps:
    def __init__(
        self,
        *,
        additional_checks: typing.Optional[builtins.bool] = None,
        continue_on_error_annotations: typing.Optional[builtins.bool] = None,
        outdir: typing.Optional[builtins.str] = None,
        skip_validation: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Configuration properties for setting up a ``Project`` instance.

        :param additional_checks: 
        :param continue_on_error_annotations: 
        :param outdir: 
        :param skip_validation: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__450639eccdc42a348c0099dbce603df8cd9197de52538522be8040114716859d)
            check_type(argname="argument additional_checks", value=additional_checks, expected_type=type_hints["additional_checks"])
            check_type(argname="argument continue_on_error_annotations", value=continue_on_error_annotations, expected_type=type_hints["continue_on_error_annotations"])
            check_type(argname="argument outdir", value=outdir, expected_type=type_hints["outdir"])
            check_type(argname="argument skip_validation", value=skip_validation, expected_type=type_hints["skip_validation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if additional_checks is not None:
            self._values["additional_checks"] = additional_checks
        if continue_on_error_annotations is not None:
            self._values["continue_on_error_annotations"] = continue_on_error_annotations
        if outdir is not None:
            self._values["outdir"] = outdir
        if skip_validation is not None:
            self._values["skip_validation"] = skip_validation

    @builtins.property
    def additional_checks(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("additional_checks")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def continue_on_error_annotations(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("continue_on_error_annotations")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def outdir(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("outdir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def skip_validation(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("skip_validation")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="github-actions-cdk.PullRequestOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class PullRequestOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Options for pull request events.

        :param types: (experimental) Activity types to trigger on. Default: - triggers on all activity types

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68171705c985be084dbdca2a1ff2fd3444b5e640d632c443aa15eba47ab5bb67)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Activity types to trigger on.

        :default: - triggers on all activity types

        :stability: experimental
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PullRequestOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="github-actions-cdk.PullRequestReviewCommentOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class PullRequestReviewCommentOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Options for pull request review comment events.

        :param types: (experimental) Activity types to trigger on. Default: - triggers on all activity types

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1607ee4b141291975fd72d3420b264f24669240b48469ea6fec28a7bb7c524e)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Activity types to trigger on.

        :default: - triggers on all activity types

        :stability: experimental
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PullRequestReviewCommentOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="github-actions-cdk.PullRequestReviewOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class PullRequestReviewOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Options for pull request review events.

        :param types: (experimental) Activity types to trigger on. Default: - triggers on all activity types

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5c37c0870fb5ff9b5dceab001bb8fd29e70d138f195ff3a791bbf8f4da178c7)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Activity types to trigger on.

        :default: - triggers on all activity types

        :stability: experimental
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PullRequestReviewOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="github-actions-cdk.PushOptions",
    jsii_struct_bases=[],
    name_mapping={"branches": "branches", "paths": "paths", "tags": "tags"},
)
class PushOptions:
    def __init__(
        self,
        *,
        branches: typing.Optional[typing.Sequence[builtins.str]] = None,
        paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Options for push-like events, such as specifying branches, tags, and paths.

        :param branches: (experimental) Branches to trigger on. For pull requests, only base branches are evaluated.
        :param paths: (experimental) File path patterns to trigger on. Default: - triggers on all paths
        :param tags: (experimental) Tags to trigger on. Default: - triggers on all tags

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b2dbee06284bd070f84759371f9d3e47ea1a2959e2747c9ef5348e41c0507fd)
            check_type(argname="argument branches", value=branches, expected_type=type_hints["branches"])
            check_type(argname="argument paths", value=paths, expected_type=type_hints["paths"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if branches is not None:
            self._values["branches"] = branches
        if paths is not None:
            self._values["paths"] = paths
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def branches(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Branches to trigger on.

        For pull requests, only base branches are evaluated.

        :see: https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#filter-pattern-cheat-sheet
        :stability: experimental
        '''
        result = self._values.get("branches")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) File path patterns to trigger on.

        :default: - triggers on all paths

        :stability: experimental
        '''
        result = self._values.get("paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Tags to trigger on.

        :default: - triggers on all tags

        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PushOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="github-actions-cdk.RegistryPackageOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class RegistryPackageOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Options for registry package events.

        :param types: (experimental) Activity types to trigger on. Default: - triggers on all activity types

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51ffb436656ac8c1233b106fe75017220f3ca1cbe93321807f6a71425e7024e4)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Activity types to trigger on.

        :default: - triggers on all activity types

        :stability: experimental
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RegistryPackageOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="github-actions-cdk.RegularStepProps",
    jsii_struct_bases=[CommonStepProps],
    name_mapping={
        "condition": "condition",
        "continue_on_error": "continueOnError",
        "env": "env",
        "name": "name",
        "timeout_minutes": "timeoutMinutes",
        "uses": "uses",
        "parameters": "parameters",
    },
)
class RegularStepProps(CommonStepProps):
    def __init__(
        self,
        *,
        condition: typing.Optional[builtins.str] = None,
        continue_on_error: typing.Optional[builtins.bool] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        timeout_minutes: typing.Optional[jsii.Number] = None,
        uses: builtins.str,
        parameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> None:
        '''(experimental) Configuration for a step that uses a predefined GitHub Action.

        :param condition: (experimental) Conditional expression to determine if the step should run (equivalent to ``if`` in GitHub Actions). Supports GitHub Actions expressions, e.g., ``${{ success() }}``.
        :param continue_on_error: (experimental) Whether the job should continue if this step fails. Default: false
        :param env: (experimental) Environment variables specific to this step, overriding job-level or workflow-level variables.
        :param name: (experimental) A descriptive name for the step, displayed in the GitHub Actions UI.
        :param timeout_minutes: (experimental) Maximum execution time for the step, in minutes.
        :param uses: (experimental) GitHub Action to run, identified by repository or Docker image reference.
        :param parameters: (experimental) Input parameters for the action, passed as a key-value map.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__143dd96d6b01c63c85ed87ccf4d0bf586729876d49a336389777dc744bdf347f)
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument continue_on_error", value=continue_on_error, expected_type=type_hints["continue_on_error"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument timeout_minutes", value=timeout_minutes, expected_type=type_hints["timeout_minutes"])
            check_type(argname="argument uses", value=uses, expected_type=type_hints["uses"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "uses": uses,
        }
        if condition is not None:
            self._values["condition"] = condition
        if continue_on_error is not None:
            self._values["continue_on_error"] = continue_on_error
        if env is not None:
            self._values["env"] = env
        if name is not None:
            self._values["name"] = name
        if timeout_minutes is not None:
            self._values["timeout_minutes"] = timeout_minutes
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def condition(self) -> typing.Optional[builtins.str]:
        '''(experimental) Conditional expression to determine if the step should run (equivalent to ``if`` in GitHub Actions).

        Supports GitHub Actions expressions, e.g., ``${{ success() }}``.

        :stability: experimental

        Example::

            "${{ github.event_name == 'push' }}"
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def continue_on_error(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the job should continue if this step fails.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("continue_on_error")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Environment variables specific to this step, overriding job-level or workflow-level variables.

        :stability: experimental

        Example::

            { "NODE_ENV": "production" }
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A descriptive name for the step, displayed in the GitHub Actions UI.

        :stability: experimental

        Example::

            "Install dependencies"
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout_minutes(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Maximum execution time for the step, in minutes.

        :stability: experimental

        Example::

            10
        '''
        result = self._values.get("timeout_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def uses(self) -> builtins.str:
        '''(experimental) GitHub Action to run, identified by repository or Docker image reference.

        :stability: experimental

        Example::

            "actions/checkout@v2"
        '''
        result = self._values.get("uses")
        assert result is not None, "Required property 'uses' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Input parameters for the action, passed as a key-value map.

        :stability: experimental

        Example::

            { "token": "${{ secrets.GITHUB_TOKEN }}" }
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RegularStepProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="github-actions-cdk.ReleaseOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class ReleaseOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Options for release events.

        :param types: (experimental) Activity types to trigger on. Default: - triggers on all activity types

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__901c704f807a3bc66d62aca75564f6e9fa9ee5ef0df3967465126a7358291a92)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Activity types to trigger on.

        :default: - triggers on all activity types

        :stability: experimental
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReleaseOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="github-actions-cdk.RepositoryDispatchOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class RepositoryDispatchOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Options for triggering on repository dispatch events.

        :param types: (experimental) List of activity types to trigger on. Default: - triggers on all activity types

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a077abe81a20c3b60a3bd4ce5d7da8a5d920dbc1e7cbe5febe1d4f88fec3359d)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of activity types to trigger on.

        :default: - triggers on all activity types

        :stability: experimental
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryDispatchOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="github-actions-cdk.RunSettings",
    jsii_struct_bases=[],
    name_mapping={"shell": "shell", "working_directory": "workingDirectory"},
)
class RunSettings:
    def __init__(
        self,
        *,
        shell: typing.Optional[builtins.str] = None,
        working_directory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Configuration options for the execution environment of a job's steps.

        ``RunSettings`` provides control over the shell, working directory, and other
        environment-specific options used when running commands in a job step.

        :param shell: (experimental) Specifies the shell to use for executing the step's commands. This property allows you to define the command-line shell used for the step. Common options include ``bash``, ``sh``, ``cmd``, ``powershell``, or ``python``, depending on the operating system and specific requirements of the step. Default: The shell is determined automatically based on the operating system and job configuration.
        :param working_directory: (experimental) Defines the working directory for the step. The ``workingDirectory`` specifies the file path where the command should be executed. This can be an absolute path or relative to the root of the GitHub workspace. If not specified, the default working directory is the GitHub workspace root (typically ``/home/runner/work/{repo-name}/{repo-name}`` on Linux runners).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__136f7dd5df10bc3efc63ac68784be915348e8e271405b406ee967bb475a85aa3)
            check_type(argname="argument shell", value=shell, expected_type=type_hints["shell"])
            check_type(argname="argument working_directory", value=working_directory, expected_type=type_hints["working_directory"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if shell is not None:
            self._values["shell"] = shell
        if working_directory is not None:
            self._values["working_directory"] = working_directory

    @builtins.property
    def shell(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies the shell to use for executing the step's commands.

        This property allows you to define the command-line shell used for the step.
        Common options include ``bash``, ``sh``, ``cmd``, ``powershell``, or ``python``, depending
        on the operating system and specific requirements of the step.

        :default:

        The shell is determined automatically based on the operating system
        and job configuration.

        :stability: experimental

        Example::

            shell: "powershell"
        '''
        result = self._values.get("shell")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def working_directory(self) -> typing.Optional[builtins.str]:
        '''(experimental) Defines the working directory for the step.

        The ``workingDirectory`` specifies the file path where the command should be executed.
        This can be an absolute path or relative to the root of the GitHub workspace.
        If not specified, the default working directory is the GitHub workspace root
        (typically ``/home/runner/work/{repo-name}/{repo-name}`` on Linux runners).

        :stability: experimental

        Example::

            workingDirectory: "/home/runner/work/my-repo/my-repo"
        '''
        result = self._values.get("working_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RunSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="github-actions-cdk.RunStepProps",
    jsii_struct_bases=[CommonStepProps],
    name_mapping={
        "condition": "condition",
        "continue_on_error": "continueOnError",
        "env": "env",
        "name": "name",
        "timeout_minutes": "timeoutMinutes",
        "run": "run",
        "shell": "shell",
        "working_directory": "workingDirectory",
    },
)
class RunStepProps(CommonStepProps):
    def __init__(
        self,
        *,
        condition: typing.Optional[builtins.str] = None,
        continue_on_error: typing.Optional[builtins.bool] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        timeout_minutes: typing.Optional[jsii.Number] = None,
        run: typing.Union[builtins.str, typing.Sequence[builtins.str]],
        shell: typing.Optional[builtins.str] = None,
        working_directory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Configuration for a step that runs a shell command.

        :param condition: (experimental) Conditional expression to determine if the step should run (equivalent to ``if`` in GitHub Actions). Supports GitHub Actions expressions, e.g., ``${{ success() }}``.
        :param continue_on_error: (experimental) Whether the job should continue if this step fails. Default: false
        :param env: (experimental) Environment variables specific to this step, overriding job-level or workflow-level variables.
        :param name: (experimental) A descriptive name for the step, displayed in the GitHub Actions UI.
        :param timeout_minutes: (experimental) Maximum execution time for the step, in minutes.
        :param run: (experimental) Commands or scripts to execute in this step.
        :param shell: (experimental) Shell environment for this step, allowing custom shells like ``bash``, ``pwsh``, etc. Default: "bash"
        :param working_directory: (experimental) Directory in which the step's command or action executes. Defaults to the job's working directory if not specified.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffdd2ad37969e8a3bc529751e5cc2b383b87766524f9b8d68ee5af9bdcb6d8e6)
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument continue_on_error", value=continue_on_error, expected_type=type_hints["continue_on_error"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument timeout_minutes", value=timeout_minutes, expected_type=type_hints["timeout_minutes"])
            check_type(argname="argument run", value=run, expected_type=type_hints["run"])
            check_type(argname="argument shell", value=shell, expected_type=type_hints["shell"])
            check_type(argname="argument working_directory", value=working_directory, expected_type=type_hints["working_directory"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "run": run,
        }
        if condition is not None:
            self._values["condition"] = condition
        if continue_on_error is not None:
            self._values["continue_on_error"] = continue_on_error
        if env is not None:
            self._values["env"] = env
        if name is not None:
            self._values["name"] = name
        if timeout_minutes is not None:
            self._values["timeout_minutes"] = timeout_minutes
        if shell is not None:
            self._values["shell"] = shell
        if working_directory is not None:
            self._values["working_directory"] = working_directory

    @builtins.property
    def condition(self) -> typing.Optional[builtins.str]:
        '''(experimental) Conditional expression to determine if the step should run (equivalent to ``if`` in GitHub Actions).

        Supports GitHub Actions expressions, e.g., ``${{ success() }}``.

        :stability: experimental

        Example::

            "${{ github.event_name == 'push' }}"
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def continue_on_error(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the job should continue if this step fails.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("continue_on_error")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Environment variables specific to this step, overriding job-level or workflow-level variables.

        :stability: experimental

        Example::

            { "NODE_ENV": "production" }
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A descriptive name for the step, displayed in the GitHub Actions UI.

        :stability: experimental

        Example::

            "Install dependencies"
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout_minutes(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Maximum execution time for the step, in minutes.

        :stability: experimental

        Example::

            10
        '''
        result = self._values.get("timeout_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def run(self) -> typing.Union[builtins.str, typing.List[builtins.str]]:
        '''(experimental) Commands or scripts to execute in this step.

        :stability: experimental

        Example::

            ["npm", "install"]
        '''
        result = self._values.get("run")
        assert result is not None, "Required property 'run' is missing"
        return typing.cast(typing.Union[builtins.str, typing.List[builtins.str]], result)

    @builtins.property
    def shell(self) -> typing.Optional[builtins.str]:
        '''(experimental) Shell environment for this step, allowing custom shells like ``bash``, ``pwsh``, etc.

        :default: "bash"

        :stability: experimental

        Example::

            "pwsh"
        '''
        result = self._values.get("shell")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def working_directory(self) -> typing.Optional[builtins.str]:
        '''(experimental) Directory in which the step's command or action executes.

        Defaults to the job's working directory if not specified.

        :stability: experimental

        Example::

            "src/"
        '''
        result = self._values.get("working_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RunStepProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StepBase(
    Component,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="github-actions-cdk.StepBase",
):
    '''(experimental) Base class representing a single step within a GitHub Actions job.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        condition: typing.Optional[builtins.str] = None,
        continue_on_error: typing.Optional[builtins.bool] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        timeout_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Creates a new ``StepBase`` instance.

        :param scope: - The scope in which to define this construct.
        :param id: - The unique identifier for this step.
        :param condition: (experimental) Conditional expression to determine if the step should run (equivalent to ``if`` in GitHub Actions). Supports GitHub Actions expressions, e.g., ``${{ success() }}``.
        :param continue_on_error: (experimental) Whether the job should continue if this step fails. Default: false
        :param env: (experimental) Environment variables specific to this step, overriding job-level or workflow-level variables.
        :param name: (experimental) A descriptive name for the step, displayed in the GitHub Actions UI.
        :param timeout_minutes: (experimental) Maximum execution time for the step, in minutes.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0432591929c3c2329eefcdae16020d8b81732031b2761d403ad6ad8948be0d7b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CommonStepProps(
            condition=condition,
            continue_on_error=continue_on_error,
            env=env,
            name=name,
            timeout_minutes=timeout_minutes,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="isStepBase")
    @builtins.classmethod
    def is_step_base(cls, x: typing.Any) -> builtins.bool:
        '''(experimental) Checks if an object is an instance of ``StepBase``.

        :param x: - The object to check.

        :return: ``true`` if ``x`` is a ``StepBase``; otherwise, ``false``.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d5c5071a05d3c40ca0e26005f92644373502ebc50d93c3ae0ed9893b1092eb9)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isStepBase", [x]))

    @jsii.member(jsii_name="outputExpression")
    def output_expression(self, name: builtins.str) -> builtins.str:
        '''(experimental) Generates the GitHub Actions output expression for this step.

        This method constructs a formatted string that represents the GitHub Actions
        output expression for the specified output name. The returned string can be
        used in workflows to reference outputs from this step in a reusable format.

        :param name: - The name of the specific output to reference from this step.

        :return:

        The full GitHub Actions expression for accessing this output, e.g.,
        "${{ steps.stepId.outputs.outputName }}".

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a94739a86ea2b0733bd3333cde61bb43462286e9e8e6c243cac71a73e2c0683f)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast(builtins.str, jsii.invoke(self, "outputExpression", [name]))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''(experimental) Retrieves the step's unique identifier within the context of a workflow job.

        :return: The unique identifier for this step.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="continueOnError")
    def continue_on_error(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "continueOnError"))

    @builtins.property
    @jsii.member(jsii_name="env")
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "env"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeoutMinutes")
    def timeout_minutes(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutMinutes"))


class _StepBaseProxy(
    StepBase,
    jsii.proxy_for(Component), # type: ignore[misc]
):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, StepBase).__jsii_proxy_class__ = lambda : _StepBaseProxy


@jsii.data_type(
    jsii_type="github-actions-cdk.Strategy",
    jsii_struct_bases=[],
    name_mapping={
        "fail_fast": "failFast",
        "matrix": "matrix",
        "max_parallel": "maxParallel",
    },
)
class Strategy:
    def __init__(
        self,
        *,
        fail_fast: typing.Optional[builtins.bool] = None,
        matrix: typing.Optional[typing.Union[Matrix, typing.Dict[builtins.str, typing.Any]]] = None,
        max_parallel: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Defines a strategy for job execution, including matrix and concurrency settings.

        :param fail_fast: (experimental) Cancels all in-progress matrix jobs if one fails. Default: true
        :param matrix: (experimental) Configuration matrix for job variations.
        :param max_parallel: (experimental) Limits the number of concurrent jobs in the matrix.

        :stability: experimental
        '''
        if isinstance(matrix, dict):
            matrix = Matrix(**matrix)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__940058bd717a823643f0fa71e7845f3424e4d1bb4f6b6e9d54c9d10888d7c231)
            check_type(argname="argument fail_fast", value=fail_fast, expected_type=type_hints["fail_fast"])
            check_type(argname="argument matrix", value=matrix, expected_type=type_hints["matrix"])
            check_type(argname="argument max_parallel", value=max_parallel, expected_type=type_hints["max_parallel"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if fail_fast is not None:
            self._values["fail_fast"] = fail_fast
        if matrix is not None:
            self._values["matrix"] = matrix
        if max_parallel is not None:
            self._values["max_parallel"] = max_parallel

    @builtins.property
    def fail_fast(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Cancels all in-progress matrix jobs if one fails.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("fail_fast")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def matrix(self) -> typing.Optional[Matrix]:
        '''(experimental) Configuration matrix for job variations.

        :stability: experimental
        '''
        result = self._values.get("matrix")
        return typing.cast(typing.Optional[Matrix], result)

    @builtins.property
    def max_parallel(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Limits the number of concurrent jobs in the matrix.

        :stability: experimental
        '''
        result = self._values.get("max_parallel")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Strategy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="github-actions-cdk.ValidationErrorMessage",
    jsii_struct_bases=[],
    name_mapping={"message": "message", "source": "source"},
)
class ValidationErrorMessage:
    def __init__(
        self,
        *,
        message: builtins.str,
        source: _constructs_77d1e7e8.IConstruct,
    ) -> None:
        '''(experimental) Represents a validation error message with its source.

        :param message: (experimental) The message describing the validation error.
        :param source: (experimental) The source construct where the error originated.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c7994564a0243148b62974f55dce47cb0c156adc21b83781f56cf9c92f78a02)
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "message": message,
            "source": source,
        }

    @builtins.property
    def message(self) -> builtins.str:
        '''(experimental) The message describing the validation error.

        :stability: experimental
        '''
        result = self._values.get("message")
        assert result is not None, "Required property 'message' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source(self) -> _constructs_77d1e7e8.IConstruct:
        '''(experimental) The source construct where the error originated.

        :stability: experimental
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(_constructs_77d1e7e8.IConstruct, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ValidationErrorMessage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_constructs_77d1e7e8.IValidation)
class Validator(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="github-actions-cdk.Validator",
):
    '''(experimental) Abstract base class for all validators.

    :stability: experimental
    :remarks:

    The ``Validator`` class provides core error management and validation
    methods, ensuring common validation operations across different
    workflow constructs. Subclasses implement specific validations based
    on construct types.
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="checkRequired")
    def _check_required(
        self,
        property: typing.Any,
        name: builtins.str,
    ) -> typing.List[builtins.str]:
        '''(experimental) Verifies that a required property is set.

        :param property: - The property to check for presence.
        :param name: - The name of the property to include in error messages.

        :return: An array containing an error message if the property is missing, or an empty array if it exists.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a127734cf9ec3d6224c134b97fa8221cd56f6b8ae5191ea2a24515e6f3db0915)
            check_type(argname="argument property", value=property, expected_type=type_hints["property"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "checkRequired", [property, name]))

    @jsii.member(jsii_name="validate")
    @abc.abstractmethod
    def validate(self) -> typing.List[builtins.str]:
        '''(experimental) Executes the validation logic for the instance.

        :return: An array of error messages if validation fails, or an empty array if successful.

        :stability: experimental
        '''
        ...


class _ValidatorProxy(Validator):
    @jsii.member(jsii_name="validate")
    def validate(self) -> typing.List[builtins.str]:
        '''(experimental) Executes the validation logic for the instance.

        :return: An array of error messages if validation fails, or an empty array if successful.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validate", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, Validator).__jsii_proxy_class__ = lambda : _ValidatorProxy


@jsii.data_type(
    jsii_type="github-actions-cdk.WatchOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class WatchOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Options for watch events.

        :param types: (experimental) Activity types to trigger on. Default: - triggers on all activity types

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__785dc16d175b076483963c67da231a63908f82840f73cbe4b3bec91891692591)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Activity types to trigger on.

        :default: - triggers on all activity types

        :stability: experimental
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WatchOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Workflow(
    Component,
    metaclass=jsii.JSIIMeta,
    jsii_type="github-actions-cdk.Workflow",
):
    '''(experimental) Represents a GitHub Workflow.

    This class defines the workflow, its triggers, environment variables,
    defaults, permissions, concurrency settings, and allows for job creation.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        comment_at_top: typing.Optional[builtins.str] = None,
        concurrency: typing.Optional[typing.Union[ConcurrencyOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        defaults: typing.Optional[typing.Union[Defaults, typing.Dict[builtins.str, typing.Any]]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        permissions: typing.Optional[typing.Union[typing.Union[PermissionsEvent, typing.Dict[builtins.str, typing.Any]], builtins.str]] = None,
        run_name: typing.Optional[builtins.str] = None,
        synthesizer: typing.Optional[IWorkflowSynthesizer] = None,
        triggers: typing.Optional[typing.Union["WorkflowTriggers", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Initializes a new instance of the Workflow class.

        :param scope: -
        :param id: -
        :param comment_at_top: (experimental) An optional comment that can be included at the top of the generated workflow YAML. This can serve as a note or reminder for users not to modify the generated output directly. Default: "Generated by github-actions-cdk, DO NOT EDIT DIRECTLY!"
        :param concurrency: (experimental) Configuration for concurrency control of workflow runs.
        :param defaults: (experimental) Default configuration settings for jobs in this workflow.
        :param env: (experimental) Environment variables that will be available to all jobs in the workflow.
        :param name: (experimental) The name of the workflow. GitHub displays the names of your workflows under your repository's "Actions" tab. If you omit the name, GitHub displays the workflow file path relative to the root of the repository.
        :param permissions: (experimental) Permissions required by the workflow.
        :param run_name: (experimental) The name for workflow runs generated from the workflow. GitHub displays the workflow run name in the list of workflow runs on your repository's "Actions" tab. If ``run-name`` is omitted or is only whitespace, then the run name is set to event-specific information for the workflow run. For example, for a workflow triggered by a ``push`` or ``pull_request`` event, it is set as the commit message or the title of the pull request. This value can include expressions and can reference the ``github`` and ``inputs`` contexts.
        :param synthesizer: (experimental) Custom synthesizer for rendering the workflow YAML.
        :param triggers: (experimental) Triggers that define when this workflow should run.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdbc398a16d0309222333c5d160ce820ecd2201180eefcc6e06ee4dbca746de0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = WorkflowProps(
            comment_at_top=comment_at_top,
            concurrency=concurrency,
            defaults=defaults,
            env=env,
            name=name,
            permissions=permissions,
            run_name=run_name,
            synthesizer=synthesizer,
            triggers=triggers,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="isWorkflow")
    @builtins.classmethod
    def is_workflow(cls, x: typing.Any) -> builtins.bool:
        '''(experimental) Checks if an object is an instance of ``Workflow``.

        :param x: - The object to check.

        :return: ``true`` if ``x`` is a ``workflow``; otherwise, ``false``.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f28757ff3d4552ffc090efd7c6174706e8f33b3f0134a50749d04b29931d1a2)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isWorkflow", [x]))

    @jsii.member(jsii_name="addJob")
    def add_job(
        self,
        id: builtins.str,
        *,
        container: typing.Optional[typing.Union[ContainerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        continue_on_error: typing.Optional[builtins.bool] = None,
        defaults: typing.Optional[typing.Union[Defaults, typing.Dict[builtins.str, typing.Any]]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        environment: typing.Optional[typing.Union[Environment, typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        needs: typing.Optional[typing.Sequence[builtins.str]] = None,
        outputs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        permissions: typing.Optional[typing.Union[typing.Union[PermissionsEvent, typing.Dict[builtins.str, typing.Any]], builtins.str]] = None,
        required_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
        runner_labels: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
        runs_on: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
        services: typing.Optional[typing.Mapping[builtins.str, typing.Union[ContainerOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        strategy: typing.Optional[typing.Union[Strategy, typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_minutes: typing.Optional[jsii.Number] = None,
    ) -> Job:
        '''(experimental) Adds a new job to the workflow.

        :param id: - The unique identifier of the job.
        :param container: (experimental) A container to run any steps in a job that don't already specify a container. If you have steps that use both script and container actions, the container actions will run as sibling containers on the same network with the same volume mounts.
        :param continue_on_error: (experimental) Prevents a workflow run from failing when a job fails. Set to true to allow a workflow run to pass when this job fails.
        :param defaults: (experimental) Default configuration settings for job steps.
        :param env: (experimental) Environment variables for all steps in the job.
        :param environment: (experimental) GitHub environment target for this job.
        :param name: (experimental) Display name for the job.
        :param needs: (experimental) List of job dependencies that must complete before this job starts.
        :param outputs: (experimental) Outputs produced by this job, accessible by downstream jobs.
        :param permissions: (experimental) Permissions granted to the job.
        :param required_checks: (experimental) List of checks required to pass before this job runs.
        :param runner_labels: (experimental) Runner labels for selecting a self-hosted runner.
        :param runs_on: (experimental) Runner environment, e.g., "ubuntu-latest".
        :param services: (experimental) Used to host service containers for a job in a workflow. Service containers are useful for creating databases or cache services like Redis. The runner automatically creates a Docker network and manages the life cycle of the service containers.
        :param strategy: (experimental) Strategy settings, including matrix configuration and concurrency limits.
        :param timeout_minutes: (experimental) Timeout duration for the job, in minutes.

        :return: The created Job instance.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f34a806b49cc8fdf5c1996cee37edcf0e6e6b71f2f941a306977ec746287a7a3)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = JobProps(
            container=container,
            continue_on_error=continue_on_error,
            defaults=defaults,
            env=env,
            environment=environment,
            name=name,
            needs=needs,
            outputs=outputs,
            permissions=permissions,
            required_checks=required_checks,
            runner_labels=runner_labels,
            runs_on=runs_on,
            services=services,
            strategy=strategy,
            timeout_minutes=timeout_minutes,
        )

        return typing.cast(Job, jsii.invoke(self, "addJob", [id, props]))

    @jsii.member(jsii_name="hasJobs")
    def has_jobs(self) -> builtins.bool:
        '''(experimental) Checks if the current workflow contains any jobs.

        This method iterates through the children of the node associated with
        the workflow and checks if any of those children are instances of Job.
        If at least one child is a job, the method returns true; otherwise, it
        returns false.

        :return: True if the workflow has one or more jobs; otherwise, false.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.invoke(self, "hasJobs", []))

    @builtins.property
    @jsii.member(jsii_name="commentAtTop")
    def comment_at_top(self) -> builtins.str:
        '''(experimental) The comment included at the top of the generated workflow YAML.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "commentAtTop"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''(experimental) Gets the id of the workflow.

        :return: The unique identifier of the workflow.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="synthesizer")
    def synthesizer(self) -> IWorkflowSynthesizer:
        '''(experimental) Synthesizer responsible for generating the workflow YAML.

        :stability: experimental
        '''
        return typing.cast(IWorkflowSynthesizer, jsii.get(self, "synthesizer"))

    @builtins.property
    @jsii.member(jsii_name="triggers")
    def triggers(self) -> "WorkflowTriggers":
        '''(experimental) The triggers for the workflow.

        :stability: experimental
        '''
        return typing.cast("WorkflowTriggers", jsii.get(self, "triggers"))

    @builtins.property
    @jsii.member(jsii_name="concurrency")
    def concurrency(self) -> typing.Optional[ConcurrencyOptions]:
        '''(experimental) Concurrency settings for the workflow.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[ConcurrencyOptions], jsii.get(self, "concurrency"))

    @builtins.property
    @jsii.member(jsii_name="defaults")
    def defaults(self) -> typing.Optional[Defaults]:
        '''(experimental) Default settings applied to all jobs within the workflow.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[Defaults], jsii.get(self, "defaults"))

    @builtins.property
    @jsii.member(jsii_name="env")
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Environment variables available to all jobs in the workflow.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "env"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the workflow as displayed in GitHub Actions.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="permissions")
    def permissions(
        self,
    ) -> typing.Optional[typing.Union[PermissionsEvent, builtins.str]]:
        '''(experimental) Permissions required for the workflow to execute.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[PermissionsEvent, builtins.str]], jsii.get(self, "permissions"))

    @builtins.property
    @jsii.member(jsii_name="runName")
    def run_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The run name of the workflow, displayed in the GitHub Actions UI.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runName"))


@jsii.data_type(
    jsii_type="github-actions-cdk.WorkflowAnnotation",
    jsii_struct_bases=[],
    name_mapping={
        "construct_path": "constructPath",
        "level": "level",
        "message": "message",
        "stacktrace": "stacktrace",
    },
)
class WorkflowAnnotation:
    def __init__(
        self,
        *,
        construct_path: builtins.str,
        level: AnnotationMetadataEntryType,
        message: builtins.str,
        stacktrace: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Represents an annotation for a workflow, capturing details about the construct path, severity level, message, and optional stack trace.

        :param construct_path: (experimental) The path of the construct in the tree.
        :param level: (experimental) The severity level of the annotation (INFO, WARN, ERROR).
        :param message: (experimental) The message associated with the annotation.
        :param stacktrace: (experimental) Optional stack trace associated with the annotation, if applicable.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6944868d5e1f6c9a95e1ebfb3155ece01462e21eea012d4b2f712ece7a5de000)
            check_type(argname="argument construct_path", value=construct_path, expected_type=type_hints["construct_path"])
            check_type(argname="argument level", value=level, expected_type=type_hints["level"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            check_type(argname="argument stacktrace", value=stacktrace, expected_type=type_hints["stacktrace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "construct_path": construct_path,
            "level": level,
            "message": message,
        }
        if stacktrace is not None:
            self._values["stacktrace"] = stacktrace

    @builtins.property
    def construct_path(self) -> builtins.str:
        '''(experimental) The path of the construct in the tree.

        :stability: experimental
        '''
        result = self._values.get("construct_path")
        assert result is not None, "Required property 'construct_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def level(self) -> AnnotationMetadataEntryType:
        '''(experimental) The severity level of the annotation (INFO, WARN, ERROR).

        :stability: experimental
        '''
        result = self._values.get("level")
        assert result is not None, "Required property 'level' is missing"
        return typing.cast(AnnotationMetadataEntryType, result)

    @builtins.property
    def message(self) -> builtins.str:
        '''(experimental) The message associated with the annotation.

        :stability: experimental
        '''
        result = self._values.get("message")
        assert result is not None, "Required property 'message' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stacktrace(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Optional stack trace associated with the annotation, if applicable.

        :stability: experimental
        '''
        result = self._values.get("stacktrace")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowAnnotation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="github-actions-cdk.WorkflowManifest",
    jsii_struct_bases=[],
    name_mapping={
        "annotations": "annotations",
        "construct_path": "constructPath",
        "id": "id",
        "synthesized_workflow_path": "synthesizedWorkflowPath",
    },
)
class WorkflowManifest:
    def __init__(
        self,
        *,
        annotations: typing.Sequence[typing.Union[WorkflowAnnotation, typing.Dict[builtins.str, typing.Any]]],
        construct_path: builtins.str,
        id: builtins.str,
        synthesized_workflow_path: builtins.str,
    ) -> None:
        '''(experimental) Represents the manifest information for a workflow.

        :param annotations: (experimental) An array of annotations associated with the workflow.
        :param construct_path: (experimental) The construct path where the workflow is defined.
        :param id: (experimental) Unique identifier for the workflow.
        :param synthesized_workflow_path: (experimental) The file path where the synthesized workflow YAML is saved.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9b28e7e4e82969cfb65a5bb4195ccfff641ed514a8289d50621e5b747d75faa)
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument construct_path", value=construct_path, expected_type=type_hints["construct_path"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument synthesized_workflow_path", value=synthesized_workflow_path, expected_type=type_hints["synthesized_workflow_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "annotations": annotations,
            "construct_path": construct_path,
            "id": id,
            "synthesized_workflow_path": synthesized_workflow_path,
        }

    @builtins.property
    def annotations(self) -> typing.List[WorkflowAnnotation]:
        '''(experimental) An array of annotations associated with the workflow.

        :stability: experimental
        '''
        result = self._values.get("annotations")
        assert result is not None, "Required property 'annotations' is missing"
        return typing.cast(typing.List[WorkflowAnnotation], result)

    @builtins.property
    def construct_path(self) -> builtins.str:
        '''(experimental) The construct path where the workflow is defined.

        :stability: experimental
        '''
        result = self._values.get("construct_path")
        assert result is not None, "Required property 'construct_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> builtins.str:
        '''(experimental) Unique identifier for the workflow.

        :stability: experimental
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def synthesized_workflow_path(self) -> builtins.str:
        '''(experimental) The file path where the synthesized workflow YAML is saved.

        :stability: experimental
        '''
        result = self._values.get("synthesized_workflow_path")
        assert result is not None, "Required property 'synthesized_workflow_path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowManifest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="github-actions-cdk.WorkflowProps",
    jsii_struct_bases=[],
    name_mapping={
        "comment_at_top": "commentAtTop",
        "concurrency": "concurrency",
        "defaults": "defaults",
        "env": "env",
        "name": "name",
        "permissions": "permissions",
        "run_name": "runName",
        "synthesizer": "synthesizer",
        "triggers": "triggers",
    },
)
class WorkflowProps:
    def __init__(
        self,
        *,
        comment_at_top: typing.Optional[builtins.str] = None,
        concurrency: typing.Optional[typing.Union[ConcurrencyOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        defaults: typing.Optional[typing.Union[Defaults, typing.Dict[builtins.str, typing.Any]]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        permissions: typing.Optional[typing.Union[typing.Union[PermissionsEvent, typing.Dict[builtins.str, typing.Any]], builtins.str]] = None,
        run_name: typing.Optional[builtins.str] = None,
        synthesizer: typing.Optional[IWorkflowSynthesizer] = None,
        triggers: typing.Optional[typing.Union["WorkflowTriggers", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Workflow configuration properties.

        :param comment_at_top: (experimental) An optional comment that can be included at the top of the generated workflow YAML. This can serve as a note or reminder for users not to modify the generated output directly. Default: "Generated by github-actions-cdk, DO NOT EDIT DIRECTLY!"
        :param concurrency: (experimental) Configuration for concurrency control of workflow runs.
        :param defaults: (experimental) Default configuration settings for jobs in this workflow.
        :param env: (experimental) Environment variables that will be available to all jobs in the workflow.
        :param name: (experimental) The name of the workflow. GitHub displays the names of your workflows under your repository's "Actions" tab. If you omit the name, GitHub displays the workflow file path relative to the root of the repository.
        :param permissions: (experimental) Permissions required by the workflow.
        :param run_name: (experimental) The name for workflow runs generated from the workflow. GitHub displays the workflow run name in the list of workflow runs on your repository's "Actions" tab. If ``run-name`` is omitted or is only whitespace, then the run name is set to event-specific information for the workflow run. For example, for a workflow triggered by a ``push`` or ``pull_request`` event, it is set as the commit message or the title of the pull request. This value can include expressions and can reference the ``github`` and ``inputs`` contexts.
        :param synthesizer: (experimental) Custom synthesizer for rendering the workflow YAML.
        :param triggers: (experimental) Triggers that define when this workflow should run.

        :stability: experimental
        '''
        if isinstance(concurrency, dict):
            concurrency = ConcurrencyOptions(**concurrency)
        if isinstance(defaults, dict):
            defaults = Defaults(**defaults)
        if isinstance(triggers, dict):
            triggers = WorkflowTriggers(**triggers)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8c923454de3cef4072be6958820f7ace0189f13e0a83a631fe60e1bb68b6ba0)
            check_type(argname="argument comment_at_top", value=comment_at_top, expected_type=type_hints["comment_at_top"])
            check_type(argname="argument concurrency", value=concurrency, expected_type=type_hints["concurrency"])
            check_type(argname="argument defaults", value=defaults, expected_type=type_hints["defaults"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
            check_type(argname="argument run_name", value=run_name, expected_type=type_hints["run_name"])
            check_type(argname="argument synthesizer", value=synthesizer, expected_type=type_hints["synthesizer"])
            check_type(argname="argument triggers", value=triggers, expected_type=type_hints["triggers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if comment_at_top is not None:
            self._values["comment_at_top"] = comment_at_top
        if concurrency is not None:
            self._values["concurrency"] = concurrency
        if defaults is not None:
            self._values["defaults"] = defaults
        if env is not None:
            self._values["env"] = env
        if name is not None:
            self._values["name"] = name
        if permissions is not None:
            self._values["permissions"] = permissions
        if run_name is not None:
            self._values["run_name"] = run_name
        if synthesizer is not None:
            self._values["synthesizer"] = synthesizer
        if triggers is not None:
            self._values["triggers"] = triggers

    @builtins.property
    def comment_at_top(self) -> typing.Optional[builtins.str]:
        '''(experimental) An optional comment that can be included at the top of the generated workflow YAML.

        This can serve as a note or reminder for users not to modify the generated output directly.

        :default: "Generated by github-actions-cdk, DO NOT EDIT DIRECTLY!"

        :stability: experimental
        '''
        result = self._values.get("comment_at_top")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def concurrency(self) -> typing.Optional[ConcurrencyOptions]:
        '''(experimental) Configuration for concurrency control of workflow runs.

        :stability: experimental
        '''
        result = self._values.get("concurrency")
        return typing.cast(typing.Optional[ConcurrencyOptions], result)

    @builtins.property
    def defaults(self) -> typing.Optional[Defaults]:
        '''(experimental) Default configuration settings for jobs in this workflow.

        :stability: experimental
        '''
        result = self._values.get("defaults")
        return typing.cast(typing.Optional[Defaults], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Environment variables that will be available to all jobs in the workflow.

        :stability: experimental
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the workflow.

        GitHub displays the names of your workflows under your repository's "Actions" tab.
        If you omit the name, GitHub displays the workflow file path relative to the root of the repository.

        :stability: experimental

        Example::

            "CI/CD Pipeline"
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permissions(
        self,
    ) -> typing.Optional[typing.Union[PermissionsEvent, builtins.str]]:
        '''(experimental) Permissions required by the workflow.

        :stability: experimental
        '''
        result = self._values.get("permissions")
        return typing.cast(typing.Optional[typing.Union[PermissionsEvent, builtins.str]], result)

    @builtins.property
    def run_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name for workflow runs generated from the workflow.

        GitHub displays the workflow run name in the list of workflow runs on your repository's "Actions" tab.
        If ``run-name`` is omitted or is only whitespace, then the run name is set to event-specific
        information for the workflow run. For example, for a workflow triggered by a ``push`` or
        ``pull_request`` event, it is set as the commit message or the title of the pull request.

        This value can include expressions and can reference the ``github`` and ``inputs`` contexts.

        :stability: experimental

        Example::

            run-name: Deploy to ${{ inputs.deploy_target }} by@$[object Object]
        '''
        result = self._values.get("run_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def synthesizer(self) -> typing.Optional[IWorkflowSynthesizer]:
        '''(experimental) Custom synthesizer for rendering the workflow YAML.

        :stability: experimental
        '''
        result = self._values.get("synthesizer")
        return typing.cast(typing.Optional[IWorkflowSynthesizer], result)

    @builtins.property
    def triggers(self) -> typing.Optional["WorkflowTriggers"]:
        '''(experimental) Triggers that define when this workflow should run.

        :stability: experimental
        '''
        result = self._values.get("triggers")
        return typing.cast(typing.Optional["WorkflowTriggers"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="github-actions-cdk.WorkflowRunOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class WorkflowRunOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Options for workflow run events.

        :param types: (experimental) Activity types to trigger on. Default: - triggers on all activity types

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35c782811768802411aa6ff7edcbe38992320a84757598048527ae3ac7bf30c0)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Activity types to trigger on.

        :default: - triggers on all activity types

        :stability: experimental
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowRunOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IWorkflowSynthesizer)
class WorkflowSynthesizer(
    metaclass=jsii.JSIIMeta,
    jsii_type="github-actions-cdk.WorkflowSynthesizer",
):
    '''(experimental) Handles the synthesis of a GitHub Actions workflow, generating YAML output.

    :stability: experimental
    '''

    def __init__(self, workflow: Workflow) -> None:
        '''(experimental) Creates a new instance of WorkflowSynthesizer.

        :param workflow: - The workflow to be synthesized.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f337c274717486564cb9bc661de952cd08b8d23d50cb1e7f9631702d15f90ddd)
            check_type(argname="argument workflow", value=workflow, expected_type=type_hints["workflow"])
        jsii.create(self.__class__, self, [workflow])

    @jsii.member(jsii_name="synthesize")
    def synthesize(self, session: ISynthesisSession) -> None:
        '''(experimental) Synthesizes the workflow into a YAML file.

        This process includes invoking aspects, validating the workflow,
        checking annotations, and writing the output to a file.

        :param session: - The synthesis session containing configuration for the synthesis process.

        :stability: experimental
        :throws: {ValidationError} If validation errors are found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dc70ff711e96611ad50e873acd15cb50ecf1af3bad9f6330aed348379a7389e)
            check_type(argname="argument session", value=session, expected_type=type_hints["session"])
        return typing.cast(None, jsii.invoke(self, "synthesize", [session]))

    @builtins.property
    @jsii.member(jsii_name="workflow")
    def _workflow(self) -> Workflow:
        '''(experimental) - The workflow to be synthesized.

        :stability: experimental
        '''
        return typing.cast(Workflow, jsii.get(self, "workflow"))

    @_workflow.setter
    def _workflow(self, value: Workflow) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5534784f89e398682523a4b5f5dc56c836bc60f371f60013a82b78391ac8eb1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workflow", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="github-actions-cdk.WorkflowTriggers",
    jsii_struct_bases=[],
    name_mapping={
        "check_run": "checkRun",
        "check_suite": "checkSuite",
        "issue_comment": "issueComment",
        "issues": "issues",
        "label": "label",
        "milestone": "milestone",
        "project": "project",
        "project_card": "projectCard",
        "project_column": "projectColumn",
        "pull_request": "pullRequest",
        "pull_request_review": "pullRequestReview",
        "pull_request_review_comment": "pullRequestReviewComment",
        "pull_request_target": "pullRequestTarget",
        "push": "push",
        "registry_package": "registryPackage",
        "release": "release",
        "repository_dispatch": "repositoryDispatch",
        "schedule": "schedule",
        "watch": "watch",
        "workflow_dispatch": "workflowDispatch",
        "workflow_run": "workflowRun",
    },
)
class WorkflowTriggers:
    def __init__(
        self,
        *,
        check_run: typing.Optional[typing.Union[CheckRunOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        check_suite: typing.Optional[typing.Union[CheckSuiteOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        issue_comment: typing.Optional[typing.Union[IssueCommentOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        issues: typing.Optional[typing.Union[IssuesOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        label: typing.Optional[typing.Union[LabelOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        milestone: typing.Optional[typing.Union[MilestoneOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[typing.Union[ProjectOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        project_card: typing.Optional[typing.Union[ProjectCardOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        project_column: typing.Optional[typing.Union[ProjectColumnOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        pull_request: typing.Optional[typing.Union[PullRequestOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        pull_request_review: typing.Optional[typing.Union[PullRequestReviewOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        pull_request_review_comment: typing.Optional[typing.Union[PullRequestReviewCommentOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        pull_request_target: typing.Optional[typing.Union["PullRequestTargetOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        push: typing.Optional[typing.Union[PushOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        registry_package: typing.Optional[typing.Union[RegistryPackageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        release: typing.Optional[typing.Union[ReleaseOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        repository_dispatch: typing.Optional[typing.Union[RepositoryDispatchOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        schedule: typing.Optional[typing.Sequence[typing.Union[CronScheduleOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        watch: typing.Optional[typing.Union[WatchOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        workflow_dispatch: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        workflow_run: typing.Optional[typing.Union[WorkflowRunOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Available triggers for GitHub Workflows.

        :param check_run: (experimental) Triggers workflow based on check run events.
        :param check_suite: (experimental) Triggers workflow based on check suite events.
        :param issue_comment: (experimental) Triggers workflow based on issue comment events.
        :param issues: (experimental) Triggers workflow based on issue events.
        :param label: (experimental) Triggers workflow based on label events.
        :param milestone: (experimental) Triggers workflow based on milestone events.
        :param project: (experimental) Triggers workflow based on project events.
        :param project_card: (experimental) Triggers workflow based on project card events.
        :param project_column: (experimental) Triggers workflow based on project column events.
        :param pull_request: (experimental) Triggers workflow based on pull request events.
        :param pull_request_review: (experimental) Triggers workflow based on pull request review events.
        :param pull_request_review_comment: (experimental) Triggers workflow based on pull request review comment events.
        :param pull_request_target: (experimental) Triggers workflow based on pull request target events.
        :param push: (experimental) Triggers workflow based on push events to repository branches.
        :param registry_package: (experimental) Triggers workflow based on registry package publish/updates.
        :param release: (experimental) Triggers workflow based on release events.
        :param repository_dispatch: (experimental) Triggers workflow based on repository dispatch events from external activities.
        :param schedule: (experimental) Schedule for running workflows at specific UTC times using POSIX cron syntax.
        :param watch: (experimental) Triggers workflow based on watch events for repositories.
        :param workflow_dispatch: (experimental) Allows for manual triggering of workflows with custom input values.
        :param workflow_run: (experimental) Triggers workflow based on workflow run events.

        :stability: experimental
        '''
        if isinstance(check_run, dict):
            check_run = CheckRunOptions(**check_run)
        if isinstance(check_suite, dict):
            check_suite = CheckSuiteOptions(**check_suite)
        if isinstance(issue_comment, dict):
            issue_comment = IssueCommentOptions(**issue_comment)
        if isinstance(issues, dict):
            issues = IssuesOptions(**issues)
        if isinstance(label, dict):
            label = LabelOptions(**label)
        if isinstance(milestone, dict):
            milestone = MilestoneOptions(**milestone)
        if isinstance(project, dict):
            project = ProjectOptions(**project)
        if isinstance(project_card, dict):
            project_card = ProjectCardOptions(**project_card)
        if isinstance(project_column, dict):
            project_column = ProjectColumnOptions(**project_column)
        if isinstance(pull_request, dict):
            pull_request = PullRequestOptions(**pull_request)
        if isinstance(pull_request_review, dict):
            pull_request_review = PullRequestReviewOptions(**pull_request_review)
        if isinstance(pull_request_review_comment, dict):
            pull_request_review_comment = PullRequestReviewCommentOptions(**pull_request_review_comment)
        if isinstance(pull_request_target, dict):
            pull_request_target = PullRequestTargetOptions(**pull_request_target)
        if isinstance(push, dict):
            push = PushOptions(**push)
        if isinstance(registry_package, dict):
            registry_package = RegistryPackageOptions(**registry_package)
        if isinstance(release, dict):
            release = ReleaseOptions(**release)
        if isinstance(repository_dispatch, dict):
            repository_dispatch = RepositoryDispatchOptions(**repository_dispatch)
        if isinstance(watch, dict):
            watch = WatchOptions(**watch)
        if isinstance(workflow_run, dict):
            workflow_run = WorkflowRunOptions(**workflow_run)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc76e74c3cda759effeb55fe91653631fd5c1987a7e7836ecf7d77b5319583e2)
            check_type(argname="argument check_run", value=check_run, expected_type=type_hints["check_run"])
            check_type(argname="argument check_suite", value=check_suite, expected_type=type_hints["check_suite"])
            check_type(argname="argument issue_comment", value=issue_comment, expected_type=type_hints["issue_comment"])
            check_type(argname="argument issues", value=issues, expected_type=type_hints["issues"])
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument milestone", value=milestone, expected_type=type_hints["milestone"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument project_card", value=project_card, expected_type=type_hints["project_card"])
            check_type(argname="argument project_column", value=project_column, expected_type=type_hints["project_column"])
            check_type(argname="argument pull_request", value=pull_request, expected_type=type_hints["pull_request"])
            check_type(argname="argument pull_request_review", value=pull_request_review, expected_type=type_hints["pull_request_review"])
            check_type(argname="argument pull_request_review_comment", value=pull_request_review_comment, expected_type=type_hints["pull_request_review_comment"])
            check_type(argname="argument pull_request_target", value=pull_request_target, expected_type=type_hints["pull_request_target"])
            check_type(argname="argument push", value=push, expected_type=type_hints["push"])
            check_type(argname="argument registry_package", value=registry_package, expected_type=type_hints["registry_package"])
            check_type(argname="argument release", value=release, expected_type=type_hints["release"])
            check_type(argname="argument repository_dispatch", value=repository_dispatch, expected_type=type_hints["repository_dispatch"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument watch", value=watch, expected_type=type_hints["watch"])
            check_type(argname="argument workflow_dispatch", value=workflow_dispatch, expected_type=type_hints["workflow_dispatch"])
            check_type(argname="argument workflow_run", value=workflow_run, expected_type=type_hints["workflow_run"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if check_run is not None:
            self._values["check_run"] = check_run
        if check_suite is not None:
            self._values["check_suite"] = check_suite
        if issue_comment is not None:
            self._values["issue_comment"] = issue_comment
        if issues is not None:
            self._values["issues"] = issues
        if label is not None:
            self._values["label"] = label
        if milestone is not None:
            self._values["milestone"] = milestone
        if project is not None:
            self._values["project"] = project
        if project_card is not None:
            self._values["project_card"] = project_card
        if project_column is not None:
            self._values["project_column"] = project_column
        if pull_request is not None:
            self._values["pull_request"] = pull_request
        if pull_request_review is not None:
            self._values["pull_request_review"] = pull_request_review
        if pull_request_review_comment is not None:
            self._values["pull_request_review_comment"] = pull_request_review_comment
        if pull_request_target is not None:
            self._values["pull_request_target"] = pull_request_target
        if push is not None:
            self._values["push"] = push
        if registry_package is not None:
            self._values["registry_package"] = registry_package
        if release is not None:
            self._values["release"] = release
        if repository_dispatch is not None:
            self._values["repository_dispatch"] = repository_dispatch
        if schedule is not None:
            self._values["schedule"] = schedule
        if watch is not None:
            self._values["watch"] = watch
        if workflow_dispatch is not None:
            self._values["workflow_dispatch"] = workflow_dispatch
        if workflow_run is not None:
            self._values["workflow_run"] = workflow_run

    @builtins.property
    def check_run(self) -> typing.Optional[CheckRunOptions]:
        '''(experimental) Triggers workflow based on check run events.

        :stability: experimental
        '''
        result = self._values.get("check_run")
        return typing.cast(typing.Optional[CheckRunOptions], result)

    @builtins.property
    def check_suite(self) -> typing.Optional[CheckSuiteOptions]:
        '''(experimental) Triggers workflow based on check suite events.

        :stability: experimental
        '''
        result = self._values.get("check_suite")
        return typing.cast(typing.Optional[CheckSuiteOptions], result)

    @builtins.property
    def issue_comment(self) -> typing.Optional[IssueCommentOptions]:
        '''(experimental) Triggers workflow based on issue comment events.

        :stability: experimental
        '''
        result = self._values.get("issue_comment")
        return typing.cast(typing.Optional[IssueCommentOptions], result)

    @builtins.property
    def issues(self) -> typing.Optional[IssuesOptions]:
        '''(experimental) Triggers workflow based on issue events.

        :stability: experimental
        '''
        result = self._values.get("issues")
        return typing.cast(typing.Optional[IssuesOptions], result)

    @builtins.property
    def label(self) -> typing.Optional[LabelOptions]:
        '''(experimental) Triggers workflow based on label events.

        :stability: experimental
        '''
        result = self._values.get("label")
        return typing.cast(typing.Optional[LabelOptions], result)

    @builtins.property
    def milestone(self) -> typing.Optional[MilestoneOptions]:
        '''(experimental) Triggers workflow based on milestone events.

        :stability: experimental
        '''
        result = self._values.get("milestone")
        return typing.cast(typing.Optional[MilestoneOptions], result)

    @builtins.property
    def project(self) -> typing.Optional[ProjectOptions]:
        '''(experimental) Triggers workflow based on project events.

        :stability: experimental
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[ProjectOptions], result)

    @builtins.property
    def project_card(self) -> typing.Optional[ProjectCardOptions]:
        '''(experimental) Triggers workflow based on project card events.

        :stability: experimental
        '''
        result = self._values.get("project_card")
        return typing.cast(typing.Optional[ProjectCardOptions], result)

    @builtins.property
    def project_column(self) -> typing.Optional[ProjectColumnOptions]:
        '''(experimental) Triggers workflow based on project column events.

        :stability: experimental
        '''
        result = self._values.get("project_column")
        return typing.cast(typing.Optional[ProjectColumnOptions], result)

    @builtins.property
    def pull_request(self) -> typing.Optional[PullRequestOptions]:
        '''(experimental) Triggers workflow based on pull request events.

        :stability: experimental
        '''
        result = self._values.get("pull_request")
        return typing.cast(typing.Optional[PullRequestOptions], result)

    @builtins.property
    def pull_request_review(self) -> typing.Optional[PullRequestReviewOptions]:
        '''(experimental) Triggers workflow based on pull request review events.

        :stability: experimental
        '''
        result = self._values.get("pull_request_review")
        return typing.cast(typing.Optional[PullRequestReviewOptions], result)

    @builtins.property
    def pull_request_review_comment(
        self,
    ) -> typing.Optional[PullRequestReviewCommentOptions]:
        '''(experimental) Triggers workflow based on pull request review comment events.

        :stability: experimental
        '''
        result = self._values.get("pull_request_review_comment")
        return typing.cast(typing.Optional[PullRequestReviewCommentOptions], result)

    @builtins.property
    def pull_request_target(self) -> typing.Optional["PullRequestTargetOptions"]:
        '''(experimental) Triggers workflow based on pull request target events.

        :stability: experimental
        '''
        result = self._values.get("pull_request_target")
        return typing.cast(typing.Optional["PullRequestTargetOptions"], result)

    @builtins.property
    def push(self) -> typing.Optional[PushOptions]:
        '''(experimental) Triggers workflow based on push events to repository branches.

        :stability: experimental
        '''
        result = self._values.get("push")
        return typing.cast(typing.Optional[PushOptions], result)

    @builtins.property
    def registry_package(self) -> typing.Optional[RegistryPackageOptions]:
        '''(experimental) Triggers workflow based on registry package publish/updates.

        :stability: experimental
        '''
        result = self._values.get("registry_package")
        return typing.cast(typing.Optional[RegistryPackageOptions], result)

    @builtins.property
    def release(self) -> typing.Optional[ReleaseOptions]:
        '''(experimental) Triggers workflow based on release events.

        :stability: experimental
        '''
        result = self._values.get("release")
        return typing.cast(typing.Optional[ReleaseOptions], result)

    @builtins.property
    def repository_dispatch(self) -> typing.Optional[RepositoryDispatchOptions]:
        '''(experimental) Triggers workflow based on repository dispatch events from external activities.

        :stability: experimental
        '''
        result = self._values.get("repository_dispatch")
        return typing.cast(typing.Optional[RepositoryDispatchOptions], result)

    @builtins.property
    def schedule(self) -> typing.Optional[typing.List[CronScheduleOptions]]:
        '''(experimental) Schedule for running workflows at specific UTC times using POSIX cron syntax.

        :stability: experimental
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[typing.List[CronScheduleOptions]], result)

    @builtins.property
    def watch(self) -> typing.Optional[WatchOptions]:
        '''(experimental) Triggers workflow based on watch events for repositories.

        :stability: experimental
        '''
        result = self._values.get("watch")
        return typing.cast(typing.Optional[WatchOptions], result)

    @builtins.property
    def workflow_dispatch(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Allows for manual triggering of workflows with custom input values.

        :stability: experimental
        '''
        result = self._values.get("workflow_dispatch")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def workflow_run(self) -> typing.Optional[WorkflowRunOptions]:
        '''(experimental) Triggers workflow based on workflow run events.

        :stability: experimental
        '''
        result = self._values.get("workflow_run")
        return typing.cast(typing.Optional[WorkflowRunOptions], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowTriggers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkflowValidator(
    Validator,
    metaclass=jsii.JSIIMeta,
    jsii_type="github-actions-cdk.WorkflowValidator",
):
    '''(experimental) Validator for ``Workflow`` instances.

    :stability: experimental
    :remarks:

    Validates properties and configurations specific to workflows, such as
    cron schedules, environment variables, and shell defaults.
    '''

    def __init__(self, workflow: Workflow) -> None:
        '''
        :param workflow: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f0762a405dc9822d673fe740917a8ab1ff8ac9d3c6f53d4305345f6e4fc386a)
            check_type(argname="argument workflow", value=workflow, expected_type=type_hints["workflow"])
        jsii.create(self.__class__, self, [workflow])

    @jsii.member(jsii_name="validate")
    def validate(self) -> typing.List[builtins.str]:
        '''(experimental) Validates various aspects of a workflow's configuration.

        :return: An array of error messages if validation fails.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validate", []))


@jsii.data_type(
    jsii_type="github-actions-cdk.ActionProps",
    jsii_struct_bases=[CommonActionProps],
    name_mapping={
        "name": "name",
        "action_identifier": "actionIdentifier",
        "parameters": "parameters",
        "version": "version",
    },
)
class ActionProps(CommonActionProps):
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        action_identifier: builtins.str,
        parameters: typing.Mapping[builtins.str, typing.Any],
        version: builtins.str,
    ) -> None:
        '''(experimental) Configuration properties specific to defining a GitHub Action instance in a workflow.

        :param name: (experimental) Display name for the action, shown in GitHub workflow logs for better readability.
        :param action_identifier: (experimental) Unique identifier for the action, typically formatted as ``owner/repo``.
        :param parameters: (experimental) Parameters specific to this action, typically a set of key-value pairs.
        :param version: (experimental) Version of the action, which can be a specific release, branch, or commit SHA.

        :stability: experimental
        :remarks:

        ``ActionProps`` extends ``CommonActionProps`` by adding essential properties to identify a GitHub Action,
        such as ``actionIdentifier`` for the action's source and ``version`` for the specific release or branch.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c67d92ddddb47d887e29da7bf6b0e42ad1021d78b44eb09fe02d19b70124b79)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument action_identifier", value=action_identifier, expected_type=type_hints["action_identifier"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action_identifier": action_identifier,
            "parameters": parameters,
            "version": version,
        }
        if name is not None:
            self._values["name"] = name

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
    def action_identifier(self) -> builtins.str:
        '''(experimental) Unique identifier for the action, typically formatted as ``owner/repo``.

        :stability: experimental
        :remarks: This identifier specifies the source of the action, either from GitHub Marketplace or within a repository.

        Example::

            "actions/checkout" // Refers to the GitHub Actions `checkout` action
        '''
        result = self._values.get("action_identifier")
        assert result is not None, "Required property 'action_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''(experimental) Parameters specific to this action, typically a set of key-value pairs.

        :stability: experimental
        :remarks:

        These parameters are passed directly to the action, enabling customization based on the action's expected
        inputs (e.g., repository, path, or token).

        Example::

            `{ repository: "my-org/my-repo", token: "ghp_xxx..." }`
        '''
        result = self._values.get("parameters")
        assert result is not None, "Required property 'parameters' is missing"
        return typing.cast(typing.Mapping[builtins.str, typing.Any], result)

    @builtins.property
    def version(self) -> builtins.str:
        '''(experimental) Version of the action, which can be a specific release, branch, or commit SHA.

        :stability: experimental
        :remarks:

        When defined, this version ensures that the action uses a specific release. Leaving it undefined will
        generally result in the action using its latest version.

        Example::

            "v2" // Uses version 2 of the action
        '''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IAspect)
class Check(metaclass=jsii.JSIIAbstractClass, jsii_type="github-actions-cdk.Check"):
    '''(experimental) Base class for configurable check aspects.

    :stability: experimental
    '''

    def __init__(self, level: typing.Optional[builtins.str] = None) -> None:
        '''
        :param level: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f6d00ddf68ee0f86a585f65b655bded05777d266d6d6d7260d0de6432646605)
            check_type(argname="argument level", value=level, expected_type=type_hints["level"])
        jsii.create(self.__class__, self, [level])

    @jsii.member(jsii_name="annotate")
    def _annotate(
        self,
        node: _constructs_77d1e7e8.IConstruct,
        message: builtins.str,
    ) -> None:
        '''(experimental) Adds a message with the configured level to the node's annotations.

        :param node: - The construct node to annotate.
        :param message: - The message to add.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5594ababe867237e537604cc46c16c1a114cb7b4c1234529285a514365705536)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
        return typing.cast(None, jsii.invoke(self, "annotate", [node, message]))

    @jsii.member(jsii_name="visit")
    @abc.abstractmethod
    def visit(self, node: _constructs_77d1e7e8.IConstruct) -> None:
        '''(experimental) Abstract visit method to be implemented by subclasses, providing the node to check.

        :param node: -

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="level")
    def _level(self) -> builtins.str:
        '''(experimental) Default error level.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "level"))


class _CheckProxy(Check):
    @jsii.member(jsii_name="visit")
    def visit(self, node: _constructs_77d1e7e8.IConstruct) -> None:
        '''(experimental) Abstract visit method to be implemented by subclasses, providing the node to check.

        :param node: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fea27cc802b793b4aad2ed163af4911c670bb848810f9ac958604fad5419d5c3)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "visit", [node]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, Check).__jsii_proxy_class__ = lambda : _CheckProxy


class JobValidator(
    Validator,
    metaclass=jsii.JSIIMeta,
    jsii_type="github-actions-cdk.JobValidator",
):
    '''(experimental) Validator for ``Job`` instances.

    :stability: experimental
    :remarks:

    Validates properties of a job within a workflow, including its ID, environment variables, shell type,
    and the presence of at least one step.
    '''

    def __init__(self, job: Job) -> None:
        '''
        :param job: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3a97ff857bace6377e402d8c6a1b51a3b5873ea6ad900f031d649df3178b62a)
            check_type(argname="argument job", value=job, expected_type=type_hints["job"])
        jsii.create(self.__class__, self, [job])

    @jsii.member(jsii_name="validate")
    def validate(self) -> typing.List[builtins.str]:
        '''(experimental) Validates the job's configuration, including ID, environment variables, shell type, and the presence of steps.

        :return: An array of error messages if validation fails.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validate", []))


@jsii.data_type(
    jsii_type="github-actions-cdk.PullRequestTargetOptions",
    jsii_struct_bases=[PushOptions],
    name_mapping={
        "branches": "branches",
        "paths": "paths",
        "tags": "tags",
        "types": "types",
    },
)
class PullRequestTargetOptions(PushOptions):
    def __init__(
        self,
        *,
        branches: typing.Optional[typing.Sequence[builtins.str]] = None,
        paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Options for pull request target events.

        Extends push options.

        :param branches: (experimental) Branches to trigger on. For pull requests, only base branches are evaluated.
        :param paths: (experimental) File path patterns to trigger on. Default: - triggers on all paths
        :param tags: (experimental) Tags to trigger on. Default: - triggers on all tags
        :param types: (experimental) Activity types to trigger on. Default: - triggers on all activity types

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1319d4d58bfbf23a563a7e1f5938f52dd59aa97e218664fd9084b683391cb7df)
            check_type(argname="argument branches", value=branches, expected_type=type_hints["branches"])
            check_type(argname="argument paths", value=paths, expected_type=type_hints["paths"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if branches is not None:
            self._values["branches"] = branches
        if paths is not None:
            self._values["paths"] = paths
        if tags is not None:
            self._values["tags"] = tags
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def branches(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Branches to trigger on.

        For pull requests, only base branches are evaluated.

        :see: https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#filter-pattern-cheat-sheet
        :stability: experimental
        '''
        result = self._values.get("branches")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) File path patterns to trigger on.

        :default: - triggers on all paths

        :stability: experimental
        '''
        result = self._values.get("paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Tags to trigger on.

        :default: - triggers on all tags

        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Activity types to trigger on.

        :default: - triggers on all activity types

        :stability: experimental
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PullRequestTargetOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RegularStep(
    StepBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="github-actions-cdk.RegularStep",
):
    '''(experimental) Step that runs a predefined GitHub Action within a job.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        uses: builtins.str,
        parameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        condition: typing.Optional[builtins.str] = None,
        continue_on_error: typing.Optional[builtins.bool] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        timeout_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Creates a new ``RegularStep`` instance.

        :param scope: - The scope in which to define this construct.
        :param id: - The unique identifier for this step.
        :param uses: (experimental) GitHub Action to run, identified by repository or Docker image reference.
        :param parameters: (experimental) Input parameters for the action, passed as a key-value map.
        :param condition: (experimental) Conditional expression to determine if the step should run (equivalent to ``if`` in GitHub Actions). Supports GitHub Actions expressions, e.g., ``${{ success() }}``.
        :param continue_on_error: (experimental) Whether the job should continue if this step fails. Default: false
        :param env: (experimental) Environment variables specific to this step, overriding job-level or workflow-level variables.
        :param name: (experimental) A descriptive name for the step, displayed in the GitHub Actions UI.
        :param timeout_minutes: (experimental) Maximum execution time for the step, in minutes.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b950fbbd54a6db12efc3ddba957cc278be8b1fe0d82677793b7a956e54f15663)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = RegularStepProps(
            uses=uses,
            parameters=parameters,
            condition=condition,
            continue_on_error=continue_on_error,
            env=env,
            name=name,
            timeout_minutes=timeout_minutes,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="isRegularStep")
    @builtins.classmethod
    def is_regular_step(cls, x: typing.Any) -> builtins.bool:
        '''(experimental) Checks if an object is an instance of ``RegularStep``.

        :param x: - The object to check.

        :return: ``true`` if ``x`` is a ``RegularStep``; otherwise, ``false``.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e3c352efaba4562c7b667ab619020efa49db0c3954f7319a463c3fd7c935c11)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isRegularStep", [x]))

    @jsii.member(jsii_name="isDockerAction")
    def is_docker_action(self) -> builtins.bool:
        '''(experimental) Determines if the action is a Docker action.

        :return: ``true`` if the action is a Docker action; otherwise, ``false``.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.invoke(self, "isDockerAction", []))

    @jsii.member(jsii_name="isExternalAction")
    def is_external_action(self) -> builtins.bool:
        '''(experimental) Determines if the action is an external action.

        :return: ``true`` if the action is an external action; otherwise, ``false``.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.invoke(self, "isExternalAction", []))

    @jsii.member(jsii_name="isRepoAction")
    def is_repo_action(self) -> builtins.bool:
        '''(experimental) Determines if the action is a repository action.

        :return: ``true`` if the action is a repository action; otherwise, ``false``.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.invoke(self, "isRepoAction", []))

    @builtins.property
    @jsii.member(jsii_name="uses")
    def uses(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "uses"))

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], jsii.get(self, "parameters"))


class RegularStepValidator(
    Validator,
    metaclass=jsii.JSIIMeta,
    jsii_type="github-actions-cdk.RegularStepValidator",
):
    '''(experimental) Validator for ``RegularStep`` instances.

    :stability: experimental
    :remarks:

    Validates properties specific to a regular step, such as the "uses" format, ensuring it follows
    the required format for GitHub Actions reusable workflows.
    '''

    def __init__(self, step: RegularStep) -> None:
        '''
        :param step: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5146af3bc07037cf8abd259e7215ea6af345da64fc916ba7b88642b110f4e0c3)
            check_type(argname="argument step", value=step, expected_type=type_hints["step"])
        jsii.create(self.__class__, self, [step])

    @jsii.member(jsii_name="validate")
    def validate(self) -> typing.List[builtins.str]:
        '''(experimental) Validates properties specific to a regular step, such as the format of the ``uses`` property.

        :return: An array of error messages if validation fails.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validate", []))


class RunStep(
    StepBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="github-actions-cdk.RunStep",
):
    '''(experimental) Step that runs shell commands in a GitHub Actions job.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        run: typing.Union[builtins.str, typing.Sequence[builtins.str]],
        shell: typing.Optional[builtins.str] = None,
        working_directory: typing.Optional[builtins.str] = None,
        condition: typing.Optional[builtins.str] = None,
        continue_on_error: typing.Optional[builtins.bool] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        timeout_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Creates a new ``RunStep`` instance.

        :param scope: - The scope in which to define this construct.
        :param id: - The unique identifier for this step.
        :param run: (experimental) Commands or scripts to execute in this step.
        :param shell: (experimental) Shell environment for this step, allowing custom shells like ``bash``, ``pwsh``, etc. Default: "bash"
        :param working_directory: (experimental) Directory in which the step's command or action executes. Defaults to the job's working directory if not specified.
        :param condition: (experimental) Conditional expression to determine if the step should run (equivalent to ``if`` in GitHub Actions). Supports GitHub Actions expressions, e.g., ``${{ success() }}``.
        :param continue_on_error: (experimental) Whether the job should continue if this step fails. Default: false
        :param env: (experimental) Environment variables specific to this step, overriding job-level or workflow-level variables.
        :param name: (experimental) A descriptive name for the step, displayed in the GitHub Actions UI.
        :param timeout_minutes: (experimental) Maximum execution time for the step, in minutes.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47115f7c46b8aa2bd13f2ca276bcfdbb4283427f4d0f6d46ae1b6e0195649ef7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = RunStepProps(
            run=run,
            shell=shell,
            working_directory=working_directory,
            condition=condition,
            continue_on_error=continue_on_error,
            env=env,
            name=name,
            timeout_minutes=timeout_minutes,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="isRunStep")
    @builtins.classmethod
    def is_run_step(cls, x: typing.Any) -> builtins.bool:
        '''(experimental) Checks if an object is an instance of ``RunStep``.

        :param x: - The object to check.

        :return: ``true`` if ``x`` is a ``RunStep``; otherwise, ``false``.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2742a5330ae31ee341ce22632ae8f606415fb32083e38ec33b1367de384dfa0b)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isRunStep", [x]))

    @builtins.property
    @jsii.member(jsii_name="run")
    def run(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "run"))

    @builtins.property
    @jsii.member(jsii_name="shell")
    def shell(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "shell"))

    @builtins.property
    @jsii.member(jsii_name="workingDirectory")
    def working_directory(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workingDirectory"))


class RunStepValidator(
    Validator,
    metaclass=jsii.JSIIMeta,
    jsii_type="github-actions-cdk.RunStepValidator",
):
    '''(experimental) Validator for ``RunStep`` instances.

    :stability: experimental
    :remarks:

    Validates properties specific to a run step, such as shell type, ensuring
    compatibility with supported shells.
    '''

    def __init__(self, step: RunStep) -> None:
        '''
        :param step: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13ad166991bf23fc6f37c8e927d9d683905f387a1aaf8d498a0f170b5e82aee3)
            check_type(argname="argument step", value=step, expected_type=type_hints["step"])
        jsii.create(self.__class__, self, [step])

    @jsii.member(jsii_name="validate")
    def validate(self) -> typing.List[builtins.str]:
        '''(experimental) Validates properties specific to a run step, such as shell type.

        :return: An array of error messages if validation fails.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validate", []))


class StepBaseValidator(
    Validator,
    metaclass=jsii.JSIIMeta,
    jsii_type="github-actions-cdk.StepBaseValidator",
):
    '''(experimental) Validator for ``StepBase`` instances.

    :stability: experimental
    :remarks: Validates properties common to all step types within a job, such as ID and environment variables.
    '''

    def __init__(self, step: StepBase) -> None:
        '''
        :param step: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__998fa6c87ec77d4d366a8d9f14b61b39ee2de0d7cc0ff5048d9dc4aad90fc750)
            check_type(argname="argument step", value=step, expected_type=type_hints["step"])
        jsii.create(self.__class__, self, [step])

    @jsii.member(jsii_name="validate")
    def validate(self) -> typing.List[builtins.str]:
        '''(experimental) Validates common step properties, including ID format and environment variables.

        :return: An array of error messages if validation fails.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validate", []))


class Action(
    RegularStep,
    metaclass=jsii.JSIIMeta,
    jsii_type="github-actions-cdk.Action",
):
    '''(experimental) Abstract base class to represent a GitHub Action in a workflow.

    :stability: experimental
    :remarks: The ``Action`` class is a representation of a GitHub Action in a workflow.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        action_identifier: builtins.str,
        parameters: typing.Mapping[builtins.str, typing.Any],
        version: builtins.str,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Constructs a new instance of the ``Action`` class.

        :param scope: - The construct scope within which this action is defined.
        :param id: - A unique identifier for the action within the construct tree.
        :param action_identifier: (experimental) Unique identifier for the action, typically formatted as ``owner/repo``.
        :param parameters: (experimental) Parameters specific to this action, typically a set of key-value pairs.
        :param version: (experimental) Version of the action, which can be a specific release, branch, or commit SHA.
        :param name: (experimental) Display name for the action, shown in GitHub workflow logs for better readability.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9083af845695d517fd188c807376a21723381078b0375f588720ba0e18af144)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ActionProps(
            action_identifier=action_identifier,
            parameters=parameters,
            version=version,
            name=name,
        )

        jsii.create(self.__class__, self, [scope, id, props])


__all__ = [
    "Action",
    "ActionProps",
    "AnnotationMetadataEntryType",
    "Annotations",
    "Aspects",
    "Check",
    "CheckRunOptions",
    "CheckSuiteOptions",
    "CommonActionProps",
    "CommonStepProps",
    "Component",
    "ConcurrencyOptions",
    "ContainerCredentials",
    "ContainerOptions",
    "Cron",
    "CronOptions",
    "CronScheduleOptions",
    "Defaults",
    "Environment",
    "Expression",
    "IAspect",
    "IManifest",
    "ISynthesisSession",
    "IWorkflowSynthesizer",
    "IssueCommentOptions",
    "IssuesOptions",
    "Job",
    "JobProps",
    "JobValidator",
    "LabelOptions",
    "Manifest",
    "Matrix",
    "MilestoneOptions",
    "PermissionLevel",
    "PermissionsEvent",
    "Project",
    "ProjectCardOptions",
    "ProjectColumnOptions",
    "ProjectOptions",
    "ProjectProps",
    "PullRequestOptions",
    "PullRequestReviewCommentOptions",
    "PullRequestReviewOptions",
    "PullRequestTargetOptions",
    "PushOptions",
    "RegistryPackageOptions",
    "RegularStep",
    "RegularStepProps",
    "RegularStepValidator",
    "ReleaseOptions",
    "RepositoryDispatchOptions",
    "RunSettings",
    "RunStep",
    "RunStepProps",
    "RunStepValidator",
    "StepBase",
    "StepBaseValidator",
    "Strategy",
    "ValidationErrorMessage",
    "Validator",
    "WatchOptions",
    "Workflow",
    "WorkflowAnnotation",
    "WorkflowManifest",
    "WorkflowProps",
    "WorkflowRunOptions",
    "WorkflowSynthesizer",
    "WorkflowTriggers",
    "WorkflowValidator",
    "actions",
    "checks",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import actions
from . import checks

def _typecheckingstub__41853ff7ac51646114947d7ccb872e1de9083a5c4900057f8d8a456318e444b1(
    scope: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf15371b0b32189247fd2fa5d7da361f441b75c8466eb2d95e290c7c5925e1a5(
    message: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cd7b68a0f961ca03a01bb4a2848df3543dd010a8cc04387dae7427a33a274c5(
    message: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8fb2edf6217e6883f8480c7c1e3ec856adcc99d2f697a15a82ad4ba3dd9d99e(
    message: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9849ad7742ade5708dc29c2c349592e867841c1351e736e2595c097a43a8a697(
    scope: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2cd0e82cb0e76c6e1c9570a01b80475e7d91b7f38af5045f26e006bc742abde(
    aspect: IAspect,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5072f3495f4b3ba39176b029f0940e9c79221c2d0e31e596908947c243e493d1(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e104de4e65a228ba7996b869572411dc7ad5e1a2a7d6121de1f6ccd55f0e0e0(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c2457d2237bc9a4fbe495a7ad14440d0b2d6772b6a04f06098aa85b34837ac3(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4461e91974812e072653647f48469feee51054f06cb5f13a7cad6c2175e8290b(
    *,
    condition: typing.Optional[builtins.str] = None,
    continue_on_error: typing.Optional[builtins.bool] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    timeout_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cead5b79c90c5d033e0e67c6a4b6ab32d75b9b25a356a33e670e380460cbd641(
    scope: _constructs_77d1e7e8.IConstruct,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fdef1626108471936d90bdb773b97c0ad75e293b12de823502fcf8c725662c2(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2447762264aa67d0f00dbe099516e25b1326d1e83c0df0016a54fd25b6de84ac(
    path: builtins.str,
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b13408e5c019460595cf165919cb1c57a2410148d6fb00d9d9defcb7d65e776(
    *,
    group: builtins.str,
    cancel_in_progress: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5997eadaf75d9e6cd05815d9747672927e15adfd92719380a1dbbd3e31d9ec3(
    *,
    password: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5f7e57053d743d397fc21ea95452cce83840076921ca452abe46d7200ba007e(
    *,
    image: builtins.str,
    credentials: typing.Optional[typing.Union[ContainerCredentials, typing.Dict[builtins.str, typing.Any]]] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    options: typing.Optional[typing.Sequence[builtins.str]] = None,
    ports: typing.Optional[typing.Sequence[jsii.Number]] = None,
    volumes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__421e7476c56b104ee34b40b641f796adb4f6ed1124a2b669faba030276256f6c(
    expression: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a72dec72fc7f64420284eadcea6911406a89268b4330d95e815b45a734008dbd(
    expression: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f87d77789ba0ef97f504cc1ff5b1ad08e4c6aaf974d775c90a3fa4d819bc2d9(
    *,
    day: typing.Optional[builtins.str] = None,
    hour: typing.Optional[builtins.str] = None,
    minute: typing.Optional[builtins.str] = None,
    month: typing.Optional[builtins.str] = None,
    week_day: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__199600a8fe0c62df3cbff7bfcacbbf2f8e629df37768f92e7958220548d6dd60(
    *,
    cron: Cron,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37fef6d91b1101241267e5d35cbcd7e3ed2eb1139f4522bfcd355fc98907624f(
    *,
    run: typing.Optional[typing.Union[RunSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e00484e77e735ea20fd6f2113bad3b33b25a952640e97df3f6ccb53bf88c5e22(
    *,
    name: builtins.str,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__652ef72a750362b475687a33b055dad928a1e92d94365a9f021ba54bc2531888(
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c052e3e0c8198428a3912fd3a6ae477cb8b8713c50b31805c6711109db7b56f(
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a19e270a038d7235d302888dbc8430c67f616419d9e0d7622fbe25210462244a(
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75fc1df357426ae5fccdc448c6418fbf29e128e68fa95bc0e1036a13c512c920(
    node: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a272dd50f7650140229a9894b3ea042f23351f229dbf6e6bdf63d88290ddd368(
    session: ISynthesisSession,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9245f610dfdf28f8846ab53cd23fb911806e86522c4cea0c3e62e5529532c5bc(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf87540107a62d8d64ed58e95f8b01db8159513fdd767fdd8c3f30aa87899b9e(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba74ac8c28c96ce71749c13835adfaf0239f2f521dd066f17e0e73c75ff7d315(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    container: typing.Optional[typing.Union[ContainerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    continue_on_error: typing.Optional[builtins.bool] = None,
    defaults: typing.Optional[typing.Union[Defaults, typing.Dict[builtins.str, typing.Any]]] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    environment: typing.Optional[typing.Union[Environment, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    needs: typing.Optional[typing.Sequence[builtins.str]] = None,
    outputs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    permissions: typing.Optional[typing.Union[typing.Union[PermissionsEvent, typing.Dict[builtins.str, typing.Any]], builtins.str]] = None,
    required_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
    runner_labels: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
    runs_on: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
    services: typing.Optional[typing.Mapping[builtins.str, typing.Union[ContainerOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    strategy: typing.Optional[typing.Union[Strategy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04102a365a36ddd57481a063efb6b1cd4953a212e6fa1a614385d0a163d9a28c(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__560683b73063a8009cbc4b45624c887259235712969b5f491054f13ca86e6cf2(
    job: Job,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c84ddb7613f0dc156744978622a36eaccf42eb24f73fb68aadd45210e8a453a(
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af6c992ed1e3551de2bfc926e5e9d43b0d334c8ce844dfdc7a6dfcb6e483c25f(
    id: builtins.str,
    *,
    uses: builtins.str,
    parameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    condition: typing.Optional[builtins.str] = None,
    continue_on_error: typing.Optional[builtins.bool] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    timeout_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3f8799500375f858f993c7e31e1600bc24bfdd95ae1cf9e57200e7a867e49a2(
    id: builtins.str,
    *,
    run: typing.Union[builtins.str, typing.Sequence[builtins.str]],
    shell: typing.Optional[builtins.str] = None,
    working_directory: typing.Optional[builtins.str] = None,
    condition: typing.Optional[builtins.str] = None,
    continue_on_error: typing.Optional[builtins.bool] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    timeout_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20769971cc29ac6695fc59fa70f7ce92e7e4f43121f480d0ffcda1a97016201b(
    *,
    container: typing.Optional[typing.Union[ContainerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    continue_on_error: typing.Optional[builtins.bool] = None,
    defaults: typing.Optional[typing.Union[Defaults, typing.Dict[builtins.str, typing.Any]]] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    environment: typing.Optional[typing.Union[Environment, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    needs: typing.Optional[typing.Sequence[builtins.str]] = None,
    outputs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    permissions: typing.Optional[typing.Union[typing.Union[PermissionsEvent, typing.Dict[builtins.str, typing.Any]], builtins.str]] = None,
    required_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
    runner_labels: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
    runs_on: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
    services: typing.Optional[typing.Mapping[builtins.str, typing.Union[ContainerOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    strategy: typing.Optional[typing.Union[Strategy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb9e02a1d086f2f6835ff0ea1688329d1c317ce50ab856b1f80f5638e1cece8f(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e7cbe59fdc33cb58cca9416f9ec62a26538d9b96aa5706cd8f0189f8d6bf739(
    version: builtins.str,
    outdir: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dfdec75e2107c3fc50d8e620bb996f0d6bd7375948a2b8613aec4dd9d006d96(
    workflow: Workflow,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03098613492927ce72af982b6409517ead55bde8380b16f202b5570d740d05fc(
    *,
    domain: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[builtins.str]]] = None,
    exclude: typing.Optional[typing.Sequence[typing.Mapping[builtins.str, builtins.str]]] = None,
    include: typing.Optional[typing.Sequence[typing.Mapping[builtins.str, builtins.str]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de2c4c22ac0039acb049ce3c2e609e65738cb30ba50ee75b76ee87ddb332ad6f(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__250bfcabc87a33880947a3c29504b6eba32fdb6d7ba0d62131a0d5f9b95f3f5a(
    *,
    actions: typing.Optional[PermissionLevel] = None,
    checks: typing.Optional[PermissionLevel] = None,
    contents: typing.Optional[PermissionLevel] = None,
    deployments: typing.Optional[PermissionLevel] = None,
    discussions: typing.Optional[PermissionLevel] = None,
    id_token: typing.Optional[PermissionLevel] = None,
    issues: typing.Optional[PermissionLevel] = None,
    packages: typing.Optional[PermissionLevel] = None,
    pull_requests: typing.Optional[PermissionLevel] = None,
    repository_projects: typing.Optional[PermissionLevel] = None,
    security_events: typing.Optional[PermissionLevel] = None,
    statuses: typing.Optional[PermissionLevel] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f851528c9102c82f6c29bf01ec2c142ebc403fa63d25b0a6e4ede555270f048a(
    id: builtins.str,
    *,
    comment_at_top: typing.Optional[builtins.str] = None,
    concurrency: typing.Optional[typing.Union[ConcurrencyOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    defaults: typing.Optional[typing.Union[Defaults, typing.Dict[builtins.str, typing.Any]]] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    permissions: typing.Optional[typing.Union[typing.Union[PermissionsEvent, typing.Dict[builtins.str, typing.Any]], builtins.str]] = None,
    run_name: typing.Optional[builtins.str] = None,
    synthesizer: typing.Optional[IWorkflowSynthesizer] = None,
    triggers: typing.Optional[typing.Union[WorkflowTriggers, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb2f842de27922aee627b6c05553006d17dcf8a11e5f292933003092ca075b08(
    error: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7b94817da2f841c3520000a4ae8fca0578751c4ec686e7a7db759554fb271e2(
    workflows: typing.Sequence[Workflow],
    session: ISynthesisSession,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad415eff52b84a055c84337c2805ce9044b826d99699d6689cc01763af6c8119(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c3004989fcc8d55376e3ef3a1db982fc0094ca209aa3573c22b231d6389d9e7(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67d88b3a3d6d856bdf249d58a343a9ef8740ccb7f40fe245ca15140bf5b34fdb(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__450639eccdc42a348c0099dbce603df8cd9197de52538522be8040114716859d(
    *,
    additional_checks: typing.Optional[builtins.bool] = None,
    continue_on_error_annotations: typing.Optional[builtins.bool] = None,
    outdir: typing.Optional[builtins.str] = None,
    skip_validation: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68171705c985be084dbdca2a1ff2fd3444b5e640d632c443aa15eba47ab5bb67(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1607ee4b141291975fd72d3420b264f24669240b48469ea6fec28a7bb7c524e(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5c37c0870fb5ff9b5dceab001bb8fd29e70d138f195ff3a791bbf8f4da178c7(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b2dbee06284bd070f84759371f9d3e47ea1a2959e2747c9ef5348e41c0507fd(
    *,
    branches: typing.Optional[typing.Sequence[builtins.str]] = None,
    paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51ffb436656ac8c1233b106fe75017220f3ca1cbe93321807f6a71425e7024e4(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__143dd96d6b01c63c85ed87ccf4d0bf586729876d49a336389777dc744bdf347f(
    *,
    condition: typing.Optional[builtins.str] = None,
    continue_on_error: typing.Optional[builtins.bool] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    timeout_minutes: typing.Optional[jsii.Number] = None,
    uses: builtins.str,
    parameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__901c704f807a3bc66d62aca75564f6e9fa9ee5ef0df3967465126a7358291a92(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a077abe81a20c3b60a3bd4ce5d7da8a5d920dbc1e7cbe5febe1d4f88fec3359d(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__136f7dd5df10bc3efc63ac68784be915348e8e271405b406ee967bb475a85aa3(
    *,
    shell: typing.Optional[builtins.str] = None,
    working_directory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffdd2ad37969e8a3bc529751e5cc2b383b87766524f9b8d68ee5af9bdcb6d8e6(
    *,
    condition: typing.Optional[builtins.str] = None,
    continue_on_error: typing.Optional[builtins.bool] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    timeout_minutes: typing.Optional[jsii.Number] = None,
    run: typing.Union[builtins.str, typing.Sequence[builtins.str]],
    shell: typing.Optional[builtins.str] = None,
    working_directory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0432591929c3c2329eefcdae16020d8b81732031b2761d403ad6ad8948be0d7b(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    condition: typing.Optional[builtins.str] = None,
    continue_on_error: typing.Optional[builtins.bool] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    timeout_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d5c5071a05d3c40ca0e26005f92644373502ebc50d93c3ae0ed9893b1092eb9(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a94739a86ea2b0733bd3333cde61bb43462286e9e8e6c243cac71a73e2c0683f(
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__940058bd717a823643f0fa71e7845f3424e4d1bb4f6b6e9d54c9d10888d7c231(
    *,
    fail_fast: typing.Optional[builtins.bool] = None,
    matrix: typing.Optional[typing.Union[Matrix, typing.Dict[builtins.str, typing.Any]]] = None,
    max_parallel: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c7994564a0243148b62974f55dce47cb0c156adc21b83781f56cf9c92f78a02(
    *,
    message: builtins.str,
    source: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a127734cf9ec3d6224c134b97fa8221cd56f6b8ae5191ea2a24515e6f3db0915(
    property: typing.Any,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__785dc16d175b076483963c67da231a63908f82840f73cbe4b3bec91891692591(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdbc398a16d0309222333c5d160ce820ecd2201180eefcc6e06ee4dbca746de0(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    comment_at_top: typing.Optional[builtins.str] = None,
    concurrency: typing.Optional[typing.Union[ConcurrencyOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    defaults: typing.Optional[typing.Union[Defaults, typing.Dict[builtins.str, typing.Any]]] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    permissions: typing.Optional[typing.Union[typing.Union[PermissionsEvent, typing.Dict[builtins.str, typing.Any]], builtins.str]] = None,
    run_name: typing.Optional[builtins.str] = None,
    synthesizer: typing.Optional[IWorkflowSynthesizer] = None,
    triggers: typing.Optional[typing.Union[WorkflowTriggers, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f28757ff3d4552ffc090efd7c6174706e8f33b3f0134a50749d04b29931d1a2(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f34a806b49cc8fdf5c1996cee37edcf0e6e6b71f2f941a306977ec746287a7a3(
    id: builtins.str,
    *,
    container: typing.Optional[typing.Union[ContainerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    continue_on_error: typing.Optional[builtins.bool] = None,
    defaults: typing.Optional[typing.Union[Defaults, typing.Dict[builtins.str, typing.Any]]] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    environment: typing.Optional[typing.Union[Environment, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    needs: typing.Optional[typing.Sequence[builtins.str]] = None,
    outputs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    permissions: typing.Optional[typing.Union[typing.Union[PermissionsEvent, typing.Dict[builtins.str, typing.Any]], builtins.str]] = None,
    required_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
    runner_labels: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
    runs_on: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
    services: typing.Optional[typing.Mapping[builtins.str, typing.Union[ContainerOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    strategy: typing.Optional[typing.Union[Strategy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6944868d5e1f6c9a95e1ebfb3155ece01462e21eea012d4b2f712ece7a5de000(
    *,
    construct_path: builtins.str,
    level: AnnotationMetadataEntryType,
    message: builtins.str,
    stacktrace: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9b28e7e4e82969cfb65a5bb4195ccfff641ed514a8289d50621e5b747d75faa(
    *,
    annotations: typing.Sequence[typing.Union[WorkflowAnnotation, typing.Dict[builtins.str, typing.Any]]],
    construct_path: builtins.str,
    id: builtins.str,
    synthesized_workflow_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8c923454de3cef4072be6958820f7ace0189f13e0a83a631fe60e1bb68b6ba0(
    *,
    comment_at_top: typing.Optional[builtins.str] = None,
    concurrency: typing.Optional[typing.Union[ConcurrencyOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    defaults: typing.Optional[typing.Union[Defaults, typing.Dict[builtins.str, typing.Any]]] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    permissions: typing.Optional[typing.Union[typing.Union[PermissionsEvent, typing.Dict[builtins.str, typing.Any]], builtins.str]] = None,
    run_name: typing.Optional[builtins.str] = None,
    synthesizer: typing.Optional[IWorkflowSynthesizer] = None,
    triggers: typing.Optional[typing.Union[WorkflowTriggers, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35c782811768802411aa6ff7edcbe38992320a84757598048527ae3ac7bf30c0(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f337c274717486564cb9bc661de952cd08b8d23d50cb1e7f9631702d15f90ddd(
    workflow: Workflow,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dc70ff711e96611ad50e873acd15cb50ecf1af3bad9f6330aed348379a7389e(
    session: ISynthesisSession,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5534784f89e398682523a4b5f5dc56c836bc60f371f60013a82b78391ac8eb1d(
    value: Workflow,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc76e74c3cda759effeb55fe91653631fd5c1987a7e7836ecf7d77b5319583e2(
    *,
    check_run: typing.Optional[typing.Union[CheckRunOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    check_suite: typing.Optional[typing.Union[CheckSuiteOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    issue_comment: typing.Optional[typing.Union[IssueCommentOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    issues: typing.Optional[typing.Union[IssuesOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    label: typing.Optional[typing.Union[LabelOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    milestone: typing.Optional[typing.Union[MilestoneOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[typing.Union[ProjectOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    project_card: typing.Optional[typing.Union[ProjectCardOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    project_column: typing.Optional[typing.Union[ProjectColumnOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    pull_request: typing.Optional[typing.Union[PullRequestOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    pull_request_review: typing.Optional[typing.Union[PullRequestReviewOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    pull_request_review_comment: typing.Optional[typing.Union[PullRequestReviewCommentOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    pull_request_target: typing.Optional[typing.Union[PullRequestTargetOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    push: typing.Optional[typing.Union[PushOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    registry_package: typing.Optional[typing.Union[RegistryPackageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    release: typing.Optional[typing.Union[ReleaseOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    repository_dispatch: typing.Optional[typing.Union[RepositoryDispatchOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    schedule: typing.Optional[typing.Sequence[typing.Union[CronScheduleOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    watch: typing.Optional[typing.Union[WatchOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    workflow_dispatch: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    workflow_run: typing.Optional[typing.Union[WorkflowRunOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f0762a405dc9822d673fe740917a8ab1ff8ac9d3c6f53d4305345f6e4fc386a(
    workflow: Workflow,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c67d92ddddb47d887e29da7bf6b0e42ad1021d78b44eb09fe02d19b70124b79(
    *,
    name: typing.Optional[builtins.str] = None,
    action_identifier: builtins.str,
    parameters: typing.Mapping[builtins.str, typing.Any],
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f6d00ddf68ee0f86a585f65b655bded05777d266d6d6d7260d0de6432646605(
    level: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5594ababe867237e537604cc46c16c1a114cb7b4c1234529285a514365705536(
    node: _constructs_77d1e7e8.IConstruct,
    message: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fea27cc802b793b4aad2ed163af4911c670bb848810f9ac958604fad5419d5c3(
    node: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3a97ff857bace6377e402d8c6a1b51a3b5873ea6ad900f031d649df3178b62a(
    job: Job,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1319d4d58bfbf23a563a7e1f5938f52dd59aa97e218664fd9084b683391cb7df(
    *,
    branches: typing.Optional[typing.Sequence[builtins.str]] = None,
    paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b950fbbd54a6db12efc3ddba957cc278be8b1fe0d82677793b7a956e54f15663(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    uses: builtins.str,
    parameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    condition: typing.Optional[builtins.str] = None,
    continue_on_error: typing.Optional[builtins.bool] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    timeout_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e3c352efaba4562c7b667ab619020efa49db0c3954f7319a463c3fd7c935c11(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5146af3bc07037cf8abd259e7215ea6af345da64fc916ba7b88642b110f4e0c3(
    step: RegularStep,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47115f7c46b8aa2bd13f2ca276bcfdbb4283427f4d0f6d46ae1b6e0195649ef7(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    run: typing.Union[builtins.str, typing.Sequence[builtins.str]],
    shell: typing.Optional[builtins.str] = None,
    working_directory: typing.Optional[builtins.str] = None,
    condition: typing.Optional[builtins.str] = None,
    continue_on_error: typing.Optional[builtins.bool] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    timeout_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2742a5330ae31ee341ce22632ae8f606415fb32083e38ec33b1367de384dfa0b(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13ad166991bf23fc6f37c8e927d9d683905f387a1aaf8d498a0f170b5e82aee3(
    step: RunStep,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__998fa6c87ec77d4d366a8d9f14b61b39ee2de0d7cc0ff5048d9dc4aad90fc750(
    step: StepBase,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9083af845695d517fd188c807376a21723381078b0375f588720ba0e18af144(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    action_identifier: builtins.str,
    parameters: typing.Mapping[builtins.str, typing.Any],
    version: builtins.str,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
