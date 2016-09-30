# GitHub Users
`github-users` is a CLI that returns a list of users in a GitHub organization

## Example Usage
```
$ github-users krux -n name -n login -n location -h
Usage: github-users [OPTIONS] ORG_NAME

  Prints out a list of users in the given GitHub organization.

  If you want a quick list:
      github-users krux
  If you want it in CSV:
      github-users krux -f csv
  If you want it in a CSV file:
      github-users krux -f csv -o ~/tmp/users.csv
  If you want the user's location also:
      github-users krux -n name -n login -n location

Options:
  -t, --github-token TEXT         GitHub authentication token. If you don't
                                  have one, create one with `read:org`
                                  permission from here:
                                  https://github.com/settings/tokens. Can be
                                  also set as `GITHUB_TOKEN` environment
                                  variable.  [required]
  -f, --output-format [csv|json|pprint]
                                  The format in which you want the output.
                                  (default: pprint)
  -o, --output PATH               Path to the file in which the output will be
                                  written. If the file exists, it will be
                                  overwritten, not appended. If the file does
                                  not exist, it will be created. If not set,
                                  the output will be printed to stdout.
  -n, --field-names TEXT          List of fields to be written. Refer to https
                                  ://developer.github.com/v3/users/#response-1
                                  on the names of the fields. If invalid field
                                  is listed, the values will be all empty
                                  string.(default: ['name', 'login'])
  -h, --help                      Show this message and exit.
  ```
