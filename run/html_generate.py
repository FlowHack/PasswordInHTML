from webbrowser import open as web_open

from settings import encryption, path_to_html, path_to_little_ico
from settings.encryption import Encryption

from .functions import Passwords, get_settings, write_file

template_html = """<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" type="image" href="{path_to_ico}">
  <title>PasswordInHTML</title>
</head>

<body>{body}
</body>

</html>"""

template_style_1 = """
<style>
body, h1, h2, h3, h4, p, a, label {
    margin: 0;
    font-size: 100%;
    font-weight: normal
}
body {"""
template_style_2 = """
    font-family: 'Times New Roman', 'Arial', sans-serif;
    background: {background};
    color: {foreground};"""
template_style_3 = """
}
*{
    box-sizing: border-box;
}
details > summary {
    display:block
}
.content{
    font-size: 0;
    padding-top: 1rem;
}
.card{"""
template_style_4 = """
    margin: 5px auto;
    width: 75%;
    border-radius: 30px;
    padding: 13px 30px 30px 15px;
    background: {card_background};"""
template_style_5 = """
}
.card-title{
    font-weight : 500;
    font-size: 25px;
    margin-bottom: 10px;
    text-align: center;
    text-decoration: underline;
    cursor: ne-resize
}
.card-text{
    font-size: 18px;
    text-align: center
}
.card-url{
    text-decoration: none;
    color: #29e051;
}
.password-card{
    margin: 1rem auto;
}
.password-title{
    font-weight : 500;
    font-size: 23px;
    margin-top: 2rem;
    margin-bottom: 7px;
    text-align: center;
}
.password-text{
    font-weight : 500;
    font-size: 18px;
    text-align: center;
}
</style>"""

def start_template(html):
    write_file(path_to_html, html)
    web_open(path_to_html, new=2)

def generate_template():
    html = template_html
    passwords_dict, name_passwords = Passwords().get_passwords()
    encryption = Encryption()
    settings = get_settings()
    theme = settings['theme']
    background, foreground = theme['back-color'], theme['font-color']
    card_background = theme['back_card_color']
    cards = ''

    template_style = template_style_1 + template_style_2.format(
        background=background, foreground=foreground
    ) + template_style_3 + template_style_4.format(
        card_background=card_background
    ) + template_style_5

    for name, record in passwords_dict.items():
        columns = encryption.decryption(record['columns']).split('&&')
        values = encryption.decryption(record['values']).split('&&')
        url = record['url']
        records = ''

        url = '' if len(url) == 0 else f"""
        <p class="card-text">
            URL: <a target="blank"  href="{url}" class="card-url">{url}</a>
        </p>"""

        records = ''
        for i in range(len(columns)):
            records += f'''
        <h3 class="password-title">{columns[i]}</h3>
        <p class="password-text">{values[i]}</p>'''

        cards += f"""
    <details class="card">
        <summary class="card-title">{name}</summary>{url}{records}
    </details>"""
    
    html = html.format(
        path_to_ico=path_to_little_ico,
        body=template_style + '\n<section class="content">' + cards + '\n</section>'
    )
    start_template(html)
