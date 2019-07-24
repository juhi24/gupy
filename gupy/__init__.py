# coding: utf-8
from __future__ import absolute_import, division, print_function, unicode_literals
__metaclass__ = type

from urllib.parse import urlparse, urlencode

import requests


BASE_URL = 'https://api.godsunchained.com/v0'
WEI_PER_ETH = 1e18


def _tuples(key, values):
    """list of key-value tuples"""
    return [(key, value) for value in values]


def _call(endpoint, kws):
    """API call wrapper"""
    url = '{}/{}?'.format(BASE_URL, endpoint)
    url += urlencode(kws)
    return requests.get(url).json()


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


def properties(user_ids):
    """user properties"""
    kws = _tuples('user_id', user_ids)
    result = _call('properties', kws)
    return result['records']


def rank(user_id, game_mode=2):
    """per hame mode user rank"""
    kws = dict(user_id=user_id, game_mode=game_mode)
    result = _call('rank', kws)
    return result['records']


def predict(user_id, opponent_id, game_mode=2):
    """Match propability"""
    kws = {'user_id': user_id,
           'opponent_id': opponent_id,
           'game_mode': game_mode}
    return _call('predict', kws)


def user_stats(user_id):
    """user summary"""
    props = properties([user_id])
    urank = rank(user_id)
    stats = props[0]
    stats.update(urank[0])
    return stats

