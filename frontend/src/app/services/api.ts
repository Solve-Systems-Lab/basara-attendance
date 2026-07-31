/* The API client.
 *
 *     OWNER: FE track — GRP8.
 *
 * A stub with the shape sketched in. Two things to build here that the
 * reference implementation never had:
 *
 *   1. A 401 -> refresh -> retry interceptor. Without it, everyone is silently
 *      logged out the moment the access token expires, and it will look like a
 *      backend bug.
 *   2. Real error propagation. The reference silently swaps in mock data on any
 *      network failure, so a broken API looks like a working one. That is worse
 *      than crashing.
 *
 * Note there is no Content-Type header on the multipart path below. That is
 * deliberate — the browser must set it itself so it can add the boundary.
 * Setting it by hand is the classic way to break file upload.
 */

const BASE = import.meta.env.VITE_API_BASE_URL ?? ''

let accessToken: string | null = null

export function setAccessToken(token: string | null) {
  accessToken = token
}

export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
    public body?: unknown,
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const headers = new Headers(init.headers)
  if (accessToken) headers.set('Authorization', `Bearer ${accessToken}`)
  if (init.body && !(init.body instanceof FormData)) {
    headers.set('Content-Type', 'application/json')
  }

  const res = await fetch(`${BASE}${path}`, { ...init, headers })

  // TODO(GRP8): on 401, try the refresh endpoint once, then replay this request.
  if (!res.ok) {
    const body = await res.json().catch(() => undefined)
    throw new ApiError(res.status, `${init.method ?? 'GET'} ${path} -> ${res.status}`, body)
  }
  return res.status === 204 ? (undefined as T) : ((await res.json()) as T)
}

/** Liveness check. The one endpoint that already exists. */
export function health() {
  return request<{ ok: boolean }>('/api/health/')
}

// TODO(GRP8): login, refresh, me
// TODO(GRP8): markAttendance(photo: File, lat, lng, accuracy) via FormData
// TODO(GRP8): todayStatus, myRecords, adminOverview
