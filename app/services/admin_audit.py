from __future__ import annotations

from app.models.admin_audit_log import AdminAuditLog


def append_admin_audit_log(
    db,
    *,
    admin_username: str,
    action: str,
    resource_type: str,
    resource_id: str | None = None,
    before: dict | None = None,
    after: dict | None = None,
    ip: str | None = None,
):
    row = AdminAuditLog(
        admin_username=admin_username,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        before=before,
        after=after,
        ip=ip,
    )
    db.add(row)
    return row

