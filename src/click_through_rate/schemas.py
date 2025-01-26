"""Schemas for the tables used in the project."""

train_raw: dict[str, str] = {
    "id": "string",
    "click": "boolean",
    "hour": "string",
    "c1": "string",
    "banner_pos": "string",
    "site_id": "string",
    "site_domain": "string",
    "site_category": "string",
    "app_id": "string",
    "app_domain": "string",
    "app_category": "string",
    "device_id": "string",
    "device_ip": "string",
    "device_model": "string",
    "device_type": "string",
    "device_conn_type": "string",
    "c14": "string",
    "c15": "string",
    "c16": "string",
    "c17": "string",
    "c18": "string",
    "c19": "string",
    "c20": "string",
    "c21": "string",
}

test_raw: dict[str, str] = {
    "id": "string",
    "click": "boolean",
    "hour": "string",
    "c1": "string",
    "banner_pos": "string",
    "site_id": "string",
    "site_domain": "string",
    "site_category": "string",
    "app_id": "string",
    "app_domain": "string",
    "app_category": "string",
    "device_id": "string",
    "device_ip": "string",
    "device_model": "string",
    "device_type": "string",
    "device_conn_type": "string",
    "c14": "string",
    "c15": "string",
    "c16": "string",
    "c17": "string",
    "c18": "string",
    "c19": "string",
    "c20": "string",
    "c21": "string",
}

f_interactions: dict[str, str] = {
    "id": "string",
    "click": "boolean",
    "c1": "string",
    "banner_pos": "string",
    "site_id": "string",
    "app_id": "string",
    "device_id": "string",
    "c14": "string",
    "c15": "string",
    "c16": "string",
    "c17": "string",
    "c18": "string",
    "c19": "string",
    "c20": "string",
    "c21": "string",
    "timestamp": "timestamp",
}

d_devices: dict[str, str] = {
    "device_id": "string",
    "device_ip": "string",
    "device_model": "string",
    "device_type": "string",
    "device_conn_type": "string",
}

d_sites: dict[str, str] = {
    "site_id": "string",
    "site_domain": "string",
    "site_category": "string",
}

d_apps: dict[str, str] = {
    "app_id": "string",
    "app_domain": "string",
    "app_category": "string",
}

train_devices_main: dict[str, str] = {
    "click": "boolean",
    "c1": "string",
    "banner_pos": "string",
    "c14": "string",
    "c15": "string",
    "c16": "string",
    "c17": "string",
    "c18": "string",
    "c19": "string",
    "c20": "string",
    "c21": "string",
    "device_type": "string",
    "device_conn_type": "string",
    "site_category": "string",
    "app_category": "string",
    "timestamp": "timestamp",
}

train_devices_other = train_devices_main
