#!/usr/bin/env python3
"""Generate academic self-introduction PDF from homepage content."""

from __future__ import annotations

import re
from pathlib import Path

from fpdf import FPDF

OUT = Path("/Users/xiaocan/Desktop/Can_Wang_Self_Introduction.pdf")
PHOTO = Path("/Users/xiaocan/pages/assets/img/self_intro_pic.jpg")
FONT = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
NAME = "Can Wang"
LINE_H = 4.55
LINK_RGB = (0, 102, 204)
TEXT_RGB = (30, 30, 30)

URL_ADVISOR = "https://homepage.hit.edu.cn/tzy"
URL_TONGYI = "https://tongyi.aliyun.com/"
URL_HOME = "https://WangCan1178.github.io"
URL_GITHUB = "https://github.com/WangCan1178"
URL_EMAIL = "mailto:23B903072@stu.hit.edu.cn"
URL_SCHOLAR = "https://scholar.google.com/citations?user=glKP6tYAAAAJ"
URL_OPENREVIEW = "https://openreview.net/profile?id=~Can_Wang9"


class IntroPDF(FPDF):
    def footer(self):
        self.set_y(-10)
        self.set_font("Body", size=8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 7, f"{self.page_no()}", align="C")


def section_title(pdf: IntroPDF, title: str):
    pdf.ln(2)
    pdf.set_font("Body", size=12)
    pdf.set_text_color(42, 111, 151)
    pdf.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(42, 111, 151)
    pdf.set_line_width(0.4)
    y = pdf.get_y()
    pdf.line(pdf.l_margin, y, pdf.w - pdf.r_margin, y)
    pdf.ln(2.3)
    pdf.set_text_color(*TEXT_RGB)


def _apply_style(pdf: IntroPDF, *, size: float, kind: str):
    if kind == "name":
        pdf.set_font("Helvetica", "BU", size)
        pdf.set_text_color(*TEXT_RGB)
    elif kind == "link":
        pdf.set_font("Body", size=size)
        pdf.set_text_color(*LINK_RGB)
    else:
        pdf.set_font("Body", size=size)
        pdf.set_text_color(*TEXT_RGB)


def _underline(pdf: IntroPDF, x: float, y: float, w: float, line_h: float):
    pdf.set_draw_color(*LINK_RGB)
    pdf.set_line_width(0.25)
    yy = y + line_h - 0.7
    pdf.line(x, yy, x + w, yy)


def _emit_token(
    pdf: IntroPDF,
    tok: str,
    *,
    link: str | None,
    kind: str,
    size: float,
    line_h: float,
    max_x: float,
):
    _apply_style(pdf, size=size, kind=kind)
    w = pdf.get_string_width(tok)
    if tok.isspace():
        if pdf.get_x() + w > max_x:
            pdf.ln(line_h)
            pdf.set_x(pdf.l_margin)
        else:
            pdf.cell(w, line_h, tok)
        return
    if pdf.get_x() + w > max_x:
        pdf.ln(line_h)
        pdf.set_x(pdf.l_margin)
        _apply_style(pdf, size=size, kind=kind)
        w = pdf.get_string_width(tok)
    x0, y0 = pdf.get_x(), pdf.get_y()
    pdf.cell(w, line_h, tok, link=link or "")
    if kind == "link":
        _underline(pdf, x0, y0, w, line_h)


def write_runs(
    pdf: IntroPDF,
    runs: list[tuple[str, str | None, str]],
    *,
    size: float = 9.2,
    line_h: float = LINE_H,
    bullet: bool = False,
):
    """Write styled runs with wrapping.

    Each run is (text, link_or_None, kind) where kind in {"text", "link", "name"}.
    """
    pdf.set_x(pdf.l_margin)
    max_x = pdf.w - pdf.r_margin
    items = ([("•  ", None, "text")] if bullet else []) + list(runs)

    for text, link, kind in items:
        if not text:
            continue
        for tok in re.findall(r"\S+|\s+", text):
            _emit_token(
                pdf, tok, link=link, kind=kind, size=size, line_h=line_h, max_x=max_x
            )
    pdf.ln(line_h + 0.35)
    pdf.set_text_color(*TEXT_RGB)


