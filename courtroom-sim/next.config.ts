import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Pin the project root so a stray lockfile in a parent folder isn't picked up.
  turbopack: { root: __dirname },
  // Case files are read from disk by server components.
  outputFileTracingIncludes: { "/**": ["./data/cases/**"] },
};

export default nextConfig;
