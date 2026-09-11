const DASHBOARD_ROOT = "/mellowdashv2";

function isDashboardDocument(pathname) {
  return pathname === `${DASHBOARD_ROOT}/` ||
    pathname === `${DASHBOARD_ROOT}/index.html`;
}

export default {
  async fetch(request, env) {
    // dev-elx remains the source of truth for authentication and every route
    // other than the dashboard document itself. Calling it through a service
    // binding avoids a same-host route loop.
    const upstream = await env.DEV_ELX.fetch(request);
    const url = new URL(request.url);
    const servesDashboard =
      (request.method === "GET" || request.method === "HEAD") &&
      isDashboardDocument(url.pathname) &&
      upstream.status === 200;

    if (!servesDashboard) return upstream;

    const response = await env.ASSETS.fetch(request);
    const headers = new Headers(response.headers);
    headers.set("Cache-Control", "no-store");
    headers.set("X-Robots-Tag", "noindex, nofollow");

    return new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers,
    });
  },
};
