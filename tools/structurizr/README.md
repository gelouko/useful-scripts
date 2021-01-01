# Structurizr Quick Setup

When using Structurizr for the first time, you will realize that everytime you run the command to upload your DSL, you'll have to pass your workspace key, secret, and id.

The exact command would be something like this:

```bash
$ java -jar <STRUCTURIZE_LOCATION>/structurizr-cli-*.jar push -id <WS_ID> -key <WS_KEY> -secret <WS_SECRET> -workspace <DSL_FILE>
```

This script will enable you to create a config file and run structurizr like this:

```bash
$ structurizr <DSL_FILE>
```

## Requirements

- Python 3

## Installation

To enable the command, just unzip structurizr in the `~/.structurizr` directory, or set the `STRUCTURIZR_HOME` environment variable pointing to the folder where you have installed the structurizr jar.

After that, create the file `~/.structurizr/config.json` with the following configuration:

```json
{
  "id": "YOUR_WORKSPACE_ID",
  "key": "YOUR_WORKSPACE_KEY",
  "secret": "YOUR_WORKSPACE_SECRET"
}
```

Change `YOUR_WORKSPACE_ID`, `YOUR_WORKSPACE_KEY` and `YOUR_WORKSPACE_SECRET` to your workspace's values.

After that, copy the file `structurizr` from this project to your `/usr/local/bin` folder and done!

You are able to use the `structurizr` command :)


## Usage

Update a DSL template:

```bash
$ structurizr <DSL_FILENAME>
```

example:
```bash
$ structurizr my-project.dsl
```

Done!
