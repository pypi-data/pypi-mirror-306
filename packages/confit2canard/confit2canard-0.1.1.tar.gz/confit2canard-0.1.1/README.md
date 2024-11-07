[![CircleCI](https://dl.circleci.com/status-badge/img/gh/dolead/confit2canard/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/dolead/confit2canard/tree/main) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/76833f3568f2479d8470a7320429cbfe)](https://app.codacy.com/gh/dolead/confit2canard/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)

# Confit2Canard 🦆

Minimalistic library to load settings from JSON and YAML files that also
provides configuration encryption with AES-GCM.

[The history of the confit de canard](https://en.wikipedia.org/wiki/Duck_confit).

## How to use

Configuration files written to a relative path:
```yaml
# app.yml
title: How to cook?
```

```yaml
# production/tokens.yml
api:
  token: AZERTY1234
```

```yaml
# production/secrets.yml
$Vault;UZXhoxTumLPE6zkT;kRg9bGtmKFn/BeFODX5+;zFgpPMrgxAaVQW6Wv5Q6Ow==
```

The script:

```python
# main.py
from confit2canard import Config

passkey = "ThisIsSupposedToBeAKey0000000000"
configuration_files = ["app.yml",
                       "production/tokens.yml",
                       "production/secrets.yml"]
configuration = Config(configuration_files, passkey=passkey)

print(configurgation.title)
print(configurgation.find("api.token"))
```

The configuration files can be JSON or YAML.

## Command line tool

The `VAULT_PASSKEY` environment variable must be set to write encrypted
configuration with a AES-GCM key:

```shell
VAULT_PASSKEY="ThisIsSupposedToBeAKey0000000000" python \
  -m confit2canard production/secrets.yml
```
