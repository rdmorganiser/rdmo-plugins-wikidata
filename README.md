rdmo-plugins-wikidata
=====================

This plugin implements dynamic option set, that queries the Wikidata Search API at https://www.wikidata.org/w/api.php. See [Wikidata:Data_access](https://www.wikidata.org/wiki/Wikidata:Data_access) for more information about the different Wikidata endpoints. Please also note the access best practices on the same page.

Setup
-----

Install the plugin in your RDMO virtual environment using pip (directly from GitHub):

```bash
pip install git+https://github.com/rdmorganiser/rdmo-plugins-wikidata
```

Add the plugin to `OPTIONSET_PROVIDERS` in `config/settings/local.py`:

```python
OPTIONSET_PROVIDERS += [
    ('wikidata', _('Wikidata Provider'), 'rdmo_wikidata.providers.WikidataProvider')
]
```

The option set provider should now be selectable for option sets in your RDMO installation. For a minimal example catalog, see the files in `xml`.

Wikidata's policy asks to add a custom `User-Agent` to your requests so that they can perform statistical analyses and, if you add an email address, might contact you. This can be done by adding the following to your settings.

```python
WIKIDATA_PROVIDER_HEADERS = {
    'User-Agent': 'rdmo.example.com/0.0 (mail@rdmo.example.com) rdmo-plugins-wikidata/1.0'
}
```
