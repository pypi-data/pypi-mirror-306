---
gitea: none
include_toc: true
---
# dictionaries/rougail/00-base.yml

```yaml
---
version: '1.1'
network_address_eth0:
  description: Network address
  type: network
netmask_address_eth0:
  description: Network address
  type: netmask
ip_address:
  description: an IP
  type: ip
  validators:
    - type: jinja
      jinja: |
        {% if not _.ip_address | valid_in_network(_.network_address_eth0, _.netmask_address_eth0) %}
        {{ _.ip_address }} is not in network {{ _.network_address_eth0 }}/{{ _.netmask_address_eth0 }}
        {% endif %}
      description: check if IP in the previous network
```
# Variables

| Variable&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;   | Description&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;   |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **network_address_eth0**<br/>[`network`](https://rougail.readthedocs.io/en/latest/variable.html#variables-types) `basic` `mandatory`                                                                                                                                                                                                                                                                                                                                                                                                                                         | Network address.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| **netmask_address_eth0**<br/>[`netmask`](https://rougail.readthedocs.io/en/latest/variable.html#variables-types) `basic` `mandatory`                                                                                                                                                                                                                                                                                                                                                                                                                                         | Network address.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| **ip_address**<br/>[`IP`](https://rougail.readthedocs.io/en/latest/variable.html#variables-types) `basic` `mandatory`                                                                                                                                                                                                                                                                                                                                                                                                                                                        | An IP.<br/>**Validators**:<br/>- reserved IP are allowed<br/>- check if IP in the previous network.                                                                                                                                                                                                                                                                                                                                                                                                                                                           |


# Example with mandatory variables not filled in

```yaml
---
network_address_eth0: 1.1.1.0
netmask_address_eth0: 255.255.255.0
ip_address: 1.1.1.1
```
# Example with all variables modifiable

```yaml
---
network_address_eth0: 1.1.1.0
netmask_address_eth0: 255.255.255.0
ip_address: 1.1.1.1
```
