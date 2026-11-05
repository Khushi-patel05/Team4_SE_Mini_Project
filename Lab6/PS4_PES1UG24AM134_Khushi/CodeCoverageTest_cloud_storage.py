
import pytest

from cloud_storage_tier import (
    process_storage_tenants,
    monitor_replication_latency
)


# --------------------------------------------------
# PROCESS STORAGE TENANTS - INPUT VALIDATION
# --------------------------------------------------

def test_invalid_tenants_input():
    with pytest.raises(ValueError):
        process_storage_tenants(None, 10.0)


def test_negative_support_fee():
    with pytest.raises(ValueError):
        process_storage_tenants([], -5.0)


# --------------------------------------------------
# STORAGE TIER TESTS
# --------------------------------------------------

@pytest.mark.parametrize(
    "tier, expected",
    [
        ("hot", 2.5),
        ("cool", 1.5),
        ("archive", 0.5)
    ]
)
def test_storage_tier_rates(tier, expected):
    tenants = [{
        "account_active": True,
        "tier": tier,
        "buckets": [
            {"size_gb": 100, "corrupted": False, "egress_gb": 0}
        ]
    }]

    result = process_storage_tenants(tenants, 10.0)

    assert result["total_billed"] == expected
    assert result["status"] == "BILLED"


def test_default_tier_and_missing_fields():
    tenants = [{"account_active": True}]

    result = process_storage_tenants(tenants, 10.0)

    assert result == {
        "total_billed": 0.0,
        "status": "ZERO_USAGE"
    }


def test_inactive_tenant_is_skipped():
    tenants = [{
        "account_active": False,
        "tier": "hot",
        "buckets": [{"size_gb": 1000}]
    }]

    result = process_storage_tenants(tenants, 10.0)

    assert result["total_billed"] == 0.0
    assert result["status"] == "ZERO_USAGE"


def test_invalid_storage_tier():
    tenants = [{
        "account_active": True,
        "tier": "frozen",
        "buckets": [{"size_gb": 100}]
    }]

    result = process_storage_tenants(tenants, 10.0)

    assert result["total_billed"] == 0.0
    assert result["status"] == "ZERO_USAGE"


# --------------------------------------------------
# BUCKET VALIDATION AND CORRUPTION
# --------------------------------------------------

@pytest.mark.parametrize("size", [0, -10])
def test_invalid_bucket_sizes(size):
    tenants = [{
        "account_active": True,
        "tier": "hot",
        "buckets": [{"size_gb": size}]
    }]

    result = process_storage_tenants(tenants, 10.0)

    assert result["total_billed"] == 0.0
    assert result["status"] == "ZERO_USAGE"


def test_corrupted_hot_bucket():
    tenants = [{
        "account_active": True,
        "tier": "hot",
        "buckets": [{
            "size_gb": 100,
            "corrupted": True,
            "egress_gb": 0
        }]
    }]

    result = process_storage_tenants(tenants, 10.0)

    assert result["total_billed"] == 0.0
    assert result["status"] == "ZERO_USAGE"


def test_corrupted_bucket_with_egress():
    tenants = [{
        "account_active": True,
        "tier": "cool",
        "buckets": [{
            "size_gb": 100,
            "corrupted": True,
            "egress_gb": 150
        }]
    }]

    result = process_storage_tenants(tenants, 10.0)

    assert result["total_billed"] == 4.0
    assert result["status"] == "BILLED"


def test_corrupted_archive_bucket():
    tenants = [{
        "account_active": True,
        "tier": "archive",
        "buckets": [
            {"size_gb": 100, "corrupted": True},
            {"size_gb": 200, "corrupted": False}
        ]
    }]

    result = process_storage_tenants(tenants, 10.0)

    assert result["total_billed"] == 0.0
    assert result["status"] == "ZERO_USAGE"


def test_corrupted_archive_with_backup_vault():
    tenants = [{
        "account_active": True,
        "tier": "archive",
        "has_backup_vault": True,
        "buckets": [
            {"size_gb": 100, "corrupted": True}
        ]
    }]

    result = process_storage_tenants(tenants, 10.0)

    assert result["total_billed"] == 10.0
    assert result["status"] == "BILLED"


# --------------------------------------------------
# STORAGE DISCOUNT AND EGRESS TESTS
# --------------------------------------------------

def test_large_bucket_discount():
    tenants = [{
        "account_active": True,
        "tier": "hot",
        "buckets": [
            {"size_gb": 600, "corrupted": False, "egress_gb": 0}
        ]
    }]

    result = process_storage_tenants(tenants, 10.0)

    assert result["total_billed"] == 13.5


def test_bucket_exactly_500_gb():
    tenants = [{
        "account_active": True,
        "tier": "hot",
        "buckets": [
            {"size_gb": 500, "corrupted": False, "egress_gb": 100}
        ]
    }]

    result = process_storage_tenants(tenants, 10.0)

    assert result["total_billed"] == 12.5


def test_egress_above_100_gb():
    tenants = [{
        "account_active": True,
        "tier": "hot",
        "buckets": [
            {"size_gb": 100, "corrupted": False, "egress_gb": 150}
        ]
    }]

    result = process_storage_tenants(tenants, 10.0)

    assert result["total_billed"] == 6.5


# --------------------------------------------------
# BACKUP VAULT AND BILLING STATUS
# --------------------------------------------------

def test_backup_vault_fee():
    tenants = [{
        "account_active": True,
        "tier": "hot",
        "has_backup_vault": True,
        "buckets": [
            {"size_gb": 100, "corrupted": False, "egress_gb": 0}
        ]
    }]

    result = process_storage_tenants(tenants, 10.0)

    assert result["total_billed"] == 12.5
    assert result["status"] == "BILLED"


def test_audit_flagged_status():
    tenants = [{
        "account_active": True,
        "tier": "hot",
        "buckets": [
            {"size_gb": 0},
            {"size_gb": -1},
            {"size_gb": 0},
            {"size_gb": -5},
            {"size_gb": 0}
        ]
    }]

    result = process_storage_tenants(tenants, 10.0)

    assert result["total_billed"] == 0.0
    assert result["status"] == "AUDIT_FLAGGED"


# --------------------------------------------------
# REPLICATION LATENCY MONITORING
# --------------------------------------------------

def test_empty_cluster_matrix():
    assert monitor_replication_latency([]) == "NO_DATA"


def test_none_cluster_matrix():
    assert monitor_replication_latency(None) == "NO_DATA"


def test_normal_replication_latency():
    assert monitor_replication_latency(
        [[50, 100, 150, 200]]
    ) == "SYNCED"


def test_single_latency_spike():
    assert monitor_replication_latency(
        [[250, 100, 150]]
    ) == "SYNCED"


def test_two_consecutive_latency_spikes():
    assert monitor_replication_latency(
        [[250, 300]]
    ) == "SYNC_LAG_ALERT"


def test_spikes_separated_by_normal_latency():
    assert monitor_replication_latency(
        [[250, 100, 300]]
    ) == "SYNCED"


def test_latency_alert_in_later_node():
    assert monitor_replication_latency(
        [[250], [300, 350]]
    ) == "SYNC_LAG_ALERT"


def test_latency_streak_resets_between_nodes():
    assert monitor_replication_latency(
        [[250], [250]]
    ) == "SYNCED"


def test_empty_node_logs():
    assert monitor_replication_latency(
        [[], [100, 150]]
    ) == "SYNCED"
