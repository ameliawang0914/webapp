import yaml

def parse_opa_output(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip('[]\n ').split(',')

def fix_deployment(file_path):
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

def main():
    opa_output = parse_opa_output('misconfig_report.txt')
    for msg in opa_output:
        if "must not run as root" in msg:
            fix_deployment('rendered.yaml')
            print("Fixed: runAsNonRoot set to true in rendered.yaml")

if __name__ == "__main__":
    main()
