% rebase('templates/layouts/content.tpl', indexable=False)

% setdefault('error_code', '')
% setdefault('error_txt', 'Unknown error')
<div id="error-container">
  <h1>Whoops…</h1>
  <h2>An error has occurred: {{ error_code }} {{ error_txt }}</h2>
  % if defined('error_msg'):
  <pre>{{ error_msg }}</pre>
  % end
</div>
