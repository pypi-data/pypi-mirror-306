import os
import re
import sys

sys.path.append(os.path.dirname(__file__))  # noqa

from datetime import datetime

from base import (
    configure_git,
    get_release_info,
    run_process,
    CHANGELOG_FILE,
    CHANGELOG_HEADER,
    ROOT,
    VERSION_HEADER,
    VERSION_STRINGS,
)


def find_existing_changelog_files():
    changelogs = []
    changelog_paths = [ROOT, ROOT / "docs"]
    changelog_names = ["CHANGELOG", "CHANGES", "HISTORY"]
    changelog_extensions = ["", ".md", ".markdown", ".mdown", ".mkd", ".rst", ".txt"]
    for path in changelog_paths:
        for name in changelog_names:
            for ext in changelog_extensions:
                changelog = path / f"{name}{ext}"
                if changelog.is_file():
                    changelogs.append(changelog)
    if len(changelogs) > 0:
        print(f"Specified changelog file not found: {CHANGELOG_FILE}")
        print("Maybe set 'changelog-file' setting to discovered existing file:\n")
        for changelog in changelogs:
            print(f"{changelog}\n")
        sys.exit(1)


def validate_release():
    if not CHANGELOG_FILE.is_file():
        find_existing_changelog_files()

    if not os.environ.get("PYPI_PASSWORD"):
        print("PYPI_PASSWORD environment variable is not set.")
        sys.exit(1)


def update_version_strings(file_path, new_version):
    version_regex = re.compile(r"(^_*?version_*?\s*=\s*['\"])(\d+\.\d+\.\d+)", re.M)
    with open(file_path, "r+") as f:
        content = f.read()
        f.seek(0)
        f.write(
            re.sub(
                version_regex,
                lambda match: "{}{}".format(match.group(1), new_version),
                content,
            )
        )
        f.truncate()


def prepare_release():
    configure_git()
    validate_release()

    POETRY_DUMP_VERSION_OUTPUT = re.compile(
        r"Bumping version from \d+\.\d+\.\d+ to (?P<version>\d+\.\d+\.\d+)"
    )

    release_type, release_changelog = get_release_info()

    output = run_process(["poetry", "version", release_type])
    version_match = POETRY_DUMP_VERSION_OUTPUT.match(output)

    if not version_match:
        print("Unable to bump the project version using Poetry")
        sys.exit(1)

    new_version = version_match.group("version")

    if VERSION_STRINGS:
        for version_file in VERSION_STRINGS:
            file_path = ROOT / version_file
            update_version_strings(file_path, new_version)

    current_date = datetime.utcnow().strftime("%Y-%m-%d")

    old_changelog_data = ""
    header = ""

    if not CHANGELOG_FILE.is_file():
        with open(CHANGELOG_FILE, "a+") as f:
            f.write(f"CHANGELOG\n{CHANGELOG_HEADER}\n\n")

    with open(CHANGELOG_FILE, "r") as f:
        lines = f.readlines()

    for index, line in enumerate(lines):
        if CHANGELOG_HEADER != line.strip():
            continue

        old_changelog_data = lines[index + 1 :]
        header = lines[: index + 1]
        break

    with open(CHANGELOG_FILE, "w") as f:
        f.write("".join(header))

        new_version_header = f"{new_version} - {current_date}"

        f.write(f"\n{new_version_header}\n")
        f.write(f"{VERSION_HEADER * len(new_version_header)}\n\n")

        f.write(release_changelog)
        f.write("\n")

        f.write("".join(old_changelog_data))
