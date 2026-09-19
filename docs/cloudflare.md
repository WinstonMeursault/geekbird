# Cloudflare Pages 部署与后台管理

此版本使用 Cloudflare Pages 的 Worker 和 KV，不需要自己的服务器、SSH 或数据库。公开官网保持原来的三个页面。

正式域名预先登记为 <https://geekbird.net/>。在 Pages 项目的 **Custom domains（自定义域）** 中添加 `geekbird.net`，按提示配置 DNS，并等待 HTTPS 生效。

## 首次部署（Cloudflare 控制台）

1. 在 **Workers & Pages → KV** 创建一个 KV 命名空间，例如 `geekbird-settings`。
2. 在 **Workers & Pages** 创建 **Pages** 项目，连接代码仓库。框架预设选 `None`，构建命令填 `python3 scripts/cloudflare.py`，构建输出目录填 `dist/cloudflare`，根目录为仓库根目录。
3. 在该 Pages 项目的 **Settings → Bindings** 添加 KV 绑定：变量名必须为 `SITE_CONFIG`，选择刚创建的命名空间。
4. 在 **Settings → Variables and Secrets** 添加 **Secret**：名称 `ADMIN_PASSWORD`，值为自己生成的至少 16 位长密码。推荐密码管理器生成 24 位以上随机密码。不要写入源码、`config.js` 或普通公开变量。
5. 保存设置后重新部署，使绑定和密码在新的部署中生效。生产环境与预览环境的设置分别配置；预览环境如需后台，应使用独立的 KV 与密码，避免修改正式配置。

使用 Git 集成构建即可，无需 SSH。若采用其他上传方式，必须支持 Pages advanced mode 的 `_worker.js`；只上传静态 HTML 无法提供管理功能。此构建产物针对 **Pages**，不是普通 Workers 的默认部署配置。

## 打开后台

- 地址：<https://geekbird.net/_gb-settings/>；域名绑定完成前，可使用 Pages 分配的 `*.pages.dev` 域名访问同一路径。
- 浏览器会弹出身份验证窗口，用户名填 `admin`，密码填上面设置的 `ADMIN_PASSWORD`。
- 页面与读写接口都在服务端校验密码，公开导航没有后台链接；后台响应禁止缓存和搜索收录。
- 只能通过 HTTPS 在线管理。建议在个人浏览器或独立隐私窗口操作；Basic 身份验证由浏览器暂存，使用完关闭整个隐私窗口。更换密码需在 Cloudflare 更新 Secret 并重新部署。

输入 QQ 号与完整的 HTTP(S) 预约链接，点击“保存设置”。允许留空：QQ 留空时显示“QQ 号暂未公布”，预约链接留空时暂停入口。保存失败会明确提示，不会显示保存成功。

KV 在全球各地区最终一致，通常约 60 秒、部分地区可能更久；保存后稍后刷新公开网站验证。不要多人同时修改：最后一次成功写入覆盖之前的配置。

## 配置与更新

- 第一次保存前沿用根目录 `config.js` 的默认值。
- 第一次保存后，KV 中的配置优先；重新发布页面不会覆盖后台设置。
- `/config.js` 动态输出 QQ 和预约链接供公开页面使用，管理密码不会输出到页面中。
- 未绑定 KV 时公开网站仍使用原始静态配置，后台提示尚未配置。KV 读取故障时返回错误，不悄悄恢复可能已停用的旧预约链接。
- 不要为 `/config.js` 或 `/_gb-settings*` 设置“缓存所有内容”等强制缓存规则。
- 如果要重置为源码默认值，在 Cloudflare 的 KV 控制台删除 `site-config` 键即可。

## 本地检查

```sh
python3 scripts/cloudflare.py
node --test tests/cloudflare.test.mjs
```

构建仅依赖 Python 3；测试需要 Node.js 22 或以上。`dist/cloudflare` 包含原有静态文件、`_worker.js`、`_routes.json`；后台 HTML 内嵌于 Worker，不单独公开。测试覆盖密码保护、配置保存与读取、非法输入、跨站写入拦截和 KV 故障。真实 Cloudflare 绑定和全球同步仍需首次部署后验收。
