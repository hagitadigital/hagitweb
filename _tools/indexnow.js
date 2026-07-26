#!/usr/bin/env node
/**
 * IndexNow submitter — pushes URLs to Bing/Yandex/Seznam (and anything else
 * on the IndexNow network) for near-instant indexing.
 *
 * Usage:
 *   node _tools/indexnow.js                     # submit URLs changed in the last commit
 *   node _tools/indexnow.js --all               # submit every URL in sitemap.xml
 *   node _tools/indexnow.js <url> [<url> ...]   # submit specific URLs
 *   node _tools/indexnow.js --since <ref>       # URLs changed since a git ref
 *
 * The key file must stay reachable at https://hagitantebi.co.il/<KEY>.txt
 */

const { execSync } = require("child_process");
const fs = require("fs");
const path = require("path");
const https = require("https");

const HOST = "hagitantebi.co.il";
const KEY = "c5dbe77abda0a08c09dd2d814365fab840be9238a1cf379ed53b29996f7824e0";
const ROOT = path.resolve(__dirname, "..");
const MAX = 10000; // IndexNow per-request cap

/** repo-relative html path -> public URL (or null if it shouldn't be submitted) */
function toUrl(rel) {
  rel = rel.replace(/\\/g, "/");
  if (!rel.endsWith(".html")) return null;
  if (rel.startsWith("_") || rel.includes("/_") || rel === "404.html") return null;

  const abs = path.join(ROOT, rel);
  if (!fs.existsSync(abs)) return null;
  const html = fs.readFileSync(abs, "utf8");
  if (/noindex/i.test(html)) return null;

  const clean = rel.replace(/(^|\/)index\.html$/, "$1");
  return `https://${HOST}/${clean}`;
}

function fromGit(range) {
  const out = execSync(`git diff --name-only ${range}`, { cwd: ROOT }).toString();
  return out.split("\n").map((s) => s.trim()).filter(Boolean).map(toUrl).filter(Boolean);
}

function fromSitemap() {
  const xml = fs.readFileSync(path.join(ROOT, "sitemap.xml"), "utf8");
  return [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]);
}

function submit(urlList) {
  const body = JSON.stringify({
    host: HOST,
    key: KEY,
    keyLocation: `https://${HOST}/${KEY}.txt`,
    urlList,
  });

  const req = https.request(
    {
      hostname: "api.indexnow.org",
      path: "/indexnow",
      method: "POST",
      headers: { "Content-Type": "application/json; charset=utf-8", "Content-Length": Buffer.byteLength(body) },
    },
    (res) => {
      let data = "";
      res.on("data", (d) => (data += d));
      res.on("end", () => {
        // 200 = accepted, 202 = accepted pending key validation
        const ok = res.statusCode === 200 || res.statusCode === 202;
        console.log(`${ok ? "✓" : "✗"} IndexNow HTTP ${res.statusCode}${data ? " — " + data.trim() : ""}`);
        if (!ok) process.exitCode = 1;
      });
    }
  );
  req.on("error", (e) => {
    console.error("✗ request failed:", e.message);
    process.exitCode = 1;
  });
  req.write(body);
  req.end();
}

const argv = process.argv.slice(2);
let urls;

if (argv.includes("--all")) {
  urls = fromSitemap();
} else if (argv[0] === "--since") {
  urls = fromGit(`${argv[1]} HEAD`);
} else if (argv.length && argv[0].startsWith("http")) {
  urls = argv;
} else {
  urls = fromGit("HEAD~1 HEAD");
}

urls = [...new Set(urls)].slice(0, MAX);

if (!urls.length) {
  console.log("nothing to submit.");
  process.exit(0);
}

console.log(`submitting ${urls.length} URL(s):`);
urls.forEach((u) => console.log("   " + u));
submit(urls);
