"""Shopee API 示例（Shopee API in Python）。

  python main.py search "camping chair" --out products.csv # 按关键词搜商品 / search products
  python main.py product "<商品链接>" --out product.json   # 商品详情 / product details
  python main.py shop <shop_id> --out shop_products.csv    # 店铺商品 / shop products
"""
import argparse

from everyinfra import fetch, report

SORTS = ["relevance", "popular", "newest", "price_asc", "price_desc"]


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search", help="按关键词搜商品 / search products by keyword")
    s.add_argument("keyword")
    s.add_argument("--sort", choices=SORTS, help="排序 / sort order")
    pr = sub.add_parser("product", help="商品详情 / product details")
    pr.add_argument("url")
    sh = sub.add_parser("shop", help="店铺里的商品 / a shop's products")
    sh.add_argument("shop")
    for x in (s, pr, sh):
        x.add_argument("--out", help="存成 .csv 或 .json / write .csv or .json")
    a = p.parse_args()

    if a.cmd == "search":
        params = {"keyword": a.keyword, "country": "sg", **({"sort": a.sort} if a.sort else {})}
        rows, charged = fetch("search", params)
    elif a.cmd == "product":
        rows, charged = fetch("product_detail", {"url": a.url})
    else:
        rows, charged = fetch("shop", {"shop": a.shop, "country": "sg"})
    report(rows, charged, a.out)


if __name__ == "__main__":
    main()
