# snyk-gc-projects
Python script to delete old, stale projects

## Usage
If you have old projects which are no longer receiving updates and you don't want them to appear in you Snyk account, use this script.

```
python3 snyk-gc-projects.py --help
usage: python3 snyk-gc-projects.py [-h] [-o ORG_ID] [-t API_TOKEN] [-a AGE] [-d] [-v]

Scan a Snyk Org for projects and optionally delete any which have not been updated recently

options:
  -h, --help            show this help message and exit
  -o ORG_ID, --org_id ORG_ID
  -t API_TOKEN, --api_token API_TOKEN
  -a AGE, --age AGE     Set the age in days to be considered stale if lastTestedDate is older
  -d, --delete          Delete stale projects
  -v, --verbose         Print API calls
```

## Arguments

The script takes two required arguments - your Snyk API token and Org Id.

These can be supplied either as environment variables:
```
export SNYK_API_TOKEN=<your token>
export SNYK_ORG_ID=<your orgid>
```

Or passed on the command-line:
```
python3 snyk-gc-projects -t API_TOKEN -o ORG_ID

python3 snyk-gc-projects --api-token API_TOKEN --org_id ORG_ID
```

Specify the age in days at which a project will be considered stale by setting `-a` or `--age`.

By default nothing will actually be done. To force deletion supply the `-d` or `--delete` flag.

The `-v` or `--verbose` flag will cause the API calls to be printed along with additional debugging information.
