# Jiale Zhang / 张嘉乐 — Personal homepage

Live: https://tt885.github.io/  
Outdoor page: https://tt885.github.io/outdoors.html

This repository is the directly published GitHub Pages website. The November 2026 refresh uses plain HTML and CSS. No build or package installation is needed.

## Edit

- `index.html`: academic biography, publications, education, honors, experience, links.
- `outdoors.html`: outdoor profile and 2025 annual recap.
- `assets/site.css`: layout, colors, responsive behavior, portrait crops.
- `assets/profile/`: supplied portrait compositions. CSS crops out the text panels; original files in `Myblog/个人形象制作/` remain unchanged.
- `assets/outdoors/`: selected public annual-report images.

Preview from this directory:

```sh
python3 -m http.server 8765
```

Open http://localhost:8765/ and http://localhost:8765/outdoors.html.

Publish selected edits:

```sh
git diff
git add index.html outdoors.html assets/site.css assets/profile assets/outdoors assets/favicon.svg README.md .nojekyll
git commit -m "Update personal homepage"
git push origin main
```

The sibling `blog/` directory is the old Hexo source. Its historical pages and assets are retained here at their original routes, including `/projects/`, `/lectures/`, `/readings/` and `/2022/`. Running the old Hexo deployment would replace the new homepage, so future edits should use this checkout.

## Content provenance — checked 2026-11-19

- Professional biography, email, education and earlier honors: pre-existing personal homepage and local source `blog/source/_posts/01-intro.md`; advisor and research context also supplied by the owner.
- Publication titles, author order and journal issue/page metadata: publisher-deposited Crossref DOI records for `10.1109/TMC.2022.3229112`, `10.1109/TSC.2024.3376231`, `10.1109/TMC.2025.3558275`, `10.1007/978-981-96-8728-2_34`. The first TMC paper has 2022 early access and a 2024 journal issue; displayed as TMC 2024 with the early-access year noted.
- WASA Best Paper Award: owner-provided career record and coauthor Xiaochun Yang's official faculty publication list: https://faculty.neu.edu.cn/yangxiaochun/zh_CN/zdylm/266014/list/index.htm .
- National Scholarship: owner-provided career profile. Award year is omitted because it was not confirmed in the materials inspected.
- DiDi research description: owner's project updates. Exact internship dates are omitted pending confirmation.
- ORCID: author's identifier in the TSC/TMC DOI metadata. Scholar and DBLP links are explicitly searches, not guessed profile identifiers.
- Outdoor statistics: owner-supplied `2025户外年度总结-张嘉乐-小红书发布版.docx` and associated images. Distances are not added across tracking platforms. Body-weight and dietary records were not included in the page.
- Layout reference: https://gongchenooo.github.io/ . The implementation and copy are original; no theme code or third-party portrait was copied.

Next editorial pass: confirm preferred English translations of undergraduate honors; add a confirmed Scholar/DBLP profile URL and a public CV when ready; add exact internship and award dates only after checking them.
