# coding: utf-8
from __future__ import absolute_import, division, print_function, unicode_literals
__metaclass__ = type

from urllib.parse import urlparse, urlencode

import requests


BASE_URL = 'https://api.godsunchained.com/v0'
WEI_PER_ETH = 1e18


def referral_total(in_eth=False, **kws):
    """Total referral """
    kws.update({'perPage': 1000}) # TODO
    url = BASE_URL + '/referral?'
    url += urlencode(kws)
    result = requests.get(url).json()
    total_wei = sum([record['value'] for record in result['records']])
    if in_eth:
        return total_wei/WEI_PER_ETH
    return total_wei


def referral_gained_ratio(user):
    """ratio of referrals gained/given"""
    return referral_total(referrer=user)/referral_total(purchaser=user)
