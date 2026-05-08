import json

class LibraryManager:
    def __init__(self, data_path):
        self.data_path = data_path
        self.resources = self.load_resources()

    def load_resources(self):
        try:
            with open(self.data_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def search_resources(self, query):
        return [r for r in self.resources if query.lower() in r['name'].lower()]

    def get_string(self, key, lang='en'):
        """Return a localized UI string for the given key and language."""
        strings = {
            'en': {
                'search': 'Search results for',
                'no_results': 'No results found',
                'add_success': 'Resource added successfully'
            },
            'sw': {
                'search': 'Matokeo ya utafutaji kwa',
                'no_results': 'Hakuna matokeo yaliyopatikana',
                'add_success': 'Rasilimali imeongezwa kwa mafanikio'
            }
        }
        return strings.get(lang, strings['en']).get(key, key)

    def add_resource(self, name, link, category):
        new_resource = {"name": name, "link": link, "category": category}
        self.resources.append(new_resource)
        self.save_resources()

    def save_resources(self):
        with open(self.data_path, 'w') as f:
            json.dump(self.resources, f, indent=4)