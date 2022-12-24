import os
import sys
import unittest
from contextlib import contextmanager
from io import StringIO
import pytest

from bdop_cli.commands import (
    SyncAppsCommand,
    VersionCommand,
)
from bdop_cli.cliparser import parse_args
from bdop_cli.git_api import GitProvider


@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    old_environ = dict(os.environ)
    os.environ["COLUMNS"] = "80"
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err
        os.environ.clear()
        os.environ.update(old_environ)


class CliParserTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None

    def setUp(self):
        self.environ_backup = dict(os.environ)
        if "GIT_USERNAME" in os.environ:
            os.environ.pop("GIT_USERNAME")
        if "GIT_PASSWORD" in os.environ:
            os.environ.pop("GIT_PASSWORD")

    def tearDown(self):
        os.environ.clear()
        os.environ.update(self.environ_backup)

    @staticmethod
    def _capture_parse_args(args):
        with captured_output() as (stdout, stderr), pytest.raises(SystemExit) as ex:
            parse_args(args)
        return ex.value.code, stdout.getvalue(), stderr.getvalue()

    def assertType(self, o: object, t: type):
        self.assertTrue(isinstance(o, t))

    def test_no_args(self):
        exit_code, stdout, stderr = self._capture_parse_args([])
        self.assertEqual(exit_code, 2)
        self.assertEqual("", stdout)
        self.assertIn("usage: bdop-cli [-h]", stderr)

    def test_help(self):
        exit_code, stdout, stderr = self._capture_parse_args(["--help"])
        self.assertEqual(exit_code, 0)
        self.assertIn("usage: bdop-cli [-h]", stdout)
        self.assertEqual("", stderr)

    def test_help_shortcut(self):
        exit_code, stdout, stderr = self._capture_parse_args(["-h"])
        self.assertEqual(exit_code, 0)
        self.assertIn("usage: bdop-cli [-h]", stdout)
        self.assertEqual("", stderr)

    def test_sync_apps_no_args(self):
        exit_code, stdout, stderr = self._capture_parse_args(["sync-apps"])
        self.assertEqual(exit_code, 2)
        self.assertEqual("", stdout)
        self.assertIn("bdop-cli sync-apps: error: the following arguments are required: --username, --password, "
                      "--organisation, --repository-name, --root-organisation, --root-repository-name", stderr)

    def test_sync_apps_help(self):
        exit_code, stdout, stderr = self._capture_parse_args(["sync-apps", "--help"])
        self.assertEqual(exit_code, 0)
        self.assertIn("usage: bdop-cli sync-apps [-h]", stdout)
        self.assertEqual("", stderr)

    def test_sync_apps_help_shortcut(self):
        exit_code, stdout, stderr = self._capture_parse_args(["sync-apps", "--help"])
        self.assertEqual(exit_code, 0)
        self.assertIn("usage: bdop-cli sync-apps [-h]", stdout)
        self.assertEqual("", stderr)

    def test_sync_apps_required_args(self):
        verbose, args = parse_args(
            [
                "sync-apps",
                "--username",
                "USER",
                "--password",
                "PASS",
                "--git-user",
                "GIT_USER",
                "--git-email",
                "GIT_EMAIL",
                "--git-provider-url",
                "https://www.gitlab.com/",
                "--organisation",
                "ORG",
                "--repository-name",
                "REPO",
                "--root-organisation",
                "ROOT_ORGA",
                "--root-repository-name",
                "ROOT_REPO",
            ]
        )
        self.assertType(args, SyncAppsCommand.Args)

        self.assertEqual(args.username, "USER")
        self.assertEqual(args.password, "PASS")
        self.assertEqual(args.git_user, "GIT_USER")
        self.assertEqual(args.git_email, "GIT_EMAIL")
        self.assertEqual(args.organisation, "ORG")
        self.assertEqual(args.repository_name, "REPO")
        self.assertEqual(args.root_organisation, "ROOT_ORGA")
        self.assertEqual(args.root_repository_name, "ROOT_REPO")

        self.assertEqual(args.git_provider, GitProvider.GITLAB)
        self.assertEqual(args.git_provider_url, "https://www.gitlab.com/")
        self.assertFalse(verbose)

    def test_sync_apps_all_args(self):
        verbose, args = parse_args(
            [
                "sync-apps",
                "--username",
                "USER",
                "--password",
                "PASS",
                "--git-user",
                "GIT_USER",
                "--git-email",
                "GIT_EMAIL",
                "--git-provider",
                "GitHub",
                "--git-provider-url",
                "GIT_PROVIDER_URL",
                "--organisation",
                "ORG",
                "--repository-name",
                "REPO",
                "--root-organisation",
                "ROOT_ORGA",
                "--root-repository-name",
                "ROOT_REPO",
                "--verbose",
                "false",
            ]
        )
        self.assertType(args, SyncAppsCommand.Args)

        self.assertEqual(args.username, "USER")
        self.assertEqual(args.password, "PASS")
        self.assertEqual(args.git_user, "GIT_USER")
        self.assertEqual(args.git_email, "GIT_EMAIL")
        self.assertEqual(args.organisation, "ORG")
        self.assertEqual(args.repository_name, "REPO")
        self.assertEqual(args.root_organisation, "ROOT_ORGA")
        self.assertEqual(args.root_repository_name, "ROOT_REPO")

        self.assertEqual(args.git_provider, GitProvider.GITHUB)
        self.assertEqual(args.git_provider_url, "GIT_PROVIDER_URL")
        self.assertFalse(verbose)

    def test_version_args(self):
        _, args = parse_args(["version"])
        self.assertType(args, VersionCommand.Args)

    def test_version_help(self):
        exit_code, stdout, stderr = self._capture_parse_args(["version", "--help"])
        self.assertEqual(exit_code, 0)
        self.assertIn("usage: bdop-cli version", stdout)
        self.assertEqual("", stderr)

    def test_invalid_boolean(self):
        exit_code, stdout, stderr = self._capture_parse_args(
            [
                "add-pr-comment",
                "--git-provider",
                "github",
                "--username",
                "x",
                "--password",
                "x",
                "--organisation",
                "x",
                "--repository-name",
                "x",
                "--pr-id",
                "1",
                "--text",
                "x",
                "--verbose",
                "INVALID_BOOL",
            ]
        )
        self.assertEqual(exit_code, 2)
        self.assertEqual("", stdout)
        last_stderr_line = stderr.splitlines()[-1]
        self.assertEqual(
            "bdop-cli add-pr-comment: error: argument -v/--verbose: invalid bool value: 'INVALID_BOOL'",
            last_stderr_line,
        )

    def test_invalid_int(self):
        exit_code, stdout, stderr = self._capture_parse_args(
            [
                "add-pr-comment",
                "--git-provider",
                "github",
                "--username",
                "x",
                "--password",
                "x",
                "--organisation",
                "x",
                "--repository-name",
                "x",
                "--pr-id",
                "INVALID_INT",
                "--text",
                "x",
                "--verbose",
                "y",
            ]
        )
        self.assertEqual(exit_code, 2)
        self.assertEqual("", stdout)
        last_stderr_line = stderr.splitlines()[-1]
        self.assertEqual(
            "bdop-cli add-pr-comment: error: argument --pr-id: invalid int value: 'INVALID_INT'", last_stderr_line
        )

    def test_invalid_yaml(self):
        exit_code, stdout, stderr = self._capture_parse_args(
            [
                "deploy",
                "--git-provider",
                "github",
                "--username",
                "x",
                "--password",
                "x",
                "--organisation",
                "x",
                "--repository-name",
                "x",
                "--git-user",
                "x",
                "--git-email",
                "x",
                "--file",
                "x",
                "--values",
                "{ INVALID YAML",
            ]
        )
        self.assertEqual(exit_code, 2)
        self.assertEqual("", stdout)
        last_stderr_line = stderr.splitlines()[-1]
        self.assertEqual(
            "bdop-cli deploy: error: argument --values: invalid YAML value: '{ INVALID YAML'", last_stderr_line
        )

    def test_invalid_git_provider(self):
        exit_code, stdout, stderr = self._capture_parse_args(
            [
                "add-pr-comment",
                "--git-provider",
                "INVALID_PROVIDER",
                "--username",
                "x",
                "--password",
                "x",
                "--organisation",
                "x",
                "--repository-name",
                "x",
                "--pr-id",
                "1",
                "--text",
                "x",
                "--verbose",
                "y",
            ]
        )
        self.assertEqual(exit_code, 2)
        self.assertEqual("", stdout)
        last_stderr_line = stderr.splitlines()[-1]
        self.assertEqual(
            "bdop-cli add-pr-comment: error: argument --git-provider: invalid git provider value: 'INVALID_PROVIDER'",
            last_stderr_line,
        )

    def test_missing_git_provider_and_url(self):
        exit_code, stdout, stderr = self._capture_parse_args(
            [
                "add-pr-comment",
                "--username",
                "x",
                "--password",
                "x",
                "--organisation",
                "x",
                "--repository-name",
                "x",
                "--pr-id",
                "1",
                "--text",
                "x",
                "--verbose",
                "y",
            ]
        )
        self.assertEqual(exit_code, 2)
        self.assertEqual("", stdout)
        last_stderr_line = stderr.splitlines()[-1]
        self.assertEqual(
            "bdop-cli: error: please provide either --git-provider or --git-provider-url", last_stderr_line
        )

    def test_failed_git_provider_deduction_from_url(self):
        exit_code, stdout, stderr = self._capture_parse_args(
            [
                "add-pr-comment",
                "--git-provider-url",
                "http://some-unknown-url.com/",
                "--username",
                "x",
                "--password",
                "x",
                "--organisation",
                "x",
                "--repository-name",
                "x",
                "--pr-id",
                "1",
                "--text",
                "x",
                "--verbose",
                "y",
            ]
        )
        self.assertEqual(exit_code, 2)
        self.assertEqual("", stdout)
        last_stderr_line = stderr.splitlines()[-1]
        self.assertEqual(
            "bdop-cli: error: Cannot deduce git provider from --git-provider-url. Please provide --git-provider",
            last_stderr_line,
        )
