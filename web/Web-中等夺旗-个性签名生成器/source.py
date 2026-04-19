import re
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Flag 写入文件
import os
FLAG = os.environ.get("GZCTF_FLAG", "flag{test_flag}")
with open('/tmp/flag.txt', 'w') as f:
    f.write(FLAG)

INDEX_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>个性签名生成器 Pro</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: #eee;
            font-family: 'Segoe UI', sans-serif;
            min-height: 100vh;
        }
        .header {
            text-align: center; padding: 40px 20px 20px;
        }
        .header h1 { font-size: 2em; background: linear-gradient(90deg, #f093fb, #f5576c);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .header p { color: #888; margin-top: 8px; }
        .container { max-width: 650px; margin: 20px auto; padding: 0 20px; }
        .card {
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 15px; padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        }
        input[type="text"] {
            width: 100%; padding: 14px 18px;
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.15);
            border-radius: 10px; color: #fff;
            font-size: 1.1em; outline: none;
            transition: border 0.3s;
        }
        input:focus { border-color: #f5576c; }
        button {
            margin-top: 15px; padding: 12px 30px;
            background: linear-gradient(135deg, #f093fb, #f5576c);
            border: none; border-radius: 10px;
            color: white; font-size: 1em; font-weight: bold;
            cursor: pointer; transition: transform 0.2s;
        }
        button:hover { transform: scale(1.02); }
        .result {
            margin-top: 25px; padding: 30px 25px;
            background: rgba(0,0,0,0.3);
            border-radius: 10px;
            border: 1px solid rgba(245,87,108,0.3);
            text-align: center;
            position: relative;
        }
        .result::before, .result::after {
            content: "\\2727";
            position: absolute; top: 10px;
            font-size: 1.2em; color: rgba(245,87,108,0.4);
        }
        .result::before { left: 15px; }
        .result::after { right: 15px; }
        .result .sig {
            font-family: 'Georgia', 'Times New Roman', 'Palatino', cursive, serif;
            font-style: italic;
            font-size: 2em;
            letter-spacing: 3px;
            background: linear-gradient(90deg, #f093fb, #f5576c, #feca57, #f093fb);
            background-size: 200% auto;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: bold;
            word-break: break-all;
            text-shadow: 0 0 20px rgba(240,147,251,0.3);
            animation: shimmer 3s linear infinite;
            padding: 10px 0;
        }
        @keyframes shimmer {
            to { background-position: 200% center; }
        }
        .result .decoration {
            color: rgba(245,87,108,0.3);
            font-size: 1.5em;
            margin: 5px 0;
            letter-spacing: 8px;
        }
        .hint-box {
            background: rgba(255,165,2,0.1);
            border: 1px solid rgba(255,165,2,0.3);
            border-radius: 10px; padding: 20px;
            font-size: 0.9em; color: #ccc;
        }
        .hint-box h3 { color: #ffa502; margin-bottom: 10px; }
        .hint-box code {
            background: rgba(0,0,0,0.3); padding: 2px 6px;
            border-radius: 4px; color: #f5576c;
        }
        .blocked {
            color: #ff6b6b; text-align: center; padding: 15px;
            border: 1px solid rgba(255,107,107,0.3);
            border-radius: 10px; margin-top: 15px;
        }
        .share-btn {
            display: block; margin: 15px auto 0;
            padding: 10px 25px;
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 8px;
            color: #ccc; font-size: 0.95em;
            cursor: pointer; transition: all 0.3s;
        }
        .share-btn:hover {
            background: rgba(255,255,255,0.2);
            color: #fff;
        }
        .levels { margin-top: 20px; }
        .levels h3 { color: #f093fb; margin-bottom: 10px; }
        .levels ul { list-style: none; }
        .levels li { padding: 5px 0; color: #aaa; }
        .levels li::before { content: "\\25b8 "; color: #f5576c; }
    </style>
</head>
<body>
    <div class="header">
        <h1>&#10024; 个性签名生成器 Pro &#10024;</h1>
        <p>输入你的名字，生成专属个性签名！</p>
    </div>
    <div class="container">
        <div class="card">
            <form method="POST" action="/generate">
                <input type="text" name="name" placeholder="输入你的名字或个性签名..." value="{{ name }}" required>
                <button type="submit">&#9889; 生成签名</button>
            </form>
            {% if result %}
            <div class="result" id="sig-card">
                <div class="decoration">&#10040; &#10040; &#10040;</div>
                <p class="sig">''' + '{{ result|safe }}' + '''</p>
                <div class="decoration">&#10040; &#10040; &#10040;</div>
                <p style="color:#555;font-size:0.7em;margin-top:12px;">&#8212; made with Signature Pro &#10024;</p>
            </div>
            <button class="share-btn" onclick="saveAsImage()">&#128247; 保存为图片</button>
            {% endif %}
            {% if blocked %}
            <div class="blocked">
                &#9888; 检测到危险关键字，已拦截！被拦截的关键字: {{ blocked }}
            </div>
            {% endif %}
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js"></script>
    <script>
    function saveAsImage() {
        var card = document.getElementById('sig-card');
        html2canvas(card, {
            backgroundColor: '#1a1a2e',
            scale: 2
        }).then(function(canvas) {
            var link = document.createElement('a');
            link.download = 'my-signature.png';
            link.href = canvas.toDataURL();
            link.click();
        });
    }
    </script>
</body>
</html>
'''

# 黑名单关键字 (部分防御，可绕过)
BLACKLIST = [
    'os',
    'import',
    'eval',
    'exec',
    'system',
    'popen',
    'subprocess',
    '__import__',
    'globals',
    'getattr',
    'builtins',
]

@app.route('/')
def index():
    return render_template_string(INDEX_HTML, name='', result=None, blocked=None)

@app.route('/generate', methods=['POST'])
def generate():
    name = request.form.get('name', '')

    # 长度限制
    if len(name) > 300:
        return render_template_string(INDEX_HTML,
            name=name, result=None,
            blocked="输入过长 (最大300字符)")

    # 黑名单检查 (简单的字符串匹配，存在绕过空间)
    name_lower = name.lower()
    for keyword in BLACKLIST:
        if keyword in name_lower:
            return render_template_string(INDEX_HTML,
                name=name, result=None,
                blocked=f'"{keyword}"')

    # 漏洞核心：用户输入直接拼接进模板
    try:
        template = name
        result = render_template_string(template)
        return render_template_string(INDEX_HTML,
            name=name, result=result.strip(), blocked=None)
    except Exception as e:
        return render_template_string(INDEX_HTML,
            name=name, result=f"渲染错误: {str(e)}", blocked=None)

@app.route('/source')
def source():
    """故意泄露部分源码作为提示"""
    return f'''
    <pre style="background:#1a1a2e;color:#0f0;padding:30px;font-size:13px;white-space:pre-wrap;">
# 黑名单关键字 (能绕过吗？)
BLACKLIST = {BLACKLIST}

# 核心渲染逻辑
template = f'<div class="output">{{name}}</div>'
result = render_template_string(template)

# Hint:
# 1. Jinja2 可以访问 Python 对象的 __class__, __mro__, __subclasses__() 等
# 2. 黑名单是简单的字符串匹配，试试用 Jinja2 的字符串拼接绕过
# 3. 例如: "o"+"s" 可以绕过 "os" 的检测
# 4. 或者用 attr() 过滤器: "".__class__ 等价于 ""|attr("__class__")
# 5. request.args 可以通过 URL 参数传入被过滤的字符串
    </pre>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=False)