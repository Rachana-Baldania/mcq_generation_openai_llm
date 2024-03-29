from app.parsers import json, csv, docx, html, pdf, txt, youtube, sitemap, urls

FILE_PARSER = {
    ".json": json.parse_json,
    ".csv": csv.parse_csv,
    ".txt": txt.parse_txt,
    ".docx": docx.parse_docx,
    ".pdf": pdf.parse_pdf,
    ".html": html.parse_html,
    ".htm": html.parse_html,
}

URL_PARSERS = {
    "youtube": youtube.parse_youtube_video,
    "sitemap": sitemap.parse_sitemap,
    "webpage": urls.parse_url,
}
