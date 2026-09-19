# 极客鸟 GeekBird

正式部署目标为 **Cloudflare Pages**，包含三个公开页面与密码保护的配置后台。无需 SSH、独立服务器或 npm 构建依赖；管理配置保存在 Cloudflare KV。

## 正式访问地址

正式域名：<https://geekbird.net/>。域名绑定和部署完成后使用以下地址：

- 首页：<https://geekbird.net/>
- 维修服务：<https://geekbird.net/service/>
- 预约页面：<https://geekbird.net/booking/>
- 管理后台：<https://geekbird.net/_gb-settings/>

## Cloudflare 管理后台

后台不在公开导航中展示，页面和配置接口都需要密码验证。可在浏览器中修改 QQ 和预约链接，无需 SSH 或自己的服务器。配置保存在 Cloudflare KV，重新部署不会覆盖。

### 1. 创建 Pages 项目

在 Cloudflare 控制台进入 **Workers & Pages**，创建 **Pages** 项目并连接代码仓库，填写：

- 代码仓库：`galiandan/geekbird`
- 生产分支：`main`
- 框架预设：`None`
- 构建命令：`python3 scripts/cloudflare.py`
- 构建输出目录：`dist/cloudflare`
- 根目录：仓库根目录（留空）

这里要创建 **Pages** 项目，选择连接 Git 仓库。不要使用普通 Workers 的部署向导，也不要把输出目录设成仓库根目录。

在项目的 **Custom domains（自定义域）** 中添加 `geekbird.net`，按提示完成 DNS 配置，等待域名和 HTTPS 生效。绑定完成前也可使用 Cloudflare 分配的 `*.pages.dev` 地址访问。

### 2. 设置管理密码

“环境变量”就是在 Cloudflare 后台填写、供程序运行时读取的配置，不需要修改代码。管理密码应设置为 **Secret（机密）**：

1. 进入 **Workers & Pages → 你的 Pages 项目 → Settings（设置）→ Variables and Secrets（变量和机密）**。
2. 选择 **Production（生产环境）**，点击 **Add（添加）**。
3. 类型选择 **Secret（机密）**，名称填写 `ADMIN_PASSWORD`，值填写你自己的密码。
4. 密码至少 **16 位**，建议用密码管理器生成 **24 位以上随机密码**。不要把密码写进源码、`config.js` 或 README。
5. 保存后，到 **Deployments（部署）** 重新部署一次；也可以完成下面的 KV 绑定后一起重新部署。

登录用户名固定为 **`admin`**，密码就是 `ADMIN_PASSWORD` 的值。以后修改密码，同样需要更新此 Secret 并重新部署。

### 3. 创建并绑定 KV 存储

KV 用来保存 QQ 和预约链接，与管理密码是两个独立设置，两者都需要配置。

1. 在 Cloudflare 左侧进入 **Storage & Databases（存储和数据库）→ Workers KV**。
2. 点击 **Create namespace（创建命名空间）**，名称填写 `geekbird-settings`，确认创建。
3. 回到 **Workers & Pages → 你的 Pages 项目 → Settings（设置）→ Bindings（绑定）**。
4. 在 **Production（生产环境）** 点击 **Add binding（添加绑定）**，选择 **KV namespace**。
5. **变量名称**填写 `SITE_CONFIG`（必须完全一致，全部大写）；**KV 命名空间**选择刚创建的 `geekbird-settings`。
6. 保存，到 **Deployments（部署）** 重新部署一次，让密码和绑定在新的部署中生效。

生产环境和预览环境分别配置。如果访问预览部署地址，需要在预览环境设置密码和绑定；建议预览使用独立 KV，避免修改正式网站的配置。

### 4. 登录与日常修改

打开 <https://geekbird.net/_gb-settings/>，浏览器弹出身份验证窗口时，用户名填 **`admin`**，密码填自己设置的值。

- **联系 QQ**：填写 5–15 位数字，不能以 0 开头；留空显示“QQ 号暂未公布”。
- **预约链接**：填写外部预约平台的完整 `http://` 或 `https://` 链接；留空暂停预约入口。
- 点击 **保存设置**，看到成功提示后，稍后刷新公开网站验证。KV 全球同步通常需要约 1 分钟，部分地区可能更久。

首次保存前沿用源码 `config.js` 的默认值；首次保存后以 KV 配置为准，更新网站不会覆盖。后台地址可收藏，不在公开页面添加入口。建议使用个人浏览器或独立隐私窗口；浏览器会暂存登录信息，使用完关闭整个隐私窗口。

### 常见问题：提示未绑定 SITE_CONFIG

如果打开后台看到：

```json
{"error":"请先在 Cloudflare 绑定 SITE_CONFIG KV 命名空间。"}
```

说明密码验证已通过，但当前部署没有可用的 KV 绑定。按上面的“创建并绑定 KV 存储”步骤操作，并检查：

- 不只是创建命名空间，还要把它绑定到当前 **Pages 项目**。
- 绑定变量名必须是 `SITE_CONFIG`，不能填成命名空间名称 `geekbird-settings`。
- 绑定所在环境要与访问的部署一致：正式域名使用生产环境，预览地址使用对应预览环境。
- 保存绑定后必须重新部署，再重新打开后台。

更多配置、故障行为与本地测试方式见 [Cloudflare 部署说明](docs/cloudflare.md)。

## 页面与预约

- `/`：首页，黑色羽毛主视觉、组织故事与服务入口。
- `/service/`：维修服务、服务范围与原则。
- `/booking/`：建筑光井预约大界面。**只有点击“开始预约”，才前往外部预约平台。**

