import re
import os
import sys
import base64
import mimetypes
from pathlib import Path

def _package_environ(html, pattern, pre, post):

    # Find all matches
    matches = re.findall(pattern, html, flags=re.IGNORECASE)

    # Detected matches
    tags = []
    fnames = []
    for full_tag, filename in matches:
        tags.append(full_tag)
        fnames.append(filename)
       
    # replace
    for tag, fname in zip(tags, fnames):
        with open(fname, 'r') as f:
            content = f.read() 

        block  = f"\n<!-- {fname} -->\n"
        block += pre
        block += content
        block += post

        html = html.replace(tag, block)

        if len(fnames)>0:
            base_file_path = Path(fnames[0]).parent
        else:
            base_file_path = None

    return html, base_file_path


def package_css(html):
    # Pattern for finding css
    pattern = r'(<\s*link\b[^>]*rel\s*=\s*["\']stylesheet["\'][^>]*href\s*=\s*["\']([^"\']+)["\'][^>]*>)'

    pre  = "<style>\n"
    post = "\n</style>\n\n"
    return _package_environ(html, pattern, pre, post)

def package_script(html):
    # Pattern for finding script
    pattern = r'(<\s*script\b[^>]*src\s*=\s*["\']([^"\']+)["\'][^>]*>\s*</script>)'

    pre  = "<script>\n"
    post = "\n</script>\n\n"
    return _package_environ(html, pattern, pre, post)[0]

def encodeImage(fileN):
    with open(fileN, "rb") as image_file:
        encoded_img = base64.b64encode(image_file.read())
        mime = mimetypes.guess_type(fileN)[0]
    return mime, encoded_img

def package_imgs(html, css_base):
    
    # img tags
    pattern = r'(<\s*img\b[^>]*src\s*=\s*["\'])([^"\']+)(["\'][^>]*>)'

    src_values = re.findall(pattern, html, flags=re.IGNORECASE)

    replacement_map = {}

    for full_tag, src, _ in src_values:
        if (not 'data:image' in src) and (not src.startswith('https://')):
            mime, enc = encodeImage(src)
            newsrc = f'data:{mime};base64,{enc.decode("utf-8")}'
            print ('\tEncoding:',src)
            replacement_map[src] = newsrc
        
    def replace_src(match):
        original_src = match.group(2)
        new_src = replacement_map.get(original_src, original_src)  # Use original src if no replacement is found
        return f"{match.group(1)}{new_src}{match.group(3)}"
    
    out = re.sub(pattern, replace_src, html, flags=re.IGNORECASE)

    # css imgs url
    pattern = r'(background-image:\s*url\(\s*["\']?)([^"\')]+)(["\']?\s*\))'
    
    src_values = re.findall(pattern, out, flags=re.IGNORECASE)

    replacement_map = {}
    for full_tag, src, _ in src_values:
        if (not 'data:image' in src) and (not src.startswith('https://')):
            srcp = (css_base / src).resolve().relative_to(Path.cwd())
            mime, enc = encodeImage(srcp)
            #mime, enc = encodeImage('/'.join(src.split('/')[1:]))
            newsrc = f'data:{mime};base64,{enc.decode("utf-8")}'
            print ('\tEncoding:', srcp)
            replacement_map[src] = newsrc

    out2 = re.sub(pattern, replace_src, out, flags=re.IGNORECASE)

    return out2

def package_all(html):
    html, css_base = package_css(html)
    html = package_script(html)
    return package_imgs(html, css_base)

def package_file(fname):
    path  = Path(fname).parent
    fname = Path(fname).name
    fout  = str(fname).split('.')
    fout  = '.'.join(fout[:-1]) + '_pkg.' + fout[-1]

    os.chdir(path)

    with open(fname, 'r') as f:
        html = f.read()

    html = package_all(html)
    with open(fout, 'wt') as f:
        f.write(html)

    print('Done.')

if __name__ == "__main__":
    main()

