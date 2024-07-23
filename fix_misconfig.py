import yaml
from ruamel.yaml import YAML

def parse_opa_output(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip('[]\n ').split(',')

def fix_rendered_yaml(file_path):
    with open(file_path, 'r') as file:
        documents = yaml.safe_load_all(file)
        fixed_documents = []
        for doc in documents:
            if doc['kind'] == 'Deployment':
                containers = doc['spec']['template']['spec']['containers']
                for container in containers:
                    if 'securityContext' not in container:
                        container['securityContext'] = {}
                    container['securityContext']['runAsNonRoot'] = True
            fixed_documents.append(doc)

    with open(file_path, 'w') as file:
        yaml.safe_dump_all(fixed_documents, file)

def fix_values_yaml(file_path):
    yaml = YAML()
    yaml.preserve_quotes = True

    with open(file_path, 'r') as file:
        values = yaml.load(file)
        
    if 'securityContext' not in values:
        values['securityContext'] = {}
    values['securityContext']['runAsNonRoot'] = True

    with open(file_path, 'w') as file:
        yaml.dump(values, file)

def main():
    opa_output = parse_opa_output('misconfig_report.txt')
    for msg in opa_output:
        if "must not run as root" in msg:
            fix_rendered_yaml('rendered.yaml')
            fix_values_yaml('./webfrontendchart/values.yaml')
            print("Fixed: runAsNonRoot set to true in rendered.yaml and values.yaml")

if __name__ == "__main__":
    main()
