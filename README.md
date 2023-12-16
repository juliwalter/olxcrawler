# <u>OlxCrawler</u>

### Table of contents

1. [Overview](#1-overview)
2. [Start application](#2-start-application)
    1. [Local](#21-local)
    2. [Prod](#22-prod)

## 1. Overview

This application allows the user to store search request for cars on the
website https://www.olx.pt/carros-motos-e-barcos/carros/ and crawl the prices for the given request, either by
configuring scheduled task or triggered manually. In addition, the user is able to visualize the results over time
in form of a price time series.

## 2. Start application

### 2.1 Local

Create a Docker MySQL Database by running

``` shell
sh database/create-mysql-db-local.sh
```

Then run

```shell
python olxcrawler/manage.py runserver --settings=olxcrawler.settings.local --noreload 
```

`--noreload` is required due to debug mode configured to `True` for local environment, otherwise the tasks will be
executed
twice which leads to database conflicts.

### 2.2 Prod

TODO: Describe when docker is configured

