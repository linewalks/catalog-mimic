# Catalog
[![Build Status](https://travis-ci.com/linewalks/catalog-mimic.svg?branch=master)](https://travis-ci.com/linewalks/catalog-mimic)

MIMIC-III 데이터의 큐레이팅 프로젝트


## Config

* 가상환경 세팅

```
$ virtualenv -p python3.6 venv
$ pip install -r requirements.txt
```

* 데이터베이스 설정

```
$ cp catalog/config.default.py catalog/config.py
```

## Dev

* Git hook 설정    
Clean code를 위해 git hook에 PEP8 검사 루틴을 추가합니다.

```
$ vi .git/hooks/pre-commit
    #!/bin/sh 
    flake8 catalog tests
    gittyleaks --find-anything
$ chmod +x .git/hooks/pre-commit
```

## Test

```
$ pytest tests/
```
