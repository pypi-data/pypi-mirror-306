# blade
This is a web scraper python lib currently used by Indexit project.

# Set up

## build image, run and enter container
```
bash scripts/start_dev.sh
```
##  function test
using ipython inside docker container to do functiont test.

## upload new version
1. bump version in setup.py
2. python3 setup.py sdist
3. python3 -m twine upload --repository pypi dist/*
