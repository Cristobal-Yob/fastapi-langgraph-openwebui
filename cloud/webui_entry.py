"""Relocatable target packages: no build-directory virtualenv shebangs."""
from pathlib import Path
import sys
import importlib.metadata
import os
import site

def prepare_packages(packages):
    packages=Path(packages).resolve()
    if not packages.is_dir(): raise SystemExit('Build the isolated Open WebUI packages first.')
    sys.path.insert(0,str(packages))
    # Trusted installed wheels may need .pth handling (notably pywin32 on Windows).
    # This runs only in the separate WebUI process, never in the Google graph core.
    site.addsitedir(str(packages))


def main():
    packages=Path(os.environ.get('OPENWEBUI_PACKAGE_DIR',
                  str(Path(__file__).resolve().parents[1]/'.webui-packages')))
    prepare_packages(packages)
    distribution=importlib.metadata.distribution('open-webui')
    if distribution.version != '0.12.3':raise SystemExit('The pinned Open WebUI version is required.')
    entrypoints=[entry for entry in distribution.entry_points
                 if entry.group=='console_scripts' and entry.name=='open-webui']
    if len(entrypoints)!=1:raise SystemExit('The pinned Open WebUI console entrypoint is unavailable.')
    entrypoints[0].load()()


if __name__=='__main__':main()
