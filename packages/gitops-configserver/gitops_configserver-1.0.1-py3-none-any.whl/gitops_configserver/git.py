from os.path import join, dirname
from subprocess import run
from logging import getLogger
from json import dumps
from gitops_configserver.config import Config
from gitops_configserver.utils import (
    remove_dir_with_content,
    copy_file,
    create_dir,
    write_to_file,
    timestamp,
)
from gitops_configserver import __version__

logger = getLogger(__name__)


class GitWrapper:
    def __init__(self, config: Config):
        self.config = config

    def clone(self, repo_url: str, repo_dir: str):
        command = f"git clone {repo_url} {repo_dir}"
        logger.info(f"run: {command}")
        run(command, shell=True, check=True)

    def stage_file(self, filename: str, cwd: str):
        command = f"git add {filename}"
        logger.info(f"run: {command}")
        run(command, shell=True, check=True, cwd=cwd)

    def set_committer(self, cwd: str):
        command = 'git config --local user.name "GitHub Actions Bot"'
        run(command, shell=True, check=True, cwd=cwd)
        command = 'git config --local user.email "github-bot@speedwell.pl"'
        run(command, shell=True, check=True, cwd=cwd)

    def commit(self, message: str, cwd: str):
        command = f'git commit -m "{message}"'
        logger.info(f"run: {command}")
        run(command, shell=True, check=True, cwd=cwd)

    def push(self, cwd: str):
        command = f"git push"
        logger.info(f"run: {command}")
        run(command, shell=True, check=True, cwd=cwd)


class GitProvisioner:
    def __init__(self, config: Config, git_wrapper: GitWrapper) -> None:
        self.config = config
        self.git_wrapper = git_wrapper

    def provision(self, repositories: dict) -> dict:
        for repository_name, repository_value in repositories.items():
            index_file = {
                "files": [],
                "gitops_configserver": __version__,
                "timestamp": timestamp(),
            }
            if repository_value.get("type") == "github":
                repo_dir = join(self.config.TARGET_DIR, repository_name)
                remove_dir_with_content(repo_dir)
                repo_url = repository_value.get("url")
                repo_full_url = f"https://{self.config.GH_PAT}@{repo_url}"
                self.git_wrapper.clone(repo_full_url, repo_dir)
                for file_entry in repository_value.get("files", []):
                    destination_filepath = join(
                        repo_dir, file_entry["destination_filename"]
                    )
                    create_dir(dirname(destination_filepath))
                    copy_file(file_entry["tmp_path"], destination_filepath)
                    self.git_wrapper.stage_file(
                        file_entry["destination_filename"], repo_dir
                    )
                    index_file["files"].append(
                        file_entry["destination_filename"]
                    )
                write_to_file(
                    join(repo_dir, ".gitops_configserver"),
                    dumps(index_file, indent=4),
                )
                index_file["files"].append(
                    join(repo_dir, ".gitops_configserver")
                )
                self.git_wrapper.stage_file(".gitops_configserver", repo_dir)
                self.git_wrapper.set_committer(repo_dir)
                self.git_wrapper.commit("chore: Update configs", repo_dir)
                self.git_wrapper.push(repo_dir)
        return index_file
