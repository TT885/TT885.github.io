# 个人主页：编辑与发布

线上：[学术主页](https://tt885.github.io/) · [户外页面](https://tt885.github.io/outdoors.html) · [DDL 页面](https://tt885.github.io/ddls/)

## 平时改哪里？

| 文件 | 内容 |
| --- | --- |
| `content/academic.md` | 姓名与联系方式、简介、关键词、论文、教育、荣誉、经历 |
| `content/outdoors.md` | 户外头像路径、开场文字、年度数字、比赛与图片 |
| `content/deadlines.json` | 12 个会议的官方截止日期、轮次、时区、来源与核对日期 |
| `assets/site.css` | 版式、颜色和照片裁切；日常改文字不用碰 |

`index.html`、`outdoors.html` 和 `ddls/index.html` 是自动生成的结果，**不要直接改**，否则下一次生成会覆盖。旧的 `../blog/` 是历史 Hexo 源码，不再用于发布。

## 1. 修改 Markdown

用 VS Code、Sublime Text 或其他文本编辑器打开上面两个 `.md` 文件。

文件开头 `---` 之间是设置，一行一个 `字段: 值`，可改预计毕业时间、Scholar 链接和图片路径。后面就是正文。

支持普通段落、`**加粗**`、`*斜体*`、`[链接文字](网址)`、`![图片说明](图片路径)`、`- 列表`。段落之间空一行。保留现有 `##` 分区标题，以便生成器识别。

论文照着已有记录复制一组：`### [标题](DOI)`，下面依次是“会议/期刊与等级或奖项”“作者”“正式引用信息”，三段之间各空一行。没有 CCF 等级就不写，不要为排版补等级。

户外页依次为 `My Route`、`More routes`、`Personal Best`。`My Route` 和 `Personal Best` 下，每个 `###` 是一张卡片：标题、简短说明、图片。点击图片可查看原图。素材目录 `assets/outdoors/races/`、`assets/outdoors/routes/`。路线图按完整比例显示，保留距离、爬升、时间；源截图不裁切。六张路线卡为五条 Trail Running 与一条 Cycling。香山第二名使用本轮提供的真实奖杯图；海淀全马当前仍是完赛记录图。

户外页独立视觉样式在 `assets/outdoors.css`；学术页继续用 `assets/site.css`。生成器按 CSS 内容自动添加版本号，更新版式后避免继续读到旧样式。

## 2. 本地预览

在终端执行（整段复制即可）：

```sh
cd /Users/zhangjiale101/Desktop/D/00-WorkspaceArchive/Comprehensive/Career/Myblog/homepage
python3 build.py --serve
```

浏览器打开 http://localhost:8765/ ，户外页是 http://localhost:8765/outdoors.html 。

会议页是 http://localhost:8765/ddls/ 。修改 JSON 后刷新，同样自动重新生成。

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

## DDL 页怎么维护？

只改 `content/deadlines.json`，仍执行 `python3 build.py` / `python3 build.py --publish`。这是公开网站：只记录公开会议数据，不放个人稿件、研究计划或申请进度。页面“自用”不等于访问加密。

- 一个会议一条记录，`cycles` 中分别保留摘要 `abstract` 与全文 `paper`；只跟踪主会研究论文，不混用修订、Industry、Workshop 或 camera-ready 日期。
- 精确时刻写 `at`，使用带时区的 ISO 格式，如 `2027-01-14T23:59:00-12:00`。`original` 保留官网的原始日期及时区；AoE 是 UTC−12，不是北京时间。Pacific Time 要按日期区分 PST / PDT。
- 官网只给日期时写 `date`（如 `2027-01-14`）、`zone`（AoE 或 null）和 `original`，不要同时写 `at`，不要猜时分。日期级记录不换算成精确的北京时间。
- 日期未知写 `null`。已知还有一轮、但日期未公布时设 `pending: true`，并在 `note` 中写明；过去一届全截止、下一届还未核验的保留旧届并说明，不猜算下一届。
- 修改后更新该会议 `checked`；只有整页重新核对时才更新顶层 `checked`。来源必须保留官方 URL。官方延期时更新相应轮次，并在 `note` 简记变更。
- 页面随设备时钟自动排序、更新倒计时；**不会自动联网刷新会议数据，也未设置后台定时任务**。建议实际准备投稿时再次打开官方 CFP 确认。

页面布局：`assets/deadlines.css`；交互：`assets/deadlines.js`；生成与数据校验：`deadlines.py`。无新依赖，断网也能打开已生成页面查看已保存的数据和入口。设计参考 [Weihao Cui 的 DDL 页面](https://weihao-cui.com/ddls/)，日期逐项核对官方来源，未沿用第三方预测。
