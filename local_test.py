# This file is intended for local testing when contributing to this repository
# Do not commit any changes
# You will need to generate a GitLab Personal Access Token to use this
from os import environ as env
import gitlab
from gitlabchangelog.changelog import Changelog

env["GITLAB_URL"] = "https://gitlab.invenia.ca"
env["GITLAB_API_TOKEN"] = "<the-personal-access-token-you-created>"
client = gitlab.Gitlab(env["GITLAB_URL"], private_token=env["GITLAB_API_TOKEN"])

repo = "invenia/Example.jl"
p = client.projects.get(repo, lazy=True)

template = """
This is release {{ version }} of {{ package }}.

    {% if merge_requests %}
    **Summary:**
    {% for merge_request in merge_requests %}
        - {{ merge_request.labels }} {{ merge_request.title }} (!{{ merge_request.number }})
    {% endfor %}
    {% endif %}

    {% if previous_release %}
    **Changeset:** {{ compare_url }})
    {% endif %}
"""

changelog = Changelog(p, template)

tags = p.tags.list(all=False)
for tag in tags:
    commit = tag.commit["id"]
    version = tag.name

    release_notes = changelog.get(version, commit)
    print(release_notes)
    print("\n-----------------------------------------------------------------------\n")

    # Note the line below will actually set the release notes in the repository used
    # Should only be used if that is the intended behaviour
    # tag.set_release_description(release_notes)
