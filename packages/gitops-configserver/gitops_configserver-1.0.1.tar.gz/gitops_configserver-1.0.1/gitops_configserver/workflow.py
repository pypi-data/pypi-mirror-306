from abc import ABC, abstractmethod
from logging import getLogger
from gitops_configserver.templates_rendering import (
    TemplatesRendering,
    TenantsConfigLoader,
)
from gitops_configserver.git import GitProvisioner, GitWrapper
from gitops_configserver.utils import create_dir

logger = getLogger(__name__)


class WorkflowCommand(ABC):
    @abstractmethod
    def execute(self, request: dict = None) -> None:
        pass


class TemplatesRenderingCommand(WorkflowCommand):
    def __init__(self, config):
        self.config = config
        self.tenants_config_loader = TenantsConfigLoader(config)

    def execute(self, request: dict = None) -> dict:
        create_dir(self.config.TARGET_DIR)
        tenants_list = self.tenants_config_loader.index().get("tenants", [])
        repo_files = {}
        for tenant_name in tenants_list:
            templates_rendering = TemplatesRendering(self.config)
            repositories_files = templates_rendering.render(tenant_name)
            repo_files[tenant_name] = repositories_files
        logger.info(f"repo_files: {repo_files}")
        return repo_files


class GitRepositoriesCommitterCommand(WorkflowCommand):
    def __init__(self, config):
        self.config = config
        self.tenants_config_loader = TenantsConfigLoader(config)
        self.git_wrapper = GitWrapper(self.config)

    def execute(self, request: dict = None) -> dict:
        tenants_list = self.tenants_config_loader.index().get("tenants", [])
        global_repositories = self.tenants_config_loader.index().get(
            "repositories", []
        )
        for repository_name, repository_value in global_repositories.items():
            global_repositories[repository_name]["files"] = []
        for tenant_name in tenants_list:
            # tenant_config = self.tenants_config_loader.tenant(tenant_name)
            for file_entry in request[tenant_name]["files"]:
                if file_entry.get("repo") in global_repositories:
                    global_repositories[repository_name]["files"] += [
                        file_entry
                    ]
        logger.info(f"global_repositories: {global_repositories}")
        git_provisioner = GitProvisioner(self.config, self.git_wrapper)
        result = git_provisioner.provision(global_repositories)
        return result


class Workflow:
    def __init__(self, config):
        self.config = config
        self.request = {}

    def execute(self) -> None:
        commands = [TemplatesRenderingCommand, GitRepositoriesCommitterCommand]
        for command in commands:
            response = command(self.config).execute(self.request)
            self.request = response
