import boto3
from utils import calculate_age_days, get_tags, is_excluded_by_tags
from pricing import SNAPSHOT_COST_PER_GB
from decimal import Decimal


def scan_ebs_snapshots(grace_period):
    ec2 = boto3.client('ec2')
    snapshots = ec2.describe_snapshots(OwnerIds=['self'])['Snapshots']

    ebs_snapshots = []
    total_cost = Decimal('0.0')

    for snapshot in snapshots:
        age_days = calculate_age_days(snapshot['StartTime'])

        if age_days < grace_period:
            continue

        base_price = Decimal(str(SNAPSHOT_COST_PER_GB.get(
            snapshot['StorageTier'], 0.05)))
        estimated_cost = Decimal(
            str(snapshot.get('VolumeSize', 0))) * base_price

        total_cost += estimated_cost

        snapshot_info = {
            'SnapshotId': snapshot['SnapshotId'],
            'VolumeId': snapshot['VolumeId'],
            "StorageSize": snapshot.get('VolumeSize', 0),
            'EstimatedCost': float(estimated_cost),
            'StartTime': snapshot['StartTime'].strftime('%Y-%m-%d %H:%M:%S'),
            'AgeDays': age_days,
            "State": snapshot['State'],
            'StorageTier': snapshot['StorageTier'],
            'Description': snapshot.get('Description', ''),
            'Tags': get_tags(snapshot),
            'IsOlderThanGracePeriod': age_days > grace_period,
            'IsExcludedByTags': is_excluded_by_tags(get_tags(snapshot)),
        }

        ebs_snapshots.append(snapshot_info)

    return ebs_snapshots, float(total_cost)
