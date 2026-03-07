// jampack.config.mjs — P-KISS-SBC
//
// Post-processing configuration for the MkDocs static site hosted on Netlify.
// Run after `mkdocs build` via `npm run optimize`.
//
// Netlify handles gzip/brotli compression on the fly — no need for static
// pre-compression. Focus is on image optimization, CSS inlining and prefetch.

export default {
  // Disable jampack cache — ensures a clean pass on every CI build
  nocache: true,

  general: {
    // Target modern browsers (aligns with mkdocs-material's own browserslist)
    browserslist: "defaults, not IE 11",
  },

  css: {
    // Inline critical CSS in <head> to eliminate render-blocking stylesheets
    // and prevent flash of unstyled content on first load
    inline_critical_css: true,
  },

  image: {
    // Cap image width at 1200px — sufficient for technical documentation
    max_width: 1200,

    // srcset range: from HiDPI mobile (780px) to standard desktop (1200px)
    srcset_min_width: 780,
    srcset_max_width: 1200,
    srcset_step: 200,

    // JPEG quality (mozjpeg encoder)
    jpeg: {
      options: {
        quality: 82,
        mozjpeg: true,
      },
    },

    // PNG compression (max level)
    png: {
      options: {
        compressionLevel: 9,
      },
    },

    // WebP quality for lossy and lossless
    webp: {
      options_lossless: {
        effort: 5,
        quality: 80,
        mode: "lossless",
      },
      options_lossly: {
        effort: 5,
        quality: 80,
        mode: "lossly",
      },
    },

    svg: {
      // Optimize SVGs via svgo (architecture diagrams, icons)
      optimization: true,
      // Add width/height attributes to prevent layout shift (CLS)
      add_width_and_height: true,
    },

    // Do not process external images (twemoji CDN, GitHub badges, etc.)
    external: {
      process: "off",
    },
  },

  misc: {
    // Prefetch links that enter the viewport → near-instant navigation
    // between doc pages (well suited for Netlify CDN edge caching)
    prefetch_links: "in-viewport",
  },
};
