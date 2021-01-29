# GitLabChangelog
[![CI](https://github.com/invenia/gitlabchangelog/workflows/CI/badge.svg)](https://github.com/invenia/gitlabchangelog/actions?query=workflow%3ACI)
[![Python Version](https://img.shields.io/badge/python-3.8%20%7C%203.9-blue.svg)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Produces GitLab changelog release notes for projects that follow SemVer.
The changelog produced for each release based on the issues that have been closed and the merge requests that have been merged.

## Installation

To install this just install it into a virtualenv like so:

```
cd GitLabChangelog
python3 -m venv venv
. venv/bin/activate

pip install --upgrade pip
pip install -e .
```

## Contributing

This package uses the [python-gitlab](https://python-gitlab.readthedocs.io/en/stable/index.html) package to interact with GitLab.
It's useful to refer to their documentation when making changes.
You can test using their API locally by generating a [Personal Access Token](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html#creating-a-personal-access-token) and setting it in the included `local_test.py` script.

You can run tests locally by running in the virtualenv you installed the package in:
```
tox
```

New releases will automatically publish the package to TestPyPi and PyPi via GitHub Actions.
Don't forget to bump the version in `gitlabchangelog/VERSION` before tagging a new release.
## Changelog format

The changelog is completely customizable with the [Jinja](https://jinja.palletsprojects.com) templating engine.
To supply your own template, use the `template` parameter when creating Changelogs:

```python
from os import environ as env

import gitlab
from tagbotgitlab.changelog import Changelog

# Set some environment variables required for import.
env["GITLAB_URL"] = "https://gitlab.example.ca"
env["GITLAB_API_TOKEN"] = "<the-personal-access-token-you-created>"
client = gitlab.Gitlab(env["GITLAB_URL"], private_token=env["GITLAB_API_TOKEN"])

repo = "example/TestRepo"
p = client.projects.get(repo, lazy=True)

template = """
This is release {{ version }} of {{ package }}.
    {% if merge_requests %}
    **Summary:**
    {% for merge_request in merge_requests %}
        - [{{ merge_request.labels }}] {{ merge_request.title }} (!{{ merge_request.number }})
    {% endfor %}
    {% endif %}

    {% if previous_release %}
    **Changeset:** {{ compare_url }})
    {% endif %}
"""
changelog = Changelog(p, template)

commit = "abcdefgh"
version = "v1.0.1"
release_notes = changelog.get(version, commit)
print(release_notes)
```

The data available to you looks like this:

```json
{
  "compare_url": "https://gitlab.com/Owner/Repo/-/compare/previous_version...current_version (or null for first release)",
  "issues": [
    {
      "author": {
        "name": "Real Name",
        "url": "https://gitlab.com/username",
        "username": "their login"
      },
      "description": "issue description",
      "labels": ["label1", "label2"],
      "number": 123,
      "title": "issue title",
      "url": "https://gitlab.com/Owner/Repo/issues/123"
    }
  ],
  "package": "PackageName",
  "previous_release": "v1.1.2 (or null for first release)",
  "merge_requests": [
    {
      "author": {"same format as": "issue author"},
      "description": "merge request description",
      "labels": ["label1", "label2"],
      "merger": {"same format as": "issue author"},
      "number": 123,
      "title": "merge request title",
      "url": "https://gitlab.com/Owner/Repo/pull/123"
    }
  ],
  "sha": "commit SHA",
  "version": "v1.2.3",
  "version_url": "https://gitlab.com/Owner/Repo/tree/v1.2.3"
}
```

You can see the default template in `gitlabchangelog/changelog.py`.

## Ignore labels
Issues and pull requests with specified labels are not included in the changelog data.
By default, the following labels are ignored:

- changelog skip
- duplicate
- exclude from changelog
- invalid
- no changelog
- question
- wont fix

White-space, case, dashes, and underscores are ignored when comparing labels.

## License

gitlabchangelog is provided under an MIT License.
