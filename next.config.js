/** @type {import('next').NextConfig} */
const nextConfig = {
  // Configuration pour src/ directory
  experimental: {
    appDir: true,
  },
  
  // Configuration des chemins d'import
  pageExtensions: ['ts', 'tsx', 'js', 'jsx'],
  
  // Configuration pour les imports absolus
  reactStrictMode: true,
  
  // Configuration TypeScript
  typescript: {
    ignoreBuildErrors: false,
  },
  
  // Configuration ESLint
  eslint: {
    ignoreDuringBuilds: false,
  },
  
  // Configuration pour les assets statiques
  images: {
    domains: ['localhost'],
  },
  
  // Configuration Webpack pour les path mappings
  webpack: (config, { buildId, dev, isServer, defaultLoaders, webpack }) => {
    // Alias pour les imports absolus
    config.resolve.alias = {
      ...config.resolve.alias,
      '@': './src',
      '@/components': './src/common/components',
      '@/hooks': './src/common/hooks',
      '@/services': './src/common/services',
      '@/utils': './src/common/utils',
      '@/types': './src/common/types',
      '@/styles': './src/styles',
    }
    
    return config
  },
  
  // Configuration pour le dossier source
  basePath: '',
  
  // Configuration pour le mode dev
  env: {
    NODE_ENV: process.env.NODE_ENV || 'development',
  },
}

module.exports = nextConfig