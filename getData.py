import dataiku


def get_data_from_dataiku(name):
    host = "https://ai-delfi-ing-hackathon.datascience.delfi.slb.com/"
    apiKey = "KQzhMgvVpsIF3ojSjeg12L9rdp9zdFAP"
    projectKey = "DEMO_HACKUNAMATATA"

    dataiku.set_remote_dss(host, apiKey, no_check_certificate=True)
    result = dataiku.Dataset(name, project_key=projectKey).get_dataframe()
    return result
