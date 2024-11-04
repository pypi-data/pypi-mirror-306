from os.path import join
from pytest import fixture
from gitops_configserver.config import Config
from gitops_configserver.workflow import TemplatesRenderingCommand
from gitops_configserver.utils import read_file, remove_dir_with_content


@fixture
def config():
    config = Config()
    config.CONFIG_DIR = "resources/test_config"
    config.TARGET_DIR = "target_test_configserver"
    return config


@fixture
def templates_rendering_command(config):
    yield TemplatesRenderingCommand(config)
    # remove_dir_with_content(config.TARGET_DIR)


def test_rendering(templates_rendering_command, config):
    repo_files = templates_rendering_command.execute()
    assert repo_files == {
        "tenant1": {
            "repositories": {
                "test_repo1": {"type": "local", "url": "local_path"}
            },
            "files": [
                {
                    "tmp_path": "target_test_configserver/tenant1/asdf/config1-ubuntu-22.04-10-python3.10-prod.yml",
                    "destination_filename": "asdf/config1-ubuntu-22.04-10-python3.10-prod.yml",
                    "repo": "gitops-configserver-tests",
                },
                {
                    "tmp_path": "target_test_configserver/tenant1/asdf/config1-ubuntu-22.04-10-python3.11-prod.yml",
                    "destination_filename": "asdf/config1-ubuntu-22.04-10-python3.11-prod.yml",
                    "repo": "gitops-configserver-tests",
                },
                {
                    "tmp_path": "target_test_configserver/tenant1/asdf/config1-ubuntu-22.04-10-python3.12-prod.yml",
                    "destination_filename": "asdf/config1-ubuntu-22.04-10-python3.12-prod.yml",
                    "repo": "gitops-configserver-tests",
                },
                {
                    "tmp_path": "target_test_configserver/tenant1/asdf/config1-ubuntu-22.04-12-python3.10-prod.yml",
                    "destination_filename": "asdf/config1-ubuntu-22.04-12-python3.10-prod.yml",
                    "repo": "gitops-configserver-tests",
                },
                {
                    "tmp_path": "target_test_configserver/tenant1/asdf/config1-ubuntu-22.04-12-python3.11-prod.yml",
                    "destination_filename": "asdf/config1-ubuntu-22.04-12-python3.11-prod.yml",
                    "repo": "gitops-configserver-tests",
                },
                {
                    "tmp_path": "target_test_configserver/tenant1/asdf/config1-ubuntu-22.04-12-python3.12-prod.yml",
                    "destination_filename": "asdf/config1-ubuntu-22.04-12-python3.12-prod.yml",
                    "repo": "gitops-configserver-tests",
                },
                {
                    "tmp_path": "target_test_configserver/tenant1/asdf/config1-ubuntu-22.04-14-python3.10-prod.yml",
                    "destination_filename": "asdf/config1-ubuntu-22.04-14-python3.10-prod.yml",
                    "repo": "gitops-configserver-tests",
                },
                {
                    "tmp_path": "target_test_configserver/tenant1/asdf/config1-ubuntu-22.04-14-python3.11-prod.yml",
                    "destination_filename": "asdf/config1-ubuntu-22.04-14-python3.11-prod.yml",
                    "repo": "gitops-configserver-tests",
                },
                {
                    "tmp_path": "target_test_configserver/tenant1/asdf/config1-ubuntu-22.04-14-python3.12-prod.yml",
                    "destination_filename": "asdf/config1-ubuntu-22.04-14-python3.12-prod.yml",
                    "repo": "gitops-configserver-tests",
                },
                {
                    "tmp_path": "target_test_configserver/tenant1/asdf/config1-ubuntu-20.04-10-python3.10-prod.yml",
                    "destination_filename": "asdf/config1-ubuntu-20.04-10-python3.10-prod.yml",
                    "repo": "gitops-configserver-tests",
                },
                {
                    "tmp_path": "target_test_configserver/tenant1/asdf/config1-ubuntu-20.04-10-python3.11-prod.yml",
                    "destination_filename": "asdf/config1-ubuntu-20.04-10-python3.11-prod.yml",
                    "repo": "gitops-configserver-tests",
                },
                {
                    "tmp_path": "target_test_configserver/tenant1/asdf/config1-ubuntu-20.04-10-python3.12-prod.yml",
                    "destination_filename": "asdf/config1-ubuntu-20.04-10-python3.12-prod.yml",
                    "repo": "gitops-configserver-tests",
                },
                {
                    "tmp_path": "target_test_configserver/tenant1/asdf/config1-ubuntu-20.04-12-python3.10-prod.yml",
                    "destination_filename": "asdf/config1-ubuntu-20.04-12-python3.10-prod.yml",
                    "repo": "gitops-configserver-tests",
                },
                {
                    "tmp_path": "target_test_configserver/tenant1/asdf/config1-ubuntu-20.04-12-python3.11-prod.yml",
                    "destination_filename": "asdf/config1-ubuntu-20.04-12-python3.11-prod.yml",
                    "repo": "gitops-configserver-tests",
                },
                {
                    "tmp_path": "target_test_configserver/tenant1/asdf/config1-ubuntu-20.04-12-python3.12-prod.yml",
                    "destination_filename": "asdf/config1-ubuntu-20.04-12-python3.12-prod.yml",
                    "repo": "gitops-configserver-tests",
                },
                {
                    "tmp_path": "target_test_configserver/tenant1/asdf/config1-ubuntu-20.04-14-python3.10-prod.yml",
                    "destination_filename": "asdf/config1-ubuntu-20.04-14-python3.10-prod.yml",
                    "repo": "gitops-configserver-tests",
                },
                {
                    "tmp_path": "target_test_configserver/tenant1/asdf/config1-ubuntu-20.04-14-python3.11-prod.yml",
                    "destination_filename": "asdf/config1-ubuntu-20.04-14-python3.11-prod.yml",
                    "repo": "gitops-configserver-tests",
                },
                {
                    "tmp_path": "target_test_configserver/tenant1/asdf/config1-ubuntu-20.04-14-python3.12-prod.yml",
                    "destination_filename": "asdf/config1-ubuntu-20.04-14-python3.12-prod.yml",
                    "repo": "gitops-configserver-tests",
                },
                {
                    "tmp_path": "target_test_configserver/tenant1/asdf/config1-ubuntu-22.04-10-python3.7-prod.yml",
                    "destination_filename": "asdf/config1-ubuntu-22.04-10-python3.7-prod.yml",
                    "repo": "gitops-configserver-tests",
                },
                {
                    "tmp_path": "target_test_configserver/tenant1/config1-prod.yml",
                    "destination_filename": "config1-prod.yml",
                    "repo": "test_repo1",
                },
            ],
        }
    }
    print(repo_files)
    content = read_file(
        join(
            config.TARGET_DIR,
            "tenant1",
            "asdf",
            "config1-ubuntu-22.04-10-python3.12-prod.yml",
        )
    )
    assert (
        content
        == """- my_config:
  - var1: aaa1.default
  - var2: bbb1.default
  - var3: ccc1.default
  - lll: |
    - abc: 1
      def: 2
      ghi: 3
    - mmm: 4"""
    )
