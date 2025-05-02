from dotenv import load_dotenv
import os
from scan import volumes, snapshots
from utils import get_volume_summary, get_snapshot_summary, get_cost_summary

# Load environment variables from .env file
load_dotenv()
grace_period = int(os.getenv('GRACE_PERIOD', 30))


def main():

    # Scan EBS volumes and snapshots
    ebs_volumes, total_volume_cost = volumes.scan_ebs_volumes(grace_period)
    ebs_snapshots, total_snapshot_cost = snapshots.scan_ebs_snapshots(
        grace_period)

    if not ebs_volumes and not ebs_snapshots:
        print("No EBS volumes or snapshots found.")
        return

    volumes_data = get_volume_summary(ebs_volumes)
    snapshots_data = get_snapshot_summary(ebs_snapshots)
    cost_summary = get_cost_summary(total_volume_cost, total_snapshot_cost)

    if os.getenv("DEBUG_OUTPUT", "false").lower() == "true":
        import json
        print(json.dumps({
            "volumes": volumes_data,
            "snapshots": snapshots_data,
            "cost": cost_summary,
        }, indent=2))

    print(
        f"Total estimated cost for all resources: ${cost_summary['total']}")

    return {
        "volumes": volumes_data,
        "snapshots": snapshots_data,
        "cost": cost_summary,
    }


if __name__ == "__main__":
    main()
