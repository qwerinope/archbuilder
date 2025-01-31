# Archbuilder

Simple docker container based script that builds packages and repositiories for [archlinux](https://archlinux.org).

## Usage

Make sure docker is installed.  

### Using docker run

```sh
docker run --rm --volume ./data:/data ghcr.io/qweri0p/archbuilder:latest
```

Place the PKGBUILDs in the ./data/sources directory.
The structure should look like this:

### Using docker compose

Create a docker-compose.yaml file with the following contents:

```yaml
services:
  archbuilder:
    image: ghcr.io/qweri0p/archbuilder:latest
    # environment:
      # Values below are all defaults
      # - GENERATEREPO=yes        # Generate repository database
      # - REPONAME=archbuilder    # Set the name of the repository. Only used if GENERATEREPO is set to yes
    container_name: archbuilder
    restart: no
    volumes:
      - ./data:/data

```

## Configuration

Configuration is done with the following environment variables:

Variable|function|default
---|---|---
GENERATEREPO|Enable creation of repository database|"yes"
REPONAME|Set name of generated repository. Only in use when GENERATEREPO is "yes"|"archbuilder"

The file structure is as following:

```text
data/
├── sources/
│   ├── google-chrome/
│   │   └── PKGBUILD
│   └── paru/
│       └── PKGBUILD
└── packages/
    ├── archbuilder.db.tar.gz
    ├── paru-xxx.pkg.tar.zst
    └── google-chrome-xxx.pkg.tar.zst
```

All files in "packages" are generated by the program.
Documentation for PKGBUILD scripts can be found [here](https://wiki.archlinux.org/title/PKGBUILD).
