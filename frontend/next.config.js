/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  
  // API rewrite for development
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*',
      },
    ]
  },
  
  // Environment variables
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
    NEXT_PUBLIC_APP_NAME: 'AGRO-BOT & AUTOMATION',
    NEXT_PUBLIC_APP_VERSION: '1.0.0',
  },
  
  // Image domains for external images
  images: {
    domains: [
      'localhost',
      'firebase.googleapis.com',
      'firebasestorage.googleapis.com',
    ],
  },
}

module.exports = nextConfig