# SPDX-FileCopyrightText: 2024 UL Research Institutes
# SPDX-License-Identifier: Apache-2.0

from lens_focal import Finding, focal_task


@focal_task(
    name="minimal",
    conditions=dict(
        host=True,
        scheme=["http", "https"],
    ),
    focal_project_url="https://gitlab.com/saferatdayzero/lens-focal",
)
def minimal_task(resource):
    """
    This is likely the simplest task. It does nothing and always produces a
    finding.
    """
    return [
        Finding(
            description="Everything is wrong!",
            name="minimal",
            url="https://example.com",
        )
    ]
