---
gitea: none
include_toc: true
---
# dictionaries/rougail/00-base.yml

```yaml
---
version: '1.1'
condition: no    # a condition
var1:
  description: a first variable
  hidden:
    jinja: |
      {% if _.condition != "yes" %}
      condition is yes
      {% endif %}
    description: if condition is yes
  default:
    jinja: |
      {{ _.condition }}
    description: the value of condition
var2:
  description: a second variable
  hidden:
    jinja: |
      {% if rougail.condition != "yes" %}
      condition is yes
      {% endif %}
    description: if condition is yes
  default:
    jinja: |
      {{ rougail.condition }}
    description: the value of condition
```
# Variables pour "rougail"

| Variable&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;   | Description&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;   |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **rougail.condition**<br/>[`string`](https://rougail.readthedocs.io/en/latest/variable.html#variables-types) `standard` `obligatoire`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | A condition.<br/>**Défaut**: no                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| **rougail.var1**<br/>[`string`](https://rougail.readthedocs.io/en/latest/variable.html#variables-types) `standard` `obligatoire` _`caché`_                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | A first variable.<br/>**Défaut**: the value of condition.<br/>**Caché**: if condition is yes.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| **rougail.var2**<br/>[`string`](https://rougail.readthedocs.io/en/latest/variable.html#variables-types) `standard` `obligatoire` _`caché`_                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | A second variable.<br/>**Défaut**: the value of condition.<br/>**Caché**: if condition is yes.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |


