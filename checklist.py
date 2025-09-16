#!/usr/bin/env python3
import re
import sys

mandatory_sections = [
    "Tracker",
    "Documentation",
    "Tests",
]
check_chars = [
    'x',
]
section_re = re.compile(r'^- ([^(]+)( \(.+)?$')
item_re = re.compile(r'^  - \[(.+)\] (.+)$')

def parse(data):
    lines = data.split('\n')
    saw_checklist = False
    section = None
    section_checks = {}
    success = True
    for line in lines:
        if line == "## Checklist":
            saw_checklist = True
            continue

        if match := re.match(section_re, line):
            section = match.groups()[0]
            assert section not in section_checks
            section_checks[section] = 0
            if section in mandatory_sections:
                print(f"Saw mandatory section {section}")
            else:
                print(f"Saw optional section {section}")
        elif match := re.match(item_re, line):
            maybe_check = match.groups()[0].strip().lower()
            if maybe_check in check_chars:
                print(f"  Item is checked: {match.groups()[1]}")
                section_checks[section] += 1
        elif saw_checklist:
            break

    for section in mandatory_sections:
        if section_checks.setdefault(section, 0) == 0:
            print(f"Error: section {section} must have at least one item checked")
            success = False
    return 0 if success else 1

def main():
    data = sys.stdin.read()
    sys.exit(parse(data))

if __name__ == "__main__":
    main()
