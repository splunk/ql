
# encoding = utf-8
# Always put this line at the beginning of this file
import ta_addonphantom_declare

import sys

from alert_actions_base import ModularAlertBase
import modalert_phantom_forward_helper

from phantom_utils import get_search_description
class AlertActionWorkersendtophantom(ModularAlertBase):

    def __init__(self, ta_name, alert_name):
        super(AlertActionWorkersendtophantom, self).__init__(ta_name, alert_name)
        self.handle_init()

    def handle_init(self):
        config = self.settings['configuration']
        self.get_search_description()
        if config.get('phantom_server', '').endswith(' (ARR)'):
            relay_account = config.get('relay_account')
            try:
                self.get_relay_details(relay_account)
            except Exception as e:
                pass
            ## NEW FOR CIM 4.12
            ## Call our queuework method() to support distributed AR actions
            self.queuework()

    def validate_params(self):
        config = self.settings['configuration']
        if len(config['phantom_server']) == 0:
            self.log_error("Required field 'SOAR Instance' missing")
            return False
        if len(config['severity']) == 0:
            self.log_error("Required field 'severity' missing")
            return False
        if config['phantom_server'].endswith(' (ARR)'):
            relay_account = config.get('relay_account')
            if relay_account == '' or relay_account is None:
                self.log_error("Required field 'Alert Action Account' missing")
                return False
            else:
                hf_hostname = self.settings['configuration']['relay_details']['name']
                if self.worker != hf_hostname and config.get('_cam_workers', '["local"]') in ['', '["local"]', '[\"local\"]']:
                    self.log_error("Worker Set provided was 'local', but an ARR server was provided")
                    return False
            return True
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
            self.log_error("Error: {}. Please double check spelling and also verify that a compatible version of Splunk_SA_CIM is installed.".format(str(ae)))
            return 4
        except Exception as e:
            msg = "Unexpected error: {}."
            if e:
                self.log_error(msg.format(str(e)))
            else:
                import traceback
                self.log_error(msg.format(traceback.format_exc()))
            return 5
        return status

if __name__ == "__main__":
    exitcode = AlertActionWorkersendtophantom("phantom", "sendtophantom").run(sys.argv)
    sys.exit(exitcode)
