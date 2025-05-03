from datetime import datetime


def build_volume_table(volumes, title="Volume Summary"):
    if not volumes:
        return f"<h2>{title}</h2><p><em>No data available.</em></p>"

    table_rows = []
    for vol in volumes:
        delete_suggestion = "✅ Yes" if (
            vol["IsOlderThanGracePeriod"] and not vol["IsExcludedByTags"]) else "❌ No"
        row_class = "excluded" if vol.get("IsExcludedByTags") else ""
        table_rows.append(f"""
        <tr class="{row_class}">
            <td>{vol['VolumeId']}</td>
            <td>{vol['AgeDays']}</td>
            <td>${vol['EstimatedCost']:.2f}</td>
            <td>{vol['Region']}</td>
            <td>{delete_suggestion}</td>
        </tr>
        """)

    return f"""
    <h2>{title}</h2>
    <table>
        <tr>
            <th>Volume ID</th>
            <th>Age (days)</th>
            <th>Estimated Cost ($)</th>
            <th>Region</th>
            <th>Delete?</th>
        </tr>
        {''.join(table_rows)}
    </table>
    """


def build_snapshot_table(snapshots, title="Snapshot Summary"):
    if not snapshots:
        return f"<h2>{title}</h2><p><em>No data available.</em></p>"

    table_rows = []
    for snap in snapshots:
        delete_suggestion = "✅ Yes" if (
            snap["IsOlderThanGracePeriod"] and not snap["IsExcludedByTags"]) else "❌ No"
        row_class = "excluded" if snap.get("IsExcludedByTags") else ""
        table_rows.append(f"""
        <tr class="{row_class}">
            <td>{snap['SnapshotId']}</td>
            <td>{snap['AgeDays']}</td>
            <td>${snap['EstimatedCost']:.2f}</td>
            <td>{delete_suggestion}</td>
        </tr>
        """)

    return f"""
    <h2>{title}</h2>
    <table>
        <tr>
            <th>Snapshot ID</th>
            <th>Age (days)</th>
            <th>Estimated Cost ($)</th>
            <th>Delete?</th>
        </tr>
        {''.join(table_rows)}
    </table>
    """


def build_cost_summary(cost):
    return f"""
    <div class="summary-box">
        <strong>Total Volume Cost:</strong> ${cost['volumes']:.2f}<br>
        <strong>Total Snapshot Cost:</strong> ${cost['snapshots']:.2f}<br>
        <strong><u>Total Estimated Cost:</u></strong> <strong>${cost['total']:.2f}</strong>
    </div>
    """


def build_html_report(summary):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    html_content = f"""
    <html>
    <head>
        <title>AWS EBS Cleanup Report</title>
        <style>
            body {{
                font-family: 'Segoe UI', sans-serif;
                color: #333;
                background-color: #fff;
                padding: 2rem;
            }}
            h1, h2 {{
                border-bottom: 2px solid #eee;
                padding-bottom: 4px;
                margin-top: 2rem;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 1rem 0;
                font-size: 14px;
            }}
            th, td {{
                padding: 0.6rem;
                border: 1px solid #ccc;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
            }}
            .excluded {{
                background-color: #f9f9f9;
                color: #777;
                font-style: italic;
            }}
            .summary-box {{
                border: 1px solid #ccc;
                background: #fafafa;
                padding: 1rem;
                margin-bottom: 1rem;
            }}
            .timestamp {{
                font-size: 0.9em;
                color: #999;
                margin-bottom: 1rem;
            }}
        </style>
    </head>
    <body>
        <h1>AWS EBS Cleanup Report</h1>
        <div class="timestamp">Generated on: {timestamp}</div>

        {build_cost_summary(summary['cost'])}

        {build_volume_table(summary['volumes']['IncludedVolumes'], "Included Volumes")}
        {build_volume_table(summary['volumes']['ExcludedVolumes'], "Excluded Volumes")}

        {build_snapshot_table(summary['snapshots']['IncludedSnapshots'], "Included Snapshots")}
        {build_snapshot_table(summary['snapshots']['ExcludedSnapshots'], "Excluded Snapshots")}
    </body>
    </html>
    """
    return html_content
