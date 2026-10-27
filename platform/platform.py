"""Opt-in, read-only auth/admin discovery using the 0.1.2 module registry.

Run with LOAMS_PLATFORM_EXAMPLE=1 and an authorized LOAMS_API_KEY/LOAMS_TOKEN.
"""
import os

from loams import Loams
from loams.admin.v1.audit_pb2 import ListAuditEventsRequest
from loams.admin.v1.project_pb2 import ListProjectsRequest
from loams.auth.v1.auth_pb2 import ListProvidersRequest
from loams.live.v1.admin_pb2 import ListAppsRequest

if os.environ.get("LOAMS_PLATFORM_EXAMPLE") != "1":
    raise SystemExit("Set LOAMS_PLATFORM_EXAMPLE=1 to run this read-only platform example.")
if not (os.environ.get("LOAMS_API_KEY") or os.environ.get("LOAMS_TOKEN")):
    raise SystemExit("Set LOAMS_API_KEY or LOAMS_TOKEN to an authorized credential.")

with Loams.from_env() as loams:
    # Python 0.1.2 exposes auth/admin and live.admin via the generated modules map.
    providers = loams.modules["auth"].list_providers(ListProvidersRequest())
    print("sign-in providers:", [provider.name for provider in providers.providers])

    projects = loams.modules["admin.projects"].list(ListProjectsRequest(page_size=10))
    print("projects:", [project.slug for project in projects.projects])
    audit = loams.modules["admin.audit"].list(ListAuditEventsRequest(page_size=10))
    print("recent audit events:", len(audit.events))

    if loams.system.available("live"):
        apps = loams.modules["live.admin"].list_apps(ListAppsRequest(page_size=10))
        print("Live apps:", [app.name for app in apps.apps])
    else:
        print("Live admin is unavailable in this engine build")
