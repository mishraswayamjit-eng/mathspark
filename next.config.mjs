const nextConfig = {
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          { key: 'X-Frame-Options', value: 'DENY' },
          { key: 'X-Content-Type-Options', value: 'nosniff' },
          { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
          { key: 'Permissions-Policy', value: 'camera=(), microphone=(self), geolocation=()' },
          { key: 'Strict-Transport-Security', value: 'max-age=63072000; includeSubDomains; preload' },
          {
            key: 'Content-Security-Policy',
            value: [
              "default-src 'self'",
              "script-src 'self' 'unsafe-inline' https://checkout.razorpay.com",
              "style-src 'self' 'unsafe-inline'",
              "img-src 'self' data: blob:",
              "connect-src 'self' https://api.razorpay.com",
              "frame-src https://api.razorpay.com",
            ].join('; '),
          },
        ],
      },
    ];
  },
  experimental: {
    // Explicitly include the seed data file in the /api/seed serverless function bundle.
    // Without this, Vercel's file tracer misses dynamically-referenced files and
    // fs.readFileSync returns ENOENT at runtime.
    outputFileTracingIncludes: {
      '/api/seed':                  ['./data/**/*'],
      '/api/seed-test':             ['./data/**/*'],
      '/api/daily-challenge-data':  ['./data/daily-challenges.json'],
      '/api/papers':                ['./data/paper-bank.json'],
      '/api/papers/[paperId]':      ['./data/paper-bank.json'],
      '/api/mistake-patterns':      ['./data/mistake-patterns.json'],
      '/api/skill-drills':          ['./data/skill-drills.json'],
      '/api/worked-examples':       ['./data/worked-examples.json'],
      '/api/strategies':            ['./data/strategy-bank.json'],
      '/api/stories':               ['./data/math-stories.json'],
      '/api/concept-map':           ['./data/concept-map.json', './data/dependency-graph.json'],
      '/api/ipm-predictor':         ['./data/ipm-predictor.json'],
      '/api/lessons/[topicSlug]':   ['./data/lessons/**/*'],
    },
  },
};
export default nextConfig;
