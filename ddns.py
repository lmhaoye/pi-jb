import requests
import json

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109 import UpdateDomainRecordRequest, DescribeDomainRecordInfoRequest

DOMAIN = 'lmhaoye.com'
RID = '3816854167196672'

client = AcsClient(
    "LTAIgx4gRwOdGDyP",
    "lhO72l4zvD3C8prI1aWcfCROXdCrmX",
    "cn-hangzhou"
)


def ip():
    r = requests.get('http://pi.lmhaoye.com/get/ip')
    if r.status_code == 200:
        return r.text
    else:
        return None


def update_record(cip, old):
    update_pi(cip)
    req = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
    req.set_RecordId(RID)
    req.set_RR(old['RR'])
    req.set_Type(old['Type'])
    req.set_Value(cip)
    resp = client.do_action_with_exception(req)
    print(resp)
    return True


def update_pi(cip):
    postdata = {'ip': cip}
    r = requests.post('http://pi.lmhaoye.com/pi/ip', data=postdata)
    print(r.text)
    return r.text == 'ok'


def connect_dns():
    cip = ip()
    if not cip:
        return False

    req = DescribeDomainRecordInfoRequest.DescribeDomainRecordInfoRequest()
    req.set_RecordId(RID)
    resp = client.do_action_with_exception(req).decode('utf-8')
#    update_pi(cip)
    print(cip)
    old = json.loads(resp)
    if cip == old['Value']:
        return True
    else:
        return update_record(cip, old)


if __name__ == '__main__':
    connect_dns()
