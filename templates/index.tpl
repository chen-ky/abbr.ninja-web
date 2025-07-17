% rebase('templates/layouts/content.tpl')

<div class="shorten-box">
  <div class="shorten-bar-box">
    <label for="uri-input" hidden>Enter your URI:</label>
    <input
      type="url"
      id="uri-input"
      name="long-uri"
      placeholder="Enter URI..."
      oninput="isEmpty('uri-input')"
      autocomplete="off"
      required
    />
    <input type="submit" id="submit-btn" value="Shorten" />
  </div>
  <div class="result-box">
    <span id="result"></span>
  </div>
</div>

<div id="features">
  <h2>Features</h2>
  <ul>
    <li>Simple and fast webpage.</li>
    <li>Privacy friendly. We do not track what link you created or visited.</li>
    <li>
      No automatic redirection when using common browser. Preview link and
      decide if you want to visit the website. Great for security conscious
      user.
    </li>
    <li>
      Modular. Write your own front end or integrate the
      <abbr title="Application Programming Interface">API</abbr> into other
      applications.
    </li>
  </ul>
</div>