def write_paragraph_runs(
    pdf: IntroPDF,
    runs: list[tuple[str, str | None, str]],
    *,
    size: float = 9.5,
    line_h: float = 4.6,
):
    """Like write_runs but paragraph spacing."""
    max_x = pdf.w - pdf.r_margin
    pdf.set_x(pdf.l_margin)
    for text, link, kind in runs:
        if not text:
            continue
        if text == "\n":
            pdf.ln(line_h)
            pdf.set_x(pdf.l_margin)
            continue
        for tok in re.findall(r"\S+|\s+", text):
            _emit_token(
                pdf, tok, link=link, kind=kind, size=size, line_h=line_h, max_x=max_x
            )
    pdf.ln(line_h)
    pdf.set_text_color(*TEXT_RGB)


def name_runs(text: str) -> list[tuple[str, str | None, str]]:
    """Split text and highlight own name."""
    runs: list[tuple[str, str | None, str]] = []
    parts = text.split(NAME)
    for i, part in enumerate(parts):
        if i > 0:
            runs.append((NAME, None, "name"))
        if part:
            runs.append((part, None, "text"))
    return runs


def pub_line(pdf: IntroPDF, before_title: str, title: str, title_url: str, after_title: str):
    # Titles stay clickable, but use normal black body style (no blue/underline).
    runs = name_runs(before_title)
    runs.append((title, title_url, "text"))
    runs.extend(name_runs(after_title))
    write_runs(pdf, runs, bullet=True, size=9.15, line_h=4.45)


def contact_line(
    pdf: IntroPDF,
    label: str,
    text: str,
    url: str,
    *,
    left_w: float | None = None,
    size: float = 9.0,
    line_h: float = 4.3,
):
    """Label in gray + URL shown as blue underlined clickable text."""
    max_x = (pdf.l_margin + left_w) if left_w is not None else (pdf.w - pdf.r_margin)
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Body", size=size)
    pdf.set_text_color(80, 80, 80)
    label_w = pdf.get_string_width(label)
    pdf.cell(label_w, line_h, label)

    pdf.set_font("Body", size=size)
    pdf.set_text_color(*LINK_RGB)
    for ch in text:
        w = pdf.get_string_width(ch)
        if pdf.get_x() + w > max_x:
            pdf.ln(line_h)
            pdf.set_x(pdf.l_margin)
            pdf.set_font("Body", size=size)
            pdf.set_text_color(*LINK_RGB)
        x0, y0 = pdf.get_x(), pdf.get_y()
        pdf.cell(w, line_h, ch, link=url)
        _underline(pdf, x0, y0, w, line_h)
    pdf.ln(line_h)
    pdf.set_text_color(80, 80, 80)


