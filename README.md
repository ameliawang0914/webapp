# webapp
Node JS web app. Provides solution uses OPA to fix misconfiguration automatically during CI/CD stages.

## Required packages

Helm, Opa.

## Steps of Usage

```bash
helm template release ./webfrontendchart/ > rendered.yaml
yq eval -o=json rendered.yaml > rendered.json

# generate misconfiguration report
opa eval --input rendered.json --data policy.rego "data.kubernetes.admission.deny" -f pretty > misconfig_report.txt

# fix the rendered yaml report
python fix_misconfig.py
```
## Enhancement
Fix the value file and re-render and validate.
