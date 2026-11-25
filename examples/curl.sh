#!/usr/bin/env bash
# Shopee API 的 curl 示例：所有能力都发到同一个地址，只换 action 和 params。
# curl examples for the Shopee API: every capability uses the same URL; only action and params change.
#
#   export EVERYINFRA_API_KEY=<your API key>
#   bash examples/curl.sh search "camping chair"
#   bash examples/curl.sh product_detail "<product url>" # search 结果里的 url / the url from a search result
#   bash examples/curl.sh shop <shop_id>                 # search 结果里的 shop_id / the shop_id from a search result
set -euo pipefail
: "${EVERYINFRA_API_KEY:?Set EVERYINFRA_API_KEY first: https://everyinfra.com/docs#quickstart}"
action=${1:?"usage: bash examples/curl.sh <search|product_detail|shop> <value>"}
value=${2:?"value: a keyword, a product url or a shop id"}

case "$action" in
  search)         params="{\"keyword\":\"$value\",\"country\":\"sg\"}" ;;
  product_detail) params="{\"url\":\"$value\"}" ;;
  shop)           params="{\"shop\":\"$value\",\"country\":\"sg\"}" ;;
  *) echo "unknown action: $action (use search, product_detail or shop)" >&2; exit 2 ;;
esac

curl -sS -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"platform\":\"shopee\",\"action\":\"$action\",\"params\":$params}"
echo
