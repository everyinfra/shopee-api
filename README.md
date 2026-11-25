# Shopee API

[English](#english) · [中文](#中文)

## English

This repo reads public Shopee data with Python or curl. You can search products by keyword, read product details, and list a shop's products. You need one EveryInfra API key. You do not need a Shopee account or cookie. The same API also works as an MCP tool in Claude and Cursor. Billing is per call: these 3 capabilities cost $1.39 to $6.40 per 1,000 calls. Failed calls and empty results are not charged. The EveryInfra Shopee API has 4 capabilities, all listed on the platform page: <https://everyinfra.com/en/shopee-api?utm_source=github&utm_medium=example_repo&utm_campaign=shopee-api>

### Quick start

```bash
git clone https://github.com/everyinfra/shopee-api.git
cd shopee-api
pip install -r requirements.txt
export EVERYINFRA_API_KEY=<your API key>
python main.py search "camping chair" --out products.csv
python main.py product "<product url>" --out product.json
python main.py shop <shop_id> --out shop_products.csv
```

- The examples use the Singapore site (`country=sg`). To use another site, change `country` to id, sg, my, th, ph, vn, br, tw, mx, co or cl. The default is Indonesia. Prices come in that site's currency.
- For `product`, pass the `url` from a `search` result. The path must contain i.<shop id>.<item id>. The site is read from the link.
- For `shop`, pass the `shop_id` from a `search` result, or the shop's username. It returns the shop's products, not shop reviews.
- Without `--out`, the command prints the first 3 rows as JSON. With `--out`, it saves a .csv or .json file. The CSV has a BOM, so Excel opens it without garbled text.
- Register at everyinfra.com, then create the API key in the console. Steps: <https://everyinfra.com/en/docs?utm_source=github&utm_medium=example_repo&utm_campaign=shopee-api#quickstart>

### curl

```bash
curl -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"platform":"shopee","action":"search","params":{"keyword":"camping chair","country":"sg"}}'
```

All capabilities use the same URL. Change `action` and `params` to call another one. Examples for `product_detail` and `shop` are in [examples/curl.sh](examples/curl.sh).

### Claude and Cursor (MCP)

The remote MCP URL is <https://api.everyinfra.com/mcp>. Add the `Authorization: Bearer` header with your API key. EveryInfra runs the server, so you install no local program.

Claude Code:

```bash
claude mcp add --transport http everyinfra https://api.everyinfra.com/mcp --header "Authorization: Bearer <API Key>"
```

Cursor and other clients that read `mcp.json` ([examples/mcp.json](examples/mcp.json)):

```json
{
  "mcpServers": {
    "everyinfra": {
      "url": "https://api.everyinfra.com/mcp",
      "headers": {
        "Authorization": "Bearer <API Key>"
      }
    }
  }
}
```

Custom connectors in Claude on the web and desktop, and ChatGPT, accept only a URL. Enter <https://api.everyinfra.com/mcp/all>, sign in to EveryInfra when asked, and allow access. You do not need to enter a key. Full steps: <https://everyinfra.com/en/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=shopee-api>

### Price

| `action` | Per 1,000 calls |
|---|---|
| `search` | $6.40 |
| `product_detail` | $1.39 |
| `shop` | $1.39 |

- Billing is per call, about $0.0014 to $0.0064 each. Failed calls, empty results, parameter errors, and authentication failures are not charged.
- A new account gets a $1 trial allowance, valid for 24 hours. No credit card is needed. How to claim it: <https://everyinfra.com/en/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=shopee-api>
- Prices for the other 1 Shopee capabilities are on the platform page: <https://everyinfra.com/en/shopee-api?utm_source=github&utm_medium=example_repo&utm_campaign=shopee-api>

### Fields

These are the fields that the 3 capabilities returned in our test. Each meaning is the first sentence of the field's entry in the API documentation. The link under each table has the full text.

#### `search` (keyword search)

| Field | Meaning |
|---|---|
| `shop_id` | Shop ID. |
| `item_id` | Item ID. |
| `name` | Name of the object itself, for account, product and business capabilities. |
| `url` | Link to the record on the platform. |
| `image_url` | Image link. |
| `price` | Price as a number without a currency symbol; see currency. |
| `discount_pct` | Discount percentage. |
| `currency` | Currency code of the price (for example CNY, USD). |
| `rating` | Rating. **The scale varies by platform**: rating_scale on the same row gives the maximum (usually 5; Booking, Douban, iQIYI and NAVER use 10). |
| `location` | Location description passed through as is; the format varies by platform. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |
| `rating_scale` | Maximum of rating in the same row: 5 for five-star scales, 10 for ten-point scales. |

All parameters and fields: <https://everyinfra.com/en/shopee-api/search?utm_source=github&utm_medium=example_repo&utm_campaign=shopee-api>

#### `product_detail` (product details)

| Field | Meaning |
|---|---|
| `id` | The record's unique ID on the platform. |
| `url` | Link to the record on the platform. |
| `name` | Name of the object itself, for account, product and business capabilities. |
| `text` | Body text with HTML removed, returned in full and never cut short (on a few platforms the list results themselves carry only an excerpt; the platform's field notes say so). |
| `price` | Price as a number without a currency symbol; see currency. |
| `currency` | Currency code of the price (for example CNY, USD). |
| `discount` | Discount description. |
| `rating` | Rating. **The scale varies by platform**: rating_scale on the same row gives the maximum (usually 5; Booking, Douban, iQIYI and NAVER use 10). |
| `shop_name` | Shop name. |
| `shop_location` | Shop location. |
| `variants` | Product variants (options such as color or size). |
| `image_url` | Image link. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |
| `rating_scale` | Maximum of rating in the same row: 5 for five-star scales, 10 for ten-point scales. |

All parameters and fields: <https://everyinfra.com/en/shopee-api/product_detail?utm_source=github&utm_medium=example_repo&utm_campaign=shopee-api>

#### `shop` (shop)

| Field | Meaning |
|---|---|
| `shop_id` | Shop ID. |
| `item_id` | Item ID. |
| `name` | Name of the object itself, for account, product and business capabilities. |
| `url` | Link to the record on the platform. |
| `image_url` | Image link. |
| `price` | Price as a number without a currency symbol; see currency. |
| `discount_pct` | Discount percentage. |
| `currency` | Currency code of the price (for example CNY, USD). |
| `rating` | Rating. **The scale varies by platform**: rating_scale on the same row gives the maximum (usually 5; Booking, Douban, iQIYI and NAVER use 10). |
| `is_mall` | Whether the shop is an official Shopee Mall store. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |
| `rating_scale` | Maximum of rating in the same row: 5 for five-star scales, 10 for ten-point scales. |

All parameters and fields: <https://everyinfra.com/en/shopee-api/shop?utm_source=github&utm_medium=example_repo&utm_campaign=shopee-api>

### FAQ

**Do I need a Shopee account or cookie to call the API?**

No. Send the `Authorization: Bearer` header with your API key. The request body holds `platform`, `action`, and the capability parameters. You do not scan a QR code, keep a login session, or open a browser.

**How much does it cost? Are failed calls charged? Is there a free allowance?**

Billing is per call, from $1.39 per 1,000 calls. Failed calls, empty results, parameter errors, and authentication failures are not charged. A new account gets a $1 trial allowance, valid for 24 hours. No credit card is needed. How to claim it: <https://everyinfra.com/en/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=shopee-api>

**Can I connect the Shopee API to Claude or Cursor?**

Yes. The remote MCP URL is <https://api.everyinfra.com/mcp>. Add the `Authorization: Bearer` header with your API key. You install no local program. Setup for Claude, Cursor, ChatGPT, and Claude Code: <https://everyinfra.com/en/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=shopee-api>.

**What legal points apply when I use Shopee data?**

The EveryInfra Terms of Service require you to make sure your use of the data follows applicable law and the terms of the relevant platform. Do not use the data for anything illegal or anything that violates privacy or intellectual property rights. Do not use bulk scraping for harassment, fraud, or other abuse. When you use personal information such as nicknames and avatars, keep only the fields your business needs.

**Which Shopee data can I get?**

The EveryInfra Shopee API has 4 capabilities:

- keyword search
- profile or object details
- shop
- product details

Parameters and return fields for each capability are on the platform page: <https://everyinfra.com/en/shopee-api?utm_source=github&utm_medium=example_repo&utm_campaign=shopee-api>

### Tested

Before release, we ran the 3 commands in Quick start against the live API with this repo's code.

| Command | Time (Singapore, UTC+8) | Rows | Charged |
|---|---|---|---|
| `python main.py search "camping chair" --out products.csv` | 2026-11-25 12:39 | 20 | $0.006403 |
| `python main.py product "<product url>" --out product.json` | 2026-11-25 12:39 | 1 | $0.001389 |
| `python main.py shop <shop_id> --out shop_products.csv` | 2026-11-25 12:39 | 20 | $0.001389 |

## 中文

本仓库用 Python 或 curl 读 Shopee 公开数据：按关键词搜商品，读商品详情，看店铺里的商品。只需一把 EveryInfra API Key，不用 Shopee 账号和 Cookie，也能作为 MCP 工具接进 Claude、Cursor。按调用次数计费，这 3 个能力每千次 $1.39 到 $6.40，失败和空结果不收费。Shopee 共 4 个能力：<https://everyinfra.com/shopee-api?utm_source=github&utm_medium=example_repo&utm_campaign=shopee-api>

### 快速开始

```bash
git clone https://github.com/everyinfra/shopee-api.git
cd shopee-api
pip install -r requirements.txt
export EVERYINFRA_API_KEY=<你的 API Key>
python main.py search "camping chair" --out products.csv
python main.py product "<商品链接>" --out product.json
python main.py shop <shop_id> --out shop_products.csv
```

- 示例都在新加坡站（`country=sg`）；换站点改 `country`，可选 id、sg、my、th、ph、vn、br、tw、mx、co、cl，不传默认印尼站。价格按该站点的币种返回。
- `product` 传 `search` 结果里的 `url`，路径里要有 i.<店铺 ID>.<商品 ID>；站点从链接自动识别。
- `shop` 传 `search` 结果里的 `shop_id`，也可以传店铺用户名；返回店内商品，不是店铺评价。
- 不加 `--out` 时打印前 3 条 JSON；加 `--out` 存成 .csv 或 .json。CSV 带 BOM，Excel 直接打开不乱码。
- API Key 在 everyinfra.com 注册后到控制台创建，步骤见 <https://everyinfra.com/docs?utm_source=github&utm_medium=example_repo&utm_campaign=shopee-api#quickstart>

### 用 curl 调

```bash
curl -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"platform":"shopee","action":"search","params":{"keyword":"camping chair","country":"sg"}}'
```

所有能力都发到同一个地址，换 `action` 和 `params` 就行；`product_detail`、`shop` 的写法见 [examples/curl.sh](examples/curl.sh)。

### 接进 Claude、Cursor（MCP）

远程 MCP 地址是 <https://api.everyinfra.com/mcp>，请求头加 `Authorization: Bearer` 和 API Key；服务器由 EveryInfra 运行，不用装本地程序。

Claude Code：

```bash
claude mcp add --transport http everyinfra https://api.everyinfra.com/mcp --header "Authorization: Bearer <API Key>"
```

Cursor 等读 `mcp.json` 的客户端（[examples/mcp.json](examples/mcp.json)）：

```json
{
  "mcpServers": {
    "everyinfra": {
      "url": "https://api.everyinfra.com/mcp",
      "headers": {
        "Authorization": "Bearer <API Key>"
      }
    }
  }
}
```

Claude 网页版和桌面版的自定义连接器、ChatGPT 只能填网址：填 <https://api.everyinfra.com/mcp/all>，连接时登录 EveryInfra 并允许，不用填 Key。完整步骤见 <https://everyinfra.com/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=shopee-api>

### 价格

| 能力 | `action` | 每千次 |
|---|---|---|
| 关键词搜索 | `search` | $6.40 |
| 商品详情 | `product_detail` | $1.39 |
| 店铺资料 | `shop` | $1.39 |

- 按调用次数计费，每次约 $0.0014 到 $0.0064；失败、空结果、参数错误和鉴权失败都不收费。
- 新账号有 $1 试用额度，24 小时内有效，不用信用卡，领取方式见 <https://everyinfra.com/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=shopee-api>
- Shopee 其他 1 个能力的单价见平台页 <https://everyinfra.com/shopee-api?utm_source=github&utm_medium=example_repo&utm_campaign=shopee-api>

### 返回字段

下面是这 3 个能力实测返回的字段，含义取自接口文档每条说明的第一句，完整说明在每张表下面的链接里。

#### `search`（关键词搜索）

| 字段 | 含义 |
|---|---|
| `shop_id` | 店铺 ID。 |
| `item_id` | 商品 ID。 |
| `name` | 名称。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `image_url` | 图片链接。 |
| `price` | 价格数值，不含货币符号；币种见 currency。 |
| `discount_pct` | 折扣百分比。 |
| `currency` | 价格币种代码（如 CNY、USD）。 |
| `rating` | 评分。 |
| `location` | 地理位置描述，原文透传，格式随平台而异。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |
| `rating_scale` | 上一列 `rating` 的满分。 |

完整参数和字段：<https://everyinfra.com/shopee-api/search?utm_source=github&utm_medium=example_repo&utm_campaign=shopee-api>

#### `product_detail`（商品详情）

| 字段 | 含义 |
|---|---|
| `id` | 该记录在原平台上的唯一标识。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `name` | 名称。 |
| `text` | 正文内容，已去除 HTML 标签，全文返回、不截断（个别平台的列表结果本身只有摘要，以该平台的字段说明为准）。 |
| `price` | 价格数值，不含货币符号；币种见 currency。 |
| `currency` | 价格币种代码（如 CNY、USD）。 |
| `discount` | 折扣说明。 |
| `rating` | 评分。 |
| `shop_name` | 店铺名。 |
| `shop_location` | 店铺所在地。 |
| `variants` | 规格变体。 |
| `image_url` | 图片链接。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |
| `rating_scale` | 上一列 `rating` 的满分。 |

完整参数和字段：<https://everyinfra.com/shopee-api/product_detail?utm_source=github&utm_medium=example_repo&utm_campaign=shopee-api>

#### `shop`（店铺资料）

| 字段 | 含义 |
|---|---|
| `shop_id` | 店铺 ID。 |
| `item_id` | 商品 ID。 |
| `name` | 名称。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `image_url` | 图片链接。 |
| `price` | 价格数值，不含货币符号；币种见 currency。 |
| `discount_pct` | 折扣百分比。 |
| `currency` | 价格币种代码（如 CNY、USD）。 |
| `rating` | 评分。 |
| `is_mall` | 是否为 Shopee Mall 官方店。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |
| `rating_scale` | 上一列 `rating` 的满分。 |

完整参数和字段：<https://everyinfra.com/shopee-api/shop?utm_source=github&utm_medium=example_repo&utm_campaign=shopee-api>

### 常见问题

**调用时要不要提供 Shopee 账号或 Cookie？**

不用，请求头带 `Authorization: Bearer` 和 API Key 就能调，请求体写 `platform`、`action` 和能力参数。不用扫码、维护登录状态，也不用开浏览器。

**怎么收费？失败了收不收钱？有免费额度吗？**

按调用次数计费，每千次 $1.39 起。失败、空结果、参数错误和鉴权失败都不收费。新账号有 $1 试用额度，24 小时内有效，不用信用卡，领取方式见定价页 <https://everyinfra.com/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=shopee-api>

**能把 Shopee 接口接进 Claude、Cursor 吗？**

能，远程 MCP 地址是 <https://api.everyinfra.com/mcp>，请求头加 `Authorization: Bearer` 和 API Key，不用装本地程序。Claude、Cursor、ChatGPT、Claude Code 配置见 <https://everyinfra.com/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=shopee-api>。

**用 Shopee 数据要注意哪些合规问题？**

EveryInfra 服务条款要求你自行确保数据用法符合适用法律和相关平台条款，禁止用于违法、侵犯隐私或知识产权，或批量抓取用于骚扰、欺诈等恶意用途。用到昵称、头像等个人信息时，只留业务用得上的字段。

**可以拿到 Shopee 的哪些数据？**

Shopee 有 4 个能力：关键词搜索、主页或对象详情、店铺资料、商品详情。每个能力的参数和返回字段见平台页 <https://everyinfra.com/shopee-api?utm_source=github&utm_medium=example_repo&utm_campaign=shopee-api>

### 实测记录

发布前用本仓的代码对线上接口跑过一遍，命令就是「快速开始」里的 3 条。

| 命令 | 时间（新加坡时间） | 返回条数 | 扣费 |
|---|---|---|---|
| `python main.py search "camping chair" --out products.csv` | 2026-11-25 12:39 | 20 | $0.006403 |
| `python main.py product "<商品链接>" --out product.json` | 2026-11-25 12:39 | 1 | $0.001389 |
| `python main.py shop <shop_id> --out shop_products.csv` | 2026-11-25 12:39 | 20 | $0.001389 |

`product_detail` 返回的一条（正文截到 60 字，作者字段没放进来）：

```json
{
  "id": "55766383934",
  "text": "✅【All items SG Stock】\n👍100% Brand new High quality\n⏰ Shippin…",
  "price": 16.9,
  "currency": "SGD",
  "rating": 5,
  "shop_name": "Simple-Living",
  "rating_scale": 5
}
```

## License

MIT
