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
      {% if unknown is not defined %}
      unknown is undefined
      {% elif unknown == "no" %}
      unknown is no
      {% endif %}
    params:
      unknown:
        variable: _.unknown
        optional: true
    description: calculation from an unknown variable
  mandatory: false
var2:
  description: a second variable
  hidden:
    jinja: |
      {% if condition is not defined %}
      condition is undefined
      {% elif condition == "no" %}
      condition is no
      {% endif %}
    params:
      condition:
        variable: _.condition
        optional: true
    description: calculation from an condition variable
  mandatory: false
```
# Variables

| Variable&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;   | Description&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;   |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **condition**<br/>[`string`](https://rougail.readthedocs.io/en/latest/variable.html#variables-types) `standard` `obligatoire`                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | A condition.<br/>**Défaut**: no                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| **var1**<br/>[`string`](https://rougail.readthedocs.io/en/latest/variable.html#variables-types) `standard` _`caché`_                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | A first variable.<br/>**Caché**: calculation from an unknown variable.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| **var2**<br/>[`string`](https://rougail.readthedocs.io/en/latest/variable.html#variables-types) `standard` _`caché`_                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | A second variable.<br/>**Caché**: calculation from an condition variable.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |


