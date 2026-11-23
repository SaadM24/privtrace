"""Render manuscripts with semantic headings, vector tables and explicit section breaks."""
import argparse
import re
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate,Paragraph,PageBreak,Spacer,Table,TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

TEAL="#0c6667"
INK="#193541"


def render(source,out,title,summary):
    reg,bold="Helvetica","Helvetica-Bold"
    fonts=Path("/usr/share/fonts/truetype/dejavu")
    if (fonts/"DejaVuSans.ttf").exists():
        pdfmetrics.registerFont(TTFont("PTSans",str(fonts/"DejaVuSans.ttf")))
        pdfmetrics.registerFont(TTFont("PTSansB",str(fonts/"DejaVuSans-Bold.ttf")))
        reg,bold="PTSans","PTSansB"
    def style(name,font,size,leading,space=0,color=INK):
        return ParagraphStyle(name,fontName=font,fontSize=size,leading=leading,spaceAfter=space,textColor=colors.HexColor(color))
    body=style("body",reg,10.3 if summary else 9.25,15.2 if summary else 13.1,9)
    h1=style("title",bold,24,30,8)
    h2=style("section",bold,17,22,10)
    h3=style("sub",bold,11.5,15,5,TEAL)
    cell=style("cell",reg,8.4,11)
    hdr=style("header",bold,8.2,11,0,"#ffffff")
    doc=SimpleDocTemplate(str(out),pagesize=A4,leftMargin=45,rightMargin=45,topMargin=57,bottomMargin=49,title=title,author="PRIVTRACE")
    lines=source.read_text().splitlines()
    flow=[]
    i=0
    while i<len(lines):
        line=lines[i]
        i+=1
        if not line:
            continue
        if line=="<!-- page -->":
            flow.append(PageBreak())
        elif line.startswith("|"):
            grid=[line]
            while i<len(lines) and lines[i].startswith("|"):
                grid.append(lines[i])
                i+=1
            rows=[]
            for j,line in enumerate(grid):
                if j!=1:
                    rows.append([Paragraph(escape(v.strip()),hdr if j==0 else cell) for v in line.strip("|").split("|")])
            n=len(rows[0])
            widths=[doc.width*.34]+[doc.width*.66/(n-1)]*(n-1)
            table=Table(rows,colWidths=widths,repeatRows=1,hAlign="LEFT")
            table.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor(TEAL)),
                     ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#eff6f5"),colors.white]),
                     ("VALIGN",(0,0),(-1,-1),"MIDDLE"),("TOPPADDING",(0,0),(-1,-1),5),
                     ("BOTTOMPADDING",(0,0),(-1,-1),5)]))
            flow.extend([table,Spacer(1,10)])
        else:
            level=len(line)-len(line.lstrip("#"))
            st={1:h1,2:h2,3:h3}.get(level,body)
            flow.append(Paragraph(escape(line[level:].strip()),st))
    def frame(c,d):
        w,h=A4
        c.setFillColor(colors.HexColor(TEAL))
        c.setFont(bold,8.5)
        c.drawString(45,h-32,"PRIVTRACE   /   "+("RESEARCH SUMMARY" if summary else "TECHNICAL REPORT"))
        c.setStrokeColor(colors.HexColor("#abcac7"))
        c.line(45,h-40,w-45,h-40)
        c.line(45,37,w-45,37)
        c.setFont(reg,8)
        c.drawString(45,23,"Private research release   ·   v0.2   ·   November 2026")
        c.drawRightString(w-45,23,str(d.page))
    doc.build(flow,onFirstPage=frame,onLaterPages=frame)


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--out",type=Path,default=Path("papers"))
    dest=p.parse_args().out
    dest.mkdir(exist_ok=True,parents=True)
    for file,stem,title,short in [(Path("TECHNICAL_REPORT.md"),"Technical_Report","Online disclosure planning",False),
        (Path("docs/COMMITTEE_SUMMARY.md"),"Research_Summary","Online privacy-aware planning",True)]:
        render(file,dest/("PRIVTRACE_v02_"+stem+".pdf"),title,short)
