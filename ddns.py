import requests
import json
import logging
import os

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109 import UpdateDomainRecordRequest, DescribeDomainRecordInfoRequest

logging.basicConfig(filename=os.path.join(os.getcwd(),'ddns.log'),level=logging.DEBUG,format='%(asctime)s %(levelname)-8s: %(message)s')

DOMAIN = '*.com'
RID = '*'

client = AcsClient(
    "a",
    "b",
    "cn-hangzhou"
)


def ip():
    r = requests.get('http://pi.lmhaoye.com/get/ip')
    if r.status_code == 200:
        return r.text
    else:
        return None


def update_record(cip, old):
    req = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
    req.set_RecordId(RID)
    req.set_RR(old['RR'])
    req.set_Type(old['Type'])
    req.set_Value(cip)
    resp = client.do_action_with_exception(req).decode('utf-8')
    print(resp)
    return True


def update_pi(cip):
    postdata = {'ip': cip}
    r = requests.post('http://pi.lmhaoye.com/pi/ip', data=postdata)
    logging.info(r.text)
    return r.text == 'ok'


def connect_dns():
    cip = ip()
    if not cip:
        return False

    req = DescribeDomainRecordInfoRequest.DescribeDomainRecordInfoRequest()
    req.set_RecordId(RID)
    resp = client.do_action_with_exception(req).decode('utf-8')
    update_pi(cip)
    logging.info(cip)
    old = json.loads(resp)
    if cip == old['Value']:
        return True
    else:
        return update_record(cip, old)


if __name__ == '__main__':
    connect_dns()
