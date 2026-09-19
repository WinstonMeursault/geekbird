# 极客鸟 GeekBird

纯 HTML / CSS / JavaScript 三页官网，无 npm、无构建依赖、无第三方运行库（字体在站点内托管）。可直接由 Nginx 托管。

## 页面与预约

- `/`：首页，黑色羽毛主视觉、组织故事与服务入口。
- `/service/`：维修服务、服务范围与原则。
- `/booking/`：建筑光井预约大界面。**只有点击“开始预约”，才前往外部预约平台。**

其他预约入口先进入 `/booking/`。本站不提供预约表单、图片上传或提交接口，也不会自动跳转。

## 项目结构

```text
geekbird/
├── index.html                 首页
├── service/index.html         服务页
├── booking/index.html         预约首屏
├── config.js                  唯一业务配置入口
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
│   ├── copywriting.md         全站文案、字体层级与维护方式
│   ├── deployment.md          发布、检查、回滚与维护说明
│   └── image-prompts.md       生图提示、来源映射与替换方式
├── deploy/nginx.conf          与现有 54321 端口匹配的 Nginx 示例
├── scripts/
│   ├── release.py             校验与打包工具，仅依赖 Python 3
│   └── subset_fonts.py        文案修改后的字体子集更新工具
├── dist/                      生成的交付文件，不纳入版本管理
│   ├── geekbird-site.tar.gz    可部署网站，解压得到 public/
│   ├── manifest.json          每个上线文件的 SHA-256
│   └── SHA256SUMS             部署包与 manifest 的校验值
└── .gitignore
```

## 日常配置

只修改根目录 [config.js](config.js)：

- `bookingUrl`：实际外部预约平台的 HTTP(S) 链接。
- `emergencyQQ`：联系 QQ 号，保留字符串形式。

配置公开可读。预约页读取配置后更新“开始预约”的链接；未配置或无效时显示入口尚未开放。右下角联系入口使用同一个配置文件。

## 准备部署包

需要 Python 3.8 或更新版本，无需安装 Python 包。

```sh
python3 scripts/release.py --check
python3 scripts/release.py
```

打包前会检查本地链接与锚点、图片引用、预约配置以及是否残留表单；打包后逐文件核对 SHA-256。部署包只包含 `public/` 下的 18 个网站文件，不包含原图、预览、说明或工具脚本。相同输入会生成相同校验值的压缩包。

新增中文文案后，先运行 `python3 scripts/subset_fonts.py` 更新字体字符集，再重新打包。字体更新需要联网，网站访问时不请求外部字体服务。完整文案与排版说明见 [文字设计](docs/copywriting.md)。

正式发布步骤见 [部署说明](docs/deployment.md)。Nginx 必须指向部署包里的 `public/`，不要直接公开整个源项目目录。

## 当前线上基线

地址：<http://47.120.64.37:54321/>。

2026-09-19 已部署文字设计版本。线上网站目录 `/var/www/geekbird/public` 当前指向 `/var/www/geekbird/releases/20260919-075312-typography/public`，对外使用 54321 端口。

替换前备份：`/var/backups/geekbird-before-typography-20260919-075312.tar.gz`。上一版本保留在 `/var/www/geekbird/releases/20260919-073516-production/public`，可供回滚。

## 本次检查

- 三页已统一字体层级与文案，中文 Noto Sans SC、英文 Manrope 均本地加载。
- 预约入口先显示大界面，点击“开始预约”才打开外部链接；无站内表单。
- 预约页 320 / 390 / 768 / 1440 / 1920px 布局与正式图片加载。
- 部署包文件清单、校验值与重复构建一致性。
- 正式 Nginx 配置已通过语法检查并重载；公网文件 SHA-256、缓存策略、图片类型、gzip 与预约流程均已验证。
