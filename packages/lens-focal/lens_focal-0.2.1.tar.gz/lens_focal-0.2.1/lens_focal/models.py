# SPDX-FileCopyrightText: 2024 UL Research Institutes
# SPDX-License-Identifier: Apache-2.0

import datetime
import json
from dataclasses import dataclass
from typing import Optional

import psycopg

from .settings import DATABASE_URL, NAME


@dataclass
class Finding:
    description: str
    name: str
    url: str


@dataclass(frozen=True)
class Focal:
    task: str
    conditions: Optional[dict] = None
    focal_project_url: str = ""
    upstream_project_url: str = ""

    def register(self):
        now = datetime.datetime.now(datetime.timezone.utc)

        conn = psycopg.connect(DATABASE_URL)
        conn.autocommit = True

        cursor = conn.cursor()
        cursor.execute(
            (
                "INSERT INTO core_focals (focal, task, enabled, conditions, focal_project_url, upstream_project_url, created, updated) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                "ON CONFLICT DO NOTHING "
            ),
            (
                NAME,
                self.task,
                True,
                json.dumps(self.conditions),
                self.focal_project_url,
                self.upstream_project_url,
                now,
                now,
            ),
        )

        conn.close()


@dataclass(frozen=True)
class Resource:
    uri: str
    scheme: str
    host: Optional[str] = None
    port: Optional[int] = None
    path: str = ""
    query: str = ""
    fragment: str = ""
