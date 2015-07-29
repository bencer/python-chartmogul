#    Extremely simple ChatMogul read-only API wrapper
#    https://github.com/bencer/python-chartmogul
#    Copyright (C) 2015 Jorge Salamero <bencer@cauterized.net>
#
#    Authors: Jorge Salamero <bencer@cauterized.net>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3 of the License.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import urllib.request
import json
import http

class ChartMogul(object):

    #http.client.HTTPConnection.debuglevel = 1

    def __init__(self, token, secret):
        self.token = token
        self.secret = secret
        self.url = 'https://api.chartmogul.com/v1/'

        password_manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        password_manager.add_password(None, self.url,
                                      self.token, self.secret) 
        http_handler = urllib.request.HTTPBasicAuthHandler(password_manager) 
        page_opener = urllib.request.build_opener(http_handler) 
        urllib.request.install_opener(page_opener) 

    def get_mrr(self, interval, start_date, end_date):
        req = urllib.request.Request(
            '{:s}metrics/mrr?start-date={:s}&end-date={:s}&interval={:s}'.format(self.url, start_date.isoformat(), end_date.isoformat(), interval),
            method = 'GET'
        )
        try:
            res = urllib.request.urlopen(req)
        except HTTPError as e:
            print('Error code: ', e.code)
        except URLError as e:
            print('Reason: ', e.reason)
        jres = json.loads(res.read().decode('utf-8'))

        mrr_contraction = jres['entries'][0]['mrr-contraction']/100
        mrr_expansion = jres['entries'][0]['mrr-expansion']/100
        mrr_reactivation = jres['entries'][0]['mrr-reactivation']/100
        mrr_churn = jres['entries'][0]['mrr-churn']/100
        mrr = jres['entries'][0]['mrr']/100
        mrr_new_business = jres['entries'][0]['mrr-new-business']/100
        mrr_net_movement = mrr_new_business + mrr_expansion + mrr_contraction + mrr_churn + mrr_reactivation
        values = { 'mrr-contraction': round(mrr_contraction, 2),
                   'mrr-expansion': round(mrr_expansion, 2),
                   'mrr-reactivation': round(mrr_reactivation, 2),
                   'mrr-churn': round(mrr_churn, 2),
                   'mrr': round(mrr, 2),
                   'mrr-new-business': round(mrr_new_business, 2),
                   'mrr-net-movement': round(mrr_net_movement, 2) }
        return values

    def get_all(self, interval, start_date, end_date):
        req = urllib.request.Request(
            '{:s}metrics/all?start-date={:s}&end-date={:s}&interval={:s}'.format(self.url, start_date.isoformat(), end_date.isoformat(), interval),
            method = 'GET'
        )
        try:
            res = urllib.request.urlopen(req)
        except HTTPError as e:
            print('Error code: ', e.code)
        except URLError as e:
            print('Reason: ', e.reason)
        jres = json.loads(res.read().decode('utf-8'))

        customers = jres['entries'][0]['customers']
        arr = jres['entries'][0]['arr']/100
        mrr_churn_rate = jres['entries'][0]['mrr-churn-rate']
        mrr = jres['entries'][0]['mrr']/100
        customer_churn_rate = jres['entries'][0]['customer-churn-rate']

        values = { 'customers': customers,
                   'arr': round(arr, 2),
                   'mrr-churn-rate': mrr_churn_rate,
                   'mrr': round(mrr, 2),
                   'customer-churn-rate': customer_churn_rate }
        return values
