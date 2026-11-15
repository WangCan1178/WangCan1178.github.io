---
layout: page
permalink: /service/
title: service
title_zh: 学术服务
nav: true
nav_order: 2
---

<div class="lang-only" data-lang="en">
{% capture service_en %}{% include service/en.md %}{% endcapture %}
{{ service_en | markdownify }}
</div>
<div class="lang-only" data-lang="zh">
{% capture service_zh %}{% include service/zh.md %}{% endcapture %}
{{ service_zh | markdownify }}
</div>
