Random tips and tricks when dealing with Python

## `No space left on device` when installing dependencies

Set the `TMPDIR` env var to a folder on a device with enough space.
Make sure the folder has been created beforehand.

```bash
export TMPDIR=$HOME/.piptmp
mkdir -p $TMPDIR
pip install ...
```
[\[src\]](https://stackoverflow.com/questions/40755610/ioerror-errno-28-no-space-left-on-device-while-installing-tensorflow)

## Serving files over HTTP

Python comes with a builtin HTTP server that can be used to serve files:

```bash
python -m http.server
```

Default behaviour is to bind on `0.0.0.0` and listen on `8000`, and serve the files in the current directory.

To change the bind address, use the `-b, --bind` option

```bash
python -m http.server --bind 127.0.0.1
```

To change the port it listens on, provide it as parameter:

```bash
python -m http.server 9000
```

To serve a specific folder, use the `-d, --directory` option:

```bash
python -m http.server --directory /tmp/
```

[\[src\]](https://docs.python.org/3/library/http.server.html#command-line-interface)

## Dump attributes and values of a given object

```python
def dump(obj):
    from pprint import pprint
    attrs = [attr for attr in dir(obj) if not attr.startswith("_")]
    res = {}
    for attr in attrs:
        try:
            value = getattr(obj, attr)
        except Exception as e:
            value = f"<Error retrieving attribute: {e}>"
        res[attr] = value
    pprint(res)
```
