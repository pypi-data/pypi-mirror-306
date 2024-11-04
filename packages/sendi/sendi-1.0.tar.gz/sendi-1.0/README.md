# Sendi

Sendi is just another xmppsend script.
Sendi is based on python slixmpp library and support fews modern features like HTTP Upload and Omemo.

## Usage

To use it, you have to create a config file that permit us to access login information.
The default path of config file is `$XDG_CONFIG_HOME/sendi/config.toml`

```toml
[section_name]
host="mysuperndd.ndd" # host of the jabber server, default to localhost
port=5222 # jabber port to use, 5222 is the default
password="superpassword" # JID account password, this is required
jid="user@mysuperndd.ndd" # JID of the sender user, this is required
# Connection can be either
# - "standard" which mean Starttls based.
# - "tls" using directly tls connection.
# standard is the default
connection_type="standard"
# Security level can be either
# - "simple" : don't encrypt end2end
# - "encrypted" use omemo (XEP-0384 and XEP-0454)
# standard is the default
security_level="simple"
# Lang metadata in message to send, default to en
# this is rarely used by software but may be useful in some case
lang="en"
# log level for logging of sendi and library used.
# default to ERROR (40)
# other value : 10: DEBUG, 20:INFO, 30:WARN, 50: CRITICAL
loglevel=0 # max log
# custom omemo cache path, by default use "$XDG_CACHE_HOME/sendi/@bare_jid@.json" based path to keep
# omemo config for all jid used.
omemo_cache_file_path= "/tmp/mycache.json"
# force delete omemo cache path before running, useful if cache is broken.
clear_omemo_cache=true
```

### Command line Usage

```console
$ sendi [OPTIONS] CONFIG_NAME TARGETS...
```

**Arguments**:

* `CONFIG_NAME`: Config section to use form the config_file[required]
* `TARGETS...`: List of jabber id of receivers [required]

**Options**:

* `--message TEXT` : simple text message to send.
* `--file-path PATH` : path of the file to send (using http-upload feature)
* `--config-file PATH`: Config file in toml [default: $XDG_CONFIG_HOME/sendi/config.toml]
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

### Config file sample:

## Dev install

Install pyinvoke and then:

```shell
pip install invoke
invoke init
```

Run python code:

```shell
invoke build
# Typer Cli
rye run sendi

CONFIG_NAME="user"
CONFIG_PATH="config.toml"
TARGET="receiver@localhost"

rye run sendi $CONFIG_NAME $TARGET --config-file=$CONFIG_PATH --message="Ping !" --file-path=tests/test_image.jpg
```

## Install Using Container(podman):

```shell
CONFIG_NAME="user"
CONFIG_PATH="config.toml"
TARGET="receiver@localhost"
invoke build
invoke build-container
podman run -v $PWD:/mnt  localhost/sendi  $CONFIG_NAME $TARGET --config-file=/mnt/$CONFIG_PATH --message="Ping !" --file-path=/mnt/tests/test_image.jpg
```

# Experimental: Install as Deb using Wheel2deb.

Use this method only if you know what you are doing, this [may break your system](https://wiki.debian.org/fr/DontBreakDebian).
I tested this only in debian-bookworm.

```
invoke init-deb
invoke build-deb
cd deb
ls -la *.deb
# Only 5 lib from the huge number of generated lib are require to make sendi work.
# I prefer to keep debian as standard as possible.
sudo apt install ./python3-twomemo_*.deb ./python3-oldmemo_*.deb
sudo apt install ./python3-omemo*.deb
sudo apt install  ./python3-slixmpp_*.deb
sudo apt install ./python3-slixmpp-omemo_*.deb
sudo apt install ./python3-sendi_*.deb
```

## Build Container for arm64 arch on amd64 host

- you need buildah (podman) and qemu_user_static.
- clean up `dist` and `deb` dir.
- `invoke build`.
- `invoke container-build -p linux/arm64`.


## FAQ ?

- Why this name, sendi ?

It's an esperanto verb: https://en.wiktionary.org/wiki/sendi

- Why AGPL v3 ?

I used slixmpp, slixmpp-omemo and reuse some part of the old apprise xmpp plugin which as been dropped.
The license rule make possible to release all the stuff only under the agplv3 license which is the slixmpp-omemo one.
