#!/usr/bin/env python3
import os
import json
import re

def parse_frontmatter(content):
    match = re.match(r'^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$', content)
    if not match:
        return {}, content
    
    yaml_text = match[1]
    body = match[2]
    meta = {}
    current_key = None
    
    for line in yaml_text.splitlines():
        line_str = line.strip()
        if not line_str or line_str.startswith('#'):
            continue
        if line_str.startswith('- ') and current_key:
            if not isinstance(meta.get(current_key), list):
                meta[current_key] = []
            meta[current_key].append(line_str[2:].strip().strip('"\''))
            continue
        if ':' in line_str:
            key, val = line_str.split(':', 1)
            key = key.strip()
            val = val.strip().strip('"\'')
            if not val:
                meta[key] = []
                current_key = key
            else:
                meta[key] = val
                current_key = None
    return meta, body

def escape_html(text):
    return (text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;"))

def render_markdown(text):
    lines = text.splitlines()
    html_lines = []
    in_code = False
    code_lang = ""
    code_buffer = []
    in_table = False
    table_rows = []

    def flush_table():
        nonlocal in_table, table_rows, html_lines
        if not table_rows:
            in_table = False
            return
        out = ['<table>']
        for i, row in enumerate(table_rows):
            cols = [c.strip() for c in row.strip('|').split('|')]
            if i == 0:
                out.append('<thead><tr>' + ''.join(f'<th>{escape_html(c)}</th>' for c in cols) + '</tr></thead><tbody>')
            elif i == 1 and '---' in row:
                continue
            else:
                out.append('<tr>' + ''.join(f'<td>{escape_html(c)}</td>' for c in cols) + '</tr>')
        out.append('</tbody></table>')
        html_lines.append('\n'.join(out))
        table_rows = []
        in_table = False

    for line in lines:
        stripped = line.strip()
        
        # Code Blocks
        if stripped.startswith('```'):
            if in_table:
                flush_table()
            if in_code:
                html_lines.append(f'<pre><code>{escape_html("\\n".join(code_buffer))}</code></pre>')
                code_buffer = []
                in_code = False
            else:
                in_code = True
                code_lang = stripped[3:].strip()
            continue

        if in_code:
            code_buffer.append(line)
            continue

        # Tables
        if stripped.startswith('|') and stripped.endswith('|'):
            in_table = True
            table_rows.append(stripped)
            continue
        elif in_table:
            flush_table()

        # Headings
        if line.startswith('## '):
            html_lines.append(f'<h2>{escape_html(line[3:])}</h2>')
        elif line.startswith('### '):
            html_lines.append(f'<h3>{escape_html(line[4:])}</h3>')
        elif line.startswith('# '):
            html_lines.append(f'<h1>{escape_html(line[2:])}</h1>')
        elif stripped:
            html_lines.append(f'<p>{escape_html(line)}</p>')

    if in_code and code_buffer:
        html_lines.append(f'<pre><code>{escape_html("\\n".join(code_buffer))}</code></pre>')
    if in_table:
        flush_table()

    return '\n'.join(html_lines)

def build():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    skills_json_path = os.path.join(root_dir, 'skills.json')
    
    if not os.path.exists(skills_json_path):
        print("skills.json not found!")
        return
        
    with open(skills_json_path, 'r', encoding='utf-8') as f:
        skills = json.load(f)
        
    for skill in skills:
        slug = skill['slug']
        skill_dir = os.path.join(root_dir, 'skills', slug)
        skill_md_path = os.path.join(skill_dir, 'SKILL.md')
        
        if not os.path.exists(skill_md_path):
            continue
            
        with open(skill_md_path, 'r', encoding='utf-8') as f:
            raw_md = f.read()
            
        meta, body = parse_frontmatter(raw_md)
        title = meta.get('name', skill.get('name', slug))
        icon = meta.get('icon', skill.get('icon', '⚡'))
        desc = meta.get('description', skill.get('desc', ''))
        status = meta.get('status', 'stable')
        version = meta.get('version', '1.0.0')
        category = meta.get('category', 'General')
        
        scripts = meta.get('scripts', [])
        if isinstance(scripts, str): scripts = [scripts]
            
        references = meta.get('references', [])
        if isinstance(references, str): references = [references]
            
        skill_body_html = render_markdown(body)
        
        scripts_html = ""
        for script_name in scripts:
            script_path = os.path.join(skill_dir, 'scripts', script_name)
            if os.path.exists(script_path):
                with open(script_path, 'r', encoding='utf-8') as f:
                    code_content = f.read()
                scripts_html += f"""
                <div class="file-block" id="file-script-{script_name}">
                  <div class="file-block-header">
                    <div class="file-title">⚡ skills/{slug}/scripts/{script_name}</div>
                  </div>
                  <div class="file-content">
                    <pre><code>{escape_html(code_content)}</code></pre>
                  </div>
                </div>
                """

        references_html = ""
        for ref_name in references:
            ref_path = os.path.join(skill_dir, 'references', ref_name)
            if os.path.exists(ref_path):
                with open(ref_path, 'r', encoding='utf-8') as f:
                    ref_md = f.read()
                _, ref_body = parse_frontmatter(ref_md)
                references_html += f"""
                <div class="file-block" id="file-ref-{ref_name}">
                  <div class="file-block-header">
                    <div class="file-title">📖 skills/{slug}/references/{ref_name}</div>
                  </div>
                  <div class="file-content doc">
                    {render_markdown(ref_body)}
                  </div>
                </div>
                """

        nav_links = []
        for s in skills:
            active_cls = "active" if s["slug"] == slug else ""
            nav_links.append(f'<a class="nav-link {active_cls}" href="../{s["slug"]}/index.html"><span>{s.get("icon","⚡")}</span> {escape_html(s["name"])}</a>')
                
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{escape_html(title)} — AgentSkills</title>
  <meta name="description" content="{escape_html(desc)}">
  <link rel="stylesheet" href="../../style.css">
</head>
<body>
  <div class="shell">
    <aside class="sidebar">
      <div class="sidebar-brand" onclick="location.href='../../index.html'">
        <div class="brand-icon">⚡</div>
        <span>AgentSkills</span>
      </div>
      <nav>
        <div class="nav-label">Overview</div>
        <a class="nav-link" href="../../index.html">Home</a>
        <div class="nav-label">Skills Catalog</div>
        <div>
          {''.join(nav_links)}
        </div>
      </nav>
    </aside>

    <div class="main">
      <header class="topbar">
        <a href="../../index.html">AgentSkills</a>
        <span class="sep">/</span>
        <a href="../../index.html">Catalog</a>
        <span class="sep">/</span>
        <span>{escape_html(title)}</span>
      </header>

      <main class="page">
        <div class="skill-header">
          <h1><span>{icon}</span> {escape_html(title)}</h1>
          <div class="skill-meta">
            <span class="badge {status}">{status}</span>
            <span class="badge tag">{version}</span>
            <span class="badge tag">{category}</span>
          </div>
          <p class="skill-desc">{escape_html(desc)}</p>
        </div>

        <!-- Section 1: SKILL.md -->
        <div class="file-block" id="file-skill-md">
          <div class="file-block-header">
            <div class="file-title">📄 skills/{slug}/SKILL.md</div>
            <span class="file-type-badge">Primary Specification</span>
          </div>
          <div class="file-content doc">
            {skill_body_html}
          </div>
        </div>

        <!-- Section 2: Scripts -->
        {f'<div class="section-banner">Scripts ({len(scripts)})</div>{scripts_html}' if scripts_html else ''}

        <!-- Section 3: References -->
        {f'<div class="section-banner">References ({len(references)})</div>{references_html}' if references_html else ''}
      </main>
    </div>
  </div>
</body>
</html>
"""
        out_file = os.path.join(skill_dir, 'index.html')
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Pre-rendered static HTML for {slug} -> {out_file}")

if __name__ == "__main__":
    build()
