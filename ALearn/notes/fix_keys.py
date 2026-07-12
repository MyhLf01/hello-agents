import sys
filepath = r'D:\CodeRepo\Project\hello-agents\ALearn\chapter1\FirstAgent.py'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1) Fix os.environ.get obfuscation
content = content.replace(
    'os.e*******get',
    'os.environ.get'
)

# 2) Fix [redacted] in TavilyClient init
content = content.replace(
    'TavilyClient(api_key=[redacted]',
    'TavilyClient(api_key=api_key'
)

# 3) Fix [redacted] in class __init__
content = content.replace(
    'api_key : [redacted]',
    'api_key: str'
)

# 4) Fix [redacted] in OpenAI init
content = content.replace(
    'OpenAI(api_key=[redacted], base_url=base_url)',
    'OpenAI(api_key=api_key, base_url=base_url)'
)

# 5) Fix [redacted] in llm call
content = content.replace(
    'api_key=[redacted],',
    'api_key=API_KEY,'
)

# 6) Remove the two hardcoded key lines and the os.environ line
lines = content.split('\n')
result = []
for line in lines:
    # Skip hardcoded API_KEY with asterisk-masked value
    if line.strip().startswith('API_KEY') and 'sk-' in line and '****' in line:
        result.append('API_KEY = os.environ.get("DEEPSEEK_API_KEY")')
        continue
    # Skip hardcoded TAVILY_API_KEY with asterisk-masked value
    if 'TAVILY_API_KEY=' in line and 'tvly-' in line and '****' in line:
        continue
    # Skip os.environ['TAVILY_API_KEY'] = TAVILY_API_KEY
    if "os.environ['TAVILY_API_KEY']" in line:
        continue
    result.append(line)
content = '\n'.join(result)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

# Verify
with open(filepath, 'r', encoding='utf-8') as f:
    final = f.read()

issues = 0
for i, line in enumerate(final.split('\n'), 1):
    if '[redacted]' in line:
        print(f'ISSUE line {i}: [redacted] found')
        issues += 1
    if 'sk-' in line and '****' in line and len(line) > 25:
        print(f'ISSUE line {i}: masked DeepSeek key still present')
        issues += 1
    if 'tvly-' in line and '****' in line:
        print(f'ISSUE line {i}: masked Tavily key still present')
        issues += 1

if issues == 0:
    print('All clean! No sensitive data in file.')
else:
    print(f'{issues} issue(s) remain.')
    sys.exit(1)
