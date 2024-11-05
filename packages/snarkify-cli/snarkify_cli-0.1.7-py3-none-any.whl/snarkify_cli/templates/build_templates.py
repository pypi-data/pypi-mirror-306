FUNC_YAML_TEMPLATE = """specVersion: 0.35.0
name: service-{}
runtime: rust
registry: ""
image: {}
created: {}
build:
  builderImages:
    pack: ghcr.io/knative/builder-jammy-base:latest
  buildpacks:
  - docker.io/paketocommunity/rust
  builder: pack
  buildEnvs:
  - name: BP_INCLUDE_FILES
    value: '**/*'
  pvcSize: 256Mi
"""

PROCFILE_TEMPLATE = "web: /workspace/bin/snarkify"
