// Counts each Masjid Management APK download (via the site button) and
// redirects to the APK file. Requires a KV namespace bound as DOWNLOAD_COUNT.
// If the binding is missing, the download still works, just without counting.
export async function onRequestGet({ request, env }) {
  const kv = env.DOWNLOAD_COUNT;
  if (kv) {
    try {
      const current = await kv.get("masjid-apk-downloads");
      const count = (parseInt(current || "0", 10) || 0) + 1;
      await kv.put("masjid-apk-downloads", String(count));
    } catch (e) {
      // Counting must never break the download.
    }
  }
  // Response.redirect needs an absolute URL on Workers.
  const url = new URL(request.url);
  url.pathname = "/downloads/masjid-management.apk";
  return Response.redirect(url.toString(), 302);
}
