from pathlib import Path
import shutil
import subprocess
import os, sys

GENERATEREPO = os.environ.get("GENERATEREPO", "yes")
REPONAME = os.environ.get("REPONAME", "archbuilder")

datadir = Path('/data')
datadir.mkdir(exist_ok=True)

srcdir = datadir.joinpath('sources')
srcdir.mkdir(exist_ok=True)

pkgdir = datadir.joinpath('packages')
pkgdir.mkdir(exist_ok=True)

srcdirs = [
    i
    for i in srcdir.iterdir()
    if i.is_dir() and i.joinpath('PKGBUILD').exists()
]

if len(srcdirs) == 0:
    print("There are no packages to build.", file=sys.stderr)
    exit(1)

tmpsrcdir = datadir.joinpath("tmp")
tmpsrcdir.mkdir(exist_ok=True)

def buildpkg(srcpath:Path):
    tmpsrcpath = tmpsrcdir.joinpath(srcpath.name)
    if tmpsrcpath.exists():
        shutil.rmtree(tmpsrcpath)
    shutil.copytree(srcpath, tmpsrcpath)

    process = subprocess.run(['makepkg', '-scf', '--noconfirm'], cwd=tmpsrcpath)
    if process.returncode != 0:
        print(f"The '{srcpath.name}' package cannot be built! Please make sure the PKGBUILD works.", file=sys.stderr)
        return
    bins = [
        i
        for i in tmpsrcpath.iterdir()
        if i.suffixes[-3:] == ['.pkg', '.tar', '.zst']
    ]
    for bin in bins:
        shutil.copy(bin, pkgdir)
        if GENERATEREPO == "yes":
            subprocess.run(['repo-add', f'./{REPONAME}.db.tar.gz', pkgdir.joinpath(bin.name)], cwd=pkgdir)

for srcdir in srcdirs:
    buildpkg(srcdir)
