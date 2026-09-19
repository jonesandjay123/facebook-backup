import json, subprocess, sys
inp, outp = sys.argv[1], sys.argv[2]
results = []
with open(inp) as f:
    lines = [l.strip().split(' ', 1) for l in f if l.strip()]
for date, url in lines:
    try:
        r = subprocess.run(['facebook-cli','post','read','--url',url], capture_output=True, text=True, timeout=60)
        d = json.loads(r.stdout)
        p = d['posts'][0]
        results.append({'date': date, 'url': url, 'post_id': p['post_id'],
                        'author': p.get('author_name') or p.get('username'),
                        'created_at': p['created_at']})
        print(f"OK {date} {p['post_id']} {p.get('author_name') or p.get('username')}", flush=True)
    except Exception as e:
        results.append({'date': date, 'url': url, 'post_id': None, 'error': str(e)[:120]})
        print(f"FAIL {date} {url} {str(e)[:80]}", flush=True)
with open(outp, 'w') as f:
    json.dump(results, f, ensure_ascii=False, indent=1)
print(f"saved {len(results)} to {outp}")
