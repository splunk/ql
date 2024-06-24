
# encoding = utf-8
# Always put this line at the beginning of this file
import ta_addonphantom_declare

import re
import sys

from alert_actions_base import ModularAlertBase
import modalert_phantom_forward_helper

from phantom_utils import get_search_description

class AlertActionWorkerrunphantomplaybook(ModularAlertBase):

    def __init__(self, ta_name, alert_name):
        super(AlertActionWorkerrunphantomplaybook, self).__init__(ta_name, alert_name)
        self.handle_init()

    def handle_init(self):
        self.get_search_description()
        if self.is_arr() is True:
            ## NEW FOR CIM 4.12
            ## Call our queuework method() to support distributed AR actions
            self.queuework()

    def is_arr(self):
        config = self.settings['configuration']
        server_playbook_name = config.get('server_playbook_name', '')
        if server_playbook_name:
            r = re.compile('(.*):\s*(.*)')
            server = r.search(server_playbook_name).group(1)
            if server.endswith(' (ARR)'):
                relay_account = config.get('relay_account')
                try:
                    self.get_relay_details(relay_account)
                except Exception as e:
                    pass
                return True
        return False

    def validate_params(self):
        config = self.settings['configuration']
        server_playbook_name = config.get('server_playbook_name', '')
        if not server_playbook_name:
            self.log_error("Required field 'SOAR Instance and Playbook' missing")
            return False
        if len(server_playbook_name) == 0 and len(config['phantom_server']) == 0 and len(config['playbook_name']) == 0:
            self.log_error("Required fields missing")
            return False
        if len(config['severity']) == 0:
            self.log_error("Required field 'severity' missing")
            return False
        if server_playbook_name:
            r = re.compile('(.*):\s*(.*)')
            server = r.search(server_playbook_name).group(1)
            _ = r.search(server_playbook_name).group(2)
            if server.endswith(' (ARR)'):
                relay_account = config.get('relay_account')
                if relay_account == '' or relay_account is None:
                    self.log_error("Required field 'Alert Action Account' missing")
                    return False
                else:
                    hf_hostname = self.settings['configuration']['relay_details']['name']
                    if self.worker != hf_hostname and config.get('_cam_workers', '["local"]') in ['', '["local"]', '[\"local\"]']:
                        self.log_error("Worker Set provided was 'local', but an ARR server was provided")
                        return False
            # return True
        return True

    def get_relay_details(self, relay_account):
        response = self.get_user_credential_by_id(relay_account)
        if response:
            self.settings['configuration']['relay_details'] = response
    
    def get_search_description(self):
        search_name = self.settings.get('search_name', '')
        try:
            search_description = get_search_description(self, search_name)
            if search_description:
                self.settings['configuration']['search_description'] = search_description
        except Exception as e:
            pass

    def process_event(self, *args, **kwargs):
        status = 0
        try:
            if not self.validate_params():
                return 3

            status = modalert_phantom_forward_helper.process_event(self, *args, **kwargs)
        except (AttributeError, TypeError) as ae:
            self.log_error("Error: {}. Please double check spelling and also verify that a compatible version of Splunk_SA_CIM is installed.".format(ae.message))
            return 4
        except Exception as e:
            msg = "Unexpected error: {}."
            if hasattr(e, 'message'):
                self.log_error(msg.format(e.message))
            else:
                import traceback
                self.log_error(msg.format(traceback.format_exc()))
            return 5
        return status

if __name__ == "__main__":
    exitcode = AlertActionWorkerrunphantomplaybook("phantom", "runphantomplaybook").run(sys.argv)
    sys.exit(exitcode)
