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

# Generating random strings

Few options:

- Random string of 12 base64 chars:
  ```
  openssl rand -base64 12
  ```

- Random string of 12 bytes in hexadecimal:
  ```
  openssl rand -hex 12
  ```

- Random string of 13 chars with only lower, uppercase letters and digits:
  ```
  tr -dc A-Za-z0-9 </dev/urandom | head -c 13; echo
  ```

[\[src\]](https://unix.stackexchange.com/questions/230673/how-to-generate-a-random-string)

# Run `nslookup` with full URL

`nslookup` only accepts FQDN, and not full URLs with scheme, path and query parameters. Below script parses a 

```bash
nslookup () {
    if [ "$1" = "" ]; then
        echo "Usage: nslookup <hostname>"
        return 1
    fi
    s=$(cat <<EOL
from urllib.parse import urlparse
url = ('http://' + r'$1') if (not r'$1'.startswith(('http://', 'https://'))) else r'$1'
print(urlparse(url).netloc.split(':')[0])
EOL
)
    host=$(python -c "$s")
    command nslookup $host
}
```

# Reading inputs

Reading inputs can be done using the `read` command.

By default the value read is available in the `$REPLY` variable.

It is possible to provide a custom variable for the output:

```bash
read $MY_OUTPUT_VAR
```

Few useful options:

- `-r`: By default, `read` interprets the backslash as an escape character, which can cause unexpected behavior. `-r` disable backslash escaping.
- `-s`: The option allows to suppress terminal echoing.
- `-p`: The option allows to display a prompt before reading. The prompt is printed before read executes and does not include a newline.

    ```bash
    read -r -s -p "Enter your password: "
    ```


[\[more\]](https://linuxize.com/post/bash-read/)
