from SPARQLWrapper import SPARQLWrapper, POST, BASIC, CSV
import sys


class ServerConection:

    def setCredentials(configuration_file):


        TRIPLESTORE_URL = configuration_file["TRIPLESTORE_URL"]
        TRIPLESTORE_USERNAME = configuration_file["TRIPLESTORE_USERNAME"]
        TRIPLESTORE_PASSWORD = configuration_file["TRIPLESTORE_PASSWORD"]

        TRIPLESTORE = { "TRIPLESTORE_URL" : TRIPLESTORE_URL ,
                        "TRIPLESTORE_USERNAME": TRIPLESTORE_USERNAME,
                        "TRIPLESTORE_PASSWORD" : TRIPLESTORE_PASSWORD}
        if not TRIPLESTORE_URL:
            sys.exit("No endpoint defined at configuration file, please create a TRIPLESTORE parameter at your configuration file .yaml")

        return TRIPLESTORE
    
    def queryConection(triplestore_conection):

        # Query configuration
        ENDPOINT = SPARQLWrapper(triplestore_conection["TRIPLESTORE_URL"])
        ENDPOINT.setHTTPAuth(BASIC)
        ENDPOINT.setCredentials(triplestore_conection["TRIPLESTORE_USERNAME"], triplestore_conection["TRIPLESTORE_PASSWORD"])
        ENDPOINT.setMethod(POST)
        ENDPOINT.setReturnFormat(CSV)

        return ENDPOINT
