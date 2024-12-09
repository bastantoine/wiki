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
