#!/usr/bin/env bash
set -euo pipefail

# Usage: ./tools/sign_hillclimb.sh input-unsigned.apk output-signed.apk keystore.jks alias
if [[ $# -ne 4 ]]; then
  echo "Usage: $0 INPUT_UNSIGNED_APK OUTPUT_SIGNED_APK KEYSTORE_JKS KEY_ALIAS" >&2
  exit 2
fi

input=$1
output=$2
keystore=$3
alias=$4
[[ -f "$input" && -f "$keystore" ]] || { echo "Input APK or keystore missing" >&2; exit 1; }
[[ ! -e "$output" ]] || { echo "Refusing to overwrite $output" >&2; exit 1; }
command -v zipalign >/dev/null || { echo "Android build-tools zipalign required" >&2; exit 1; }
command -v apksigner >/dev/null || { echo "Android build-tools apksigner required" >&2; exit 1; }

tmp=$(mktemp --suffix=.apk)
trap 'rm -f "$tmp"' EXIT
zipalign -f -p 4 "$input" "$tmp"
apksigner sign --ks "$keystore" --ks-key-alias "$alias" --out "$output" "$tmp"
apksigner verify --verbose --print-certs "$output"
echo "Signed and verified: $output"
