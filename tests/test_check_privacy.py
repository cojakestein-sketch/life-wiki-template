"""Run with: python3 -m unittest discover tests"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_privacy.py"

PAGE = "---\nprivacy: {level}\nupdated: 2026-01-01\nsources:\n  - raw/x.md\n---\n\n# Page\n"


class CheckPrivacyTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name)
        self.git("init", "-q")

    def tearDown(self):
        self._tmp.cleanup()

    def git(self, *args):
        subprocess.run(["git", *args], cwd=self.repo, check=True, capture_output=True)

    def write(self, path, text, stage=True):
        file = self.repo / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(text)
        if stage:
            self.git("add", path)

    def run_check(self, cwd=None):
        return subprocess.run(
            [sys.executable, str(SCRIPT)],
            cwd=cwd or self.repo,
            capture_output=True,
            text=True,
        )

    def test_clean_repo_passes(self):
        self.write("me/profile.md", PAGE.format(level="sensitive"))
        self.assertEqual(self.run_check().returncode, 0)

    def test_tracked_local_only_fails(self):
        self.write("me/health.md", PAGE.format(level="local-only"))
        result = self.run_check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("tracked but labelled privacy: local-only", result.stdout)

    def test_unignored_local_only_fails_even_when_untracked(self):
        self.write("me/health.md", PAGE.format(level="local-only"), stage=False)
        result = self.run_check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("not covered by .gitignore", result.stdout)

    def test_ignored_local_only_passes(self):
        self.write(".gitignore", "private/\n")
        self.write("private/health.md", PAGE.format(level="local-only"), stage=False)
        self.assertEqual(self.run_check().returncode, 0)

    def test_maintained_page_without_frontmatter_fails(self):
        self.write("me/now.md", "# Now\n")
        result = self.run_check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("missing frontmatter privacy, updated, sources", result.stdout)

    def test_navigation_files_need_no_frontmatter(self):
        self.write("areas/README.md", "# Areas\n")
        self.write("areas/index.md", "# Areas\n")
        self.assertEqual(self.run_check().returncode, 0)

    def test_secret_fails(self):
        fake_key = "gh" + "p_" + "a" * 36  # assembled so this file passes the check
        self.write("ops/notes.md", f"token: {fake_key}\n")
        result = self.run_check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("GitHub token", result.stdout)

    def test_checks_staged_content_not_working_tree(self):
        self.write("me/profile.md", PAGE.format(level="local-only"))
        (self.repo / "me/profile.md").write_text(PAGE.format(level="sensitive"))
        self.assertEqual(self.run_check().returncode, 1)

    def test_runs_from_subdirectory(self):
        self.write("me/health.md", PAGE.format(level="local-only"), stage=False)
        (self.repo / "areas").mkdir()
        self.assertEqual(self.run_check(cwd=self.repo / "areas").returncode, 1)


if __name__ == "__main__":
    unittest.main()
