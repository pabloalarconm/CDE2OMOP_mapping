# CDE2OMOP_mapping
Mapping activities dedicated to integrate CDE semantic model with OMOP CDM

## Introductions:

Execute `requirements.txt` to install all required Python modules.

Create a YAML file with ENDPOINT, USERNAME and PASSWORD to your Triplestore at `scripts` folder:

```yaml
TRIPLESTORE_URL: "https://YOUR/ENDPOINT/URL"
TRIPLESTORE_USERNAME: "YOURUSERNAME"
TRIPLESTORE_PASSWORD: "PASSWORDPLEASE"
```
Then, execute `cde2omop.py`. Resulting tables will be created at `data` folder.