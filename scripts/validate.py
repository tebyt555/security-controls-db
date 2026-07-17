import os
import sys
import yaml
import json
import frontmatter
from jsonschema import validate, ValidationError

with open('schemas/control-schema.json', 'r') as f:
    schema = json.load(f)

errors = 0

for root, dirs, files in os.walk('controls'):
    for file in files:
        if file.endswith('.md'):
            filepath = os.path.join(root, file)
            post = frontmatter.load(filepath)
            try:
                # Validate the extracted YAML against the JSON schema
                validate(instance=post.metadata, schema=schema)
                print(f"✅ PASS: {filepath}")
            except ValidationError as e:
                print(f"❌ FAIL: {filepath}\n   Reason: {e.message}")
                errors += 1

if errors > 0:
    sys.exit(1)