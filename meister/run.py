from time import sleep
from os import environ as ENV
from requests.exceptions import RequestException
from .cgc_client.api import API as CgcAPI
from .schedulers import AFLScheduler
from farnsworth_client.api import API as ProfAPI
from farnsworth_client.models import ChallengeBinaryNode

def run():
    cgc = CgcAPI(ENV['CGC_API_URL'], ENV['CGC_API_USER'], ENV['CGC_API_PASS'])
    prof_url = "http://{}:{}".format(ENV['FARNSWORTH_SERVICE_HOST'], ENV['FARNSWORTH_SERVICE_PORT'])
    ProfAPI.init(prof_url)

    while True:
        try:
            round_n = cgc.status()['round']
            print "[Meister] Round # %s" % round_n
            binaries = cgc.binaries(round_n)['binaries']
            for binary in binaries:
                cbn = ChallengeBinaryNode.find_or_create_by(
                    name = binary['cbid'],
                    blob = binary['data'],
                    parent_id = None
                )
                AFLScheduler().schedule(cbn = cbn, cpus = 4, memory = 1)

        except RequestException as ex:
            print "[Meister] ERROR: %s" % type(ex)
            pass

        sleep(3)