# Assumes standard pricing for EU Central (Frankfurt) region
# Does not include IOPS or throughput costs for io1/io2 volumes

EBS_PRICING = {
    "gp2": 0.10,
    "gp3": 0.08,
    "io1": 0.125,
    "io2": 0.125,
    "st1": 0.045,
    "sc1": 0.015,
    "standard": 0.05,
}

SNAPSHOT_COST_PER_GB = {
    "standard": 0.05,
    "archive": 0.0125,
}
