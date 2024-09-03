from django.conf import settings
from django.utils.html import strip_tags

import dpath
import requests

from rdmo.options.providers import Provider


class WikidataProvider(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):
        if search:
            url = getattr(settings, 'WIKIDATA_PROVIDER_URL', 'https://www.wikidata.org/w/api.php')
            headers = getattr(settings, 'WIKIDATA_PROVIDER_HEADERS', {})
            response = requests.get(f'{url}/search', params={
                'action': 'query',
                'list': 'search',
                'srsearch': search,
                'srprop': 'titlesnippet|snippet',
                'format': 'json'
            }, headers=headers)

            try:
                data = response.json()
            except requests.exceptions.JSONDecodeError:
                pass
            else:
                try:
                    items = dpath.get(data, 'query/search')
                except KeyError:
                    pass
                else:
                    return [
                        {
                            'id': item['title'],
                            'text': strip_tags('{titlesnippet} ({snippet}) [{title}]'.format(**item))
                        } for item in items
                    ]

        # return an empty list by default
        return []
