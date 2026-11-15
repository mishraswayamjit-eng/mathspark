"""Measure what the live site sends for the main pages, signed out.

    python -X utf8 scripts/perf/measure.py [base-url]

For each page: time to first byte and total time over a few requests, the size of the
HTML, the cache headers, and the JavaScript and CSS files the page asks for (size on the
wire and unpacked). For a few API routes: time and the region the function ran in.
Only GET requests are made and nothing is sent. Nothing is changed.
"""
import gzip
import re
import sys
import time
import urllib.error
import urllib.request

BASE = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "https://mathspark-five.vercel.app"
PAGES = ["/", "/home", "/practice", "/chapters", "/flashcards", "/progress", "/profile", "/chat",
         "/test", "/learn/lessons", "/learn/hands-on", "/practice/grade5", "/flashcards/session", "/student/login"]
APIS = ["/api/topics", "/api/home", "/api/dashboard", "/api/questions/next?topicId=grade5",
        "/api/teach/Q_CH11_001?check=1", "/api/chat/history", "/api/auth/session", "/api/voice/stt"]
ROUNDS = 3


def get(url):
    req = urllib.request.Request(url, headers={"Accept-Encoding": "gzip", "User-Agent": "mathspark-perf-check"})
    t0 = time.perf_counter()
    try:
        resp = urllib.request.urlopen(req, timeout=40)
    except urllib.error.HTTPError as e:
        resp = e
    t1 = time.perf_counter()
    raw = resp.read()
    t2 = time.perf_counter()
    headers = dict((k.lower(), v) for k, v in resp.headers.items())
    body = raw
    if headers.get("content-encoding") == "gzip":
        try:
            body = gzip.decompress(raw)
        except OSError:
            body = raw
    return {"status": resp.getcode(), "ttfb": (t1 - t0) * 1000, "total": (t2 - t0) * 1000,
            "wire": len(raw), "size": len(body), "headers": headers, "body": body}


def kb(n):
    return "%.0f KB" % (n / 1024.0)


def main():
    print("site: %s\n" % BASE)
    assets = {}
    page_assets = {}
    print("PAGES (each fetched %d times on a new connection; times in ms include DNS and TLS)" % ROUNDS)
    for path in PAGES:
        runs = [get(BASE + path) for _ in range(ROUNDS)]
        last = runs[-1]
        h = last["headers"]
        html = last["body"].decode("utf-8", "replace")
        found = sorted(set(re.findall(r'(/_next/static/[^"\'\\ )]+\.(?:js|css))', html)))
        page_assets[path] = found
        print("%-22s %s  ttfb %s  total %s  html %s (%s on the wire)  cache=%s  %s" % (
            path, last["status"], "/".join("%.0f" % r["ttfb"] for r in runs), "/".join("%.0f" % r["total"] for r in runs),
            kb(last["size"]), kb(last["wire"]), h.get("x-vercel-cache", "-"), h.get("cache-control", "-")))
        for a in found:
            if a not in assets:
                r = get(BASE + a)
                assets[a] = (r["wire"], r["size"])

    common = None
    for path in PAGES:
        s = set(page_assets[path])
        common = s if common is None else common & s
    common = common or set()
    print("\nJAVASCRIPT AND CSS PER PAGE (on the wire / unpacked)")
    print("%-22s %s files, %s / %s  (asked for by every page above)" % (
        "shared by all", len(common), kb(sum(assets[a][0] for a in common)), kb(sum(assets[a][1] for a in common))))
    for path in PAGES:
        own = [a for a in page_assets[path] if a not in common]
        allp = page_assets[path]
        print("%-22s total %s / %s in %d files;  beyond the shared set: %s / %s in %d files" % (
            path, kb(sum(assets[a][0] for a in allp)), kb(sum(assets[a][1] for a in allp)), len(allp),
            kb(sum(assets[a][0] for a in own)), kb(sum(assets[a][1] for a in own)), len(own)))

    print("\nTEN LARGEST FILES")
    for a, (wire, size) in sorted(assets.items(), key=lambda kv: -kv[1][1])[:10]:
        users = [p for p in PAGES if a in page_assets[p]]
        print("  %s / %s  %s  used by %s" % (kb(wire), kb(size), a.split("/")[-1][:60],
                                           "every page" if len(users) == len(PAGES) else ", ".join(users[:5])))

    print("\nAPI ROUTES, SIGNED OUT (first call may include a cold start; x-vercel-id is edge::function region)")
    for path in APIS:
        runs = [get(BASE + path) for _ in range(ROUNDS)]
        h = runs[-1]["headers"]
        print("%-36s %s  ttfb %s  %s  cache=%s  %s  id=%s" % (
            path, runs[-1]["status"], "/".join("%.0f" % r["ttfb"] for r in runs), kb(runs[-1]["size"]),
            h.get("x-vercel-cache", "-"), h.get("cache-control", "-"), h.get("x-vercel-id", "-")))


if __name__ == "__main__":
    main()
