
import pytest

from cloud_storage_tier import (
    process_storage_tenants,
    monitor_replication_latency
)


# ==================================================
# 1. INPUT VALIDATION BRANCHES
# ==================================================

def test_tenants_not_a_list():
    with pytest.raises(ValueError):
        process_storage_tenants("tenant", 10.0)


def test_support_fee_negative():
    with pytest.raises(ValueError):
        process_storage_tenants([], -1.0)


def test_empty_tenant_list():
    result = process_storage_tenants([], 10.0)

    assert result == {
        "total_billed": 0.0,
        "status": "ZERO_USAGE"
    }


# ==================================================
# 2. TENANT ACTIVITY BRANCHES
# ==================================================

def test_active_tenant():
    tenants = [{
        "account_active": True,
        "tier": "hot",
        "buckets": [{"size_gb": 100}]
    }]

    result = process_storage_tenants(tenants, 10.0)

    assert result["status"] == "BILLED"


def test_inactive_tenant():
    tenants = [{
        "account_active": False,
        "tier": "hot",
        "buckets": [{"size_gb": 100}]
    }]

    result = process_storage_tenants(tenants, 10.0)

    assert result["status"] == "ZERO_USAGE"


def test_missing_account_active_defaults_to_false():
    tenants = [{
        "tier": "hot",
        "buckets": [{"size_gb": 100}]
    }]

    result = process_storage_tenants(tenants, 10.0)

    assert result["status"] == "ZERO_USAGE"


# ==================================================
# 3. STORAGE TIER BRANCHES
# ==================================================

@pytest.mark.parametrize(
    "tier, expected",
    [
        ("hot", 2.5),
        ("cool", 1.5),
        ("archive", 0.5)
    ]
)
def test_all_storage_tiers(tier, expected):
    tenants = [{
        "account_active": True,
        "tier": tier,
        "buckets": [{"size_gb": 100}]
    }]

    result = process_storage_tenants(tenants, 10.0)

    assert result["total_billed"] == expected


def test_missing_tier_defaults_to_hot():
    tenants = [{
        "account_active": True,
        "buckets": [{"size_gb": 100}]
    }]

    result = process_storage_tenants(tenants, 10.0)

    assert result["total_billed"] == 2.5


def test_invalid_tier():
    tenants = [{
        "account_active": True,
        "tier": "unknown",
        "buckets": [{"size_gb": 100}]
    }]

    result = process_storage_tenants(tenants, 10.0)

    assert result["total_billed"] == 0.0


# ==================================================
# 4. BUCKET SIZE BRANCHES
# ==================================================

@pytest.mark.parametrize("size", [0, -10])
def test_nonpositive_bucket_size(size):
    tenants = [{
        "account_active": True,
        "tier": "hot",
        "buckets": [{"size_gb": size}]
    }]

    result = process_storage_tenants(tenants, 10.0)

    assert result["total_billed"] == 0.0


def test_positive_bucket_size():
    tenants = [{
        "account_active": True,
        "tier": "hot",
        "buckets": [{"size_gb": 100}]
    }]

    result = process_storage_tenants(tenants, 10.0)

    assert result["total_billed"] == 2.5


# ==================================================
# 5. CORRUPTION BRANCHES
# ==================================================

def test_non_corrupted_bucket():
    tenants = [{
        "account_active": True,
        "tier": "hot",
        "buckets": [{
            "size_gb": 100,
            "corrupted": False
        }]
    }]

    result = process_storage_tenants(tenants, 10.0)

    assert result["total_billed"] == 2.5


def test_corrupted_hot_bucket():
    tenants = [{
        "account_active": True,
        "tier": "hot",
        "buckets": [{
            "size_gb": 100,
            "corrupted": True
        }]
    }]

    result = process_storage_tenants(tenants, 10.0)

    assert result["total_billed"] == 0.0


def test_corrupted_archive_bucket_breaks_loop():
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


# ==================================================
# 6. LARGE STORAGE BRANCHES
# ==================================================

