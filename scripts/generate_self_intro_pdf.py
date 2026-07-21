#!/usr/bin/env python3
"""Generate academic self-introduction PDF from homepage content."""

from pathlib import Path

from fpdf import FPDF

OUT = Path("/Users/xiaocan/Desktop/Can_Wang_Self_Introduction.pdf")
PHOTO = Path("/Users/xiaocan/pages/assets/img/prof_pic.jpg")
FONT = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
NAME = "Can Wang"
LINE_H = 4.5


class IntroPDF(FPDF):
    def footer(self):
        self.set_y(-12)
        self.set_font("Body", size=8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, f"{self.page_no()}", align="C")


def section_title(pdf: IntroPDF, title: str):
    pdf.ln(2)
    pdf.set_font("Body", size=12)
    pdf.set_text_color(42, 111, 151)
    pdf.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(42, 111, 151)
    pdf.set_line_width(0.4)
    y = pdf.get_y()
    pdf.line(pdf.l_margin, y, pdf.w - pdf.r_margin, y)
    pdf.ln(3)
    pdf.set_text_color(30, 30, 30)


def bullet(pdf: IntroPDF, text: str, indent: float = 0):
    pdf.set_font("Body", size=9.2)
    x = pdf.l_margin + indent
    pdf.set_x(x)
    pdf.multi_cell(pdf.w - pdf.r_margin - x, LINE_H, f"•  {text}")


def _write_chunk(pdf: IntroPDF, text: str, *, bold_underline: bool = False):
    """Write text with wrapping; optionally bold+underline via Helvetica-Bold."""
    if not text:
        return
    if bold_underline:
        pdf.set_font("Helvetica", "BU", 9.2)
    else:
        pdf.set_font("Body", size=9.2)

    max_x = pdf.w - pdf.r_margin
    for ch in text:
        w = pdf.get_string_width(ch)
        if pdf.get_x() + w > max_x:
            pdf.ln(LINE_H)
            pdf.set_x(pdf.l_margin)
            if bold_underline:
                pdf.set_font("Helvetica", "BU", 9.2)
            else:
                pdf.set_font("Body", size=9.2)
        pdf.cell(w, LINE_H, ch)


def pub_bullet(pdf: IntroPDF, text: str):
    """Publication bullet with own name bold + underlined."""
    pdf.set_text_color(30, 30, 30)
    pdf.set_x(pdf.l_margin)
    _write_chunk(pdf, "•  ")
    parts = text.split(NAME)
    for i, part in enumerate(parts):
        if i > 0:
            _write_chunk(pdf, NAME, bold_underline=True)
        _write_chunk(pdf, part)
    pdf.ln(LINE_H + 0.8)


