% setdefault('header_title', 'URL Shortener - abbr.ninja')
% setdefault('indexable', True)
<head>
  <meta charset="utf-8"/>
  <title>{{ header_title }}</title>
  <meta name="description" content="A fast and easy to use URL/URI shortener website with APIs for integration.">
  <!-- Open Graph metadata -->
  <meta property="og:title" content="{{ header_title }}">
  <meta property="og:description" content="A fast and easy to use URL/URI shortener.">
  <!-- <meta property="og:image" content=""> -->
  <meta property="og:type" content="website">

  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="theme-color" content="#003366">

  % if not indexable:
  <meta name="robots" content="noindex">
  % end

  <link rel="icon" href="/favicon.ico">

  <link rel="stylesheet" href="/css/theme/light_theme.css" preload>
  <link rel="stylesheet" href="/css/index.css">

  <script src="/js/index.js" defer></script>

  % if defined('header_tags'):
  {{ !header_tags }}
  % end
</head>