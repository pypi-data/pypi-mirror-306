r'''
# @github-actions-cdk/aws-cdk

**@github-actions-cdk/aws-cdk** is a TypeScript library for building GitHub Actions pipelines specifically for AWS CDK applications. This library allows developers to define, structure, and automate CI/CD workflows tailored to CDK projects, making it easy to deploy infrastructure through GitHub Actions in a type-safe and modular way.

## Key Features

* **Type-Safe Workflow Definition**: Use TypeScript to define GitHub Actions workflows with strict typing, ensuring correctness and reducing errors.
* **Purpose-Built for AWS CDK**: Integrates directly with AWS CDK, making it simple to add deployment stages, manage dependencies, and automate CDK operations.
* **Modular Components**: Quickly set up workflows by creating reusable jobs, triggers, and custom deployment stages.

## Installation

To get started with `@github-actions-cdk/aws-cdk`, install the package using npm or yarn:

```bash
npm install @github-actions-cdk/aws-cdk
```

or

```bash
yarn add @github-actions-cdk/aws-cdk
```

## Getting Started

### Basic Usage

Here’s an example of how to create a GitHub Actions workflow for an AWS CDK app using @github-actions-cdk/aws-cdk in TypeScript:

```python
// main.ts
import { AwsCredentials, GitHubActionsOpenIdConnectProvider, GitHubActionsPipeline, GitHubActionsRole, StageJob, Synth } from '@github-actions-cdk/aws-cdk';
import { RunStep } from 'github-actions-cdk';
import { App, Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';

import { MyStage } from './my-stage';

class GithubActionsStack extends Stack {
    constructor(scope: Construct, id: string, props?: StackProps) {
        super(scope, id, props);

        const provider = GitHubActionsOpenIdConnectProvider.fromGitHubActionsOpenIdConnectProvider(this);

        new GitHubActionsRole(this, 'GitHubActionsRole', {
            provider,
        });

        const pipeline = new GitHubActionsPipeline(this, 'Pipeline', {
            workflowOutdir: `${__dirname}/.github/workflows`,
            preBuild: { steps: (job) => {
                new RunStep(job, 'pre', {
                    run: 'echo "Hello, world!"',
                });
            }},
            synth: new Synth({
                commands: ["npm install", "npm run build"],
            }),
            awsCredentials: AwsCredentials.fromOpenIdConnect({
                gitHubActionsRoleArn: "arn:aws:iam::<account-id>:role/GitHubActionsRole",
            }),
        });

        // a wave deploys all stages concurrently
        const prod = pipeline.addWave('Prod');

        const ACCOUNT = '123456789012';
        prod.addStage(new MyStage(app, 'US', { env: { account: ACCOUNT, region: 'us-east-1' } }), {
            preJobs: [new StageJob("hello-world", {
                name: 'Hello World',
                steps: (job) => {
                    new RunStep(job, 'echo', {
                        run: 'echo "Hello world!"',
                    });
                }
            })],
        });
        prod.addStage(new MyStage(app, 'EU', { env: { account: ACCOUNT, region: 'eu-west-2' } }));
    }
}

const app = new App();
new GithubActionsStack(app, 'GithubActionsStack');

// my-stage.ts
import * as path from 'path';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as s3 from 'aws-cdk-lib/aws-s3';
import { App, RemovalPolicy, Stack, Stage, StageProps } from 'aws-cdk-lib';

const assets = path.join(__dirname, 'assets');

export class MyStage extends Stage {
  constructor(scope: App, id: string, props: StageProps = {}) {
    super(scope, id, props);

    const fnStack = new Stack(this, 'FunctionStack');
    const bucketStack = new Stack(this, 'BucketStack');

    const bucket = new s3.Bucket(bucketStack, 'Bucket', {
      autoDeleteObjects: true,
      removalPolicy: RemovalPolicy.DESTROY,
    });

    const fn = new lambda.Function(fnStack, 'Function', {
      code: lambda.Code.fromAsset(path.join(__dirname, 'assets', 'files')),
      handler: 'lambda.handler',
      runtime: lambda.Runtime.PYTHON_3_12,
      environment: {
        BUCKET_NAME: bucket.bucketName, // <-- cross stack reference
      },
    });

    bucket.grantRead(fn);
  }
}
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

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.pipelines as _aws_cdk_pipelines_ceddda9d
import constructs as _constructs_77d1e7e8
import github_actions_cdk as _github_actions_cdk_5328d874


class AwsCdkAdapter(
    _github_actions_cdk_5328d874.Project,
    metaclass=jsii.JSIIMeta,
    jsii_type="@github-actions-cdk/aws-cdk.AwsCdkAdapter",
):
    '''(experimental) The ``AwsCdkAdapter`` class integrates GitHub Actions workflows with AWS CDK constructs, inheriting from the ``Project`` base class in ``github-actions-cdk``.

    This adapter binds the lifecycle of a GitHub Actions workflow to an AWS CDK Construct,
    allowing workflow creation, error handling, and annotation of errors and warnings
    during the CDK synthesis process.

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
        '''(experimental) Constructs a new ``AwsCdkAdapter`` instance.

        :param aws_cdk_scope: - The AWS CDK construct scope associated with this adapter. This scope is used as a base for adding validations, annotations, and managing synthesis errors.
        :param additional_checks: 
        :param continue_on_error_annotations: 
        :param outdir: 
        :param skip_validation: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9625a39d38e5f209abdb7662dd5eedae25c0e5d8e76f70714e4d40cb23db1007)
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
        '''(experimental) Finalizes the synthesis process by transferring workflow annotations to the CDK context as appropriate.

        This method checks each annotation's severity level (info, warning, error) and
        adds it to the CDK scope using the ``Annotations`` utility.

        Additionally, this method stops synthesis if there are blocking errors,
        unless overridden by ``continueOnErrorAnnotations``.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "finalizeSynthesis", []))

    @jsii.member(jsii_name="handleSynthesisError")
    def _handle_synthesis_error(self, error: typing.Any) -> None:
        '''(experimental) Handles synthesis errors encountered during workflow generation.

        If the error is a validation error, it registers the error message as a validation
        message on the associated CDK scope.

        :param error: - The error encountered during synthesis.

        :stability: experimental
        :throws: Error - If the error is not a validation error, it will be re-thrown.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28fbdf0ace5064cb48481e60cbf4c8ab332ac37d0ab38ddeeeb6f0e81a4ee704)
            check_type(argname="argument error", value=error, expected_type=type_hints["error"])
        return typing.cast(None, jsii.invoke(self, "handleSynthesisError", [error]))


class AwsCredentials(
    metaclass=jsii.JSIIMeta,
    jsii_type="@github-actions-cdk/aws-cdk.AwsCredentials",
):
    '''(experimental) Factory class for creating instances of AWS credentials providers.

    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromGitHubSecrets")
    @builtins.classmethod
    def from_git_hub_secrets(
        cls,
        *,
        access_key_id: builtins.str,
        secret_access_key: builtins.str,
        session_token: typing.Optional[builtins.str] = None,
    ) -> "AwsCredentialsProvider":
        '''(experimental) Creates an AWS credentials provider that uses GitHub secrets.

        :param access_key_id: (experimental) The name of the GitHub secret that holds the AWS access key ID. Default: "AWS_ACCESS_KEY_ID"
        :param secret_access_key: (experimental) The name of the GitHub secret that holds the AWS secret access key. Default: "AWS_SECRET_ACCESS_KEY"
        :param session_token: (experimental) The name of the GitHub secret that holds the AWS session token. Default: - no session token is used

        :return: An instance of ``GitHubSecretsProvider``.

        :stability: experimental
        '''
        props = GitHubSecretsProviderProps(
            access_key_id=access_key_id,
            secret_access_key=secret_access_key,
            session_token=session_token,
        )

        return typing.cast("AwsCredentialsProvider", jsii.sinvoke(cls, "fromGitHubSecrets", [props]))

    @jsii.member(jsii_name="fromOpenIdConnect")
    @builtins.classmethod
    def from_open_id_connect(
        cls,
        *,
        git_hub_actions_role_arn: builtins.str,
        role_session_name: typing.Optional[builtins.str] = None,
    ) -> "AwsCredentialsProvider":
        '''(experimental) Creates an AWS credentials provider that uses OpenID Connect.

        :param git_hub_actions_role_arn: (experimental) The ARN of the role that GitHub Actions will assume via OpenID Connect.
        :param role_session_name: (experimental) Optional role session name to use when assuming the role. Default: - no role session name

        :return: An instance of ``OpenIdConnectProvider``.

        :stability: experimental
        '''
        props = OpenIdConnectProviderProps(
            git_hub_actions_role_arn=git_hub_actions_role_arn,
            role_session_name=role_session_name,
        )

        return typing.cast("AwsCredentialsProvider", jsii.sinvoke(cls, "fromOpenIdConnect", [props]))


class AwsCredentialsProvider(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@github-actions-cdk/aws-cdk.AwsCredentialsProvider",
):
    '''(experimental) Abstract class representing a provider for AWS credentials.

    Implementations of this class are responsible for defining how
    AWS credentials are obtained and how they are configured within
    GitHub Actions jobs.

    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="credentialSteps")
    @abc.abstractmethod
    def credential_steps(
        self,
        job: _github_actions_cdk_5328d874.Job,
        region: builtins.str,
        assume_role_arn: typing.Optional[builtins.str] = None,
    ) -> typing.List[_github_actions_cdk_5328d874.RegularStep]:
        '''(experimental) Generates a series of steps to configure AWS credentials for a GitHub Actions job.

        :param job: - The GitHub Actions job in which to configure the credentials.
        :param region: - The AWS region in which the credentials will be used.
        :param assume_role_arn: - An optional ARN for a role to assume with elevated permissions.

        :return: An array of ``RegularStep`` instances to be executed in the job.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="permissionLevel")
    @abc.abstractmethod
    def permission_level(self) -> _github_actions_cdk_5328d874.PermissionLevel:
        '''(experimental) Retrieves the permission level required by this credentials provider.

        :stability: experimental
        '''
        ...