def main():
    pdf = IntroPDF(format="A4")
    pdf.set_auto_page_break(auto=True, margin=14)
    pdf.add_font("Body", "", FONT)
    pdf.add_page()
    pdf.set_margins(16, 14, 16)

    left_w = 138
    if PHOTO.exists():
        pdf.image(str(PHOTO), x=pdf.w - pdf.r_margin - 32, y=14, w=32)

    pdf.set_font("Body", size=20)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(left_w, 9, "Can Wang (王灿)", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Body", size=11)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(left_w, 6, "Ph.D. Student in Software Engineering", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(left_w, 6, "Harbin Institute of Technology (HIT)", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Body", size=9)
    pdf.set_text_color(80, 80, 80)
    pdf.multi_cell(
        left_w,
        4.5,
        "Email: 23B903072@stu.hit.edu.cn\n"
        "Homepage: https://WangCan1178.github.io\n"
        "GitHub: https://github.com/WangCan1178",
    )

    section_title(pdf, "About")
    pdf.set_font("Body", size=9.5)
    bio = (
        "I am a Ph.D. student in Software Engineering at Harbin Institute of Technology (HIT), "
        "under the supervision of Prof. Zhiying Tu. I am affiliated with the Research Center of "
        "Intelligent Computing for Enterprises & Services (ICES). Previously, I received my B.E. in "
        "Software Engineering from HIT.\n\n"
        "I study LLM agents, focusing on making large language model services more effective, "
        "reliable, and usable in real systems. Currently, I work on controllable data synthesis "
        "and training at Alibaba Cloud Tongyi. Previously, I worked on "
        "service invocation, performance estimation, and self-improvement for LLM agents."
    )
    pdf.multi_cell(0, 4.6, bio)

    section_title(pdf, "Education")
    bullet(
        pdf,
        "Ph.D. in Software Engineering, Harbin Institute of Technology, Sep. 2023 – Present (Advisor: Prof. Zhiying Tu)",
    )
    bullet(
        pdf,
        "B.E. in Software Engineering, Harbin Institute of Technology, Sep. 2019 – Jun. 2023 (GPA: 90.28/100; Rank: 2/33)",
    )

    section_title(pdf, "Experience")
    bullet(
        pdf,
        "Research Intern, Alibaba Cloud Tongyi, 2025 – Present — Controllable data synthesis and training",
    )
    bullet(
        pdf,
        "Head of Algorithms, Shenzhen Yangli Technology Enterprises (AI-for-Science startup), 2026 – Present — AI-assisted finite element analysis for scientific research",
    )
    bullet(
        pdf,
        "National Key R&D Program, ICES, 2024 – 2025 — Key technologies for large-scale complex digital service networks",
    )

    section_title(pdf, "Publications")
    # Ordered by authorship (first → second → third); arXiv entries last.
    # Own name is bold + underlined in each entry.
    publications = [
        "Can Wang, Dianbo Sui, Bolin Zhang, Xiaoyu Liu, Jiabao Kang, Zhidong Qiao, Zhiying Tu. A Framework for Effective Invocation Methods of Various LLM Services. In COLING 2025 (CCF-B), pages 6953–6965.",
        "Can Wang, Hao Ding, Yongchao Xing, Bohai Zhao, Dianbo Sui, Zhiying Tu. Unlocking Hidden Capabilities: A Self-Improving Workflow for Chatbots to Utilize Unintegrated Services. In IEEE ICWS 2025 (CCF-B), pages 498–500.",
        "Can Wang, Dianbo Sui, Hongliang Sun, Hao Ding, Bolin Zhang, Zhiying Tu. Plug-and-Play Performance Estimation for LLM Services without Relying on Labeled Data. In ICSOC 2024 (CCF-B), pages 202–217.",
        "Hao Ding, Can Wang, J. Li, X. Piao, B. Jia, J. Ai, H. Song, Z. Ji. Latency Performance Modeling and Analysis for Cross-Chain Transaction Processing. Simulation Modelling Practice and Theory, 2026, 103304 (JCR-Q1).",
        "Hao Ding, Can Wang, J. Li, H. Ren, X. Piao, H. Song, Z. Ji. Revisiting NFT Transactions in Web 3.0 Service Through the Lenses of Higher-Order Network. In IEEE ICWS 2025 (CCF-B), pages 873–879.",
        "Hongliang Sun, Jinlan Liu, Can Wang, Jiabao Kang, Zhiying Tu, Dianhui Chu, Xiaofei Xu. MSKD: A Knowledge Denoising Framework for Metaverse Service Recommendation. IEEE Transactions on Services Computing, 2025 (CCF-A, JCR-Q1).",
        "Hongliang Sun, Jinlan Liu, Can Wang, Dianbo Sui, Zhiying Tu, Xiaofei Xu. Learning Dynamic Knowledge Graph Embedding in Evolving Service Ecosystems via Meta-Learning. In IEEE ICWS 2024 (CCF-B), pages 601–610.",
        "Bolin Zhang, Zhiying Tu, Can Wang, Hongliang Sun, Dianhui Chu. Requirements Elicitation and Response Generation for Conversational Services. Applied Intelligence, 54(7):5576–5592, 2024 (CCF-C, JCR-Q2).",
        "Can Wang, Shengwei Wang, Bolin Zhang, Zhiying Tu, Dianhui Chu. An Effective Router for Vision-Language Model Selection. arXiv preprint arXiv:2606.08970, 2026.",
        "Haowen Gao, Haoran Chen, Can Wang, Shasha Guo, Liang Pang, Zhaoyang Liu, Huawei Shen, Xueqi Cheng. SkillAudit: Ground-Truth-Free Skill Evolution via Paired Trajectory Auditing. arXiv preprint arXiv:2606.14239, 2026.",
    ]
    for p in publications:
        pub_bullet(pdf, p)

    section_title(pdf, "Academic Service")
    bullet(
        pdf,
        "Conference Reviewer: ICML 2026, NeurIPS 2026, ACM MM 2026, ICWS 2025, ICSOC 2025",
    )
    bullet(pdf, "Journal Reviewer: IEEE Transactions on Services Computing (TSC)")

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
        bullet(pdf, h)

    pdf.output(str(OUT))
    site_out = Path("/Users/xiaocan/pages/assets/pdf/Can_Wang_Self_Introduction.pdf")
    site_out.parent.mkdir(parents=True, exist_ok=True)
    site_out.write_bytes(OUT.read_bytes())
    print(f"Wrote {OUT}")
    print(f"Wrote {site_out}")


if __name__ == "__main__":
    main()
