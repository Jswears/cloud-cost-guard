import boto3
from pricing import EBS_PRICING
from utils import calculate_age_days, get_tags, is_excluded_by_tags


def scan_ebs_volumes(grace_period):
    ec2 = boto3.client('ec2')
    volumes = ec2.describe_volumes()['Volumes']

    ebs_volumes = []
    total_cost = 0.0

    for volume in volumes:
        if volume['State'] != 'available':
            continue

        base_price = EBS_PRICING.get(volume['VolumeType'], 0.08)
        estimated_cost = volume.get('Size', 0) * base_price
        total_cost += estimated_cost

        age_days = calculate_age_days(volume['CreateTime'])

        volume_info = {
            'VolumeId': volume['VolumeId'],
            'VolumeType': volume['VolumeType'],
            'Size': volume['Size'],
            'EstimatedCost': estimated_cost,
            "State": volume['State'],
            'CreateTime': volume['CreateTime'].strftime('%Y-%m-%d %H:%M:%S'),
            'AgeDays': age_days,
            "Region": volume['AvailabilityZone'][:-1],
            "Tags": get_tags(volume),
            "IsOlderThanGracePeriod": age_days > grace_period,
            "IsExcludedByTags": is_excluded_by_tags(get_tags(volume)),
        }

        ebs_volumes.append(volume_info)

    return ebs_volumes, total_cost
