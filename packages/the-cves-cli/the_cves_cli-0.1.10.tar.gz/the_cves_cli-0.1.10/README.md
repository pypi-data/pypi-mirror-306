# Installation instructions
## Prerequisities 
- Python 3.12 or higher
- UV CLI


### Once the cli is published to PyPi, install it using pip:
```pip install the_cves_cli```
### Otherwise meanwhile one needs to clone the repo, build and install from local: 
1. ```uv build```
2. Install it from local
``` uv pip install /Users/user/the-cves/dist/the_cves_cli-0.1.1-py3-none-any.whl```

### Running the CLI
```the-cves-cli  --help```

### Env variables required
```shell
THE_CVES_CLI_HOST=<host of the cves backend>
THE_CVES_CLI_USERNAME=<user name of the app>
THE_CVES_CLI_API_KEY=<the cves app token>
THE_CVES_CLI_CONFLUENCE_DOMAIN=<confluence domain>
THE_CVES_CLI_CONFLUENCE_TOKEN=<confluence token>
THE_CVES_CLI_CONFLUENCE_USER=<confluence user>
```

example for cli commands:
running a new CVE report (from the repo root path):
```shell
PYTHONPATH=$(pwd) python the_cves_cli/the_cves_cli/main.py run_report <product-id> <release-id> <confluence-space-key> --image-id=<image-id-value> --cve=<cve-value>

```

