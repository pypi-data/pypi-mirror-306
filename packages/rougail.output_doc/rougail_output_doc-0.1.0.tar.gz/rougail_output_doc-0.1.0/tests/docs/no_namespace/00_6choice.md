---
gitea: none
include_toc: true
---
# dictionaries/rougail/00-base.yml

```yaml
---
version: '1.1'
var1:
  description: the first variable
  choices:
    - a
    - b
    - c
var2:
  description: the second variable
  choices:
    - a
    - b
    - c
var3:
  description: the third variable
  choices:
    - a
    - b
    - c
  mandatory: false
var4:
  description: the forth variable
  choices:
    - 
    - b
    - c
  mandatory: false
var5:
  description: the fifth variable
  choices:
    - a
    - b
    - c
  default: a
var6:
  description: the sixth variable
  choices:
    - 1
    - 2
    - 3
  default: 1
```
# Variables

| Variable&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;   | Description&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;   |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **var1**<br/>[`choice`](https://rougail.readthedocs.io/en/latest/variable.html#variables-types) `basic` `obligatoire`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | The first variable.<br/>**Choix**: <br/>- a<br/>- b<br/>- c                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| **var2**<br/>[`choice`](https://rougail.readthedocs.io/en/latest/variable.html#variables-types) `basic` `obligatoire`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | The second variable.<br/>**Choix**: <br/>- a<br/>- b<br/>- c                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| **var3**<br/>[`choice`](https://rougail.readthedocs.io/en/latest/variable.html#variables-types) `standard`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | The third variable.<br/>**Choix**: <br/>- a<br/>- b<br/>- c<br/>- null                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| **var4**<br/>[`choice`](https://rougail.readthedocs.io/en/latest/variable.html#variables-types) `standard`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | The forth variable.<br/>**Choix**: <br/>- null<br/>- b<br/>- c                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| **var5**<br/>[`choice`](https://rougail.readthedocs.io/en/latest/variable.html#variables-types) `standard` `obligatoire`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | The fifth variable.<br/>**Choix**: <br/>- a ← (defaut)<br/>- b<br/>- c                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| **var6**<br/>[`choice`](https://rougail.readthedocs.io/en/latest/variable.html#variables-types) `standard` `obligatoire`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | The sixth variable.<br/>**Choix**: <br/>- 1 ← (defaut)<br/>- 2<br/>- 3                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |


