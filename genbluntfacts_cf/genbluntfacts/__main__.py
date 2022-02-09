import argparse
import json
from genbluntfacts.gen_blunt_facts import gen_blunt_facts

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate information about a strain')
    parser.add_argument('-s', '--strain', help='Name of strain to generate for',required=True)
    args = parser.parse_args()

    print(json.dumps(gen_blunt_facts(args.strain), indent=4))