def main():
    pdf = IntroPDF(format="A4")
    pdf.set_auto_page_break(auto=True, margin=13)
    pdf.add_font("Body", "", FONT)
    pdf.add_page()
    pdf.set_margins(16, 13, 16)

    # Portrait MEITU photo is taller; size for a reasonable headshot height.
    photo_w = 28
    photo_y = 13
    left_w = pdf.w - pdf.l_margin - pdf.r_margin - photo_w - 6
    if PHOTO.exists():
        pdf.image(str(PHOTO), x=pdf.w - pdf.r_margin - photo_w, y=photo_y, w=photo_w)

    pdf.set_font("Body", size=20)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(left_w, 9, "Can Wang (王灿)", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Body", size=11)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(
        left_w,
        6,
        "Ph.D. Student in Software Engineering, Harbin Institute of Technology (HIT)",
        new_x="LMARGIN",
        new_y="NEXT",
    )

    # Keep contacts beside the photo; long URLs wrap within left column.
    contact_line(pdf, "Email: ", "23B903072@stu.hit.edu.cn", URL_EMAIL, left_w=left_w)
    contact_line(pdf, "Homepage: ", URL_HOME, URL_HOME, left_w=left_w)
    contact_line(pdf, "GitHub: ", URL_GITHUB, URL_GITHUB, left_w=left_w)
    contact_line(pdf, "Google Scholar: ", URL_SCHOLAR, URL_SCHOLAR, left_w=left_w)
    contact_line(pdf, "OpenReview: ", URL_OPENREVIEW, URL_OPENREVIEW, left_w=left_w)

    section_title(pdf, "About")
    write_paragraph_runs(
        pdf,
        [
            ("I am a Ph.D. student in Software Engineering at ", None, "text"),
            ("Harbin Institute of Technology (HIT)", None, "text"),
            (", under the supervision of Prof. ", None, "text"),
            ("Zhiying Tu", URL_ADVISOR, "link"),
            (". I am affiliated with ICES. Previously, I received my B.E. in Software Engineering from HIT.", None, "text"),
            ("\n", None, "text"),
            ("\n", None, "text"),
            (
                "I study LLM agents, focusing on making large language model services more effective, "
                "reliable, and usable in real applications. Currently, I work on controllable data synthesis "
                "and training for the financial domain at ",
                None,
                "text",
            ),
            ("Alibaba Cloud Tongyi", URL_TONGYI, "link"),
            (
                ". Previously, I worked on LLM invocation quality and self-improvement for LLM agents.",
                None,
                "text",
            ),
        ],
        size=9.4,
        line_h=4.55,
    )

    section_title(pdf, "Education")
    write_runs(
        pdf,
        [
            (
                "Ph.D. in Software Engineering, Harbin Institute of Technology, Sep. 2023 – Present "
                "(Advisor: Prof. ",
                None,
                "text",
            ),
            ("Zhiying Tu", URL_ADVISOR, "link"),
            (")", None, "text"),
        ],
        bullet=True,
        size=9.2,
    )
    write_runs(
        pdf,
        [
            (
                "B.E. in Software Engineering, Harbin Institute of Technology, Sep. 2019 – Jun. 2023 "
                "(GPA: 90.28/100; Rank: 2/33)",
                None,
                "text",
            )
        ],
        bullet=True,
        size=9.2,
    )

    section_title(pdf, "Experience")
    write_runs(
        pdf,
        [
            ("Research Intern, ", None, "text"),
            ("Alibaba Cloud Tongyi", URL_TONGYI, "link"),
            (
                ", 2025 – Present — Controllable data synthesis and training for the financial domain",
                None,
                "text",
            ),
        ],
        bullet=True,
        size=9.2,
    )
    write_runs(
        pdf,
        [
            (
                "National Key R&D Program, ICES, 2024 – 2025 — Key technologies for "
                "large-scale complex digital service networks",
                None,
                "text",
            ),
        ],
        bullet=True,
        size=9.2,
    )

    section_title(pdf, "Publications")
    publications = [
        (
            "Can Wang, Dianbo Sui, Bolin Zhang, Xiaoyu Liu, Jiabao Kang, Zhidong Qiao, Zhiying Tu. ",
            "A Framework for Effective Invocation Methods of Various LLM Services",
            "https://aclanthology.org/2025.coling-main.464/",
            ". In COLING 2025 (CCF-B), pages 6953–6965.",
        ),
        (
            "Can Wang, Hao Ding, Yongchao Xing, Bohai Zhao, Dianbo Sui, Zhiying Tu. ",
            "Unlocking Hidden Capabilities: A Self-Improving Workflow for Chatbots to Utilize Unintegrated Services",
            "https://ieeexplore.ieee.org/document/11169693/",
            ". In IEEE ICWS 2025 (CCF-B), pages 498–500.",
        ),
        (
            "Can Wang, Dianbo Sui, Hongliang Sun, Hao Ding, Bolin Zhang, Zhiying Tu. ",
            "Plug-and-Play Performance Estimation for LLM Services without Relying on Labeled Data",
            "https://link.springer.com/chapter/10.1007/978-981-96-0805-8_15",
            ". In ICSOC 2024 (CCF-B), pages 202–217.",
        ),
        (
            "Hao Ding, Can Wang, J. Li, X. Piao, B. Jia, J. Ai, H. Song, Z. Ji. ",
            "Latency Performance Modeling and Analysis for Cross-Chain Transaction Processing",
            "https://doi.org/10.1016/j.simpat.2026.103304",
            ". Simulation Modelling Practice and Theory, 2026, 103304 (JCR-Q1).",
        ),
        (
            "Hao Ding, Can Wang, J. Li, H. Ren, X. Piao, H. Song, Z. Ji. ",
            "Revisiting NFT Transactions in Web 3.0 Service Through the Lenses of Higher-Order Network",
            "https://doi.org/10.1109/icws67624.2025.00113",
            ". In IEEE ICWS 2025 (CCF-B), pages 873–879.",
        ),
        (
            "Hongliang Sun, Jinlan Liu, Can Wang, Jiabao Kang, Zhiying Tu, Dianhui Chu, Xiaofei Xu. ",
            "MSKD: A Knowledge Denoising Framework for Metaverse Service Recommendation",
            "https://ieeexplore.ieee.org/document/11216084/",
            ". IEEE Transactions on Services Computing, 2025 (CCF-A, JCR-Q1).",
        ),
        (
            "Hongliang Sun, Jinlan Liu, Can Wang, Dianbo Sui, Zhiying Tu, Xiaofei Xu. ",
            "Learning Dynamic Knowledge Graph Embedding in Evolving Service Ecosystems via Meta-Learning",
            "https://ieeexplore.ieee.org/document/10707511/",
            ". In IEEE ICWS 2024 (CCF-B), pages 601–610.",
        ),
        (
            "Bolin Zhang, Zhiying Tu, Can Wang, Hongliang Sun, Dianhui Chu. ",
            "Requirements Elicitation and Response Generation for Conversational Services",
            "https://link.springer.com/article/10.1007/s10489-024-05454-6",
            ". Applied Intelligence, 54(7):5576–5592, 2024 (CCF-C, JCR-Q2).",
        ),
    ]
    for before, title, url, after in publications:
        pub_line(pdf, before, title, url, after)

    section_title(pdf, "Academic Service")
    write_runs(
        pdf,
        [
            (
                "Conference Reviewer: AAAI 2026, ICML 2026, NeurIPS 2026, ACM MM 2026, ICWS 2025, ICSOC 2025",
                None,
                "text",
            )
        ],
        bullet=True,
        size=9.2,
    )
    write_runs(
        pdf,
        [("Journal Reviewer: IEEE Transactions on Services Computing (TSC)", None, "text")],
        bullet=True,
        size=9.2,
    )

    section_title(pdf, "Honors")
    honors = [
        "National First Prize, The 19th Challenge Cup National College Students' Competition",
        "Silver Award, China International College Students' Innovation Competition, 2025",
        "Outstanding Graduate of Shandong Province, 2023",
        "Meritorious Winner, Mathematical Contest in Modeling (MCM/ICM), 2022",
        "National Scholarship, 2021",
        "Second Prize, RoboMaster National University Robot Competition, 2021",
    ]
    for h in honors:
        write_runs(pdf, [(h, None, "text")], bullet=True, size=9.2)

    pdf.output(str(OUT))
    site_out = Path("/Users/xiaocan/pages/assets/pdf/Can_Wang_Self_Introduction.pdf")
    site_out.parent.mkdir(parents=True, exist_ok=True)
    site_out.write_bytes(OUT.read_bytes())
    print(f"Wrote {OUT}")
    print(f"Wrote {site_out}")


if __name__ == "__main__":
    main()
