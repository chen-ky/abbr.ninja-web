<!DOCTYPE html>
<html lang="en">
  % include('templates/components/header.tpl')
  <body>
    <div id="page-container">
      % include('templates/components/top_nav_bar.tpl')

      <div class="main limit-width">
        <div id="content">
          % if defined('base'):
          {{ !base }}
          % end
        </div>
      </div>

      % include('templates/components/footer.tpl')
    </div>
  </body>
</html>
