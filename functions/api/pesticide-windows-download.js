// Counts each Pesticide Shop Calculator Windows download (via the site
// button or the short link) and redirects to the Windows ZIP hosted as
// a GitHub Release (too large for Pages hosting). Requires a KV
// namespace bound as DOWNLOAD_COUNT. If the binding is missing, the
// download still works, just without counting.
export async function onRequestGet({ env }) {
  const kv = env.DOWNLOAD_COUNT;
  if (kv) {
    try {
      const current = await kv.get("pesticide-windows-downloads");
      const count = (parseInt(current || "0", 10) || 0) + 1;
      await kv.put("pesticide-windows-downloads", String(count));
    } catch (e) {
      // Counting must never break the download.
    }
  }
  return Response.redirect(
    "https://github.com/Atikur009/pesticide-shop-calculator/releases/download/v3.5.0/pesticide-shop-calculator-windows-3.5.0.zip",
    302
  );
}
