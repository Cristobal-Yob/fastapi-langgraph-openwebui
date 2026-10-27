# Upstream slim dependency provenance

`requirements-slim.txt` is copied byte-for-byte from the Open WebUI v0.12.3 tag:

- [Exact upstream dependency file](https://raw.githubusercontent.com/open-webui/open-webui/v0.12.3/backend/requirements-slim.txt)
- [Upstream Dockerfile selecting that list](https://raw.githubusercontent.com/open-webui/open-webui/v0.12.3/Dockerfile)
- [Retained upstream license](../licenses/OpenWebUI-LICENSE.txt)

SHA-256: `6dc3e004a3935f4bcc19f804f791e536c1f4be381049d866f842b2c2e4a88509`.
License SHA-256: `5f1bd74c48bf13ab0f82e177ad9e637313b92533d20ead2593d49347a47fc232`.

This project's **pip-target installation is an adaptation**, not an officially
documented Open WebUI pip-slim installation. It uses that exact upstream closure,
then installs the pinned official wheel without rehydrating its full ML dependency
set. `USE_SLIM_DOCKER=true` selects the corresponding upstream runtime imports.
The packaged wheel's console entrypoint is resolved through distribution metadata;
Docker/source-mode commands and packaged frontend paths are not mixed.

The main graph stays in the normal Python environment. Only the separate WebUI
process prepends `.webui-packages`, so its `langchain-core==1.4.8` cannot replace the
Google graph provider's required `langchain-core>=1.6.10` in the core process.

Python 3.12 dependency resolution is checked separately. A successful solve is not
a Linux/Heroku build, slug-size, memory, startup or real-provider proof. No Torch,
sentence-transformers or ONNX runtime dependency is added as a startup workaround.
