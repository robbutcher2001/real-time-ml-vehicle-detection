import { get } from '@vercel/edge-config'

export const config = { runtime: 'nodejs', matcher: '/api/status' }

export default async () =>
  new Response(JSON.stringify(await get('rtvd')), {
    status: 200,
    headers: { 'Content-Type': 'application/json' },
  })
