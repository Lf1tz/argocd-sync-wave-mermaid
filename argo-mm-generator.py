import os
import yaml

# Directory containing your Kubernetes manifests
base_manifests_dir = '/app/tmp/argocd/kustomize'

# Dictionary to hold sync waves and their resources
sync_waves = {}

# Function to process each YAML file
def process_yaml_file(filepath):
    with open(filepath, 'r') as file:
        try:
            # Load all documents from a YAML file
            docs = yaml.safe_load_all(file)
            for doc in docs:
                if doc and 'metadata' in doc:
                    wave = '1'  # Default sync wave
                    if 'annotations' in doc['metadata'] and 'argocd.argoproj.io/sync-wave' in doc['metadata']['annotations']:
                        wave = doc['metadata']['annotations']['argocd.argoproj.io/sync-wave']
                    name = doc['metadata']['name']
                    kind = doc['kind']
                    
                    # Add the resource to the appropriate sync wave
                    if wave not in sync_waves:
                        sync_waves[wave] = []
                    sync_waves[wave].append(f"{kind}/{name}")
        except yaml.YAMLError as exc:
            print(f"Error processing {filepath}: {exc}")

# Recursively process all YAML files in the directory and subdirectories
for root, dirs, files in os.walk(base_manifests_dir):
    for filename in files:
        if filename.endswith('.yaml') or filename.endswith('.yml'):
            process_yaml_file(os.path.join(root, filename))

# Sort the sync waves by their wave number (convert keys to integers for sorting)
sync_waves_sorted = dict(sorted(sync_waves.items(), key=lambda item: int(item[0])))

# Generate the Mermaid diagram
mermaid_diagram = "graph TD\n"
for wave, resources in sync_waves_sorted.items():
    # Create a subgraph for each wave
    mermaid_diagram += f"    subgraph wave{wave} [\"Wave {wave}\"]\n"
    previous_resource_node = None
    for resource in resources:
        resource_node = resource.replace('/', '_').replace(' ', '_')
        mermaid_diagram += f"        {resource_node}[\"{resource}\"]\n"
        if previous_resource_node:
            # Connect resources within the same wave
            mermaid_diagram += f"        {previous_resource_node} --> {resource_node}\n"
        previous_resource_node = resource_node
    mermaid_diagram += "    end\n"

# Manually connect the last resource of one wave to the first resource of the next wave
last_resource_of_previous_wave = None
for wave, resources in sync_waves_sorted.items():
    first_resource_of_current_wave = resources[0].replace('/', '_').replace(' ', '_')
    if last_resource_of_previous_wave:
        mermaid_diagram += f"    {last_resource_of_previous_wave} --> {first_resource_of_current_wave}\n"
    last_resource_of_previous_wave = resources[-1].replace('/', '_').replace(' ', '_')

# Print the Mermaid diagram script
print(mermaid_diagram)