// Returns the current Masjid Management APK download count as JSON.
// Requires a KV namespace bound as DOWNLOAD_COUNT; without it, returns 0.
export async function onRequestGet({ env }) {
  let count = 0;
  const kv = env.DOWNLOAD_COUNT;
  if (kv) {
    try {
      const current = await kv.get("masjid-apk-downloads");
      count = parseInt(current || "0", 10) || 0;
    } catch (e) {
      count = 0;
    }
  }
  return new Response(JSON.stringify({ count }), {
    headers: { "content-type": "application/json", "cache-control": "no-store" },
  });
}
