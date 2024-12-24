# wait-for-it

`wait-for-it.sh` is a pure bash script that will wait on the availability of a
host and TCP port. It is useful for synchronizing the spin-up of
interdependent services, such as linked docker containers. Since it is a pure
bash script, it does not have any external dependencies.

## Usage

```text
wait-for-it.sh [-u url] [-s] [-t timeout] [-- command args]
-u URL | --url=URL          Url under test
-s | --strict               Only execute subcommand if the test succeeds
-q | --quiet                Don't output any status messages
-t TIMEOUT | --timeout=TIMEOUT
                            Timeout in seconds, zero for no timeout
-- COMMAND ARGS             Execute command with args after the test finishes
```

## Examples

For example, let's test to see if we can access port 80 on `www.google.com`,
and if it is available, echo the message `google is up`.

```text
$ ./wait-for-it.sh --url="https://google.com" -- echo "google is up"
wait-for-it.sh: waiting 15 seconds for https://google.com
wait-for-it.sh: www.google.com:80 is available after 0 seconds
google is up
```

You can set your own timeout with the `-t` or `--timeout=` option. Setting
the timeout value to 0 will disable the timeout:

```text
$ ./wait-for-it.sh -t 0 --url="https://google.com" -- echo "google is up"
wait-for-it.sh: waiting for https://google.com without a timeout
wait-for-it.sh: https://google.com is available after 0 seconds
google is up
```

The subcommand will be executed regardless if the service is up or not. If you
wish to execute the subcommand only if the service is up, add the `--strict`
argument. In this example, we will test port 81 on `google.com` which will
fail:

```text
$ ./wait-for-it.sh --url="https://google.com:81" --timeout=1 --strict -- echo "google is up"
wait-for-it.sh: waiting 1 seconds for https://google.com:81
wait-for-it.sh: timeout occurred after waiting 1 seconds for https://google.com:81
wait-for-it.sh: strict mode, refusing to execute subprocess
```

If you don't want to execute a subcommand, leave off the `--` argument. This
way, you can test the exit condition of `wait-for-it.sh` in your own scripts,
and determine how to proceed:

```text
$ ./wait-for-it.sh --url="https://google.com"
wait-for-it.sh: waiting 15 seconds for https://google.com
wait-for-it.sh: https://google.com is available after 0 seconds
$ echo $?
0
$ ./wait-for-it.sh --url="https://google.com:81"
wait-for-it.sh: waiting 15 seconds for www.google.com:81
wait-for-it.sh: timeout occurred after waiting 15 seconds for www.google.com:81
$ echo $?
124
```

## Community

_Debian_: There is a [Debian package](https://tracker.debian.org/pkg/wait-for-it).
