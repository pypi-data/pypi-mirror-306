from contextlib import contextmanager

from localstack.sdk.chaos.client import get_default
from localstack.sdk.models import FaultRule


@contextmanager
def fault_configuration(fault_rules: list[FaultRule]):
    client = get_default()
    try:
        client.set_fault_rules(fault_rules=fault_rules)
        yield
    finally:
        client.delete_fault_rules(fault_rules=fault_rules)
