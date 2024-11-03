# Plasted

[![Continuous Integration](https://github.com/mardiros/plasted/actions/workflows/tests.yml/badge.svg)](https://github.com/mardiros/plasted/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/mardiros/plasted/graph/badge.svg?token=gi0lEALVAo)](https://codecov.io/gh/mardiros/plasted)


Fix the problem to run an WSGI app configured with plaster using uwsgi.

uwsgi has many loaders, but it does not support plaster, only the old paste.ini
format.

Plasted

```bash
export PLASTER_URI=file+yaml://test.yaml
uwsgi -M --workers 1 --http 127.0.0.1:8000  --module pasted:app
```
