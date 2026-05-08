import json
import os

DEFAULT_CONFIG = {
    "data_path": "data/resources.json",
    "default_language": "en"
}

def load_config(config_path="config.json"):
    """Load configuration from file, falling back to defaults."""
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            user_config = json.load(f)
        return {**DEFAULT_CONFIG, **user_config}
    return DEFAULT_CONFIG

class LibraryManager:
    def __init__(self, config=None):
        if config is None:
            config = load_config()
        self.config = config
        self.data_path = config["data_path"]
        self.default_lang = config.get("default_language", "en")
        self.resources = self.load_resources()

    def load_resources(self):
        try:
            with open(self.data_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def search_resources(self, query, category=None):
        """Search resources by name with optional category filtering."""
        results = [r for r in self.resources if query.lower() in r['name'].lower()]
        if category:
            results = [r for r in results if r.get('category') == category]
        return results

    def get_categories(self):
        """Return a list of all unique categories."""
        return list(set(r.get('category') for r in self.resources if r.get('category')))

    def get_string(self, key, lang=None):
        """Return a localized UI string for the given key and language."""
        if lang is None:
            lang = self.default_lang
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

if __name__ == "__main__":
    manager = LibraryManager()
    print(manager.search_resources('open'))