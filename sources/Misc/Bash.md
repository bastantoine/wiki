Random bash tips and tricks to (_try to_) use Bash properly and efficiently...

# Loops

To iterate over a sequence of numbers:

1. With a know fixed upper limit
    ```bash
    for i in {1..5}; do
        echo $i;
    done
    ```

2. With a possibly unknown upper limit
    ```bash
    END=5
    for i in $(seq 1 $END); do
        echo $i;
    done
    ```

3. If `seq` can't be used
    ```bash
    END=5
    for ((i=1;i<=END;i++)); do
        echo $i
    done
    ```

[\[ref\]](https://stackoverflow.com/questions/169511/how-do-i-iterate-over-a-range-of-numbers-defined-by-variables-in-bash)

# Tar archives manipulation

## Listing content

To list the content of an archive without extracting, use the `--list`/`-t` option:

```bash
tar --list --file <my-archive.tar>
tar -tf <my-archive.tar>
```

## Creating archives

To create an archive, use the `--create`/`-c` option:

```bash
tar --create --file <my-archive.tar> <file1> <dir1>
tar -cf <my-archive.tar> <file1> <dir1>
```

## Extracting the content

To extract the files of an archive, use the `--extract`/`-x` option:

```bash
tar --extract --file <my-archive.tar>
tar -xf <my-archive.tar>
```

This will extract all the content of the archive in the current folder

To extract in a different folder:

```bash
tar -xf <my-archive.tar> -C </my/folder>
```

*Note:* the folder needs to exists first.

To extract only specific files:

```bash
tar -xf <my-archive.tar> <file1> <dir1>
```

*Note:* The name of the files and/or dirs to extract must be the same as listed using the `--list` option.

## Other

To manipulate `.tar.gz` archives, add the `-z` option to all commands.

By default, all commands will read from `stdin` or write to `stdout`, allowing incoming and outgoing piping. To read to or from an existing archive, use the `--file`/`-f` option.

# `Here documents`

`Here documents` (or `heredocs`) are a way to provide multiline input directly to a command or script. The syntax is the following:

```shell
COMMAND <<DELIMITOR
...
...
DELIMITOR
```

`DELIMITOR` is used to control when to start and stop the input. It can be any string without spaces, and should then be choosed wiselly so that it won't apear in the input:

```shell
$ cat <<ThisIsADelimitor
Hello
There
ThisIsADelimitor
Hello
There
$ cat <<1
Hello
There
1
Hello
There
```

`Heredocs` allows for parameter expansion as well:

```shell
$ export FIRSTNAME='Obi-Wan'
$ export LASTNAME='Kenobi'
$ cat <<EOF
Hello $FIRSTNAME $LASTNAME
EOF
Hello Obi-Wan Kenobi
```

Default behavior of the `heredocs` is to preserve the leading tabs:

```shell
$ cat <<EOF
        hello
there
EOF
    hello
there
```

You can strip them by prefixing the delimitor with a dash:

```shell
$ cat <<-EOF
        hello
there
EOF
hello
there
```

This will strip all leading tabs, allowing the input to be more readable visually.

Note though that this strips only leading tabs, but not spaces.

# Showing disk usage

To show disk usage, you can use `df` and `du`:

1. To show free space over all mounted drives:
   ```shell
   df -h
   ```

2. To check the size of a directory:
   ```shell
   du -sh /path/to/directory
   ```

3. To list sizes of all subdirectories:
   ```shell
   du -h --max-depth=1 /path/to/directory
   ```
