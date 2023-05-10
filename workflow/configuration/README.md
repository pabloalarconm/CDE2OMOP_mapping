# Configuration requirements:

Create a YAML file named `config.yaml` at this location (`workflow/configuration`)

YAML must required endpoint and credentials for accessing the triplestore used to obtain the data. 

exemplar config.yaml file:

```yaml
TRIPLESTORE_URL: "https://YOUR/ENDPOINT/URL"
TRIPLESTORE_USERNAME: "YOURUSERNAME"
TRIPLESTORE_PASSWORD: "PASSWORDPLEASE"
```

This webservice will search this location and this filename for the credentials.