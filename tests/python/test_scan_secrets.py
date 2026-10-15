"""tools/scan_secrets.py in a throwaway git repository.

Key-shaped strings are assembled at runtime so that this file itself contains none, and nothing
is ever committed: files are only staged.
"""

from __future__ import annotations

import subprocess

import pytest


def fake_keys():
    """Return {pattern name: fake secret}, each built from pieces."""
    return {
        "aws-access-key": "AK" + "IA" + "ABCDEFGHIJKLMNOP",
        "github-token": "gh" + "p_" + "a1B2c3D4e5" * 4,
        "github-fine-grained-token": "github" + "_pat_" + "a1B2c3D4e5" * 3,
        "anthropic-api-key": "sk" + "-ant-" + "api03-" + "a1B2c3D4e5" * 3,
        "openai-api-key": "sk" + "-proj-" + "a1B2c3D4e5" * 4,
        "slack-token": "xo" + "xb-" + "1234567890-abcdefghij",
        "google-api-key": "AI" + "za" + "SyA1b2C3d4E5f6G7h8I9j0K1l2M3n4O5pQ6",
        "private-key-header": "-----BEGIN " + "RSA PRIVATE KEY-----",
        "api-key-assignment": "OPENAI_API_" + "KEY=" + "q8w7e6r5t4y3u2i1o0p9a8s7",
    }


@pytest.fixture
def repo(tmp_path):
    """Return an empty git repository."""
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    return tmp_path


def stage(repo, relative, text):
    """Write a file and stage it (never commit)."""
    path = repo / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf8")
    subprocess.run(["git", "add", relative], cwd=repo, check=True)


def scan(run_tool, repo):
    """Run the scanner on the repository."""
    return run_tool("scan_secrets.py", repo, cwd=repo)


def test_clean_repository_passes(repo, run_tool):
    stage(repo, "README.md", "Set OPENAI_API_KEY=your-key-here before running.\n")
    stage(repo, ".github/ci.yml", "token: ${{ secrets.GITHUB_TOKEN }}\nAPI_KEY: ${{ secrets.KEY }}\n")
    result = scan(run_tool, repo)
    assert result.returncode == 0, result.stdout
    assert "secrets: OK" in result.stdout


@pytest.mark.parametrize("name", sorted(fake_keys()))
def test_each_kind_of_secret_is_detected_and_masked(name, repo, run_tool):
    secret = fake_keys()[name]
    stage(repo, "src/config.txt", f"line one\nvalue = {secret}\nline three\n")
    result = scan(run_tool, repo)
    assert result.returncode == 1, result.stdout
    assert f"src/config.txt:2: {name}:" in result.stdout
    assert secret not in result.stdout + result.stderr
    assert secret[8:-4] not in result.stdout, "the masked output must not leak the middle of the secret"


def test_untracked_files_that_are_not_ignored_are_scanned(repo, run_tool):
    (repo / "notes.txt").write_text(fake_keys()["github-token"], encoding="utf8")
    assert scan(run_tool, repo).returncode == 1


def test_ignored_untracked_files_are_not_scanned(repo, run_tool):
    stage(repo, ".gitignore", "local.txt\n")
    (repo / "local.txt").write_text(fake_keys()["github-token"], encoding="utf8")
    assert scan(run_tool, repo).returncode == 0


@pytest.mark.parametrize("folder", ["dist", "dist-public", "artifacts", "dist-e2e", "test-results"])
def test_build_output_folders_are_scanned_even_when_ignored(folder, repo, run_tool):
    stage(repo, ".gitignore", f"{folder}/\n")
    path = repo / folder / "assets" / "app.js"
    path.parent.mkdir(parents=True)
    path.write_text(f'const key = "{fake_keys()["anthropic-api-key"]}";', encoding="utf8")
    result = scan(run_tool, repo)
    assert result.returncode == 1, result.stdout
    assert f"{folder}/assets/app.js:1:" in result.stdout


def test_binary_files_are_skipped(repo, run_tool):
    (repo / "blob.bin").write_bytes(b"\0\1\2" + fake_keys()["github-token"].encode())
    assert scan(run_tool, repo).returncode == 0


def test_not_a_git_repository_is_a_setup_error(tmp_path, run_tool):
    result = run_tool("scan_secrets.py", tmp_path, cwd=tmp_path)
    assert result.returncode == 2
    assert "not a git repository" in result.stderr


def test_this_repository_has_no_secrets(run_tool):
    """The real tree, as `make secrets` scans it."""
    result = run_tool("scan_secrets.py")
    assert result.returncode == 0, result.stdout
