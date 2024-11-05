from __future__ import annotations

from collections.abc import Sequence

from ..service import Service
from .base import GeneratorBase


class CaddyFileGenerator(GeneratorBase):
    def __init__(self, services: Sequence[Service]):
        super().__init__()
        self.services = services

    def generate(self):
        for service in self.services:
            self.add_block("{:}.bone6.top {{".format(service.get_domain()), "}", indentation=4)
            self.add_line("reverse_proxy {:}".format(service.target))
            self.add_line("tls {")
            self.add_line("    dns dnspod {$DNSPOD_ID},{$DNSPOD_TOKEN}")
            self.add_line("}")
        super().generate()
