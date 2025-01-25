# Wiki

A personal wiki with various stuff.

Source files are in [`./sources`](./sources/). They are raw markdown files meant to be used in almost all platforms that can handle markdown files. I try to not use any markdown extensions so that the files are portable.

Right now the wiki is built using [Vitepress](https://vitepress.dev).

File pre-processing is done using the `main.py` script that will process all the markdown files to make them compatible with Vitepress and to leverage as much as possible this framework.

## Building the wiki

To process the source files, run:

```shell
make build-sources
```

To build the static files using Vitepress, run:

```shell
make build-static
```

To build everything (ie. process the source files and build the static), run:

```shell
make build
```

All the available command can be listed by running:

```shell
make help
```
