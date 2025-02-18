from checkov.common.models.enums import CheckCategories, CheckResult
from checkov.kubernetes.checks.resource.base_spec_check import BaseK8Check

class ApiServerInsecureBindAddress(BaseK8Check):
    def __init__(self):
        id = "CKV_K8S_86"
        name = "Ensure that the --insecure-bind-address argument is not set"
        categories = [CheckCategories.KUBERNETES]
        supported_kind = ['containers']
        super().__init__(name=name, id=id, categories=categories, supported_entities=supported_kind)

    def get_resource_id(self, conf):
        return f'{conf["parent"]} - {conf["name"]}' if conf.get('name') else conf["parent"]

    def scan_spec_conf(self, conf):
        if "command" in conf:
            if "kube-apiserver" in conf["command"]:
                strippedArgs = [arg.split("=")[0] for arg in conf["command"]]
                if "--insecure-bind-address" in strippedArgs:
                    return CheckResult.FAILED

        return CheckResult.PASSED

check = ApiServerInsecureBindAddress()