def test_bucket_above_500_gb():
    tenants = [{
        "account_active": True,
        "tier": "hot",
        "buckets": [{"size_gb": 600}]
    }]

    result = process_storage_tenants(tenants, 10.0)

    assert result["total_billed"] == 13.5


def test_bucket_exactly_500_gb():
    tenants = [{
        "account_active": True,
        "tier": "hot",
        "buckets": [{"size_gb": 500}]
    }]

    result = process_storage_tenants(tenants, 10.0)

    assert result["total_billed"] == 12.5


# ==================================================
# 7. EGRESS BRANCHES
# ==================================================

def test_egress_above_100_gb():
    tenants = [{
        "account_active": True,
        "tier": "hot",
        "buckets": [{
            "size_gb": 100,
            "egress_gb": 150
        }]
    }]

    result = process_storage_tenants(tenants, 10.0)

    assert result["total_billed"] == 6.5


def test_egress_exactly_100_gb():
    tenants = [{
        "account_active": True,
        "tier": "hot",
        "buckets": [{
            "size_gb": 100,
            "egress_gb": 100
        }]
    }]

    result = process_storage_tenants(tenants, 10.0)

    assert result["total_billed"] == 2.5


# ==================================================
# 8. BACKUP VAULT BRANCHES
# ==================================================

def test_backup_vault_enabled():
    tenants = [{
        "account_active": True,
        "tier": "hot",
        "has_backup_vault": True,
        "buckets": [{"size_gb": 100}]
    }]

    result = process_storage_tenants(tenants, 10.0)

    assert result["total_billed"] == 12.5


def test_backup_vault_disabled():
    tenants = [{
        "account_active": True,
        "tier": "hot",
        "has_backup_vault": False,
        "buckets": [{"size_gb": 100}]
    }]

    result = process_storage_tenants(tenants, 10.0)

    assert result["total_billed"] == 2.5


# ==================================================
# 9. AUDIT AND BILLING STATUS BRANCHES
# ==================================================

def test_audit_threshold_exactly_four():
    tenants = [{
        "account_active": True,
        "tier": "hot",
        "buckets": [
            {"size_gb": 0},
            {"size_gb": 0},
            {"size_gb": 0},
            {"size_gb": 0}
        ]
    }]

    result = process_storage_tenants(tenants, 10.0)

    assert result["status"] == "ZERO_USAGE"


def test_audit_threshold_above_four():
    tenants = [{
        "account_active": True,
        "tier": "hot",
        "buckets": [
            {"size_gb": 0},
            {"size_gb": 0},
            {"size_gb": 0},
            {"size_gb": 0},
            {"size_gb": 0}
        ]
    }]

    result = process_storage_tenants(tenants, 10.0)

    assert result["status"] == "AUDIT_FLAGGED"


def test_billed_status():
    tenants = [{
        "account_active": True,
        "tier": "cool",
        "buckets": [{"size_gb": 100}]
    }]

    result = process_storage_tenants(tenants, 10.0)

    assert result["status"] == "BILLED"


# ==================================================
# 10. REPLICATION LATENCY BRANCHES
# ==================================================

def test_empty_matrix():
    assert monitor_replication_latency([]) == "NO_DATA"


def test_normal_latency():
    assert monitor_replication_latency(
        [[50, 100, 150, 200]]
    ) == "SYNCED"


def test_latency_above_200():
    assert monitor_replication_latency(
        [[250]]
    ) == "SYNCED"


def test_two_consecutive_spikes():
    assert monitor_replication_latency(
        [[250, 300]]
    ) == "SYNC_LAG_ALERT"


def test_spikes_separated_by_normal_latency():
    assert monitor_replication_latency(
        [[250, 100, 300]]
    ) == "SYNCED"


def test_alert_on_second_node():
    assert monitor_replication_latency(
        [[100], [250, 300]]
    ) == "SYNC_LAG_ALERT"


def test_streak_resets_for_new_node():
    assert monitor_replication_latency(
        [[250], [250]]
    ) == "SYNCED"


def test_empty_node_logs():
    assert monitor_replication_latency(
        [[], [100, 150]]
    ) == "SYNCED"


def test_none_matrix():
    assert monitor_replication_latency(None) == "NO_DATA"
