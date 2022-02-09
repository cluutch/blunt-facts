import logging
import requests
from genbluntfacts.known_tags import STRAIN_TYPES, STRAIN_AROMAS, STRAIN_FEELINGS, IGNORE_TAGS
import google.cloud.logging

logging_client = google.cloud.logging.Client()
logging_client.setup_logging()

STRAIN_TYPE = 'strain_type'
STRAIN_AROMA = 'strain_aroma'
STRAIN_FEELING = 'strain_feeling'
STRAIN_OTHER_ATTRIBUTES = 'strain_other_attributes'
STRAIN_INFO_CLASSIFICATIONS = [
    {'category': STRAIN_TYPE, 'options': STRAIN_TYPES},
    {'category': STRAIN_AROMA, 'options': STRAIN_AROMAS},
    {'category': STRAIN_FEELING, 'options': STRAIN_FEELINGS}
  ]


def get_total_for_options(options, strain_json):
    # count total
    def count_for_option(option):
        try:
            return int(strain_json["is_" + option])
        except Exception:
            logging.exception(f"Could not process {strain_json}")
            return 0

    option_counts = list(map(count_for_option, options))
    return sum(option_counts)


def mutate_strain_json_to_percentages(strain_json, category, options, total):
    strain_json[category] = {}
    for option in options:
        pct = int(strain_json['is_' + option]) / total
        pct = round(pct * 100, 2)
        del strain_json['is_' + option]
        strain_json[category][option] = pct

    best_match = max(strain_json[category], key=strain_json[category].get)
    best_pct = str(round(strain_json[category][best_match]))
    strain_json[category]['best'] = best_match.title() + ": " + best_pct +  "%"


def strip_whitespace(tag):
    return tag.strip()


def get_sanitized_tags(strain_json):
    def filter_irrelevant_tags(tag):
        irrelevant_tags = STRAIN_TYPES + \
                          STRAIN_AROMAS + \
                          STRAIN_FEELINGS + \
                          IGNORE_TAGS

        return tag not in irrelevant_tags and \
            strain_json['strain'] not in tag

    tags = strain_json['tags']
    tags = tags.lower()
    tags = tags.split(';')
    tags = map(strip_whitespace, tags)
    tags = list(filter(filter_irrelevant_tags, tags))
    return tags


def update_strain_other_attributes(strain_json, tags):
    for tag in tags:
        if tag not in strain_json[STRAIN_OTHER_ATTRIBUTES]:
            strain_json[STRAIN_OTHER_ATTRIBUTES][tag] = 1
        else:
            strain_json[STRAIN_OTHER_ATTRIBUTES][tag] += 1


def mutate_tags_to_percentages(strain_json, total):
    for tag in strain_json[STRAIN_OTHER_ATTRIBUTES].keys():
        pct = int(strain_json[STRAIN_OTHER_ATTRIBUTES][tag]) / total
        pct = round(pct * 100, 2)
        strain_json[STRAIN_OTHER_ATTRIBUTES][tag] = pct

    best_match = max(strain_json[STRAIN_OTHER_ATTRIBUTES], key=strain_json[STRAIN_OTHER_ATTRIBUTES].get)
    best_pct = str(round(strain_json[STRAIN_OTHER_ATTRIBUTES][best_match]))
    strain_json[STRAIN_OTHER_ATTRIBUTES]['best'] = best_match.title() + ": " + best_pct +  "%"


def process_other_tags(strain_json):
    strain_json[STRAIN_OTHER_ATTRIBUTES] = {}
    tags = get_sanitized_tags(strain_json)
    update_strain_other_attributes(strain_json, tags)
    del strain_json['tags']
    total_listings_for_option = len(tags)
    mutate_tags_to_percentages(strain_json, total_listings_for_option)


def process_strain_json(strain_json):
    for classification in STRAIN_INFO_CLASSIFICATIONS:
        logging.info(f"Processing classification {classification}")
        category = classification['category']
        options = classification['options']

        total_listings_for_option = get_total_for_options(options, strain_json)
        mutate_strain_json_to_percentages(strain_json, category, options, total_listings_for_option)

    logging.info("Processing other tags")
    process_other_tags(strain_json)
    return strain_json


def get_strain_json(strain: str):
    params = {'strain': strain}
    logging.info(f"Requesting info about strain {strain}")
    return requests.get('https://us-central1-cluutch.cloudfunctions.net/get-strain-info', params=params).json()


def gen_blunt_facts(strain: str):
    strain_json = get_strain_json(strain)
    return process_strain_json(strain_json)


        errors = []
        if self.ADD_GATEWAY_TXN_NAME_KEY in self.keys():
            if self.ADD_GATEWAY_TXN_PAYLOAD_KEY not in self.keys():
Write Preview
 
Attach files by dragging & dropping, selecting or pasting them.
Add review comment
Cancel
                return [self.ADD_GATEWAY_TXN_PAYLOAD_KEY]

            txn_payload = self.get(self.ADD_GATEWAY_TXN_PAYLOAD_KEY, {})
            if not txn_payload:
                return self.ADD_GATEWAY_TXN_PAYLOAD_CONTENT_KEYS

            for key in self.ADD_GATEWAY_TXN_PAYLOAD_CONTENT_KEYS:
                if key not in txn_payload or \
                        txn_payload[key] is None \
                        or txn_payload[key] == '':