class _AwsCredentialsProviderProxy(AwsCredentialsProvider):
    @jsii.member(jsii_name="credentialSteps")
    def credential_steps(
        self,
        job: _github_actions_cdk_5328d874.Job,
        region: builtins.str,
        assume_role_arn: typing.Optional[builtins.str] = None,
    ) -> typing.List[_github_actions_cdk_5328d874.RegularStep]:
        '''(experimental) Generates a series of steps to configure AWS credentials for a GitHub Actions job.

        :param job: - The GitHub Actions job in which to configure the credentials.
        :param region: - The AWS region in which the credentials will be used.
        :param assume_role_arn: - An optional ARN for a role to assume with elevated permissions.

        :return: An array of ``RegularStep`` instances to be executed in the job.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3989ae456ab07886845ef790414c195483d97f4bf4b555588b1b7131d01a30f2)
            check_type(argname="argument job", value=job, expected_type=type_hints["job"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument assume_role_arn", value=assume_role_arn, expected_type=type_hints["assume_role_arn"])
        return typing.cast(typing.List[_github_actions_cdk_5328d874.RegularStep], jsii.invoke(self, "credentialSteps", [job, region, assume_role_arn]))

    @jsii.member(jsii_name="permissionLevel")
    def permission_level(self) -> _github_actions_cdk_5328d874.PermissionLevel:
        '''(experimental) Retrieves the permission level required by this credentials provider.

        :stability: experimental
        '''
        return typing.cast(_github_actions_cdk_5328d874.PermissionLevel, jsii.invoke(self, "permissionLevel", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, AwsCredentialsProvider).__jsii_proxy_class__ = lambda : _AwsCredentialsProviderProxy


class GitHubActionsOpenIdConnectProvider(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@github-actions-cdk/aws-cdk.GitHubActionsOpenIdConnectProvider",
):
    '''(experimental) Represents an OpenID Connect (OIDC) provider for GitHub Actions.

    This provider allows GitHub Actions to assume roles in AWS by connecting through OpenID Connect.

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
        :param thumbprints: (experimental) Optional thumbprints to verify GitHub's certificates. Ensure to update these when GitHub rotates their certificates. Default: - Uses predefined, up-to-date thumbprints.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28884f9a6760c9ce8250d1ffb6d95ef6f49a2cb27284940e17468e9049473ac7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GitHubActionsOpenIdConnectProviderProps(thumbprints=thumbprints)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromGitHubActionsOpenIdConnectProvider")
    @builtins.classmethod
    def from_git_hub_actions_open_id_connect_provider(
        cls,
        scope: _constructs_77d1e7e8.Construct,
    ) -> _aws_cdk_aws_iam_ceddda9d.IOpenIdConnectProvider:
        '''(experimental) Imports an existing GitHub Actions OpenID Connect provider by ARN.

        :param scope: - The construct scope to define the provider within.

        :return: The imported OIDC provider interface.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61b3a88322723cd90fe1abfc29c6f24564ad07a5b6c00c29d0e42b1ddecaf436)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IOpenIdConnectProvider, jsii.sinvoke(cls, "fromGitHubActionsOpenIdConnectProvider", [scope]))


@jsii.data_type(
    jsii_type="@github-actions-cdk/aws-cdk.GitHubActionsOpenIdConnectProviderProps",
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

        :param thumbprints: (experimental) Optional thumbprints to verify GitHub's certificates. Ensure to update these when GitHub rotates their certificates. Default: - Uses predefined, up-to-date thumbprints.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7543176371b9644ce378e7f7db82027af30d0eddb1835e8aebcfcd9a8fbaef30)
            check_type(argname="argument thumbprints", value=thumbprints, expected_type=type_hints["thumbprints"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if thumbprints is not None:
            self._values["thumbprints"] = thumbprints

    @builtins.property
    def thumbprints(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Optional thumbprints to verify GitHub's certificates.

        Ensure to update these when GitHub rotates their certificates.

        :default: - Uses predefined, up-to-date thumbprints.

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


class GitHubActionsPipeline(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@github-actions-cdk/aws-cdk.GitHubActionsPipeline",
):
    '''(experimental) Constructs a GitHub Actions pipeline for deploying AWS resources.

    :stability: experimental
    :remarks:

    The ``GitHubActionsPipeline`` provides methods to define and manage deployment stages and job waves in
    a GitHub Actions pipeline, utilizing AWS credentials and CDK output for cloud infrastructure automation.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        aws_credentials: AwsCredentialsProvider,
        synth: "Synth",
        post_build: typing.Optional["IJobPhase"] = None,
        pre_build: typing.Optional["IJobPhase"] = None,
        single_publisher_per_asset_type: typing.Optional[builtins.bool] = None,
        version_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        workflow_env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        workflow_filename: typing.Optional[builtins.str] = None,
        workflow_name: typing.Optional[builtins.str] = None,
        workflow_outdir: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Constructs a new instance of ``GitHubActionsPipeline``.

        :param scope: - The parent construct scope.
        :param id: - Unique identifier for this pipeline construct.
        :param aws_credentials: (experimental) AWS credentials provider for authenticating AWS actions.
        :param synth: (experimental) Synthesizer for CDK applications.
        :param post_build: (experimental) Optional phase for jobs to execute after the main build steps.
        :param pre_build: (experimental) Optional phase for jobs to execute before the main build steps.
        :param single_publisher_per_asset_type: (experimental) Whether to enable a single publisher for each asset type. Default: false
        :param version_overrides: (experimental) Version overrides for GitHub Actions used in the workflow.
        :param workflow_env: (experimental) Environment variables to set in the workflow.
        :param workflow_filename: (experimental) Filename for the workflow file. Default: "deploy"
        :param workflow_name: (experimental) Optional name for the GitHub Actions workflow. Default: "Deploy"
        :param workflow_outdir: (experimental) Directory path for the workflow output files. Default: ".github/workflows"

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96fcd40eb072e8c0530c8c54766297ac99a2b7b419e4e8b2e613d60d866dd0a9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GitHubActionsPipelineProps(
            aws_credentials=aws_credentials,
            synth=synth,
            post_build=post_build,
            pre_build=pre_build,
            single_publisher_per_asset_type=single_publisher_per_asset_type,
            version_overrides=version_overrides,
            workflow_env=workflow_env,
            workflow_filename=workflow_filename,
            workflow_name=workflow_name,
            workflow_outdir=workflow_outdir,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addStage")
    def add_stage(
        self,
        stage: _aws_cdk_ceddda9d.Stage,
        *,
        git_hub_environment: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
        post_jobs: typing.Optional[typing.Sequence["StageJob"]] = None,
        pre_jobs: typing.Optional[typing.Sequence["StageJob"]] = None,
        stack_capabilities: typing.Optional[typing.Sequence["StackCapabilities"]] = None,
    ) -> _aws_cdk_pipelines_ceddda9d.StageDeployment:
        '''(experimental) Adds a stage to the pipeline with GitHub-specific configuration options.

        :param stage: - The CDK Stage to add to the pipeline.
        :param git_hub_environment: (experimental) Optional GitHub environment configuration for the stage. This configuration specifies the environment context in which the jobs will run.
        :param post_jobs: (experimental) Optional list of jobs to run after the main stage execution. These jobs can perform cleanup or other necessary tasks.
        :param pre_jobs: (experimental) Optional list of jobs to run before the main stage execution. These jobs can prepare the environment or handle setup tasks.
        :param stack_capabilities: (experimental) Optional capabilities that the stack should acknowledge during deployment. These capabilities are particularly relevant for stacks with IAM resources or macros.

        :return: Deployment details for the added stage.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89ab5e8eaef92c0d10c05fb4cc4c421c9eae63fb62e4d1a7e272d176d8a7d9d3)
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        options = StageOptions(
            git_hub_environment=git_hub_environment,
            post_jobs=post_jobs,
            pre_jobs=pre_jobs,
            stack_capabilities=stack_capabilities,
        )

        return typing.cast(_aws_cdk_pipelines_ceddda9d.StageDeployment, jsii.invoke(self, "addStage", [stage, options]))

    @jsii.member(jsii_name="addWave")
    def add_wave(
        self,
        id: builtins.str,
        *,
        post_jobs: typing.Optional[typing.Sequence["StageJob"]] = None,
        pre_jobs: typing.Optional[typing.Sequence["StageJob"]] = None,
    ) -> "GitHubWave":
        '''(experimental) Adds a wave of jobs to the pipeline.

        :param id: - Unique identifier for the wave.
        :param post_jobs: (experimental) Optional list of jobs to run after all stages in the wave. This can be useful for cleanup or finalization tasks that should occur after all stages have completed.
        :param pre_jobs: (experimental) Optional list of jobs to run before any stages in the wave. This allows for preparatory tasks or environment setup for the entire wave.

        :return: The created GitHub wave instance.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a737c584d1136e2411d6dfa2c83f7db9beb11b36eae8e4bd153734536de4b73)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = WaveOptions(post_jobs=post_jobs, pre_jobs=pre_jobs)

        return typing.cast("GitHubWave", jsii.invoke(self, "addWave", [id, options]))

    @builtins.property
    @jsii.member(jsii_name="workflowFilename")
    def workflow_filename(self) -> builtins.str:
        '''(experimental) Returns the filename for the workflow file.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "workflowFilename"))

    @builtins.property
    @jsii.member(jsii_name="workflowName")
    def workflow_name(self) -> builtins.str:
        '''(experimental) Returns the name of the workflow.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "workflowName"))

    @builtins.property
    @jsii.member(jsii_name="workflowOutdir")
    def workflow_outdir(self) -> builtins.str:
        '''(experimental) Returns the output directory path for the workflow files.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "workflowOutdir"))


@jsii.data_type(
    jsii_type="@github-actions-cdk/aws-cdk.GitHubActionsPipelineProps",
    jsii_struct_bases=[],
    name_mapping={
        "aws_credentials": "awsCredentials",
        "synth": "synth",
        "post_build": "postBuild",
        "pre_build": "preBuild",
        "single_publisher_per_asset_type": "singlePublisherPerAssetType",
        "version_overrides": "versionOverrides",
        "workflow_env": "workflowEnv",
        "workflow_filename": "workflowFilename",
        "workflow_name": "workflowName",
        "workflow_outdir": "workflowOutdir",
    },
)
class GitHubActionsPipelineProps:
    def __init__(
        self,
        *,
        aws_credentials: AwsCredentialsProvider,
        synth: "Synth",
        post_build: typing.Optional["IJobPhase"] = None,
        pre_build: typing.Optional["IJobPhase"] = None,
        single_publisher_per_asset_type: typing.Optional[builtins.bool] = None,
        version_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        workflow_env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        workflow_filename: typing.Optional[builtins.str] = None,
        workflow_name: typing.Optional[builtins.str] = None,
        workflow_outdir: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for configuring the GitHub Actions pipeline.

        :param aws_credentials: (experimental) AWS credentials provider for authenticating AWS actions.
        :param synth: (experimental) Synthesizer for CDK applications.
        :param post_build: (experimental) Optional phase for jobs to execute after the main build steps.
        :param pre_build: (experimental) Optional phase for jobs to execute before the main build steps.
        :param single_publisher_per_asset_type: (experimental) Whether to enable a single publisher for each asset type. Default: false
        :param version_overrides: (experimental) Version overrides for GitHub Actions used in the workflow.
        :param workflow_env: (experimental) Environment variables to set in the workflow.
        :param workflow_filename: (experimental) Filename for the workflow file. Default: "deploy"
        :param workflow_name: (experimental) Optional name for the GitHub Actions workflow. Default: "Deploy"
        :param workflow_outdir: (experimental) Directory path for the workflow output files. Default: ".github/workflows"

        :stability: experimental
        :remarks:

        Provides options for defining the workflow environment, AWS credentials, job phases, and version overrides,
        along with paths and naming conventions for GitHub Actions workflows.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27649c8ad4ab55b72c155b45a971e424248d7098e0b389f6e2885320c401c388)
            check_type(argname="argument aws_credentials", value=aws_credentials, expected_type=type_hints["aws_credentials"])
            check_type(argname="argument synth", value=synth, expected_type=type_hints["synth"])
            check_type(argname="argument post_build", value=post_build, expected_type=type_hints["post_build"])
            check_type(argname="argument pre_build", value=pre_build, expected_type=type_hints["pre_build"])
            check_type(argname="argument single_publisher_per_asset_type", value=single_publisher_per_asset_type, expected_type=type_hints["single_publisher_per_asset_type"])
            check_type(argname="argument version_overrides", value=version_overrides, expected_type=type_hints["version_overrides"])
            check_type(argname="argument workflow_env", value=workflow_env, expected_type=type_hints["workflow_env"])
            check_type(argname="argument workflow_filename", value=workflow_filename, expected_type=type_hints["workflow_filename"])
            check_type(argname="argument workflow_name", value=workflow_name, expected_type=type_hints["workflow_name"])
            check_type(argname="argument workflow_outdir", value=workflow_outdir, expected_type=type_hints["workflow_outdir"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "aws_credentials": aws_credentials,
            "synth": synth,
        }
        if post_build is not None:
            self._values["post_build"] = post_build
        if pre_build is not None:
            self._values["pre_build"] = pre_build
        if single_publisher_per_asset_type is not None:
            self._values["single_publisher_per_asset_type"] = single_publisher_per_asset_type
        if version_overrides is not None:
            self._values["version_overrides"] = version_overrides
        if workflow_env is not None:
            self._values["workflow_env"] = workflow_env
        if workflow_filename is not None:
            self._values["workflow_filename"] = workflow_filename
        if workflow_name is not None:
            self._values["workflow_name"] = workflow_name
        if workflow_outdir is not None:
            self._values["workflow_outdir"] = workflow_outdir

    @builtins.property
    def aws_credentials(self) -> AwsCredentialsProvider:
        '''(experimental) AWS credentials provider for authenticating AWS actions.

        :stability: experimental
        '''
        result = self._values.get("aws_credentials")
        assert result is not None, "Required property 'aws_credentials' is missing"
        return typing.cast(AwsCredentialsProvider, result)

    @builtins.property
    def synth(self) -> "Synth":
        '''(experimental) Synthesizer for CDK applications.

        :stability: experimental
        '''
        result = self._values.get("synth")
        assert result is not None, "Required property 'synth' is missing"
        return typing.cast("Synth", result)

    @builtins.property
    def post_build(self) -> typing.Optional["IJobPhase"]:
        '''(experimental) Optional phase for jobs to execute after the main build steps.

        :stability: experimental
        '''
        result = self._values.get("post_build")
        return typing.cast(typing.Optional["IJobPhase"], result)

    @builtins.property
    def pre_build(self) -> typing.Optional["IJobPhase"]:
        '''(experimental) Optional phase for jobs to execute before the main build steps.

        :stability: experimental
        '''
        result = self._values.get("pre_build")
        return typing.cast(typing.Optional["IJobPhase"], result)

    @builtins.property
    def single_publisher_per_asset_type(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to enable a single publisher for each asset type.

        :default: false

        :stability: experimental
        :remarks: When true, consolidates publishing jobs to reduce redundant asset publishing.
        '''
        result = self._values.get("single_publisher_per_asset_type")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def version_overrides(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Version overrides for GitHub Actions used in the workflow.

        :stability: experimental
        '''
        result = self._values.get("version_overrides")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def workflow_env(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Environment variables to set in the workflow.

        :stability: experimental
        '''
        result = self._values.get("workflow_env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def workflow_filename(self) -> typing.Optional[builtins.str]:
        '''(experimental) Filename for the workflow file.

        :default: "deploy"

        :stability: experimental
        '''
        result = self._values.get("workflow_filename")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workflow_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Optional name for the GitHub Actions workflow.

        :default: "Deploy"

        :stability: experimental
        '''
        result = self._values.get("workflow_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workflow_outdir(self) -> typing.Optional[builtins.str]:
        '''(experimental) Directory path for the workflow output files.

        :default: ".github/workflows"

        :stability: experimental
        '''
        result = self._values.get("workflow_outdir")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitHubActionsPipelineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GitHubActionsRole(
    _aws_cdk_aws_iam_ceddda9d.Role,
    metaclass=jsii.JSIIMeta,
    jsii_type="@github-actions-cdk/aws-cdk.GitHubActionsRole",
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
        provider: _aws_cdk_aws_iam_ceddda9d.IOpenIdConnectProvider,
        repos: typing.Optional[typing.Sequence[builtins.str]] = None,
        role_name: typing.Optional[builtins.str] = None,
        subject_claims: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Constructs a new instance of ``GitHubActionsRole``.

        :param scope: - The construct scope to define the role within.
        :param id: - The unique identifier for this role.
        :param provider: (experimental) The OpenID Connect provider that GitHub Actions will use to assume this role.
        :param repos: (experimental) A list of GitHub repositories that are permitted to assume this role. Each repository should be formatted as ``owner/repo``.
        :param role_name: (experimental) The name for the GitHub Actions IAM role. Default: - "GitHubActionsRole"
        :param subject_claims: (experimental) Additional custom subject claims to allow for the role. Each claim should conform to the format used in GitHub OIDC conditions.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d00bdbd3fd92f21748337063ff3f61dcfa08621b09dfebc9cafac8d3ce583503)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GitHubActionsRoleProps(
            provider=provider,
            repos=repos,
            role_name=role_name,
            subject_claims=subject_claims,
        )

        jsii.create(self.__class__, self, [scope, id, props])


class GitHubActionsRoleArn(
    metaclass=jsii.JSIIMeta,
    jsii_type="@github-actions-cdk/aws-cdk.GitHubActionsRoleArn",
):
    '''(experimental) Helper class for generating ARNs for GitHub Actions roles.

    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromAccount")
    @builtins.classmethod
    def from_account(
        cls,
        account_id: builtins.str,
        role_name: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        '''(experimental) Creates an ARN for a GitHub Actions role based on the account ID.

        :param account_id: - The AWS account ID.
        :param role_name: - The name of the IAM role (defaults to "GitHubActionsRole").

        :return: The full ARN of the specified role.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b111a2b07706fe91b3329a040650d384c1bb9ceddc1cebac1fd6349d873e84b9)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument role_name", value=role_name, expected_type=type_hints["role_name"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "fromAccount", [account_id, role_name]))


@jsii.data_type(
    jsii_type="@github-actions-cdk/aws-cdk.GitHubActionsRoleProps",
    jsii_struct_bases=[],
    name_mapping={
        "provider": "provider",
        "repos": "repos",
        "role_name": "roleName",
        "subject_claims": "subjectClaims",
    },
)
class GitHubActionsRoleProps:
    def __init__(
        self,
        *,
        provider: _aws_cdk_aws_iam_ceddda9d.IOpenIdConnectProvider,
        repos: typing.Optional[typing.Sequence[builtins.str]] = None,
        role_name: typing.Optional[builtins.str] = None,
        subject_claims: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Properties for creating a GitHub Actions IAM role.

        :param provider: (experimental) The OpenID Connect provider that GitHub Actions will use to assume this role.
        :param repos: (experimental) A list of GitHub repositories that are permitted to assume this role. Each repository should be formatted as ``owner/repo``.
        :param role_name: (experimental) The name for the GitHub Actions IAM role. Default: - "GitHubActionsRole"
        :param subject_claims: (experimental) Additional custom subject claims to allow for the role. Each claim should conform to the format used in GitHub OIDC conditions.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__561aa80ba2071f8035e588f52b4c2478bfc7397203e23ba0bf6858136a68e60d)
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument repos", value=repos, expected_type=type_hints["repos"])
            check_type(argname="argument role_name", value=role_name, expected_type=type_hints["role_name"])
            check_type(argname="argument subject_claims", value=subject_claims, expected_type=type_hints["subject_claims"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "provider": provider,
        }
        if repos is not None:
            self._values["repos"] = repos
        if role_name is not None:
            self._values["role_name"] = role_name
        if subject_claims is not None:
            self._values["subject_claims"] = subject_claims

    @builtins.property
    def provider(self) -> _aws_cdk_aws_iam_ceddda9d.IOpenIdConnectProvider:
        '''(experimental) The OpenID Connect provider that GitHub Actions will use to assume this role.

        :stability: experimental
        '''
        result = self._values.get("provider")
        assert result is not None, "Required property 'provider' is missing"
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IOpenIdConnectProvider, result)

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


@jsii.data_type(
    jsii_type="@github-actions-cdk/aws-cdk.GitHubSecretsProviderProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_key_id": "accessKeyId",
        "secret_access_key": "secretAccessKey",
        "session_token": "sessionToken",
    },
)
class GitHubSecretsProviderProps:
    def __init__(
        self,
        *,
        access_key_id: builtins.str,
        secret_access_key: builtins.str,
        session_token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for configuring the GitHub Secrets provider.

        :param access_key_id: (experimental) The name of the GitHub secret that holds the AWS access key ID. Default: "AWS_ACCESS_KEY_ID"
        :param secret_access_key: (experimental) The name of the GitHub secret that holds the AWS secret access key. Default: "AWS_SECRET_ACCESS_KEY"
        :param session_token: (experimental) The name of the GitHub secret that holds the AWS session token. Default: - no session token is used

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32b8bf3d5dc2ad82ec42e5edb11e84ec37b8764bc0f97d631224d4ce13de8d7a)
            check_type(argname="argument access_key_id", value=access_key_id, expected_type=type_hints["access_key_id"])
            check_type(argname="argument secret_access_key", value=secret_access_key, expected_type=type_hints["secret_access_key"])
            check_type(argname="argument session_token", value=session_token, expected_type=type_hints["session_token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access_key_id": access_key_id,
            "secret_access_key": secret_access_key,
        }
        if session_token is not None:
            self._values["session_token"] = session_token

    @builtins.property
    def access_key_id(self) -> builtins.str:
        '''(experimental) The name of the GitHub secret that holds the AWS access key ID.

        :default: "AWS_ACCESS_KEY_ID"

        :stability: experimental
        '''
        result = self._values.get("access_key_id")
        assert result is not None, "Required property 'access_key_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_access_key(self) -> builtins.str:
        '''(experimental) The name of the GitHub secret that holds the AWS secret access key.

        :default: "AWS_SECRET_ACCESS_KEY"

        :stability: experimental
        '''
        result = self._values.get("secret_access_key")
        assert result is not None, "Required property 'secret_access_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def session_token(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the GitHub secret that holds the AWS session token.

        :default: - no session token is used

        :stability: experimental
        '''
        result = self._values.get("session_token")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitHubSecretsProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GitHubWave(
    metaclass=jsii.JSIIMeta,
    jsii_type="@github-actions-cdk/aws-cdk.GitHubWave",
):
    '''(experimental) Represents a wave in the GitHub Actions pipeline.

    This class provides a wrapper around the Wave class from the AWS CDK pipelines module,
    enabling additional functionality for managing stages with specific options and configurations.

    :stability: experimental
    '''

    def __init__(
        self,
        id: builtins.str,
        wave_stage_adder: "IWaveStageAdder",
        *,
        post: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.Step]] = None,
        pre: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.Step]] = None,
    ) -> None:
        '''(experimental) Constructs a new instance of GitHubWave.

        :param id: - Unique identifier for the wave.
        :param wave_stage_adder: - An instance of IWaveStageAdder to manage the addition of stages.
        :param post: Additional steps to run after all of the stages in the wave. Default: - No additional steps
        :param pre: Additional steps to run before any of the stages in the wave. Default: - No additional steps

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93ab778c5ce108a8bc9b72ebc9e8e66e869734e0a86a57246522989522bbcd97)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument wave_stage_adder", value=wave_stage_adder, expected_type=type_hints["wave_stage_adder"])
        props = _aws_cdk_pipelines_ceddda9d.WaveProps(post=post, pre=pre)

        jsii.create(self.__class__, self, [id, wave_stage_adder, props])

    @jsii.member(jsii_name="addStage")
    def add_stage(
        self,
        stage: _aws_cdk_ceddda9d.Stage,
        *,
        git_hub_environment: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
        post_jobs: typing.Optional[typing.Sequence["StageJob"]] = None,
        pre_jobs: typing.Optional[typing.Sequence["StageJob"]] = None,
        stack_capabilities: typing.Optional[typing.Sequence["StackCapabilities"]] = None,
    ) -> _aws_cdk_pipelines_ceddda9d.StageDeployment:
        '''(experimental) Adds a stage to the wave with specified options.

        This method creates a deployment for the provided stage and integrates it
        into the wave, managing pre- and post-jobs as configured.

        :param stage: - The stage to be added to the wave.
        :param git_hub_environment: (experimental) Optional GitHub environment configuration for the stage. This configuration specifies the environment context in which the jobs will run.
        :param post_jobs: (experimental) Optional list of jobs to run after the main stage execution. These jobs can perform cleanup or other necessary tasks.
        :param pre_jobs: (experimental) Optional list of jobs to run before the main stage execution. These jobs can prepare the environment or handle setup tasks.
        :param stack_capabilities: (experimental) Optional capabilities that the stack should acknowledge during deployment. These capabilities are particularly relevant for stacks with IAM resources or macros.

        :return: The deployment information for the added stage.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ee7f04229445b2055a0617e3b09015b1ff1425e9bbfae250e48d9ca5c59c4cb)
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        options = StageOptions(
            git_hub_environment=git_hub_environment,
            post_jobs=post_jobs,
            pre_jobs=pre_jobs,
            stack_capabilities=stack_capabilities,
        )

        return typing.cast(_aws_cdk_pipelines_ceddda9d.StageDeployment, jsii.invoke(self, "addStage", [stage, options]))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''(experimental) - Unique identifier for the wave.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "id"))


@jsii.interface(jsii_type="@github-actions-cdk/aws-cdk.IJobPhase")
class IJobPhase(typing_extensions.Protocol):
    '''(experimental) Interface for defining a phase of job steps in the pipeline.

    :stability: experimental
    '''

    @jsii.member(jsii_name="steps")
    def steps(self, job: "PipelineJob") -> None:
        '''(experimental) Defines the steps to be executed for this job phase.

        :param job: - The pipeline job in which to add the steps.

        :stability: experimental
        '''
        ...


class _IJobPhaseProxy:
    '''(experimental) Interface for defining a phase of job steps in the pipeline.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@github-actions-cdk/aws-cdk.IJobPhase"

    @jsii.member(jsii_name="steps")
    def steps(self, job: "PipelineJob") -> None:
        '''(experimental) Defines the steps to be executed for this job phase.

        :param job: - The pipeline job in which to add the steps.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ead53d1c4c954d13546340faf629f1a4478781acb18a0c3c0e6513d26daa9e8)
            check_type(argname="argument job", value=job, expected_type=type_hints["job"])
        return typing.cast(None, jsii.invoke(self, "steps", [job]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IJobPhase).__jsii_proxy_class__ = lambda : _IJobPhaseProxy


@jsii.interface(jsii_type="@github-actions-cdk/aws-cdk.IStageJobOptions")
class IStageJobOptions(IJobPhase, typing_extensions.Protocol):
    '''(experimental) Options for configuring a job in a stage of the GitHub Actions pipeline.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="env")
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Optional environment variables for the job.

        These variables will be set in the job's execution environment.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(self) -> typing.Optional[_github_actions_cdk_5328d874.Environment]:
        '''(experimental) Optional configuration for the job's environment.

        This allows for additional customization of the job's execution context.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Optional name for the job.

        If not specified, a default name will be generated.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="permissions")
    def permissions(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _github_actions_cdk_5328d874.PermissionsEvent]]:
        '''(experimental) Optional permissions for the job.

        These permissions control the actions that the job can perform in the GitHub Actions environment.

        :stability: experimental
        '''
        ...


