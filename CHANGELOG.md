# Changelog

## 0.2 (2018-07-20)
- Remove `mara print_config` command (moved to mara-config package).
- Allow for click.Group packages to keep their original name. 
  This allows for packages to set a shorter name and provide the 
  rest of their commands as subcommands. This should be used 
  sparingly, as this has the danger of submitting two 
  subcommands under the same name (which results in a 
  `RuntimeError`)
- Remove the '--log-to-syslog' option (was unused)

## Required changes:
* Adjust scripts which used `mara print_config` to use 
  `mara config print`.

## 0.1.1 (2018-07-09)

- Adjust to mara-config changes by using
  `init_mara_config_once()` instead of our own code.


## 0.1.0 (2018-05-22)

- Initial version with this functionality:
  - `mara` commandline app
  - `mara print_config` subcommand
- automatically upload tags to pypi

