# <u>OlxCrawler</u>

### Table of contents
1. [Database](#1-database)
2. [Start application](#2-start-application)
   1. [Local](#21-local)
   2. [Prod](#22-prod)

## 1. Database
Create a Docker MySQL Database by running
``` shell
sh database/create-mysql-db-local.sh
```

## 2. Start application

### 2.1 Local

```shell
python olxcrawler/manage.py runserver --settings=olxcrawler.settings.local --noreload 
```

No reload is needed due to debug mode configured to `True` for local environment. Otherwise the tasks will be executed
twice which leads to database conflicts. When using Pycharm simply press the green arrow left to the prompt.

### 2.2 Prod

TODO: Describe when docker is configured

