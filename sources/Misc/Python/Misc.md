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
