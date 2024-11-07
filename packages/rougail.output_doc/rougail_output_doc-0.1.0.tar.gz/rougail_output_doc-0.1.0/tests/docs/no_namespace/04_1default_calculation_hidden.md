---
gitea: none
include_toc: true
---
# dictionaries/rougail/00-base.yml

```yaml
---
version: 1.1

var1:
  description: a first variable
  default: value

var2:
  description: a second variable
  disabled:
    variable: _.var1
    when: value

var3:
  description: a third variable
  default:
    jinja: |
      {% if _.var1 == 'value' or _.var2 == 'blah' %}
      value
      {% endif %}
```
# Variables

| Variable&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;   | Description&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;   |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **var1**<br/>[`string`](https://rougail.readthedocs.io/en/latest/variable.html#variables-types) `standard` `obligatoire`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | A first variable.<br/>**Défaut**: value                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| **var2**<br/>[`string`](https://rougail.readthedocs.io/en/latest/variable.html#variables-types) `basic` `obligatoire` _`désactivé`_                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | A second variable.<br/>**Désactivé**: when the variable "var1" has the value "value".                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| **var3**<br/>[`string`](https://rougail.readthedocs.io/en/latest/variable.html#variables-types) `standard` `obligatoire`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | A third variable.<br/>**Défaut**: depends on a calculation.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |


