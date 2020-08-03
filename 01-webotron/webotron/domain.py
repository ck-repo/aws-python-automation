# -*- coding: utf-8 -*-

# Classes for AWS Domain Management

class DomainManager:
    """Manage AWS Route53 Domains."""

    def __init__(self, session):
        """Create a DomainManager object."""
        self.session = session
        self.client = self.session.client("route53")

    def find_hosted_zone(self, domain_name):
        """Find zone matching domain_name."""
        paginator = self.client.get_paginator('list_hosted_zones')
        for page in paginator.paginate():
            for zone in page['HostedZones']:
                if domain_name.endswith(zone['Name'][:-1]):
                    return zone

        return None


