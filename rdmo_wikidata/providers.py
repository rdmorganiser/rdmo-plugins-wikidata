import re

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
            response = requests.get(
                f'{url}/search',
                params={
                    'action': 'query',
                    'list': 'search',
                    'srsearch': self.get_search(search),
                    'srprop': 'titlesnippet|snippet',
                    'format': 'json',
                },
                headers=headers,
            )

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
                            'id': self.get_id(item),
                            'text': self.get_text(item)
                        } for item in items
                    ]

        # return an empty list by default
        return []

    def get_id(self, item):
        return item['title']

    def get_text(self, item):
        wd_id = item['title']

        wd_text = ''
        if item.get('titlesnippet'):
            wd_text += strip_tags(item['titlesnippet'])
        if item.get('snippet'):
            wd_text += f' ({strip_tags(item['snippet'])})'

        wd_link = f'<a href="https://www.wikidata.org/wiki/{wd_id}">{wd_id}</a>'
        return f'{wd_text} [{wd_link}]'

    def get_search(self, search):
        # reverse get_text to perform the search, remove everything after (
        match = re.match(r'^[^([]+', search)
        if match:
            tokens = match[0].split()
        else:
            tokens = search.split()

        return '+AND+'.join(tokens)