class _IStageJobOptionsProxy(
    jsii.proxy_for(IJobPhase), # type: ignore[misc]
):
    '''(experimental) Options for configuring a job in a stage of the GitHub Actions pipeline.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@github-actions-cdk/aws-cdk.IStageJobOptions"

    @builtins.property
    @jsii.member(jsii_name="env")
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Optional environment variables for the job.

        These variables will be set in the job's execution environment.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "env"))

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(self) -> typing.Optional[_github_actions_cdk_5328d874.Environment]:
        '''(experimental) Optional configuration for the job's environment.

        This allows for additional customization of the job's execution context.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_github_actions_cdk_5328d874.Environment], jsii.get(self, "environment"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Optional name for the job.

        If not specified, a default name will be generated.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="permissions")
    def permissions(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _github_actions_cdk_5328d874.PermissionsEvent]]:
        '''(experimental) Optional permissions for the job.

        These permissions control the actions that the job can perform in the GitHub Actions environment.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, _github_actions_cdk_5328d874.PermissionsEvent]], jsii.get(self, "permissions"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IStageJobOptions).__jsii_proxy_class__ = lambda : _IStageJobOptionsProxy


@jsii.interface(jsii_type="@github-actions-cdk/aws-cdk.IWaveStageAdder")
class IWaveStageAdder(typing_extensions.Protocol):
    '''(experimental) Interface for adding stages to a wave in the GitHub Actions pipeline.

    This interface provides a method to incorporate stages from a stage deployment
    into a wave, allowing for organized grouping of related stages.

    :stability: experimental
    '''

    @jsii.member(jsii_name="addStageFromWave")
    def add_stage_from_wave(
        self,
        stage_deployment: _aws_cdk_pipelines_ceddda9d.StageDeployment,
        *,
        git_hub_environment: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
        post_jobs: typing.Optional[typing.Sequence["StageJob"]] = None,
        pre_jobs: typing.Optional[typing.Sequence["StageJob"]] = None,
        stack_capabilities: typing.Optional[typing.Sequence["StackCapabilities"]] = None,
    ) -> None:
        '''(experimental) Adds a stage from a given stage deployment into the wave.

        :param stage_deployment: - The deployment information for the stage to be added.
        :param git_hub_environment: (experimental) Optional GitHub environment configuration for the stage. This configuration specifies the environment context in which the jobs will run.
        :param post_jobs: (experimental) Optional list of jobs to run after the main stage execution. These jobs can perform cleanup or other necessary tasks.
        :param pre_jobs: (experimental) Optional list of jobs to run before the main stage execution. These jobs can prepare the environment or handle setup tasks.
        :param stack_capabilities: (experimental) Optional capabilities that the stack should acknowledge during deployment. These capabilities are particularly relevant for stacks with IAM resources or macros.

        :stability: experimental
        '''
        ...


class _IWaveStageAdderProxy:
    '''(experimental) Interface for adding stages to a wave in the GitHub Actions pipeline.

    This interface provides a method to incorporate stages from a stage deployment
    into a wave, allowing for organized grouping of related stages.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@github-actions-cdk/aws-cdk.IWaveStageAdder"

    @jsii.member(jsii_name="addStageFromWave")
    def add_stage_from_wave(
        self,
        stage_deployment: _aws_cdk_pipelines_ceddda9d.StageDeployment,
        *,
        git_hub_environment: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
        post_jobs: typing.Optional[typing.Sequence["StageJob"]] = None,
        pre_jobs: typing.Optional[typing.Sequence["StageJob"]] = None,
        stack_capabilities: typing.Optional[typing.Sequence["StackCapabilities"]] = None,
    ) -> None:
        '''(experimental) Adds a stage from a given stage deployment into the wave.

        :param stage_deployment: - The deployment information for the stage to be added.
        :param git_hub_environment: (experimental) Optional GitHub environment configuration for the stage. This configuration specifies the environment context in which the jobs will run.
        :param post_jobs: (experimental) Optional list of jobs to run after the main stage execution. These jobs can perform cleanup or other necessary tasks.
        :param pre_jobs: (experimental) Optional list of jobs to run before the main stage execution. These jobs can prepare the environment or handle setup tasks.
        :param stack_capabilities: (experimental) Optional capabilities that the stack should acknowledge during deployment. These capabilities are particularly relevant for stacks with IAM resources or macros.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8584c189be576e1cd8125bdbf6d2ca5571be42084577864870c7d6cdb216300)
            check_type(argname="argument stage_deployment", value=stage_deployment, expected_type=type_hints["stage_deployment"])
        options = StageOptions(
            git_hub_environment=git_hub_environment,
            post_jobs=post_jobs,
            pre_jobs=pre_jobs,
            stack_capabilities=stack_capabilities,
        )

        return typing.cast(None, jsii.invoke(self, "addStageFromWave", [stage_deployment, options]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IWaveStageAdder).__jsii_proxy_class__ = lambda : _IWaveStageAdderProxy


@jsii.data_type(
    jsii_type="@github-actions-cdk/aws-cdk.OpenIdConnectProviderProps",
    jsii_struct_bases=[],
    name_mapping={
        "git_hub_actions_role_arn": "gitHubActionsRoleArn",
        "role_session_name": "roleSessionName",
    },
)
class OpenIdConnectProviderProps:
    def __init__(
        self,
        *,
        git_hub_actions_role_arn: builtins.str,
        role_session_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for configuring the OpenID Connect provider.

        :param git_hub_actions_role_arn: (experimental) The ARN of the role that GitHub Actions will assume via OpenID Connect.
        :param role_session_name: (experimental) Optional role session name to use when assuming the role. Default: - no role session name

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28c8df414e643b7f1c0e52605e917a8fd26640b62bec595734d57faaf0236f75)
            check_type(argname="argument git_hub_actions_role_arn", value=git_hub_actions_role_arn, expected_type=type_hints["git_hub_actions_role_arn"])
            check_type(argname="argument role_session_name", value=role_session_name, expected_type=type_hints["role_session_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "git_hub_actions_role_arn": git_hub_actions_role_arn,
        }
        if role_session_name is not None:
            self._values["role_session_name"] = role_session_name

    @builtins.property
    def git_hub_actions_role_arn(self) -> builtins.str:
        '''(experimental) The ARN of the role that GitHub Actions will assume via OpenID Connect.

        :stability: experimental
        '''
        result = self._values.get("git_hub_actions_role_arn")
        assert result is not None, "Required property 'git_hub_actions_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_session_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Optional role session name to use when assuming the role.

        :default: - no role session name

        :stability: experimental
        '''
        result = self._values.get("role_session_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OpenIdConnectProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipelineJob(
    _github_actions_cdk_5328d874.Job,
    metaclass=jsii.JSIIMeta,
    jsii_type="@github-actions-cdk/aws-cdk.PipelineJob",
):
    '''(experimental) Represents a job within the pipeline that requires AWS credentials and CDK output.

    :stability: experimental
    :remarks:

    The ``PipelineJob`` class extends the ``Job`` class and includes specific properties and methods for managing
    AWS authentication, CDK output references, and version control for GitHub Actions used in the pipeline.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        aws_credentials: AwsCredentialsProvider,
        cdkout_dir: builtins.str,
        version_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        container: typing.Optional[typing.Union[_github_actions_cdk_5328d874.ContainerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        continue_on_error: typing.Optional[builtins.bool] = None,
        defaults: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Defaults, typing.Dict[builtins.str, typing.Any]]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        environment: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        needs: typing.Optional[typing.Sequence[builtins.str]] = None,
        outputs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        permissions: typing.Optional[typing.Union[typing.Union[_github_actions_cdk_5328d874.PermissionsEvent, typing.Dict[builtins.str, typing.Any]], builtins.str]] = None,
        required_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
        runner_labels: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
        runs_on: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
        services: typing.Optional[typing.Mapping[builtins.str, typing.Union[_github_actions_cdk_5328d874.ContainerOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        strategy: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Strategy, typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Constructs a new instance of ``PipelineJob``.

        :param scope: - The scope in which to define this job construct.
        :param id: - Unique identifier for this job within the workflow.
        :param aws_credentials: (experimental) Provider for AWS credentials to be used within this job.
        :param cdkout_dir: (experimental) Directory path where CDK output files are located.
        :param version_overrides: (experimental) Optional version overrides for specific GitHub Actions.
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0a1b56d71fea410fac564beb0d9f7eefec6642781632cddad618cdcfe638a48)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PipelineJobProps(
            aws_credentials=aws_credentials,
            cdkout_dir=cdkout_dir,
            version_overrides=version_overrides,
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

    @jsii.member(jsii_name="lookupVersion")
    def lookup_version(
        self,
        action_identifier: builtins.str,
    ) -> typing.Optional[builtins.str]:
        '''(experimental) Looks up the version override for a given action identifier, if available.

        :param action_identifier: - The identifier of the GitHub Action to retrieve the version for.

        :return: The overridden version (or SHA) for the action, if specified; otherwise, ``undefined``.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2873fe2e3b952f8b3cb820a2ee5469748a397d1635469c974d4bd18b0f704c68)
            check_type(argname="argument action_identifier", value=action_identifier, expected_type=type_hints["action_identifier"])
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "lookupVersion", [action_identifier]))

    @builtins.property
    @jsii.member(jsii_name="awsCredentials")
    def aws_credentials(self) -> AwsCredentialsProvider:
        '''(experimental) AWS credentials provider associated with this job.

        :stability: experimental
        '''
        return typing.cast(AwsCredentialsProvider, jsii.get(self, "awsCredentials"))

    @builtins.property
    @jsii.member(jsii_name="cdkoutDir")
    def cdkout_dir(self) -> builtins.str:
        '''(experimental) Directory containing the CDK output files for this job.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "cdkoutDir"))

    @builtins.property
    @jsii.member(jsii_name="versionOverrides")
    def version_overrides(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''(experimental) Specific version overrides for GitHub Actions, if any are provided.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "versionOverrides"))


@jsii.data_type(
    jsii_type="@github-actions-cdk/aws-cdk.PipelineJobProps",
    jsii_struct_bases=[_github_actions_cdk_5328d874.JobProps],
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
        "aws_credentials": "awsCredentials",
        "cdkout_dir": "cdkoutDir",
        "version_overrides": "versionOverrides",
    },
)
class PipelineJobProps(_github_actions_cdk_5328d874.JobProps):
    def __init__(
        self,
        *,
        container: typing.Optional[typing.Union[_github_actions_cdk_5328d874.ContainerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        continue_on_error: typing.Optional[builtins.bool] = None,
        defaults: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Defaults, typing.Dict[builtins.str, typing.Any]]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        environment: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        needs: typing.Optional[typing.Sequence[builtins.str]] = None,
        outputs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        permissions: typing.Optional[typing.Union[typing.Union[_github_actions_cdk_5328d874.PermissionsEvent, typing.Dict[builtins.str, typing.Any]], builtins.str]] = None,
        required_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
        runner_labels: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
        runs_on: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
        services: typing.Optional[typing.Mapping[builtins.str, typing.Union[_github_actions_cdk_5328d874.ContainerOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        strategy: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Strategy, typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_minutes: typing.Optional[jsii.Number] = None,
        aws_credentials: AwsCredentialsProvider,
        cdkout_dir: builtins.str,
        version_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''(experimental) Configuration properties for defining a job in the pipeline.

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
        :param aws_credentials: (experimental) Provider for AWS credentials to be used within this job.
        :param cdkout_dir: (experimental) Directory path where CDK output files are located.
        :param version_overrides: (experimental) Optional version overrides for specific GitHub Actions.

        :stability: experimental
        :remarks:

        ``PipelineJobProps`` allows for specifying the AWS credentials provider, any version overrides for actions,
        and the CDK output directory used within the pipeline job.
        '''
        if isinstance(container, dict):
            container = _github_actions_cdk_5328d874.ContainerOptions(**container)
        if isinstance(defaults, dict):
            defaults = _github_actions_cdk_5328d874.Defaults(**defaults)
        if isinstance(environment, dict):
            environment = _github_actions_cdk_5328d874.Environment(**environment)
        if isinstance(strategy, dict):
            strategy = _github_actions_cdk_5328d874.Strategy(**strategy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8217b395daebe0e7a395128c1609592bee8af021b8216b27d66bc65daee5596)
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
            check_type(argname="argument aws_credentials", value=aws_credentials, expected_type=type_hints["aws_credentials"])
            check_type(argname="argument cdkout_dir", value=cdkout_dir, expected_type=type_hints["cdkout_dir"])
            check_type(argname="argument version_overrides", value=version_overrides, expected_type=type_hints["version_overrides"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "aws_credentials": aws_credentials,
            "cdkout_dir": cdkout_dir,
        }
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
        if version_overrides is not None:
            self._values["version_overrides"] = version_overrides

    @builtins.property
    def container(
        self,
    ) -> typing.Optional[_github_actions_cdk_5328d874.ContainerOptions]:
        '''(experimental) A container to run any steps in a job that don't already specify a container.

        If you have steps that use both script and container actions,
        the container actions will run as sibling containers on the same network
        with the same volume mounts.

        :stability: experimental
        '''
        result = self._values.get("container")
        return typing.cast(typing.Optional[_github_actions_cdk_5328d874.ContainerOptions], result)

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
    def defaults(self) -> typing.Optional[_github_actions_cdk_5328d874.Defaults]:
        '''(experimental) Default configuration settings for job steps.

        :stability: experimental
        '''
        result = self._values.get("defaults")
        return typing.cast(typing.Optional[_github_actions_cdk_5328d874.Defaults], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Environment variables for all steps in the job.

        :stability: experimental
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def environment(self) -> typing.Optional[_github_actions_cdk_5328d874.Environment]:
        '''(experimental) GitHub environment target for this job.

        :stability: experimental
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[_github_actions_cdk_5328d874.Environment], result)

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
    ) -> typing.Optional[typing.Union[_github_actions_cdk_5328d874.PermissionsEvent, builtins.str]]:
        '''(experimental) Permissions granted to the job.

        :stability: experimental
        '''
        result = self._values.get("permissions")
        return typing.cast(typing.Optional[typing.Union[_github_actions_cdk_5328d874.PermissionsEvent, builtins.str]], result)

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
    ) -> typing.Optional[typing.Mapping[builtins.str, _github_actions_cdk_5328d874.ContainerOptions]]:
        '''(experimental) Used to host service containers for a job in a workflow.

        Service
        containers are useful for creating databases or cache services like Redis.
        The runner automatically creates a Docker network and manages the life
        cycle of the service containers.

        :stability: experimental
        '''
        result = self._values.get("services")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _github_actions_cdk_5328d874.ContainerOptions]], result)

    @builtins.property
    def strategy(self) -> typing.Optional[_github_actions_cdk_5328d874.Strategy]:
        '''(experimental) Strategy settings, including matrix configuration and concurrency limits.

        :stability: experimental
        '''
        result = self._values.get("strategy")
        return typing.cast(typing.Optional[_github_actions_cdk_5328d874.Strategy], result)

    @builtins.property
    def timeout_minutes(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Timeout duration for the job, in minutes.

        :stability: experimental
        '''
        result = self._values.get("timeout_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def aws_credentials(self) -> AwsCredentialsProvider:
        '''(experimental) Provider for AWS credentials to be used within this job.

        :stability: experimental
        :remarks: This enables the job to authenticate and interact with AWS resources.
        '''
        result = self._values.get("aws_credentials")
        assert result is not None, "Required property 'aws_credentials' is missing"
        return typing.cast(AwsCredentialsProvider, result)

    @builtins.property
    def cdkout_dir(self) -> builtins.str:
        '''(experimental) Directory path where CDK output files are located.

        :stability: experimental
        :remarks:

        Specifies the folder that contains synthesized output files from AWS CDK. This path is used by the pipeline
        job to locate and utilize CDK artifacts in subsequent workflow steps.
        '''
        result = self._values.get("cdkout_dir")
        assert result is not None, "Required property 'cdkout_dir' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version_overrides(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Optional version overrides for specific GitHub Actions.

        :stability: experimental
        :remarks:

        Provides a way to specify custom versions (or SHA values) for GitHub Actions, allowing for precise control
        over which versions are used in the workflow.
        '''
        result = self._values.get("version_overrides")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipelineJobProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipelineWorkflow(
    _github_actions_cdk_5328d874.Workflow,
    metaclass=jsii.JSIIMeta,
    jsii_type="@github-actions-cdk/aws-cdk.PipelineWorkflow",
):
    '''(experimental) Represents a GitHub Actions workflow to manage CDK pipeline jobs for synthesizing, publishing, and deploying AWS resources.

    :stability: experimental
    :remarks: Extends ``Workflow`` from ``github-actions-cdk``, and provides structured job orchestration based on the AWS CDK pipeline graph.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        aws_credentials: AwsCredentialsProvider,
        cdkout_dir: builtins.str,
        pipeline: _aws_cdk_pipelines_ceddda9d.PipelineBase,
        stack_options: typing.Mapping[builtins.str, typing.Union["StackOptions", typing.Dict[builtins.str, typing.Any]]],
        post_build: typing.Optional[IJobPhase] = None,
        pre_build: typing.Optional[IJobPhase] = None,
        single_publisher_per_asset_type: typing.Optional[builtins.bool] = None,
        version_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        comment_at_top: typing.Optional[builtins.str] = None,
        concurrency: typing.Optional[typing.Union[_github_actions_cdk_5328d874.ConcurrencyOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        defaults: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Defaults, typing.Dict[builtins.str, typing.Any]]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        permissions: typing.Optional[typing.Union[typing.Union[_github_actions_cdk_5328d874.PermissionsEvent, typing.Dict[builtins.str, typing.Any]], builtins.str]] = None,
        run_name: typing.Optional[builtins.str] = None,
        synthesizer: typing.Optional[_github_actions_cdk_5328d874.IWorkflowSynthesizer] = None,
        triggers: typing.Optional[typing.Union[_github_actions_cdk_5328d874.WorkflowTriggers, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Initializes a new ``PipelineWorkflow``.

        :param scope: - The scope within which this construct is created.
        :param id: - The unique identifier for this workflow.
        :param aws_credentials: (experimental) Provider for AWS credentials required to interact with AWS services.
        :param cdkout_dir: (experimental) Directory where CDK generates CloudFormation templates.
        :param pipeline: (experimental) The CDK pipeline, including its stages and job configuration. Defines the sequence and structure of actions for synthesizing, publishing, and deploying.
        :param stack_options: (experimental) Configuration options for individual stacks in the pipeline.
        :param post_build: (experimental) Optional job phase to run after the main build jobs.
        :param pre_build: (experimental) Optional job phase to run before the main build jobs.
        :param single_publisher_per_asset_type: (experimental) Whether to use a single publisher job for each type of asset.
        :param version_overrides: (experimental) Overrides for specific action versions in GitHub Actions.
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
            type_hints = typing.get_type_hints(_typecheckingstub__636c480c4cb48ef189ebd2ce3ba795a9cb75b585ca1454a679f50fd5c97a0860)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PipelineWorkflowProps(
            aws_credentials=aws_credentials,
            cdkout_dir=cdkout_dir,
            pipeline=pipeline,
            stack_options=stack_options,
            post_build=post_build,
            pre_build=pre_build,
            single_publisher_per_asset_type=single_publisher_per_asset_type,
            version_overrides=version_overrides,
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

    @jsii.member(jsii_name="createDeployJob")
    def _create_deploy_job(
        self,
        id: builtins.str,
        needs: typing.Sequence[builtins.str],
        stack: _aws_cdk_pipelines_ceddda9d.StackDeployment,
    ) -> None:
        '''(experimental) Creates a job for deploying a stack to AWS.

        :param id: - Unique identifier for the deploy job.
        :param needs: - List of dependencies for this job.
        :param stack: - Stack deployment information.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__797dac26a066a8ec56c185ada275b2cd85824838cdae521c876c628102574cc4)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument needs", value=needs, expected_type=type_hints["needs"])
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
        return typing.cast(None, jsii.invoke(self, "createDeployJob", [id, needs, stack]))

    @jsii.member(jsii_name="createPublishJob")
    def _create_publish_job(
        self,
        id: builtins.str,
        needs: typing.Sequence[builtins.str],
        assets: typing.Sequence[typing.Union[_aws_cdk_pipelines_ceddda9d.StackAsset, typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''(experimental) Creates a job for publishing stack assets.

        :param id: - Unique identifier for the publish job.
        :param needs: - List of dependencies for this job.
        :param assets: - List of assets to publish.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fb9b17aa49b07b12d5403e6eea5120e283d94984ac11f25c8ca90b9b0c7ca10)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument needs", value=needs, expected_type=type_hints["needs"])
            check_type(argname="argument assets", value=assets, expected_type=type_hints["assets"])
        return typing.cast(None, jsii.invoke(self, "createPublishJob", [id, needs, assets]))

    @jsii.member(jsii_name="createStageJob")
    def _create_stage_job(
        self,
        id: builtins.str,
        needs: typing.Sequence[builtins.str],
        job: "StageJob",
    ) -> None:
        '''(experimental) Creates a job for running a stage job in the pipeline.

        :param id: - Unique identifier for the stage job.
        :param needs: - List of dependencies for this job.
        :param job: - Configuration of the stage job.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f667bc728647daae0bc3e038e48953f906a5a9770f1a80884f0cfa8ae5d887e)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument needs", value=needs, expected_type=type_hints["needs"])
            check_type(argname="argument job", value=job, expected_type=type_hints["job"])
        return typing.cast(None, jsii.invoke(self, "createStageJob", [id, needs, job]))

    @jsii.member(jsii_name="createSynthJob")
    def _create_synth_job(
        self,
        id: builtins.str,
        needs: typing.Sequence[builtins.str],
        synth: "Synth",
        pre_build: typing.Optional[IJobPhase] = None,
        post_build: typing.Optional[IJobPhase] = None,
    ) -> None:
        '''(experimental) Creates a job for synthesizing the CDK application.

        :param id: - Unique identifier for the synth job.
        :param needs: - List of dependencies for this job.
        :param synth: - Synth step configuration.
        :param pre_build: - Optional jobs to run before the synth job.
        :param post_build: - Optional jobs to run after the synth job.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee60549ea66f57d360fb786684c7d896f8430d32ce57cbe8e14d5feea5b43c3c)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument needs", value=needs, expected_type=type_hints["needs"])
            check_type(argname="argument synth", value=synth, expected_type=type_hints["synth"])
            check_type(argname="argument pre_build", value=pre_build, expected_type=type_hints["pre_build"])
            check_type(argname="argument post_build", value=post_build, expected_type=type_hints["post_build"])
        return typing.cast(None, jsii.invoke(self, "createSynthJob", [id, needs, synth, pre_build, post_build]))

    @builtins.property
    @jsii.member(jsii_name="awsCredentials")
    def aws_credentials(self) -> AwsCredentialsProvider:
        '''
        :stability: experimental
        '''
        return typing.cast(AwsCredentialsProvider, jsii.get(self, "awsCredentials"))

    @builtins.property
    @jsii.member(jsii_name="cdkoutDir")
    def cdkout_dir(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "cdkoutDir"))

    @builtins.property
    @jsii.member(jsii_name="versionOverrides")
    def version_overrides(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "versionOverrides"))


@jsii.data_type(
    jsii_type="@github-actions-cdk/aws-cdk.PipelineWorkflowProps",
    jsii_struct_bases=[_github_actions_cdk_5328d874.WorkflowProps],
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
        "aws_credentials": "awsCredentials",
        "cdkout_dir": "cdkoutDir",
        "pipeline": "pipeline",
        "stack_options": "stackOptions",
        "post_build": "postBuild",
        "pre_build": "preBuild",
        "single_publisher_per_asset_type": "singlePublisherPerAssetType",
        "version_overrides": "versionOverrides",
    },
)
class PipelineWorkflowProps(_github_actions_cdk_5328d874.WorkflowProps):
    def __init__(
        self,
        *,
        comment_at_top: typing.Optional[builtins.str] = None,
        concurrency: typing.Optional[typing.Union[_github_actions_cdk_5328d874.ConcurrencyOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        defaults: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Defaults, typing.Dict[builtins.str, typing.Any]]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        permissions: typing.Optional[typing.Union[typing.Union[_github_actions_cdk_5328d874.PermissionsEvent, typing.Dict[builtins.str, typing.Any]], builtins.str]] = None,
        run_name: typing.Optional[builtins.str] = None,
        synthesizer: typing.Optional[_github_actions_cdk_5328d874.IWorkflowSynthesizer] = None,
        triggers: typing.Optional[typing.Union[_github_actions_cdk_5328d874.WorkflowTriggers, typing.Dict[builtins.str, typing.Any]]] = None,
        aws_credentials: AwsCredentialsProvider,
        cdkout_dir: builtins.str,
        pipeline: _aws_cdk_pipelines_ceddda9d.PipelineBase,
        stack_options: typing.Mapping[builtins.str, typing.Union["StackOptions", typing.Dict[builtins.str, typing.Any]]],
        post_build: typing.Optional[IJobPhase] = None,
        pre_build: typing.Optional[IJobPhase] = None,
        single_publisher_per_asset_type: typing.Optional[builtins.bool] = None,
        version_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''(experimental) Properties for defining a Pipeline Workflow.

        :param comment_at_top: (experimental) An optional comment that can be included at the top of the generated workflow YAML. This can serve as a note or reminder for users not to modify the generated output directly. Default: "Generated by github-actions-cdk, DO NOT EDIT DIRECTLY!"
        :param concurrency: (experimental) Configuration for concurrency control of workflow runs.
        :param defaults: (experimental) Default configuration settings for jobs in this workflow.
        :param env: (experimental) Environment variables that will be available to all jobs in the workflow.
        :param name: (experimental) The name of the workflow. GitHub displays the names of your workflows under your repository's "Actions" tab. If you omit the name, GitHub displays the workflow file path relative to the root of the repository.
        :param permissions: (experimental) Permissions required by the workflow.
        :param run_name: (experimental) The name for workflow runs generated from the workflow. GitHub displays the workflow run name in the list of workflow runs on your repository's "Actions" tab. If ``run-name`` is omitted or is only whitespace, then the run name is set to event-specific information for the workflow run. For example, for a workflow triggered by a ``push`` or ``pull_request`` event, it is set as the commit message or the title of the pull request. This value can include expressions and can reference the ``github`` and ``inputs`` contexts.
        :param synthesizer: (experimental) Custom synthesizer for rendering the workflow YAML.
        :param triggers: (experimental) Triggers that define when this workflow should run.
        :param aws_credentials: (experimental) Provider for AWS credentials required to interact with AWS services.
        :param cdkout_dir: (experimental) Directory where CDK generates CloudFormation templates.
        :param pipeline: (experimental) The CDK pipeline, including its stages and job configuration. Defines the sequence and structure of actions for synthesizing, publishing, and deploying.
        :param stack_options: (experimental) Configuration options for individual stacks in the pipeline.
        :param post_build: (experimental) Optional job phase to run after the main build jobs.
        :param pre_build: (experimental) Optional job phase to run before the main build jobs.
        :param single_publisher_per_asset_type: (experimental) Whether to use a single publisher job for each type of asset.
        :param version_overrides: (experimental) Overrides for specific action versions in GitHub Actions.

        :stability: experimental
        :remarks: This interface extends WorkflowProps and adds properties specific to AWS CDK Pipelines and job execution.
        '''
        if isinstance(concurrency, dict):
            concurrency = _github_actions_cdk_5328d874.ConcurrencyOptions(**concurrency)
        if isinstance(defaults, dict):
            defaults = _github_actions_cdk_5328d874.Defaults(**defaults)
        if isinstance(triggers, dict):
            triggers = _github_actions_cdk_5328d874.WorkflowTriggers(**triggers)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd66f4263f804ebdde225a8646d12b8b07b3893a0d7565be96d9dfa6869f63dc)
            check_type(argname="argument comment_at_top", value=comment_at_top, expected_type=type_hints["comment_at_top"])
            check_type(argname="argument concurrency", value=concurrency, expected_type=type_hints["concurrency"])
            check_type(argname="argument defaults", value=defaults, expected_type=type_hints["defaults"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
            check_type(argname="argument run_name", value=run_name, expected_type=type_hints["run_name"])
            check_type(argname="argument synthesizer", value=synthesizer, expected_type=type_hints["synthesizer"])
            check_type(argname="argument triggers", value=triggers, expected_type=type_hints["triggers"])
            check_type(argname="argument aws_credentials", value=aws_credentials, expected_type=type_hints["aws_credentials"])
            check_type(argname="argument cdkout_dir", value=cdkout_dir, expected_type=type_hints["cdkout_dir"])
            check_type(argname="argument pipeline", value=pipeline, expected_type=type_hints["pipeline"])
            check_type(argname="argument stack_options", value=stack_options, expected_type=type_hints["stack_options"])
            check_type(argname="argument post_build", value=post_build, expected_type=type_hints["post_build"])
            check_type(argname="argument pre_build", value=pre_build, expected_type=type_hints["pre_build"])
            check_type(argname="argument single_publisher_per_asset_type", value=single_publisher_per_asset_type, expected_type=type_hints["single_publisher_per_asset_type"])
            check_type(argname="argument version_overrides", value=version_overrides, expected_type=type_hints["version_overrides"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "aws_credentials": aws_credentials,
            "cdkout_dir": cdkout_dir,
            "pipeline": pipeline,
            "stack_options": stack_options,
        }
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
        if post_build is not None:
            self._values["post_build"] = post_build
        if pre_build is not None:
            self._values["pre_build"] = pre_build
        if single_publisher_per_asset_type is not None:
            self._values["single_publisher_per_asset_type"] = single_publisher_per_asset_type
        if version_overrides is not None:
            self._values["version_overrides"] = version_overrides

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
    def concurrency(
        self,
    ) -> typing.Optional[_github_actions_cdk_5328d874.ConcurrencyOptions]:
        '''(experimental) Configuration for concurrency control of workflow runs.

        :stability: experimental
        '''
        result = self._values.get("concurrency")
        return typing.cast(typing.Optional[_github_actions_cdk_5328d874.ConcurrencyOptions], result)

    @builtins.property
    def defaults(self) -> typing.Optional[_github_actions_cdk_5328d874.Defaults]:
        '''(experimental) Default configuration settings for jobs in this workflow.

        :stability: experimental
        '''
        result = self._values.get("defaults")
        return typing.cast(typing.Optional[_github_actions_cdk_5328d874.Defaults], result)

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
    ) -> typing.Optional[typing.Union[_github_actions_cdk_5328d874.PermissionsEvent, builtins.str]]:
        '''(experimental) Permissions required by the workflow.

        :stability: experimental
        '''
        result = self._values.get("permissions")
        return typing.cast(typing.Optional[typing.Union[_github_actions_cdk_5328d874.PermissionsEvent, builtins.str]], result)

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
    def synthesizer(
        self,
    ) -> typing.Optional[_github_actions_cdk_5328d874.IWorkflowSynthesizer]:
        '''(experimental) Custom synthesizer for rendering the workflow YAML.

        :stability: experimental
        '''
        result = self._values.get("synthesizer")
        return typing.cast(typing.Optional[_github_actions_cdk_5328d874.IWorkflowSynthesizer], result)

    @builtins.property
    def triggers(
        self,
    ) -> typing.Optional[_github_actions_cdk_5328d874.WorkflowTriggers]:
        '''(experimental) Triggers that define when this workflow should run.

        :stability: experimental
        '''
        result = self._values.get("triggers")
        return typing.cast(typing.Optional[_github_actions_cdk_5328d874.WorkflowTriggers], result)

    @builtins.property
    def aws_credentials(self) -> AwsCredentialsProvider:
        '''(experimental) Provider for AWS credentials required to interact with AWS services.

        :stability: experimental
        '''
        result = self._values.get("aws_credentials")
        assert result is not None, "Required property 'aws_credentials' is missing"
        return typing.cast(AwsCredentialsProvider, result)

    @builtins.property
    def cdkout_dir(self) -> builtins.str:
        '''(experimental) Directory where CDK generates CloudFormation templates.

        :stability: experimental
        '''
        result = self._values.get("cdkout_dir")
        assert result is not None, "Required property 'cdkout_dir' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pipeline(self) -> _aws_cdk_pipelines_ceddda9d.PipelineBase:
        '''(experimental) The CDK pipeline, including its stages and job configuration.

        Defines the sequence and structure of actions for synthesizing, publishing, and deploying.

        :stability: experimental
        '''
        result = self._values.get("pipeline")
        assert result is not None, "Required property 'pipeline' is missing"
        return typing.cast(_aws_cdk_pipelines_ceddda9d.PipelineBase, result)

    @builtins.property
    def stack_options(self) -> typing.Mapping[builtins.str, "StackOptions"]:
        '''(experimental) Configuration options for individual stacks in the pipeline.

        :stability: experimental
        '''
        result = self._values.get("stack_options")
        assert result is not None, "Required property 'stack_options' is missing"
        return typing.cast(typing.Mapping[builtins.str, "StackOptions"], result)

    @builtins.property
    def post_build(self) -> typing.Optional[IJobPhase]:
        '''(experimental) Optional job phase to run after the main build jobs.

        :stability: experimental
        '''
        result = self._values.get("post_build")
        return typing.cast(typing.Optional[IJobPhase], result)

    @builtins.property
    def pre_build(self) -> typing.Optional[IJobPhase]:
        '''(experimental) Optional job phase to run before the main build jobs.

        :stability: experimental
        '''
        result = self._values.get("pre_build")
        return typing.cast(typing.Optional[IJobPhase], result)

    @builtins.property
    def single_publisher_per_asset_type(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to use a single publisher job for each type of asset.

        :stability: experimental
        :remarks:

        If ``true``, each asset type (e.g., file assets, Docker images) will be published by a single job in the workflow,
        consolidating multiple asset publication steps into one job. This can reduce the total number of jobs needed,
        making the workflow more efficient when dealing with large numbers of assets.

        Defaults to ``false``, meaning each asset is published in its own job.
        '''
        result = self._values.get("single_publisher_per_asset_type")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def version_overrides(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Overrides for specific action versions in GitHub Actions.

        :stability: experimental
        '''
        result = self._values.get("version_overrides")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipelineWorkflowProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PublishPipelineJob(
    PipelineJob,
    metaclass=jsii.JSIIMeta,
    jsii_type="@github-actions-cdk/aws-cdk.PublishPipelineJob",
):
    '''(experimental) A job that publishes stack assets to AWS.

    :stability: experimental
    :remarks:

    The ``PublishPipelineJob`` class handles the process of publishing assets to AWS.
    It defines the steps required to download artifacts, install necessary dependencies,
    and execute the publish command for each asset. The job integrates with AWS
    credentials for secure authentication and provides hooks for outputting asset hashes.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        asset_hash_map: typing.Mapping[builtins.str, builtins.str],
        assets: typing.Sequence[typing.Union[_aws_cdk_pipelines_ceddda9d.StackAsset, typing.Dict[builtins.str, typing.Any]]],
        cdk_cli_version: typing.Optional[builtins.str] = None,
        aws_credentials: AwsCredentialsProvider,
        cdkout_dir: builtins.str,
        version_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        container: typing.Optional[typing.Union[_github_actions_cdk_5328d874.ContainerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        continue_on_error: typing.Optional[builtins.bool] = None,
        defaults: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Defaults, typing.Dict[builtins.str, typing.Any]]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        environment: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        needs: typing.Optional[typing.Sequence[builtins.str]] = None,
        outputs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        permissions: typing.Optional[typing.Union[typing.Union[_github_actions_cdk_5328d874.PermissionsEvent, typing.Dict[builtins.str, typing.Any]], builtins.str]] = None,
        required_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
        runner_labels: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
        runs_on: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
        services: typing.Optional[typing.Mapping[builtins.str, typing.Union[_github_actions_cdk_5328d874.ContainerOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        strategy: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Strategy, typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Constructs a new instance of ``PublishPipelineJob``.

        :param scope: - The parent construct scope.
        :param id: - Unique identifier for this publish job.
        :param asset_hash_map: (experimental) A mapping of asset identifiers to their corresponding output expressions.
        :param assets: (experimental) The stack assets to be published.
        :param cdk_cli_version: (experimental) Optional version of the CDK CLI to use for publishing.
        :param aws_credentials: (experimental) Provider for AWS credentials to be used within this job.
        :param cdkout_dir: (experimental) Directory path where CDK output files are located.
        :param version_overrides: (experimental) Optional version overrides for specific GitHub Actions.
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
        :remarks:

        The constructor initializes the publish job by setting up the necessary steps
        to download artifacts, install dependencies, and publish assets. It iterates
        through each asset and creates the appropriate publish steps.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53e7850def2e5e1ec7b09e87c095d95e13e1342749a760f7b76c87604d50052e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PublishPipelineJobProps(
            asset_hash_map=asset_hash_map,
            assets=assets,
            cdk_cli_version=cdk_cli_version,
            aws_credentials=aws_credentials,
            cdkout_dir=cdkout_dir,
            version_overrides=version_overrides,
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


@jsii.data_type(
    jsii_type="@github-actions-cdk/aws-cdk.PublishPipelineJobProps",
    jsii_struct_bases=[PipelineJobProps],
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
        "aws_credentials": "awsCredentials",
        "cdkout_dir": "cdkoutDir",
        "version_overrides": "versionOverrides",
        "asset_hash_map": "assetHashMap",
        "assets": "assets",
        "cdk_cli_version": "cdkCliVersion",
    },
)
class PublishPipelineJobProps(PipelineJobProps):
    def __init__(
        self,
        *,
        container: typing.Optional[typing.Union[_github_actions_cdk_5328d874.ContainerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        continue_on_error: typing.Optional[builtins.bool] = None,
        defaults: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Defaults, typing.Dict[builtins.str, typing.Any]]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        environment: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        needs: typing.Optional[typing.Sequence[builtins.str]] = None,
        outputs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        permissions: typing.Optional[typing.Union[typing.Union[_github_actions_cdk_5328d874.PermissionsEvent, typing.Dict[builtins.str, typing.Any]], builtins.str]] = None,
        required_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
        runner_labels: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
        runs_on: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
        services: typing.Optional[typing.Mapping[builtins.str, typing.Union[_github_actions_cdk_5328d874.ContainerOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        strategy: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Strategy, typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_minutes: typing.Optional[jsii.Number] = None,
        aws_credentials: AwsCredentialsProvider,
        cdkout_dir: builtins.str,
        version_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        asset_hash_map: typing.Mapping[builtins.str, builtins.str],
        assets: typing.Sequence[typing.Union[_aws_cdk_pipelines_ceddda9d.StackAsset, typing.Dict[builtins.str, typing.Any]]],
        cdk_cli_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for a publish pipeline job.

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
        :param aws_credentials: (experimental) Provider for AWS credentials to be used within this job.
        :param cdkout_dir: (experimental) Directory path where CDK output files are located.
        :param version_overrides: (experimental) Optional version overrides for specific GitHub Actions.
        :param asset_hash_map: (experimental) A mapping of asset identifiers to their corresponding output expressions.
        :param assets: (experimental) The stack assets to be published.
        :param cdk_cli_version: (experimental) Optional version of the CDK CLI to use for publishing.

        :stability: experimental
        :remarks:

        This interface defines the configuration options for a publish job in the pipeline,
        including the stack assets that need to be published, their corresponding hash mappings,
        and the optional version of the CDK CLI to use.
        '''
        if isinstance(container, dict):
            container = _github_actions_cdk_5328d874.ContainerOptions(**container)
        if isinstance(defaults, dict):
            defaults = _github_actions_cdk_5328d874.Defaults(**defaults)
        if isinstance(environment, dict):
            environment = _github_actions_cdk_5328d874.Environment(**environment)
        if isinstance(strategy, dict):
            strategy = _github_actions_cdk_5328d874.Strategy(**strategy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be1f9153f78791e125c464c4a3ee931ee0b1ae6f44bb96472fd3fbc58947c7a0)
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
            check_type(argname="argument aws_credentials", value=aws_credentials, expected_type=type_hints["aws_credentials"])
            check_type(argname="argument cdkout_dir", value=cdkout_dir, expected_type=type_hints["cdkout_dir"])
            check_type(argname="argument version_overrides", value=version_overrides, expected_type=type_hints["version_overrides"])
            check_type(argname="argument asset_hash_map", value=asset_hash_map, expected_type=type_hints["asset_hash_map"])
            check_type(argname="argument assets", value=assets, expected_type=type_hints["assets"])
            check_type(argname="argument cdk_cli_version", value=cdk_cli_version, expected_type=type_hints["cdk_cli_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "aws_credentials": aws_credentials,
            "cdkout_dir": cdkout_dir,
            "asset_hash_map": asset_hash_map,
            "assets": assets,
        }
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
        if version_overrides is not None:
            self._values["version_overrides"] = version_overrides
        if cdk_cli_version is not None:
            self._values["cdk_cli_version"] = cdk_cli_version

    @builtins.property
    def container(
        self,
    ) -> typing.Optional[_github_actions_cdk_5328d874.ContainerOptions]:
        '''(experimental) A container to run any steps in a job that don't already specify a container.

        If you have steps that use both script and container actions,
        the container actions will run as sibling containers on the same network
        with the same volume mounts.

        :stability: experimental
        '''
        result = self._values.get("container")
        return typing.cast(typing.Optional[_github_actions_cdk_5328d874.ContainerOptions], result)

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
    def defaults(self) -> typing.Optional[_github_actions_cdk_5328d874.Defaults]:
        '''(experimental) Default configuration settings for job steps.

        :stability: experimental
        '''
        result = self._values.get("defaults")
        return typing.cast(typing.Optional[_github_actions_cdk_5328d874.Defaults], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Environment variables for all steps in the job.

        :stability: experimental
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def environment(self) -> typing.Optional[_github_actions_cdk_5328d874.Environment]:
        '''(experimental) GitHub environment target for this job.

        :stability: experimental
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[_github_actions_cdk_5328d874.Environment], result)

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
    ) -> typing.Optional[typing.Union[_github_actions_cdk_5328d874.PermissionsEvent, builtins.str]]:
        '''(experimental) Permissions granted to the job.

        :stability: experimental
        '''
        result = self._values.get("permissions")
        return typing.cast(typing.Optional[typing.Union[_github_actions_cdk_5328d874.PermissionsEvent, builtins.str]], result)

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
    ) -> typing.Optional[typing.Mapping[builtins.str, _github_actions_cdk_5328d874.ContainerOptions]]:
        '''(experimental) Used to host service containers for a job in a workflow.

        Service
        containers are useful for creating databases or cache services like Redis.
        The runner automatically creates a Docker network and manages the life
        cycle of the service containers.

        :stability: experimental
        '''
        result = self._values.get("services")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _github_actions_cdk_5328d874.ContainerOptions]], result)

    @builtins.property
    def strategy(self) -> typing.Optional[_github_actions_cdk_5328d874.Strategy]:
        '''(experimental) Strategy settings, including matrix configuration and concurrency limits.

        :stability: experimental
        '''
        result = self._values.get("strategy")
        return typing.cast(typing.Optional[_github_actions_cdk_5328d874.Strategy], result)

    @builtins.property
    def timeout_minutes(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Timeout duration for the job, in minutes.

        :stability: experimental
        '''
        result = self._values.get("timeout_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def aws_credentials(self) -> AwsCredentialsProvider:
        '''(experimental) Provider for AWS credentials to be used within this job.

        :stability: experimental
        :remarks: This enables the job to authenticate and interact with AWS resources.
        '''
        result = self._values.get("aws_credentials")
        assert result is not None, "Required property 'aws_credentials' is missing"
        return typing.cast(AwsCredentialsProvider, result)

    @builtins.property
    def cdkout_dir(self) -> builtins.str:
        '''(experimental) Directory path where CDK output files are located.

        :stability: experimental
        :remarks:

        Specifies the folder that contains synthesized output files from AWS CDK. This path is used by the pipeline
        job to locate and utilize CDK artifacts in subsequent workflow steps.
        '''
        result = self._values.get("cdkout_dir")
        assert result is not None, "Required property 'cdkout_dir' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version_overrides(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Optional version overrides for specific GitHub Actions.

        :stability: experimental
        :remarks:

        Provides a way to specify custom versions (or SHA values) for GitHub Actions, allowing for precise control
        over which versions are used in the workflow.
        '''
        result = self._values.get("version_overrides")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def asset_hash_map(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''(experimental) A mapping of asset identifiers to their corresponding output expressions.

        :stability: experimental
        :remarks:

        This map is used to track the outputs of each asset publish step,
        where the keys are asset identifiers, and the values are the output
        expressions that reference the published asset hashes in the GitHub Actions
        workflow. This enables downstream jobs in the pipeline to access the published
        asset information as needed.
        '''
        result = self._values.get("asset_hash_map")
        assert result is not None, "Required property 'asset_hash_map' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    @builtins.property
    def assets(self) -> typing.List[_aws_cdk_pipelines_ceddda9d.StackAsset]:
        '''(experimental) The stack assets to be published.

        :stability: experimental
        :remarks:

        This is an array of ``StackAsset`` objects that represent the resources
        in the AWS CDK application that need to be published to AWS. Each asset should
        be included to ensure they are correctly managed and deployed.
        '''
        result = self._values.get("assets")
        assert result is not None, "Required property 'assets' is missing"
        return typing.cast(typing.List[_aws_cdk_pipelines_ceddda9d.StackAsset], result)

    @builtins.property
    def cdk_cli_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Optional version of the CDK CLI to use for publishing.

        :stability: experimental
        :remarks:

        If provided, this version will be used to run the publish commands.
        If omitted, the latest installed version of the CDK CLI will be used.
        Specifying a version can help prevent compatibility issues when deploying
        assets, especially in environments with multiple CDK versions.
        '''
        result = self._values.get("cdk_cli_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PublishPipelineJobProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@github-actions-cdk/aws-cdk.StackCapabilities")
class StackCapabilities(enum.Enum):
    '''(experimental) Enumeration for IAM capabilities that must be acknowledged in AWS CloudFormation templates.

    These capabilities are required for stacks that include IAM resources or specific features.

    :see: `AWS CloudFormation IAM Capabilities Documentation <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#capabilities>`_
    :stability: experimental
    '''

    IAM = "IAM"
    '''(experimental) Acknowledge that the stack includes IAM resources.

    :stability: experimental
    '''
    NAMED_IAM = "NAMED_IAM"
    '''(experimental) Acknowledge that the stack includes custom names for IAM resources.

    :stability: experimental
    '''
    AUTO_EXPAND = "AUTO_EXPAND"
    '''(experimental) Acknowledge that the stack contains one or more macros.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@github-actions-cdk/aws-cdk.StackOptions",
    jsii_struct_bases=[],
    name_mapping={"capabilities": "capabilities", "environment": "environment"},
)
class StackOptions:
    def __init__(
        self,
        *,
        capabilities: typing.Optional[typing.Sequence[StackCapabilities]] = None,
        environment: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Options for the deployment of a stack.

        :param capabilities: (experimental) The capabilities for the stack deployment.
        :param environment: (experimental) The GitHub environment for the stack deployment.

        :stability: experimental
        '''
        if isinstance(environment, dict):
            environment = _github_actions_cdk_5328d874.Environment(**environment)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1e8e3d089ff20ef18b6231aa6e4349e5b21b37ab02c7f35aa88ff0360017ebc)
            check_type(argname="argument capabilities", value=capabilities, expected_type=type_hints["capabilities"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if capabilities is not None:
            self._values["capabilities"] = capabilities
        if environment is not None:
            self._values["environment"] = environment

    @builtins.property
    def capabilities(self) -> typing.Optional[typing.List[StackCapabilities]]:
        '''(experimental) The capabilities for the stack deployment.

        :stability: experimental
        '''
        result = self._values.get("capabilities")
        return typing.cast(typing.Optional[typing.List[StackCapabilities]], result)

    @builtins.property
    def environment(self) -> typing.Optional[_github_actions_cdk_5328d874.Environment]:
        '''(experimental) The GitHub environment for the stack deployment.

        :stability: experimental
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[_github_actions_cdk_5328d874.Environment], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StackOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StageJob(
    _aws_cdk_pipelines_ceddda9d.Step,
    metaclass=jsii.JSIIMeta,
    jsii_type="@github-actions-cdk/aws-cdk.StageJob",
):
    '''(experimental) Represents a job in a stage of the GitHub Actions pipeline.

    This class extends the Step class, providing functionality for executing a job
    with specified options and configurations.

    :stability: experimental
    '''

    def __init__(self, id: builtins.str, props: IStageJobOptions) -> None:
        '''(experimental) Constructs a new instance of StageJob.

        :param id: - Unique identifier for the job step.
        :param props: - Configuration options for the job.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bb3634e18fa12d7ac6153212aea971a4857105a1ad07f241296170cbf29ee04)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [id, props])

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''(experimental) - Unique identifier for the job step.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> IStageJobOptions:
        '''(experimental) - Configuration options for the job.

        :stability: experimental
        '''
        return typing.cast(IStageJobOptions, jsii.get(self, "props"))

    @props.setter
    def props(self, value: IStageJobOptions) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a31d18b6fc7a59f39b409ab74749ebc7122116f6de79527eacb5a56b328e9514)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "props", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@github-actions-cdk/aws-cdk.StageOptions",
    jsii_struct_bases=[],
    name_mapping={
        "git_hub_environment": "gitHubEnvironment",
        "post_jobs": "postJobs",
        "pre_jobs": "preJobs",
        "stack_capabilities": "stackCapabilities",
    },
)
class StageOptions:
    def __init__(
        self,
        *,
        git_hub_environment: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
        post_jobs: typing.Optional[typing.Sequence[StageJob]] = None,
        pre_jobs: typing.Optional[typing.Sequence[StageJob]] = None,
        stack_capabilities: typing.Optional[typing.Sequence[StackCapabilities]] = None,
    ) -> None:
        '''(experimental) Options for configuring a stage in the GitHub Actions pipeline.

        :param git_hub_environment: (experimental) Optional GitHub environment configuration for the stage. This configuration specifies the environment context in which the jobs will run.
        :param post_jobs: (experimental) Optional list of jobs to run after the main stage execution. These jobs can perform cleanup or other necessary tasks.
        :param pre_jobs: (experimental) Optional list of jobs to run before the main stage execution. These jobs can prepare the environment or handle setup tasks.
        :param stack_capabilities: (experimental) Optional capabilities that the stack should acknowledge during deployment. These capabilities are particularly relevant for stacks with IAM resources or macros.

        :stability: experimental
        '''
        if isinstance(git_hub_environment, dict):
            git_hub_environment = _github_actions_cdk_5328d874.Environment(**git_hub_environment)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd2f61903188a1fdb9485b8949b8c0f3fbe8dfc60b28fd63a493f3100e25dbc1)
            check_type(argname="argument git_hub_environment", value=git_hub_environment, expected_type=type_hints["git_hub_environment"])
            check_type(argname="argument post_jobs", value=post_jobs, expected_type=type_hints["post_jobs"])
            check_type(argname="argument pre_jobs", value=pre_jobs, expected_type=type_hints["pre_jobs"])
            check_type(argname="argument stack_capabilities", value=stack_capabilities, expected_type=type_hints["stack_capabilities"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if git_hub_environment is not None:
            self._values["git_hub_environment"] = git_hub_environment
        if post_jobs is not None:
            self._values["post_jobs"] = post_jobs
        if pre_jobs is not None:
            self._values["pre_jobs"] = pre_jobs
        if stack_capabilities is not None:
            self._values["stack_capabilities"] = stack_capabilities

    @builtins.property
    def git_hub_environment(
        self,
    ) -> typing.Optional[_github_actions_cdk_5328d874.Environment]:
        '''(experimental) Optional GitHub environment configuration for the stage.

        This configuration specifies the environment context in which the jobs will run.

        :stability: experimental
        '''
        result = self._values.get("git_hub_environment")
        return typing.cast(typing.Optional[_github_actions_cdk_5328d874.Environment], result)

    @builtins.property
    def post_jobs(self) -> typing.Optional[typing.List[StageJob]]:
        '''(experimental) Optional list of jobs to run after the main stage execution.

        These jobs can perform cleanup or other necessary tasks.

        :stability: experimental
        '''
        result = self._values.get("post_jobs")
        return typing.cast(typing.Optional[typing.List[StageJob]], result)

    @builtins.property
    def pre_jobs(self) -> typing.Optional[typing.List[StageJob]]:
        '''(experimental) Optional list of jobs to run before the main stage execution.

        These jobs can prepare the environment or handle setup tasks.

        :stability: experimental
        '''
        result = self._values.get("pre_jobs")
        return typing.cast(typing.Optional[typing.List[StageJob]], result)

    @builtins.property
    def stack_capabilities(self) -> typing.Optional[typing.List[StackCapabilities]]:
        '''(experimental) Optional capabilities that the stack should acknowledge during deployment.

        These capabilities are particularly relevant for stacks with IAM resources or macros.

        :stability: experimental
        '''
        result = self._values.get("stack_capabilities")
        return typing.cast(typing.Optional[typing.List[StackCapabilities]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StageOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StagePipelineJob(
    PipelineJob,
    metaclass=jsii.JSIIMeta,
    jsii_type="@github-actions-cdk/aws-cdk.StagePipelineJob",
):
    '''(experimental) A job that executes a specific phase of steps in the pipeline.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        phase: IJobPhase,
        aws_credentials: AwsCredentialsProvider,
        cdkout_dir: builtins.str,
        version_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        container: typing.Optional[typing.Union[_github_actions_cdk_5328d874.ContainerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        continue_on_error: typing.Optional[builtins.bool] = None,
        defaults: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Defaults, typing.Dict[builtins.str, typing.Any]]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        environment: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        needs: typing.Optional[typing.Sequence[builtins.str]] = None,
        outputs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        permissions: typing.Optional[typing.Union[typing.Union[_github_actions_cdk_5328d874.PermissionsEvent, typing.Dict[builtins.str, typing.Any]], builtins.str]] = None,
        required_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
        runner_labels: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
        runs_on: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
        services: typing.Optional[typing.Mapping[builtins.str, typing.Union[_github_actions_cdk_5328d874.ContainerOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        strategy: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Strategy, typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: Retrieves the unique identifier for the job.
        :param phase: (experimental) The phase that defines the steps to execute in this job.
        :param aws_credentials: (experimental) Provider for AWS credentials to be used within this job.
        :param cdkout_dir: (experimental) Directory path where CDK output files are located.
        :param version_overrides: (experimental) Optional version overrides for specific GitHub Actions.
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
            type_hints = typing.get_type_hints(_typecheckingstub__327c48fda1f490a47af4c0d4959f594802a797dfda71b2425d6753c6f58ce2c3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = StagePipelineJobProps(
            phase=phase,
            aws_credentials=aws_credentials,
            cdkout_dir=cdkout_dir,
            version_overrides=version_overrides,
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


@jsii.data_type(
    jsii_type="@github-actions-cdk/aws-cdk.StagePipelineJobProps",
    jsii_struct_bases=[PipelineJobProps],
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
        "aws_credentials": "awsCredentials",
        "cdkout_dir": "cdkoutDir",
        "version_overrides": "versionOverrides",
        "phase": "phase",
    },
)
class StagePipelineJobProps(PipelineJobProps):
    def __init__(
        self,
        *,
        container: typing.Optional[typing.Union[_github_actions_cdk_5328d874.ContainerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        continue_on_error: typing.Optional[builtins.bool] = None,
        defaults: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Defaults, typing.Dict[builtins.str, typing.Any]]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        environment: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        needs: typing.Optional[typing.Sequence[builtins.str]] = None,
        outputs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        permissions: typing.Optional[typing.Union[typing.Union[_github_actions_cdk_5328d874.PermissionsEvent, typing.Dict[builtins.str, typing.Any]], builtins.str]] = None,
        required_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
        runner_labels: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
        runs_on: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
        services: typing.Optional[typing.Mapping[builtins.str, typing.Union[_github_actions_cdk_5328d874.ContainerOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        strategy: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Strategy, typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_minutes: typing.Optional[jsii.Number] = None,
        aws_credentials: AwsCredentialsProvider,
        cdkout_dir: builtins.str,
        version_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        phase: IJobPhase,
    ) -> None:
        '''(experimental) Properties for a stage pipeline job.

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
        :param aws_credentials: (experimental) Provider for AWS credentials to be used within this job.
        :param cdkout_dir: (experimental) Directory path where CDK output files are located.
        :param version_overrides: (experimental) Optional version overrides for specific GitHub Actions.
        :param phase: (experimental) The phase that defines the steps to execute in this job.

        :stability: experimental
        '''
        if isinstance(container, dict):
            container = _github_actions_cdk_5328d874.ContainerOptions(**container)
        if isinstance(defaults, dict):
            defaults = _github_actions_cdk_5328d874.Defaults(**defaults)
        if isinstance(environment, dict):
            environment = _github_actions_cdk_5328d874.Environment(**environment)
        if isinstance(strategy, dict):
            strategy = _github_actions_cdk_5328d874.Strategy(**strategy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc68638ce4b20529ab7d8fb346be5b128762ccd6d962a792eafbefc3cd09a285)
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
            check_type(argname="argument aws_credentials", value=aws_credentials, expected_type=type_hints["aws_credentials"])
            check_type(argname="argument cdkout_dir", value=cdkout_dir, expected_type=type_hints["cdkout_dir"])
            check_type(argname="argument version_overrides", value=version_overrides, expected_type=type_hints["version_overrides"])
            check_type(argname="argument phase", value=phase, expected_type=type_hints["phase"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "aws_credentials": aws_credentials,
            "cdkout_dir": cdkout_dir,
            "phase": phase,
        }
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
        if version_overrides is not None:
            self._values["version_overrides"] = version_overrides

    @builtins.property
    def container(
        self,
    ) -> typing.Optional[_github_actions_cdk_5328d874.ContainerOptions]:
        '''(experimental) A container to run any steps in a job that don't already specify a container.

        If you have steps that use both script and container actions,
        the container actions will run as sibling containers on the same network
        with the same volume mounts.

        :stability: experimental
        '''
        result = self._values.get("container")
        return typing.cast(typing.Optional[_github_actions_cdk_5328d874.ContainerOptions], result)

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
    def defaults(self) -> typing.Optional[_github_actions_cdk_5328d874.Defaults]:
        '''(experimental) Default configuration settings for job steps.

        :stability: experimental
        '''
        result = self._values.get("defaults")
        return typing.cast(typing.Optional[_github_actions_cdk_5328d874.Defaults], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Environment variables for all steps in the job.

        :stability: experimental
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def environment(self) -> typing.Optional[_github_actions_cdk_5328d874.Environment]:
        '''(experimental) GitHub environment target for this job.

        :stability: experimental
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[_github_actions_cdk_5328d874.Environment], result)

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
    ) -> typing.Optional[typing.Union[_github_actions_cdk_5328d874.PermissionsEvent, builtins.str]]:
        '''(experimental) Permissions granted to the job.

        :stability: experimental
        '''
        result = self._values.get("permissions")
        return typing.cast(typing.Optional[typing.Union[_github_actions_cdk_5328d874.PermissionsEvent, builtins.str]], result)

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
    ) -> typing.Optional[typing.Mapping[builtins.str, _github_actions_cdk_5328d874.ContainerOptions]]:
        '''(experimental) Used to host service containers for a job in a workflow.

        Service
        containers are useful for creating databases or cache services like Redis.
        The runner automatically creates a Docker network and manages the life
        cycle of the service containers.

        :stability: experimental
        '''
        result = self._values.get("services")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _github_actions_cdk_5328d874.ContainerOptions]], result)

    @builtins.property
    def strategy(self) -> typing.Optional[_github_actions_cdk_5328d874.Strategy]:
        '''(experimental) Strategy settings, including matrix configuration and concurrency limits.

        :stability: experimental
        '''
        result = self._values.get("strategy")
        return typing.cast(typing.Optional[_github_actions_cdk_5328d874.Strategy], result)

    @builtins.property
    def timeout_minutes(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Timeout duration for the job, in minutes.

        :stability: experimental
        '''
        result = self._values.get("timeout_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def aws_credentials(self) -> AwsCredentialsProvider:
        '''(experimental) Provider for AWS credentials to be used within this job.

        :stability: experimental
        :remarks: This enables the job to authenticate and interact with AWS resources.
        '''
        result = self._values.get("aws_credentials")
        assert result is not None, "Required property 'aws_credentials' is missing"
        return typing.cast(AwsCredentialsProvider, result)

    @builtins.property
    def cdkout_dir(self) -> builtins.str:
        '''(experimental) Directory path where CDK output files are located.

        :stability: experimental
        :remarks:

        Specifies the folder that contains synthesized output files from AWS CDK. This path is used by the pipeline
        job to locate and utilize CDK artifacts in subsequent workflow steps.
        '''
        result = self._values.get("cdkout_dir")
        assert result is not None, "Required property 'cdkout_dir' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version_overrides(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Optional version overrides for specific GitHub Actions.

        :stability: experimental
        :remarks:

        Provides a way to specify custom versions (or SHA values) for GitHub Actions, allowing for precise control
        over which versions are used in the workflow.
        '''
        result = self._values.get("version_overrides")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def phase(self) -> IJobPhase:
        '''(experimental) The phase that defines the steps to execute in this job.

        :stability: experimental
        '''
        result = self._values.get("phase")
        assert result is not None, "Required property 'phase' is missing"
        return typing.cast(IJobPhase, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StagePipelineJobProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Synth(
    _aws_cdk_pipelines_ceddda9d.ShellStep,
    metaclass=jsii.JSIIMeta,
    jsii_type="@github-actions-cdk/aws-cdk.Synth",
):
    '''(experimental) Represents a Synth step in a GitHub Actions pipeline.

    This step is responsible for synthesizing the AWS CloudFormation templates
    from the CDK application. It extends the ShellStep to execute shell commands
    defined in the properties.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        commands: typing.Sequence[builtins.str],
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        install_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Constructs a new instance of the Synth step.

        :param commands: (experimental) The main commands to execute for the synth step. These commands typically include build or synthesis commands for the CDK application.
        :param env: (experimental) Optional environment variables to set during the step execution. These variables can be used to configure the behavior of the commands run in the synth step.
        :param install_commands: (experimental) Optional list of commands to run for installing dependencies before executing the main commands. Default: - No install commands will be executed.

        :stability: experimental
        '''
        props = SynthProps(
            commands=commands, env=env, install_commands=install_commands
        )

        jsii.create(self.__class__, self, [props])


class SynthPipelineJob(
    PipelineJob,
    metaclass=jsii.JSIIMeta,
    jsii_type="@github-actions-cdk/aws-cdk.SynthPipelineJob",
):
    '''(experimental) A job that synthesizes the CloudFormation template using CDK.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        commands: typing.Sequence[builtins.str],
        install_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
        post_build: typing.Optional[IJobPhase] = None,
        pre_build: typing.Optional[IJobPhase] = None,
        aws_credentials: AwsCredentialsProvider,
        cdkout_dir: builtins.str,
        version_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        container: typing.Optional[typing.Union[_github_actions_cdk_5328d874.ContainerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        continue_on_error: typing.Optional[builtins.bool] = None,
        defaults: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Defaults, typing.Dict[builtins.str, typing.Any]]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        environment: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        needs: typing.Optional[typing.Sequence[builtins.str]] = None,
        outputs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        permissions: typing.Optional[typing.Union[typing.Union[_github_actions_cdk_5328d874.PermissionsEvent, typing.Dict[builtins.str, typing.Any]], builtins.str]] = None,
        required_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
        runner_labels: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
        runs_on: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
        services: typing.Optional[typing.Mapping[builtins.str, typing.Union[_github_actions_cdk_5328d874.ContainerOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        strategy: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Strategy, typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: Retrieves the unique identifier for the job.
        :param commands: (experimental) Commands to run for the build.
        :param install_commands: (experimental) Commands to run for installation before the build.
        :param post_build: (experimental) Optional post-build phase steps.
        :param pre_build: (experimental) Optional pre-build phase steps.
        :param aws_credentials: (experimental) Provider for AWS credentials to be used within this job.
        :param cdkout_dir: (experimental) Directory path where CDK output files are located.
        :param version_overrides: (experimental) Optional version overrides for specific GitHub Actions.
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
            type_hints = typing.get_type_hints(_typecheckingstub__db03dbc629da621d6e04dbe8c8870b89102cebb5a7ecb6360a3ab6d2a0df928b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SynthPipelineJobProps(
            commands=commands,
            install_commands=install_commands,
            post_build=post_build,
            pre_build=pre_build,
            aws_credentials=aws_credentials,
            cdkout_dir=cdkout_dir,
            version_overrides=version_overrides,
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


@jsii.data_type(
    jsii_type="@github-actions-cdk/aws-cdk.SynthPipelineJobProps",
    jsii_struct_bases=[PipelineJobProps],
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
        "aws_credentials": "awsCredentials",
        "cdkout_dir": "cdkoutDir",
        "version_overrides": "versionOverrides",
        "commands": "commands",
        "install_commands": "installCommands",
        "post_build": "postBuild",
        "pre_build": "preBuild",
    },
)
class SynthPipelineJobProps(PipelineJobProps):
    def __init__(
        self,
        *,
        container: typing.Optional[typing.Union[_github_actions_cdk_5328d874.ContainerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        continue_on_error: typing.Optional[builtins.bool] = None,
        defaults: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Defaults, typing.Dict[builtins.str, typing.Any]]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        environment: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        needs: typing.Optional[typing.Sequence[builtins.str]] = None,
        outputs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        permissions: typing.Optional[typing.Union[typing.Union[_github_actions_cdk_5328d874.PermissionsEvent, typing.Dict[builtins.str, typing.Any]], builtins.str]] = None,
        required_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
        runner_labels: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
        runs_on: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
        services: typing.Optional[typing.Mapping[builtins.str, typing.Union[_github_actions_cdk_5328d874.ContainerOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        strategy: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Strategy, typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_minutes: typing.Optional[jsii.Number] = None,
        aws_credentials: AwsCredentialsProvider,
        cdkout_dir: builtins.str,
        version_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        commands: typing.Sequence[builtins.str],
        install_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
        post_build: typing.Optional[IJobPhase] = None,
        pre_build: typing.Optional[IJobPhase] = None,
    ) -> None:
        '''(experimental) Properties for a synthetic pipeline job, including build phases and commands.

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
        :param aws_credentials: (experimental) Provider for AWS credentials to be used within this job.
        :param cdkout_dir: (experimental) Directory path where CDK output files are located.
        :param version_overrides: (experimental) Optional version overrides for specific GitHub Actions.
        :param commands: (experimental) Commands to run for the build.
        :param install_commands: (experimental) Commands to run for installation before the build.
        :param post_build: (experimental) Optional post-build phase steps.
        :param pre_build: (experimental) Optional pre-build phase steps.

        :stability: experimental
        '''
        if isinstance(container, dict):
            container = _github_actions_cdk_5328d874.ContainerOptions(**container)
        if isinstance(defaults, dict):
            defaults = _github_actions_cdk_5328d874.Defaults(**defaults)
        if isinstance(environment, dict):
            environment = _github_actions_cdk_5328d874.Environment(**environment)
        if isinstance(strategy, dict):
            strategy = _github_actions_cdk_5328d874.Strategy(**strategy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85f01c48664e0e50639c9427e58f78884676d5e4a19d663473644eb3b68308e4)
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
            check_type(argname="argument aws_credentials", value=aws_credentials, expected_type=type_hints["aws_credentials"])
            check_type(argname="argument cdkout_dir", value=cdkout_dir, expected_type=type_hints["cdkout_dir"])
            check_type(argname="argument version_overrides", value=version_overrides, expected_type=type_hints["version_overrides"])
            check_type(argname="argument commands", value=commands, expected_type=type_hints["commands"])
            check_type(argname="argument install_commands", value=install_commands, expected_type=type_hints["install_commands"])
            check_type(argname="argument post_build", value=post_build, expected_type=type_hints["post_build"])
            check_type(argname="argument pre_build", value=pre_build, expected_type=type_hints["pre_build"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "aws_credentials": aws_credentials,
            "cdkout_dir": cdkout_dir,
            "commands": commands,
        }
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
        if version_overrides is not None:
            self._values["version_overrides"] = version_overrides
        if install_commands is not None:
            self._values["install_commands"] = install_commands
        if post_build is not None:
            self._values["post_build"] = post_build
        if pre_build is not None:
            self._values["pre_build"] = pre_build

    @builtins.property
    def container(
        self,
    ) -> typing.Optional[_github_actions_cdk_5328d874.ContainerOptions]:
        '''(experimental) A container to run any steps in a job that don't already specify a container.

        If you have steps that use both script and container actions,
        the container actions will run as sibling containers on the same network
        with the same volume mounts.

        :stability: experimental
        '''
        result = self._values.get("container")
        return typing.cast(typing.Optional[_github_actions_cdk_5328d874.ContainerOptions], result)

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
    def defaults(self) -> typing.Optional[_github_actions_cdk_5328d874.Defaults]:
        '''(experimental) Default configuration settings for job steps.

        :stability: experimental
        '''
        result = self._values.get("defaults")
        return typing.cast(typing.Optional[_github_actions_cdk_5328d874.Defaults], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Environment variables for all steps in the job.

        :stability: experimental
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def environment(self) -> typing.Optional[_github_actions_cdk_5328d874.Environment]:
        '''(experimental) GitHub environment target for this job.

        :stability: experimental
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[_github_actions_cdk_5328d874.Environment], result)

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
    ) -> typing.Optional[typing.Union[_github_actions_cdk_5328d874.PermissionsEvent, builtins.str]]:
        '''(experimental) Permissions granted to the job.

        :stability: experimental
        '''
        result = self._values.get("permissions")
        return typing.cast(typing.Optional[typing.Union[_github_actions_cdk_5328d874.PermissionsEvent, builtins.str]], result)

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
    ) -> typing.Optional[typing.Mapping[builtins.str, _github_actions_cdk_5328d874.ContainerOptions]]:
        '''(experimental) Used to host service containers for a job in a workflow.

        Service
        containers are useful for creating databases or cache services like Redis.
        The runner automatically creates a Docker network and manages the life
        cycle of the service containers.

        :stability: experimental
        '''
        result = self._values.get("services")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _github_actions_cdk_5328d874.ContainerOptions]], result)

    @builtins.property
    def strategy(self) -> typing.Optional[_github_actions_cdk_5328d874.Strategy]:
        '''(experimental) Strategy settings, including matrix configuration and concurrency limits.

        :stability: experimental
        '''
        result = self._values.get("strategy")
        return typing.cast(typing.Optional[_github_actions_cdk_5328d874.Strategy], result)

    @builtins.property
    def timeout_minutes(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Timeout duration for the job, in minutes.

        :stability: experimental
        '''
        result = self._values.get("timeout_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def aws_credentials(self) -> AwsCredentialsProvider:
        '''(experimental) Provider for AWS credentials to be used within this job.

        :stability: experimental
        :remarks: This enables the job to authenticate and interact with AWS resources.
        '''
        result = self._values.get("aws_credentials")
        assert result is not None, "Required property 'aws_credentials' is missing"
        return typing.cast(AwsCredentialsProvider, result)

    @builtins.property
    def cdkout_dir(self) -> builtins.str:
        '''(experimental) Directory path where CDK output files are located.

        :stability: experimental
        :remarks:

        Specifies the folder that contains synthesized output files from AWS CDK. This path is used by the pipeline
        job to locate and utilize CDK artifacts in subsequent workflow steps.
        '''
        result = self._values.get("cdkout_dir")
        assert result is not None, "Required property 'cdkout_dir' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version_overrides(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Optional version overrides for specific GitHub Actions.

        :stability: experimental
        :remarks:

        Provides a way to specify custom versions (or SHA values) for GitHub Actions, allowing for precise control
        over which versions are used in the workflow.
        '''
        result = self._values.get("version_overrides")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def commands(self) -> typing.List[builtins.str]:
        '''(experimental) Commands to run for the build.

        :stability: experimental
        '''
        result = self._values.get("commands")
        assert result is not None, "Required property 'commands' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def install_commands(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Commands to run for installation before the build.

        :stability: experimental
        '''
        result = self._values.get("install_commands")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def post_build(self) -> typing.Optional[IJobPhase]:
        '''(experimental) Optional post-build phase steps.

        :stability: experimental
        '''
        result = self._values.get("post_build")
        return typing.cast(typing.Optional[IJobPhase], result)

    @builtins.property
    def pre_build(self) -> typing.Optional[IJobPhase]:
        '''(experimental) Optional pre-build phase steps.

        :stability: experimental
        '''
        result = self._values.get("pre_build")
        return typing.cast(typing.Optional[IJobPhase], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SynthPipelineJobProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@github-actions-cdk/aws-cdk.SynthProps",
    jsii_struct_bases=[],
    name_mapping={
        "commands": "commands",
        "env": "env",
        "install_commands": "installCommands",
    },
)
class SynthProps:
    def __init__(
        self,
        *,
        commands: typing.Sequence[builtins.str],
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        install_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Properties for configuring a Synth step in the GitHub Actions pipeline.

        :param commands: (experimental) The main commands to execute for the synth step. These commands typically include build or synthesis commands for the CDK application.
        :param env: (experimental) Optional environment variables to set during the step execution. These variables can be used to configure the behavior of the commands run in the synth step.
        :param install_commands: (experimental) Optional list of commands to run for installing dependencies before executing the main commands. Default: - No install commands will be executed.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffd19534aa0aef691c79e308f97a51cf85d74e5c66b39fb4559d18e51d01c654)
            check_type(argname="argument commands", value=commands, expected_type=type_hints["commands"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument install_commands", value=install_commands, expected_type=type_hints["install_commands"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "commands": commands,
        }
        if env is not None:
            self._values["env"] = env
        if install_commands is not None:
            self._values["install_commands"] = install_commands

    @builtins.property
    def commands(self) -> typing.List[builtins.str]:
        '''(experimental) The main commands to execute for the synth step.

        These commands typically include build or synthesis commands for the CDK application.

        :stability: experimental
        '''
        result = self._values.get("commands")
        assert result is not None, "Required property 'commands' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Optional environment variables to set during the step execution.

        These variables can be used to configure the behavior of the commands run in the synth step.

        :stability: experimental
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def install_commands(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Optional list of commands to run for installing dependencies before executing the main commands.

        :default: - No install commands will be executed.

        :stability: experimental
        '''
        result = self._values.get("install_commands")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SynthProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@github-actions-cdk/aws-cdk.WaveOptions",
    jsii_struct_bases=[],
    name_mapping={"post_jobs": "postJobs", "pre_jobs": "preJobs"},
)
class WaveOptions:
    def __init__(
        self,
        *,
        post_jobs: typing.Optional[typing.Sequence[StageJob]] = None,
        pre_jobs: typing.Optional[typing.Sequence[StageJob]] = None,
    ) -> None:
        '''(experimental) Options for configuring a wave in the GitHub Actions pipeline.

        :param post_jobs: (experimental) Optional list of jobs to run after all stages in the wave. This can be useful for cleanup or finalization tasks that should occur after all stages have completed.
        :param pre_jobs: (experimental) Optional list of jobs to run before any stages in the wave. This allows for preparatory tasks or environment setup for the entire wave.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb4cb59421d9014e33af6f3971bffa61839881acb86b0277612f2d5abd3c6728)
            check_type(argname="argument post_jobs", value=post_jobs, expected_type=type_hints["post_jobs"])
            check_type(argname="argument pre_jobs", value=pre_jobs, expected_type=type_hints["pre_jobs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if post_jobs is not None:
            self._values["post_jobs"] = post_jobs
        if pre_jobs is not None:
            self._values["pre_jobs"] = pre_jobs

    @builtins.property
    def post_jobs(self) -> typing.Optional[typing.List[StageJob]]:
        '''(experimental) Optional list of jobs to run after all stages in the wave.

        This can be useful for cleanup or finalization tasks that should occur
        after all stages have completed.

        :stability: experimental
        '''
        result = self._values.get("post_jobs")
        return typing.cast(typing.Optional[typing.List[StageJob]], result)

    @builtins.property
    def pre_jobs(self) -> typing.Optional[typing.List[StageJob]]:
        '''(experimental) Optional list of jobs to run before any stages in the wave.

        This allows for preparatory tasks or environment setup for the entire wave.

        :stability: experimental
        '''
        result = self._values.get("pre_jobs")
        return typing.cast(typing.Optional[typing.List[StageJob]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WaveOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DeployPipelineJob(
    PipelineJob,
    metaclass=jsii.JSIIMeta,
    jsii_type="@github-actions-cdk/aws-cdk.DeployPipelineJob",
):
    '''(experimental) A job that deploys a CloudFormation stack.

    :stability: experimental
    :remarks:

    The ``DeployPipelineJob`` class is responsible for executing the deployment of a
    specified CloudFormation stack. It integrates with AWS credentials for authentication
    and ensures that the stack is deployed with the correct template and asset replacements.
    The job will throw errors if required properties are not provided, ensuring
    robustness in the deployment process.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        asset_hash_map: typing.Mapping[builtins.str, builtins.str],
        stack: _aws_cdk_pipelines_ceddda9d.StackDeployment,
        stack_options: typing.Optional[typing.Union[StackOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        aws_credentials: AwsCredentialsProvider,
        cdkout_dir: builtins.str,
        version_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        container: typing.Optional[typing.Union[_github_actions_cdk_5328d874.ContainerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        continue_on_error: typing.Optional[builtins.bool] = None,
        defaults: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Defaults, typing.Dict[builtins.str, typing.Any]]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        environment: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        needs: typing.Optional[typing.Sequence[builtins.str]] = None,
        outputs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        permissions: typing.Optional[typing.Union[typing.Union[_github_actions_cdk_5328d874.PermissionsEvent, typing.Dict[builtins.str, typing.Any]], builtins.str]] = None,
        required_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
        runner_labels: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
        runs_on: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
        services: typing.Optional[typing.Mapping[builtins.str, typing.Union[_github_actions_cdk_5328d874.ContainerOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        strategy: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Strategy, typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Constructs a new instance of ``DeployPipelineJob``.

        :param scope: - The parent construct scope.
        :param id: - Unique identifier for this deployment job.
        :param asset_hash_map: (experimental) A mapping of asset identifiers to their corresponding output expressions.
        :param stack: (experimental) The stack to be deployed.
        :param stack_options: (experimental) Optional stack-specific options.
        :param aws_credentials: (experimental) Provider for AWS credentials to be used within this job.
        :param cdkout_dir: (experimental) Directory path where CDK output files are located.
        :param version_overrides: (experimental) Optional version overrides for specific GitHub Actions.
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
        :remarks:

        The constructor validates required properties for the stack and sets up the
        necessary steps to deploy the CloudFormation stack using the provided asset hash
        mappings and options. It initializes the deployment action with AWS CloudFormation.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc04c3a48e0c57481a53cb8f8e54b10f287a5b85f6b43d0cf8567fcbc230aefa)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DeployPipelineJobProps(
            asset_hash_map=asset_hash_map,
            stack=stack,
            stack_options=stack_options,
            aws_credentials=aws_credentials,
            cdkout_dir=cdkout_dir,
            version_overrides=version_overrides,
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


@jsii.data_type(
    jsii_type="@github-actions-cdk/aws-cdk.DeployPipelineJobProps",
    jsii_struct_bases=[PipelineJobProps],
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
        "aws_credentials": "awsCredentials",
        "cdkout_dir": "cdkoutDir",
        "version_overrides": "versionOverrides",
        "asset_hash_map": "assetHashMap",
        "stack": "stack",
        "stack_options": "stackOptions",
    },
)
class DeployPipelineJobProps(PipelineJobProps):
    def __init__(
        self,
        *,
        container: typing.Optional[typing.Union[_github_actions_cdk_5328d874.ContainerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        continue_on_error: typing.Optional[builtins.bool] = None,
        defaults: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Defaults, typing.Dict[builtins.str, typing.Any]]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        environment: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        needs: typing.Optional[typing.Sequence[builtins.str]] = None,
        outputs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        permissions: typing.Optional[typing.Union[typing.Union[_github_actions_cdk_5328d874.PermissionsEvent, typing.Dict[builtins.str, typing.Any]], builtins.str]] = None,
        required_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
        runner_labels: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
        runs_on: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
        services: typing.Optional[typing.Mapping[builtins.str, typing.Union[_github_actions_cdk_5328d874.ContainerOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        strategy: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Strategy, typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_minutes: typing.Optional[jsii.Number] = None,
        aws_credentials: AwsCredentialsProvider,
        cdkout_dir: builtins.str,
        version_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        asset_hash_map: typing.Mapping[builtins.str, builtins.str],
        stack: _aws_cdk_pipelines_ceddda9d.StackDeployment,
        stack_options: typing.Optional[typing.Union[StackOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Properties for a deployment pipeline job.

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
        :param aws_credentials: (experimental) Provider for AWS credentials to be used within this job.
        :param cdkout_dir: (experimental) Directory path where CDK output files are located.
        :param version_overrides: (experimental) Optional version overrides for specific GitHub Actions.
        :param asset_hash_map: (experimental) A mapping of asset identifiers to their corresponding output expressions.
        :param stack: (experimental) The stack to be deployed.
        :param stack_options: (experimental) Optional stack-specific options.

        :stability: experimental
        :remarks:

        This interface defines the configuration options required for a deployment job
        in the pipeline. It includes the CloudFormation stack to be deployed, a mapping
        of asset hashes for use in the stack template, and optional stack-specific options.
        '''
        if isinstance(container, dict):
            container = _github_actions_cdk_5328d874.ContainerOptions(**container)
        if isinstance(defaults, dict):
            defaults = _github_actions_cdk_5328d874.Defaults(**defaults)
        if isinstance(environment, dict):
            environment = _github_actions_cdk_5328d874.Environment(**environment)
        if isinstance(strategy, dict):
            strategy = _github_actions_cdk_5328d874.Strategy(**strategy)
        if isinstance(stack_options, dict):
            stack_options = StackOptions(**stack_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a34fdc24473a47a37196aabb89fd535118ac3cc6f156d2303f43c602c9c8c39)
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
            check_type(argname="argument aws_credentials", value=aws_credentials, expected_type=type_hints["aws_credentials"])
            check_type(argname="argument cdkout_dir", value=cdkout_dir, expected_type=type_hints["cdkout_dir"])
            check_type(argname="argument version_overrides", value=version_overrides, expected_type=type_hints["version_overrides"])
            check_type(argname="argument asset_hash_map", value=asset_hash_map, expected_type=type_hints["asset_hash_map"])
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
            check_type(argname="argument stack_options", value=stack_options, expected_type=type_hints["stack_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "aws_credentials": aws_credentials,
            "cdkout_dir": cdkout_dir,
            "asset_hash_map": asset_hash_map,
            "stack": stack,
        }
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
        if version_overrides is not None:
            self._values["version_overrides"] = version_overrides
        if stack_options is not None:
            self._values["stack_options"] = stack_options

    @builtins.property
    def container(
        self,
    ) -> typing.Optional[_github_actions_cdk_5328d874.ContainerOptions]:
        '''(experimental) A container to run any steps in a job that don't already specify a container.

        If you have steps that use both script and container actions,
        the container actions will run as sibling containers on the same network
        with the same volume mounts.

        :stability: experimental
        '''
        result = self._values.get("container")
        return typing.cast(typing.Optional[_github_actions_cdk_5328d874.ContainerOptions], result)

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
    def defaults(self) -> typing.Optional[_github_actions_cdk_5328d874.Defaults]:
        '''(experimental) Default configuration settings for job steps.

        :stability: experimental
        '''
        result = self._values.get("defaults")
        return typing.cast(typing.Optional[_github_actions_cdk_5328d874.Defaults], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Environment variables for all steps in the job.

        :stability: experimental
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def environment(self) -> typing.Optional[_github_actions_cdk_5328d874.Environment]:
        '''(experimental) GitHub environment target for this job.

        :stability: experimental
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[_github_actions_cdk_5328d874.Environment], result)

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
    ) -> typing.Optional[typing.Union[_github_actions_cdk_5328d874.PermissionsEvent, builtins.str]]:
        '''(experimental) Permissions granted to the job.

        :stability: experimental
        '''
        result = self._values.get("permissions")
        return typing.cast(typing.Optional[typing.Union[_github_actions_cdk_5328d874.PermissionsEvent, builtins.str]], result)

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
    ) -> typing.Optional[typing.Mapping[builtins.str, _github_actions_cdk_5328d874.ContainerOptions]]:
        '''(experimental) Used to host service containers for a job in a workflow.

        Service
        containers are useful for creating databases or cache services like Redis.
        The runner automatically creates a Docker network and manages the life
        cycle of the service containers.

        :stability: experimental
        '''
        result = self._values.get("services")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _github_actions_cdk_5328d874.ContainerOptions]], result)

    @builtins.property
    def strategy(self) -> typing.Optional[_github_actions_cdk_5328d874.Strategy]:
        '''(experimental) Strategy settings, including matrix configuration and concurrency limits.

        :stability: experimental
        '''
        result = self._values.get("strategy")
        return typing.cast(typing.Optional[_github_actions_cdk_5328d874.Strategy], result)

    @builtins.property
    def timeout_minutes(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Timeout duration for the job, in minutes.

        :stability: experimental
        '''
        result = self._values.get("timeout_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def aws_credentials(self) -> AwsCredentialsProvider:
        '''(experimental) Provider for AWS credentials to be used within this job.

        :stability: experimental
        :remarks: This enables the job to authenticate and interact with AWS resources.
        '''
        result = self._values.get("aws_credentials")
        assert result is not None, "Required property 'aws_credentials' is missing"
        return typing.cast(AwsCredentialsProvider, result)

    @builtins.property
    def cdkout_dir(self) -> builtins.str:
        '''(experimental) Directory path where CDK output files are located.

        :stability: experimental
        :remarks:

        Specifies the folder that contains synthesized output files from AWS CDK. This path is used by the pipeline
        job to locate and utilize CDK artifacts in subsequent workflow steps.
        '''
        result = self._values.get("cdkout_dir")
        assert result is not None, "Required property 'cdkout_dir' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version_overrides(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Optional version overrides for specific GitHub Actions.

        :stability: experimental
        :remarks:

        Provides a way to specify custom versions (or SHA values) for GitHub Actions, allowing for precise control
        over which versions are used in the workflow.
        '''
        result = self._values.get("version_overrides")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def asset_hash_map(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''(experimental) A mapping of asset identifiers to their corresponding output expressions.

        :stability: experimental
        :remarks:

        This map is used to replace asset hash placeholders in the CloudFormation template
        with the actual asset values at deployment time. The keys are asset identifiers,
        and the values are the output expressions derived from the publishing steps.
        '''
        result = self._values.get("asset_hash_map")
        assert result is not None, "Required property 'asset_hash_map' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    @builtins.property
    def stack(self) -> _aws_cdk_pipelines_ceddda9d.StackDeployment:
        '''(experimental) The stack to be deployed.

        :stability: experimental
        :remarks:

        This property represents the ``StackDeployment`` object which contains metadata
        about the CloudFormation stack. It must specify properties such as the stack name,
        region, and the URL of the CloudFormation template to be used for deployment.
        '''
        result = self._values.get("stack")
        assert result is not None, "Required property 'stack' is missing"
        return typing.cast(_aws_cdk_pipelines_ceddda9d.StackDeployment, result)

    @builtins.property
    def stack_options(self) -> typing.Optional[StackOptions]:
        '''(experimental) Optional stack-specific options.

        :stability: experimental
        :remarks:

        These options can include capabilities, tags, and other settings specific to
        the deployment of the stack. Providing these options allows for customization
        of the deployment process, such as enabling IAM capabilities or specifying tags.
        '''
        result = self._values.get("stack_options")
        return typing.cast(typing.Optional[StackOptions], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeployPipelineJobProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AwsCdkAdapter",
    "AwsCredentials",
    "AwsCredentialsProvider",
    "DeployPipelineJob",
    "DeployPipelineJobProps",
    "GitHubActionsOpenIdConnectProvider",
    "GitHubActionsOpenIdConnectProviderProps",
    "GitHubActionsPipeline",
    "GitHubActionsPipelineProps",
    "GitHubActionsRole",
    "GitHubActionsRoleArn",
    "GitHubActionsRoleProps",
    "GitHubSecretsProviderProps",
    "GitHubWave",
    "IJobPhase",
    "IStageJobOptions",
    "IWaveStageAdder",
    "OpenIdConnectProviderProps",
    "PipelineJob",
    "PipelineJobProps",
    "PipelineWorkflow",
    "PipelineWorkflowProps",
    "PublishPipelineJob",
    "PublishPipelineJobProps",
    "StackCapabilities",
    "StackOptions",
    "StageJob",
    "StageOptions",
    "StagePipelineJob",
    "StagePipelineJobProps",
    "Synth",
    "SynthPipelineJob",
    "SynthPipelineJobProps",
    "SynthProps",
    "WaveOptions",
]

publication.publish()

def _typecheckingstub__9625a39d38e5f209abdb7662dd5eedae25c0e5d8e76f70714e4d40cb23db1007(
    aws_cdk_scope: _constructs_77d1e7e8.Construct,
    *,
    additional_checks: typing.Optional[builtins.bool] = None,
    continue_on_error_annotations: typing.Optional[builtins.bool] = None,
    outdir: typing.Optional[builtins.str] = None,
    skip_validation: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28fbdf0ace5064cb48481e60cbf4c8ab332ac37d0ab38ddeeeb6f0e81a4ee704(
    error: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3989ae456ab07886845ef790414c195483d97f4bf4b555588b1b7131d01a30f2(
    job: _github_actions_cdk_5328d874.Job,
    region: builtins.str,
    assume_role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28884f9a6760c9ce8250d1ffb6d95ef6f49a2cb27284940e17468e9049473ac7(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    thumbprints: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61b3a88322723cd90fe1abfc29c6f24564ad07a5b6c00c29d0e42b1ddecaf436(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7543176371b9644ce378e7f7db82027af30d0eddb1835e8aebcfcd9a8fbaef30(
    *,
    thumbprints: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96fcd40eb072e8c0530c8c54766297ac99a2b7b419e4e8b2e613d60d866dd0a9(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    aws_credentials: AwsCredentialsProvider,
    synth: Synth,
    post_build: typing.Optional[IJobPhase] = None,
    pre_build: typing.Optional[IJobPhase] = None,
    single_publisher_per_asset_type: typing.Optional[builtins.bool] = None,
    version_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    workflow_env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    workflow_filename: typing.Optional[builtins.str] = None,
    workflow_name: typing.Optional[builtins.str] = None,
    workflow_outdir: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89ab5e8eaef92c0d10c05fb4cc4c421c9eae63fb62e4d1a7e272d176d8a7d9d3(
    stage: _aws_cdk_ceddda9d.Stage,
    *,
    git_hub_environment: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
    post_jobs: typing.Optional[typing.Sequence[StageJob]] = None,
    pre_jobs: typing.Optional[typing.Sequence[StageJob]] = None,
    stack_capabilities: typing.Optional[typing.Sequence[StackCapabilities]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a737c584d1136e2411d6dfa2c83f7db9beb11b36eae8e4bd153734536de4b73(
    id: builtins.str,
    *,
    post_jobs: typing.Optional[typing.Sequence[StageJob]] = None,
    pre_jobs: typing.Optional[typing.Sequence[StageJob]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27649c8ad4ab55b72c155b45a971e424248d7098e0b389f6e2885320c401c388(
    *,
    aws_credentials: AwsCredentialsProvider,
    synth: Synth,
    post_build: typing.Optional[IJobPhase] = None,
    pre_build: typing.Optional[IJobPhase] = None,
    single_publisher_per_asset_type: typing.Optional[builtins.bool] = None,
    version_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    workflow_env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    workflow_filename: typing.Optional[builtins.str] = None,
    workflow_name: typing.Optional[builtins.str] = None,
    workflow_outdir: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d00bdbd3fd92f21748337063ff3f61dcfa08621b09dfebc9cafac8d3ce583503(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    provider: _aws_cdk_aws_iam_ceddda9d.IOpenIdConnectProvider,
    repos: typing.Optional[typing.Sequence[builtins.str]] = None,
    role_name: typing.Optional[builtins.str] = None,
    subject_claims: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b111a2b07706fe91b3329a040650d384c1bb9ceddc1cebac1fd6349d873e84b9(
    account_id: builtins.str,
    role_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__561aa80ba2071f8035e588f52b4c2478bfc7397203e23ba0bf6858136a68e60d(
    *,
    provider: _aws_cdk_aws_iam_ceddda9d.IOpenIdConnectProvider,
    repos: typing.Optional[typing.Sequence[builtins.str]] = None,
    role_name: typing.Optional[builtins.str] = None,
    subject_claims: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32b8bf3d5dc2ad82ec42e5edb11e84ec37b8764bc0f97d631224d4ce13de8d7a(
    *,
    access_key_id: builtins.str,
    secret_access_key: builtins.str,
    session_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93ab778c5ce108a8bc9b72ebc9e8e66e869734e0a86a57246522989522bbcd97(
    id: builtins.str,
    wave_stage_adder: IWaveStageAdder,
    *,
    post: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.Step]] = None,
    pre: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.Step]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ee7f04229445b2055a0617e3b09015b1ff1425e9bbfae250e48d9ca5c59c4cb(
    stage: _aws_cdk_ceddda9d.Stage,
    *,
    git_hub_environment: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
    post_jobs: typing.Optional[typing.Sequence[StageJob]] = None,
    pre_jobs: typing.Optional[typing.Sequence[StageJob]] = None,
    stack_capabilities: typing.Optional[typing.Sequence[StackCapabilities]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ead53d1c4c954d13546340faf629f1a4478781acb18a0c3c0e6513d26daa9e8(
    job: PipelineJob,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8584c189be576e1cd8125bdbf6d2ca5571be42084577864870c7d6cdb216300(
    stage_deployment: _aws_cdk_pipelines_ceddda9d.StageDeployment,
    *,
    git_hub_environment: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
    post_jobs: typing.Optional[typing.Sequence[StageJob]] = None,
    pre_jobs: typing.Optional[typing.Sequence[StageJob]] = None,
    stack_capabilities: typing.Optional[typing.Sequence[StackCapabilities]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28c8df414e643b7f1c0e52605e917a8fd26640b62bec595734d57faaf0236f75(
    *,
    git_hub_actions_role_arn: builtins.str,
    role_session_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0a1b56d71fea410fac564beb0d9f7eefec6642781632cddad618cdcfe638a48(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    aws_credentials: AwsCredentialsProvider,
    cdkout_dir: builtins.str,
    version_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    container: typing.Optional[typing.Union[_github_actions_cdk_5328d874.ContainerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    continue_on_error: typing.Optional[builtins.bool] = None,
    defaults: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Defaults, typing.Dict[builtins.str, typing.Any]]] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    environment: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    needs: typing.Optional[typing.Sequence[builtins.str]] = None,
    outputs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    permissions: typing.Optional[typing.Union[typing.Union[_github_actions_cdk_5328d874.PermissionsEvent, typing.Dict[builtins.str, typing.Any]], builtins.str]] = None,
    required_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
    runner_labels: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
    runs_on: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
    services: typing.Optional[typing.Mapping[builtins.str, typing.Union[_github_actions_cdk_5328d874.ContainerOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    strategy: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Strategy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2873fe2e3b952f8b3cb820a2ee5469748a397d1635469c974d4bd18b0f704c68(
    action_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8217b395daebe0e7a395128c1609592bee8af021b8216b27d66bc65daee5596(
    *,
    container: typing.Optional[typing.Union[_github_actions_cdk_5328d874.ContainerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    continue_on_error: typing.Optional[builtins.bool] = None,
    defaults: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Defaults, typing.Dict[builtins.str, typing.Any]]] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    environment: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    needs: typing.Optional[typing.Sequence[builtins.str]] = None,
    outputs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    permissions: typing.Optional[typing.Union[typing.Union[_github_actions_cdk_5328d874.PermissionsEvent, typing.Dict[builtins.str, typing.Any]], builtins.str]] = None,
    required_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
    runner_labels: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
    runs_on: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
    services: typing.Optional[typing.Mapping[builtins.str, typing.Union[_github_actions_cdk_5328d874.ContainerOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    strategy: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Strategy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_minutes: typing.Optional[jsii.Number] = None,
    aws_credentials: AwsCredentialsProvider,
    cdkout_dir: builtins.str,
    version_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__636c480c4cb48ef189ebd2ce3ba795a9cb75b585ca1454a679f50fd5c97a0860(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    aws_credentials: AwsCredentialsProvider,
    cdkout_dir: builtins.str,
    pipeline: _aws_cdk_pipelines_ceddda9d.PipelineBase,
    stack_options: typing.Mapping[builtins.str, typing.Union[StackOptions, typing.Dict[builtins.str, typing.Any]]],
    post_build: typing.Optional[IJobPhase] = None,
    pre_build: typing.Optional[IJobPhase] = None,
    single_publisher_per_asset_type: typing.Optional[builtins.bool] = None,
    version_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    comment_at_top: typing.Optional[builtins.str] = None,
    concurrency: typing.Optional[typing.Union[_github_actions_cdk_5328d874.ConcurrencyOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    defaults: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Defaults, typing.Dict[builtins.str, typing.Any]]] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    permissions: typing.Optional[typing.Union[typing.Union[_github_actions_cdk_5328d874.PermissionsEvent, typing.Dict[builtins.str, typing.Any]], builtins.str]] = None,
    run_name: typing.Optional[builtins.str] = None,
    synthesizer: typing.Optional[_github_actions_cdk_5328d874.IWorkflowSynthesizer] = None,
    triggers: typing.Optional[typing.Union[_github_actions_cdk_5328d874.WorkflowTriggers, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__797dac26a066a8ec56c185ada275b2cd85824838cdae521c876c628102574cc4(
    id: builtins.str,
    needs: typing.Sequence[builtins.str],
    stack: _aws_cdk_pipelines_ceddda9d.StackDeployment,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fb9b17aa49b07b12d5403e6eea5120e283d94984ac11f25c8ca90b9b0c7ca10(
    id: builtins.str,
    needs: typing.Sequence[builtins.str],
    assets: typing.Sequence[typing.Union[_aws_cdk_pipelines_ceddda9d.StackAsset, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f667bc728647daae0bc3e038e48953f906a5a9770f1a80884f0cfa8ae5d887e(
    id: builtins.str,
    needs: typing.Sequence[builtins.str],
    job: StageJob,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee60549ea66f57d360fb786684c7d896f8430d32ce57cbe8e14d5feea5b43c3c(
    id: builtins.str,
    needs: typing.Sequence[builtins.str],
    synth: Synth,
    pre_build: typing.Optional[IJobPhase] = None,
    post_build: typing.Optional[IJobPhase] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd66f4263f804ebdde225a8646d12b8b07b3893a0d7565be96d9dfa6869f63dc(
    *,
    comment_at_top: typing.Optional[builtins.str] = None,
    concurrency: typing.Optional[typing.Union[_github_actions_cdk_5328d874.ConcurrencyOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    defaults: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Defaults, typing.Dict[builtins.str, typing.Any]]] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    permissions: typing.Optional[typing.Union[typing.Union[_github_actions_cdk_5328d874.PermissionsEvent, typing.Dict[builtins.str, typing.Any]], builtins.str]] = None,
    run_name: typing.Optional[builtins.str] = None,
    synthesizer: typing.Optional[_github_actions_cdk_5328d874.IWorkflowSynthesizer] = None,
    triggers: typing.Optional[typing.Union[_github_actions_cdk_5328d874.WorkflowTriggers, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_credentials: AwsCredentialsProvider,
    cdkout_dir: builtins.str,
    pipeline: _aws_cdk_pipelines_ceddda9d.PipelineBase,
    stack_options: typing.Mapping[builtins.str, typing.Union[StackOptions, typing.Dict[builtins.str, typing.Any]]],
    post_build: typing.Optional[IJobPhase] = None,
    pre_build: typing.Optional[IJobPhase] = None,
    single_publisher_per_asset_type: typing.Optional[builtins.bool] = None,
    version_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53e7850def2e5e1ec7b09e87c095d95e13e1342749a760f7b76c87604d50052e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    asset_hash_map: typing.Mapping[builtins.str, builtins.str],
    assets: typing.Sequence[typing.Union[_aws_cdk_pipelines_ceddda9d.StackAsset, typing.Dict[builtins.str, typing.Any]]],
    cdk_cli_version: typing.Optional[builtins.str] = None,
    aws_credentials: AwsCredentialsProvider,
    cdkout_dir: builtins.str,
    version_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    container: typing.Optional[typing.Union[_github_actions_cdk_5328d874.ContainerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    continue_on_error: typing.Optional[builtins.bool] = None,
    defaults: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Defaults, typing.Dict[builtins.str, typing.Any]]] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    environment: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    needs: typing.Optional[typing.Sequence[builtins.str]] = None,
    outputs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    permissions: typing.Optional[typing.Union[typing.Union[_github_actions_cdk_5328d874.PermissionsEvent, typing.Dict[builtins.str, typing.Any]], builtins.str]] = None,
    required_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
    runner_labels: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
    runs_on: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
    services: typing.Optional[typing.Mapping[builtins.str, typing.Union[_github_actions_cdk_5328d874.ContainerOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    strategy: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Strategy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be1f9153f78791e125c464c4a3ee931ee0b1ae6f44bb96472fd3fbc58947c7a0(
    *,
    container: typing.Optional[typing.Union[_github_actions_cdk_5328d874.ContainerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    continue_on_error: typing.Optional[builtins.bool] = None,
    defaults: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Defaults, typing.Dict[builtins.str, typing.Any]]] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    environment: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    needs: typing.Optional[typing.Sequence[builtins.str]] = None,
    outputs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    permissions: typing.Optional[typing.Union[typing.Union[_github_actions_cdk_5328d874.PermissionsEvent, typing.Dict[builtins.str, typing.Any]], builtins.str]] = None,
    required_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
    runner_labels: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
    runs_on: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
    services: typing.Optional[typing.Mapping[builtins.str, typing.Union[_github_actions_cdk_5328d874.ContainerOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    strategy: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Strategy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_minutes: typing.Optional[jsii.Number] = None,
    aws_credentials: AwsCredentialsProvider,
    cdkout_dir: builtins.str,
    version_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    asset_hash_map: typing.Mapping[builtins.str, builtins.str],
    assets: typing.Sequence[typing.Union[_aws_cdk_pipelines_ceddda9d.StackAsset, typing.Dict[builtins.str, typing.Any]]],
    cdk_cli_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1e8e3d089ff20ef18b6231aa6e4349e5b21b37ab02c7f35aa88ff0360017ebc(
    *,
    capabilities: typing.Optional[typing.Sequence[StackCapabilities]] = None,
    environment: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bb3634e18fa12d7ac6153212aea971a4857105a1ad07f241296170cbf29ee04(
    id: builtins.str,
    props: IStageJobOptions,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a31d18b6fc7a59f39b409ab74749ebc7122116f6de79527eacb5a56b328e9514(
    value: IStageJobOptions,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd2f61903188a1fdb9485b8949b8c0f3fbe8dfc60b28fd63a493f3100e25dbc1(
    *,
    git_hub_environment: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
    post_jobs: typing.Optional[typing.Sequence[StageJob]] = None,
    pre_jobs: typing.Optional[typing.Sequence[StageJob]] = None,
    stack_capabilities: typing.Optional[typing.Sequence[StackCapabilities]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__327c48fda1f490a47af4c0d4959f594802a797dfda71b2425d6753c6f58ce2c3(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    phase: IJobPhase,
    aws_credentials: AwsCredentialsProvider,
    cdkout_dir: builtins.str,
    version_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    container: typing.Optional[typing.Union[_github_actions_cdk_5328d874.ContainerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    continue_on_error: typing.Optional[builtins.bool] = None,
    defaults: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Defaults, typing.Dict[builtins.str, typing.Any]]] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    environment: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    needs: typing.Optional[typing.Sequence[builtins.str]] = None,
    outputs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    permissions: typing.Optional[typing.Union[typing.Union[_github_actions_cdk_5328d874.PermissionsEvent, typing.Dict[builtins.str, typing.Any]], builtins.str]] = None,
    required_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
    runner_labels: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
    runs_on: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
    services: typing.Optional[typing.Mapping[builtins.str, typing.Union[_github_actions_cdk_5328d874.ContainerOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    strategy: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Strategy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc68638ce4b20529ab7d8fb346be5b128762ccd6d962a792eafbefc3cd09a285(
    *,
    container: typing.Optional[typing.Union[_github_actions_cdk_5328d874.ContainerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    continue_on_error: typing.Optional[builtins.bool] = None,
    defaults: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Defaults, typing.Dict[builtins.str, typing.Any]]] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    environment: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    needs: typing.Optional[typing.Sequence[builtins.str]] = None,
    outputs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    permissions: typing.Optional[typing.Union[typing.Union[_github_actions_cdk_5328d874.PermissionsEvent, typing.Dict[builtins.str, typing.Any]], builtins.str]] = None,
    required_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
    runner_labels: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
    runs_on: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
    services: typing.Optional[typing.Mapping[builtins.str, typing.Union[_github_actions_cdk_5328d874.ContainerOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    strategy: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Strategy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_minutes: typing.Optional[jsii.Number] = None,
    aws_credentials: AwsCredentialsProvider,
    cdkout_dir: builtins.str,
    version_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    phase: IJobPhase,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db03dbc629da621d6e04dbe8c8870b89102cebb5a7ecb6360a3ab6d2a0df928b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    commands: typing.Sequence[builtins.str],
    install_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
    post_build: typing.Optional[IJobPhase] = None,
    pre_build: typing.Optional[IJobPhase] = None,
    aws_credentials: AwsCredentialsProvider,
    cdkout_dir: builtins.str,
    version_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    container: typing.Optional[typing.Union[_github_actions_cdk_5328d874.ContainerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    continue_on_error: typing.Optional[builtins.bool] = None,
    defaults: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Defaults, typing.Dict[builtins.str, typing.Any]]] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    environment: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    needs: typing.Optional[typing.Sequence[builtins.str]] = None,
    outputs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    permissions: typing.Optional[typing.Union[typing.Union[_github_actions_cdk_5328d874.PermissionsEvent, typing.Dict[builtins.str, typing.Any]], builtins.str]] = None,
    required_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
    runner_labels: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
    runs_on: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
    services: typing.Optional[typing.Mapping[builtins.str, typing.Union[_github_actions_cdk_5328d874.ContainerOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    strategy: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Strategy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85f01c48664e0e50639c9427e58f78884676d5e4a19d663473644eb3b68308e4(
    *,
    container: typing.Optional[typing.Union[_github_actions_cdk_5328d874.ContainerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    continue_on_error: typing.Optional[builtins.bool] = None,
    defaults: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Defaults, typing.Dict[builtins.str, typing.Any]]] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    environment: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    needs: typing.Optional[typing.Sequence[builtins.str]] = None,
    outputs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    permissions: typing.Optional[typing.Union[typing.Union[_github_actions_cdk_5328d874.PermissionsEvent, typing.Dict[builtins.str, typing.Any]], builtins.str]] = None,
    required_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
    runner_labels: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
    runs_on: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
    services: typing.Optional[typing.Mapping[builtins.str, typing.Union[_github_actions_cdk_5328d874.ContainerOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    strategy: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Strategy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_minutes: typing.Optional[jsii.Number] = None,
    aws_credentials: AwsCredentialsProvider,
    cdkout_dir: builtins.str,
    version_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    commands: typing.Sequence[builtins.str],
    install_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
    post_build: typing.Optional[IJobPhase] = None,
    pre_build: typing.Optional[IJobPhase] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffd19534aa0aef691c79e308f97a51cf85d74e5c66b39fb4559d18e51d01c654(
    *,
    commands: typing.Sequence[builtins.str],
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    install_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb4cb59421d9014e33af6f3971bffa61839881acb86b0277612f2d5abd3c6728(
    *,
    post_jobs: typing.Optional[typing.Sequence[StageJob]] = None,
    pre_jobs: typing.Optional[typing.Sequence[StageJob]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc04c3a48e0c57481a53cb8f8e54b10f287a5b85f6b43d0cf8567fcbc230aefa(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    asset_hash_map: typing.Mapping[builtins.str, builtins.str],
    stack: _aws_cdk_pipelines_ceddda9d.StackDeployment,
    stack_options: typing.Optional[typing.Union[StackOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_credentials: AwsCredentialsProvider,
    cdkout_dir: builtins.str,
    version_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    container: typing.Optional[typing.Union[_github_actions_cdk_5328d874.ContainerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    continue_on_error: typing.Optional[builtins.bool] = None,
    defaults: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Defaults, typing.Dict[builtins.str, typing.Any]]] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    environment: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    needs: typing.Optional[typing.Sequence[builtins.str]] = None,
    outputs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    permissions: typing.Optional[typing.Union[typing.Union[_github_actions_cdk_5328d874.PermissionsEvent, typing.Dict[builtins.str, typing.Any]], builtins.str]] = None,
    required_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
    runner_labels: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
    runs_on: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
    services: typing.Optional[typing.Mapping[builtins.str, typing.Union[_github_actions_cdk_5328d874.ContainerOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    strategy: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Strategy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a34fdc24473a47a37196aabb89fd535118ac3cc6f156d2303f43c602c9c8c39(
    *,
    container: typing.Optional[typing.Union[_github_actions_cdk_5328d874.ContainerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    continue_on_error: typing.Optional[builtins.bool] = None,
    defaults: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Defaults, typing.Dict[builtins.str, typing.Any]]] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    environment: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    needs: typing.Optional[typing.Sequence[builtins.str]] = None,
    outputs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    permissions: typing.Optional[typing.Union[typing.Union[_github_actions_cdk_5328d874.PermissionsEvent, typing.Dict[builtins.str, typing.Any]], builtins.str]] = None,
    required_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
    runner_labels: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
    runs_on: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
    services: typing.Optional[typing.Mapping[builtins.str, typing.Union[_github_actions_cdk_5328d874.ContainerOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    strategy: typing.Optional[typing.Union[_github_actions_cdk_5328d874.Strategy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_minutes: typing.Optional[jsii.Number] = None,
    aws_credentials: AwsCredentialsProvider,
    cdkout_dir: builtins.str,
    version_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    asset_hash_map: typing.Mapping[builtins.str, builtins.str],
    stack: _aws_cdk_pipelines_ceddda9d.StackDeployment,
    stack_options: typing.Optional[typing.Union[StackOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass
