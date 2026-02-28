const nextConfig = {
  experimental: {
    // Explicitly include the seed data file in the /api/seed serverless function bundle.
    // Without this, Vercel's file tracer misses dynamically-referenced files and
    // fs.readFileSync returns ENOENT at runtime.
    outputFileTracingIncludes: {
      '/api/seed':      ['./data/**/*'],
      '/api/seed-test': ['./data/**/*'],
    },
  },
};
export default nextConfig;
