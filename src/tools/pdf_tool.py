from pathlib import Path
import markdown
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

class ReportGenerator:
    def __init__(self, output_dir: str = "outputs/reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save_markdown(self, filename: str, content: str) -> Path:
        file_path = self.output_dir / f"{filename}.md"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return file_path

    def save_pdf(self, filename: str, content: str) -> Path:
        file_path = self.output_dir / f"{filename}.pdf"
        doc = SimpleDocTemplate(str(file_path), pagesize=letter)
        styles = getSampleStyleSheet()
        
        custom_body = ParagraphStyle(
            'ReportBody',
            parent=styles['Normal'],
            fontSize=10,
            leading=14,
            textColor=colors.HexColor('#2d3748')
        )
        
        story = []
        for line in content.split('\n'):
            line = line.strip()
            if not line:
                story.append(Spacer(1, 8))
            elif line.startswith('# '):
                story.append(Paragraph(line[2:], styles['Title']))
                story.append(Spacer(1, 10))
            elif line.startswith('## '):
                story.append(Paragraph(line[3:], styles['Heading2']))
                story.append(Spacer(1, 6))
            elif line.startswith('### '):
                story.append(Paragraph(line[4:], styles['Heading3']))
                story.append(Spacer(1, 4))
            else:
                story.append(Paragraph(line, custom_body))
                story.append(Spacer(1, 4))
                
        doc.build(story)
        return file_path
