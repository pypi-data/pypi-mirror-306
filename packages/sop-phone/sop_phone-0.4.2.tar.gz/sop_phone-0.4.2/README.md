# NetBox - Sop-Phone plugin

> [NetBox](https://github.com/netbox-community/netbox) plugin to manage phone informations for each site.

## Installation

### Prerequisites

This plugin requires phonenumbers to work.

```bash
echo "phonenumbers" >> local_requirements.txt
```

### Auto-upgrade installation

Add the plugin to NetBox local_requirements
```bash
echo "sop-phone" >> local_requirements.txt
```

Add the plugin to netbox/configuration.py
```python
PLUGINS = [
    ...
    'sop-phone',
]
```

Run NetBox upgrade.sh script
```bash
sudo ./upgrade.sh
```

## Features

This plugin provides the following features:
-   Add a new "**Phone**" tab in */dcim/sites/your_site_id*
-   Add a new item "**Phone**" in the navigation menu bar
-   A fast pattern phone-number search for every in-range numbers.

## Models

-   [**Phone Maintainer**](https://github.com/sop-it/sop-voice/tree/main/docs/phone-maintainer.md)
-   [**Phone Info**](https://github.com/sop-it/sop-voice/tree/main/docs/phone-info.md)
-   [**Phone Delivery**](https://github.com/sop-it/sop-voice/tree/main/docs/phone-delivery.md)
-   [**Phone DIDs**](https://github.com/sop-it/sop-voice/tree/main/docs/phone-dids.md)

## API

-   [**Phone API**](https://github.com/sop-it/sop-voice/tree/main/docs/api.md)

## UNIT-TESTS

This plugin has django unit-test in order to check its proper functioning as modifications are made.
To run the unit-test, it is recommended to add *django-test-without-migrations* in NetBox *local_requirements.txt*.

```bash
echo -e "django-test-without-migrations" >> local_requirements.txt
```

And run it like this:
```bash
python3 netbox/manage.py test -n sop_phone.tests
```

