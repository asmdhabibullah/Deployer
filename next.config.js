/** @type {import('next').NextConfig} */
require("dotenv/config")

const nextConfig = {
  reactStrictMode: true,
  env: {
    SERVER_API: process.env.NODE_ENV.SERVER_API
  }
}

module.exports = nextConfig
