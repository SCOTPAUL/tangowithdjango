import json
import urllib2
import keys

BING_API_KEY = keys.BING_API_KEY


def run_query(search_terms):
    # Base URL
    root_url = 'https://api.datamarket.azure.com/Bing/Search/'
    source = 'Web'

    results_per_page = 10
    offset = 0

    # Wrap search terms in quotation marks and make URL safe
    query = urllib2.quote("'{0}'".format(search_terms))

    # The full URL, giving results in JSON with parameters above
    search_url = "{0}{1}?$format=json&$top={2}&$skip={3}&Query={4}".format(
        root_url,
        source,
        results_per_page,
        offset,
        query)

    # Used for authenticating with Bing servers
    username = ''

    # Authentication handler
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, search_url, username, BING_API_KEY)

    # List of search results
    results = []

    try:
        # Prepare for connection to Bing's servers
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)

        # Connect to Bing server and read the response given
        response = urllib2.urlopen(search_url).read()

        # Convert JSON response to python dictionary
        json_response = json.loads(response)

        # Populate results list
        for result in json_response['d']['results']:
            results.append({
                'title': result['Title'],
                'link': result['Url'],
                'summary': result['Description']})

    except urllib2.URLError as e:
        print "Error when querying the Bing API: " + e

    return results
