from datetime import datetime, timezone


def calculate_age_days(dt):
    return (datetime.now(timezone.utc) - dt).days


def is_older_than(resource, days):
    return calculate_age_days(resource['StartTime']) > days


def get_tags(resource):
    return {tag['Key']: tag['Value'] for tag in resource.get('Tags', [])}


def is_excluded_by_tags(tags):
    if not tags:
        return False
    exclude_pairs = {
        ("donotdelete", "true"),
        ("environment", "prod")
    }
    for key, value in tags.items():
        if (key.lower(), value.lower()) in exclude_pairs:
            return True
    return False


def get_volume_summary(volumes):
    include_volumes = []
    excluded_volumes = []
    for vol in volumes:
        if vol["IsExcludedByTags"]:
            excluded_volumes.append(vol)
        else:
            include_volumes.append(vol)
    total = len(volumes)
    excluded_pct = (len(excluded_volumes) / total * 100) if total > 0 else 0.0
    return {
        "TotalScannedVolumes": len(volumes),
        "IncludedVolumes": include_volumes,
        "ExcludedVolumes": excluded_volumes,
        "PercentageExcludedVolumes": excluded_pct,
    }


def get_snapshot_summary(snapshots):
    include_snapshots = []
    excluded_snapshots = []
    for snap in snapshots:
        if snap["IsExcludedByTags"]:
            excluded_snapshots.append(snap)
        else:
            include_snapshots.append(snap)
    total = len(snapshots)
    excluded_pct = (len(excluded_snapshots) /
                    total * 100) if total > 0 else 0.0
    return {
        "TotalScannedSnapshots": len(snapshots),
        "IncludedSnapshots": include_snapshots,
        "ExcludedSnapshots": excluded_snapshots,
        "PercentageExcludedSnapshots": excluded_pct,
    }


def get_cost_summary(volume_cost, snapshot_cost):
    total = round(volume_cost + snapshot_cost, 2)
    return {
        "volumes": round(volume_cost, 2),
        "snapshots": round(snapshot_cost, 2),
        "total": total,
    }
