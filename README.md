# 个人主页：编辑与发布

线上：[学术主页](https://tt885.github.io/) · [户外页面](https://tt885.github.io/outdoors.html)

## 平时改哪里？

| 文件 | 内容 |
| --- | --- |
| `content/academic.md` | 姓名与联系方式、简介、关键词、论文、教育、荣誉、经历 |
| `content/outdoors.md` | 户外头像路径、开场文字、年度数字、比赛与图片 |
| `assets/site.css` | 版式、颜色和照片裁切；日常改文字不用碰 |

`index.html` 和 `outdoors.html` 是自动生成的结果，**不要直接改**，否则下一次生成会覆盖。旧的 `../blog/` 是历史 Hexo 源码，不再用于发布。

## 1. 修改 Markdown

用 VS Code、Sublime Text 或其他文本编辑器打开上面两个 `.md` 文件。

文件开头 `---` 之间是设置，一行一个 `字段: 值`，可改预计毕业时间、Scholar 链接和图片路径。后面就是正文。

支持普通段落、`**加粗**`、`*斜体*`、`[链接文字](网址)`、`![图片说明](图片路径)`、`- 列表`。段落之间空一行。保留现有 `##` 分区标题，以便生成器识别。

论文照着已有记录复制一组：`### [标题](DOI)`，下面依次是“会议/期刊与等级或奖项”“作者”“正式引用信息”，三段之间各空一行。没有 CCF 等级就不写，不要为排版补等级。

户外页 `Race highlights` 和 `Selected routes` 下，每个 `###` 是一张卡片：标题、简短说明、图片。点击图片可查看原图。其余路线在 `More routes` 的列表里修改。素材目录 `assets/outdoors/races/`、`assets/outdoors/routes/`。海淀全马当前素材是完赛路线记录，不冒充正式证书；香山证书实际为第 3 名，与个人最好第 2 名分开标注。

## 2. 本地预览

在终端执行（整段复制即可）：

```sh
cd /Users/zhangjiale101/Desktop/D/00-WorkspaceArchive/Comprehensive/Career/Myblog/homepage
python3 build.py --serve
```

浏览器打开 http://localhost:8765/ ，户外页是 http://localhost:8765/outdoors.html 。

**保存 Markdown → 刷新浏览器**，预览会重新生成。终端按 `Control + C` 停止预览。

只生成文件、不启动浏览器服务：

```sh
python3 build.py
```

Python 使用标准库，没有 pip、Node 或 Hexo 安装步骤。

## 3. 发布到 GitHub

确认本地效果后，在同一目录执行：

```sh
python3 build.py --publish
```

这条命令依次完成 **生成 HTML → Git 提交 → 推送 main**。GitHub Pages 随后自动部署，可在 [Actions](https://github.com/TT885/TT885.github.io/actions) 查看是否成功。命令执行前即意味着你准备公开这次修改。

也可以继续直接告诉生涯助手改什么，由助手完成同一流程。

## 网址

`site_url` 只用于页面元数据，不会申请或变更域名。GitHub 免费用户站域名绑定 GitHub 用户名。2026-11-19 查询时，`zhangjiale` 账号已存在，不能直接将 TT885 的网站改到这个地址。后续选可用的姓名变体并迁移账号，或购买自己的域名再绑定。当前继续使用 `tt885.github.io`。

本轮追加查询：`zhangjiale101` 已存在；`zhangjiale100` 的公开用户 API 返回 404，最终是否可用以 GitHub 账号设置为准。迁移步骤：用户在 https://github.com/settings/admin 完成账号名修改，然后将原用户站仓库重命名为 `zhangjiale100.github.io`；更新本地 `origin` 与 `content/academic.md` 的 `site_url` 后重新生成发布。账号名尚未更改前，不预先将页面 canonical 或远程指向不存在的新地址。

## 内容来源

- 个人经历、荣誉和户外记录：用户既有主页、Career 画像、2025 年度户外报告与本轮明确修订。
- 本轮补充：预计 2027 毕业、2024–2026 滴滴实习、2022–2026 辅导员、2021–2023 MCM 训练营 TA、2022–2023 算法设计与分析 TA、国家级 IPP 项目主持及卓越助教奖，均由用户明确提供。
- 䇹政英文使用 Chun-Tsung，参照 [SJTU 官方英文资料](https://tdllib.sjtu.edu.cn/en/info/1761/12662.htm)。它与 PRP 是不同项目，旧译已纠正。
- Google Scholar 个人页：用户指定 `Xj2PkcsAAAAJ`。
- 五篇论文的题目、作者及引用信息：出版社 Crossref 元数据；COCOA DOI 为 `10.1007/978-3-031-49611-0_27`，作者顺序依正式出版记录。COCOA 2023 最佳论文奖依用户本轮确认。
- CCF-A：[TMC 官方目录](https://www.ccf.org.cn/Academic_Evaluation/CN/)、[TSC 官方目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)。只标注两篇 TMC 与一篇 TSC；WASA、COCOA 不标 A。
- DBLP 个人页：[Jiale Zhang 0016](https://dblp.org/pid/218/2216-16.html)，核对同一组论文与合作者。
- 设计参考：[公辰主页](https://gongchenooo.github.io/)。

原站的 `/projects/`、`/lectures/`、`/readings/` 和历史文章路径保留。新页面素材与原始照片分开，源照片不被修改。
