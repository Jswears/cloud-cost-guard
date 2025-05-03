from dotenv import load_dotenv
import os
from scan import volumes, snapshots
from utils import get_volume_summary, get_snapshot_summary, get_cost_summary
from report import build_html_report

load_dotenv()
grace_period = int(os.getenv('GRACE_PERIOD', 30))


def main():
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

    summary = {
        "volumes": volumes_data,
        "snapshots": snapshots_data,
        "cost": cost_summary,
    }

    html_report = build_html_report(summary)

    with open("output/report.html", "w") as report_file:
        report_file.write(html_report)
    print("Report generated: output/report.html")


if __name__ == "__main__":
    main()
