% rebase('templates/layouts/content.tpl', header_title='Redirect to External Site - abbr.ninja', indexable=False)

<div>
  <h1>Redirect</h1>
  <p>This is an external website. <em>Please make sure you trust the link before clicking on it!</em></p>
  <a href="{{ encoded_uri }}" rel="noopener">
    <pre>{{ html_safe_uri }}</pre>
  </a>
</div>