其他预约入口直接打开问卷星预约表单，服务反馈按钮直接打开反馈表单。旧 `/booking/` 页面保留兼容，不再作为必经入口；本站不收集或提交表单数据。

## 项目结构

```text
geekbird/
├── index.html                 首页
├── service/index.html         服务页
├── booking/index.html         预约首屏
├── config.js                  初始业务配置，Cloudflare 首次保存后以 KV 为准
├── cloudflare/
│   ├── admin.html             管理页面，构建时内嵌于 Worker
│   └── worker.js              密码验证、配置读取与保存
├── assets/
│   ├── app.js                 导航配置、联系与页面动效
│   ├── style.css              统一视觉及响应式样式
│   ├── fonts/                 本地中文 / 英文字体、子集样式与许可
│   ├── logo.svg               网页使用的 Logo
│   └── images/                三组桌面 / 手机 WebP，共六张
├── design/                    设计源文件，不部署
│   ├── brand/                 原始 Logo
│   ├── originals/             正式图片原始 PNG
│   ├── references/            用户提供的三张网站效果图
│   └── previews/              桌面、手机实际页面截图
├── docs/
│   ├── cloudflare.md          Cloudflare Pages 部署与后台管理
│   ├── copywriting.md         全站文案、字体层级与维护方式
│   ├── deployment.md          发布、检查、回滚与维护说明
│   └── image-prompts.md       生图提示、来源映射与替换方式
├── deploy/nginx.conf          与现有 54321 端口匹配的 Nginx 示例
├── scripts/
│   ├── cloudflare.py          Cloudflare Pages 构建工具
│   ├── release.py             校验与打包工具，仅依赖 Python 3
│   └── subset_fonts.py        文案修改后的字体子集更新工具
├── tests/cloudflare.test.mjs   后台权限与配置接口测试
├── dist/                      生成的交付文件，不纳入版本管理
│   ├── cloudflare/            Pages 构建输出，共 24 个文件
│   ├── geekbird-cloudflare-pages.zip  Pages 专用部署包
│   ├── cloudflare-manifest.json      Pages 文件 SHA-256 清单
│   ├── cloudflare-SHA256SUMS         Pages 压缩包与清单校验值
│   ├── geekbird-site.tar.gz    可部署网站，解压得到 public/
│   ├── manifest.json          每个上线文件的 SHA-256
│   └── SHA256SUMS             部署包与 manifest 的校验值
└── .gitignore
```

## 日常配置

Cloudflare 部署后通过管理页修改以下配置。根目录 [config.js](config.js) 作为第一次保存前的默认值；纯静态部署仍直接修改此文件：

- `bookingUrl`：实际外部预约平台的 HTTP(S) 链接。
- `emergencyQQ`：联系 QQ 号，保留字符串形式。

QQ 和预约链接是公开配置，管理密码只保存在 Cloudflare Secret 中。所有页面读取 `/config.js` 后更新全部预约链接；未配置或无效时禁用预约入口并显示提示。服务反馈链接固定指向 `https://www.wjx.top/m/93298004.aspx`，不受预约开关影响。右下角联系入口使用同一份配置。

## 正式发布前检查

```sh
python3 scripts/cloudflare.py
node --test tests/*.test.mjs
```

构建仅需 Python 3；测试需要 Node.js 22 或以上。构建会生成 `dist/cloudflare/`、`dist/geekbird-cloudflare-pages.zip` 和 SHA-256 清单，检查打包文件一致性。产物只包含公开静态资源和 Pages Worker，不包含管理密码、VPS 服务、文档或原始设计稿。

已补齐自定义 404、静态资源缓存规则、正式域名 canonical、`robots.txt` 和只包含三个公开页面的站点地图。后台保持无公开入口，页面和接口均禁止缓存与搜索收录。

本地 Cloudflare 运行环境的完整检查方式、迁移顺序和上线验收见 [Cloudflare 部署说明](docs/cloudflare.md)。本地测试通过不代表 Cloudflare 账号中的域名、密码和 KV 已配置完成。

## 从 VPS 迁移

1. 先通过 Pages 分配的 `*.pages.dev` 地址验证页面、密码登录和配置保存。
2. VPS 的配置不会自动同步到 Cloudflare KV。部署前核对 VPS 后台的 QQ 与预约链接，在 Pages 后台保存一遍；此前尚未保存时会使用源码 `config.js` 的默认值。
3. 在 Pages 的 **Custom domains（自定义域）** 添加 `geekbird.net`，按提示调整 DNS，等待 HTTPS 生效后再验证正式地址。
4. 保留 VPS 供切换期间回退。Pages 回滚部署不会回滚 KV 配置；修改重要配置前记下原值。

VPS 网站：<https://47.120.64.37/>，VPS 后台：<https://47.120.64.37/_gb-settings/>；原 `http://47.120.64.37:54321/` 也保留。两套后台各自保存配置和密码，互不同步。历史服务、备份和证书续期说明见 [VPS 部署记录](docs/vps.md)，早期纯静态部署见 [Nginx 部署说明](docs/deployment.md)。

### 直达表单与本地预览

- 默认预约：<https://www.wjx.top/m/93277562.aspx>。
- 服务反馈：<https://www.wjx.top/m/93298004.aspx>。
- 若线上后台已经保存了旧公众号链接，发布后需要在后台将预约链接更新为上述表单；源码默认值不会覆盖已保存的 KV / VPS 配置。
- 未启用 JavaScript 时使用 HTML 中的默认预约链接；更换默认表单时同步修改三个公开页面。
- 本地静态预览：`python3 -m http.server 8080 --bind 127.0.0.1`，访问 `http://127.0.0.1:8080/`。此方式仅预览公开页面，不运行管理后台。
