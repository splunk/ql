# Copyright (C) 2023-2024 Splunk Inc. All Rights Reserved.

APP_NAME = "splunk_app_soar"

SOAR_CONF = f"/servicesNS/nobody/{APP_NAME}/configs/conf-soar"
INPUTS_CONF = f"/servicesNS/nobody/{APP_NAME}/configs/conf-inputs"
SOAR_PASSWORDS_CONF = f"/servicesNS/nobody/{APP_NAME}/storage/passwords"
SOAR_CONF_PROPS = f"/servicesNS/nobody/{APP_NAME}/properties/soar"
INPUTS_CONF_PROPS = f"/servicesNS/nobody/{APP_NAME}/properties/inputs"

GLOBAL_ACCOUNT = f"/servicesNS/nobody/{APP_NAME}/ta_splunk_app_soar_account"
INPUT_ENDPOINT = f"/servicesNS/nobody/{APP_NAME}/ta_splunk_app_soar_sas_audit"

# Phantom/SOAR REST endpoints
PHANTOM_VERIFY_SERVER_URL_PH_USER = (
    "{server}/rest/ph_user?include_automation=true&_filter_token__key='{auth_token}'"
)
PHANTOM_VERIFY_SERVER_URL_ASSET = "{server}/rest/asset?_filter_token__key='{auth_token}'"
