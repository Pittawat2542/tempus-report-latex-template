#!/bin/sh
# CI wrapper: run a TeX Live engine in the pinned image, keeping host PDF tools.
set -eu
engine=$(basename "$0")
exec docker run --rm --user "$(id -u):$(id -g)" \
  -e TEXMFVAR=/tmp/texmf-var -e TEXMFCONFIG=/tmp/texmf-config \
  -v "$TEMPUS_WORKSPACE:$TEMPUS_WORKSPACE" -w "$PWD" \
  --entrypoint "$engine" "$TEMPUS_TEXLIVE_IMAGE" "$@"
