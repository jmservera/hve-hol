/* Load synchronously before site.css so saved preferences apply before first paint. */
window.HVE_GUIDE_TRANSLATIONS_READY.then(function (messages) {
  'use strict';

  if (!messages) return;
  var root = document.documentElement;
  var key = 'hve-guide:v1:theme';
  var system = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;
  var override = null;
  var buttons = [];

  function warnStorage(error) {
    console.warn(messages.themeStorageUnavailable, error);
  }

  function validTheme(value) {
    return value === 'light' || value === 'dark';
  }

  try {
    var saved = window.localStorage.getItem(key);
    if (validTheme(saved)) override = saved;
  } catch (error) {
    warnStorage(error);
  }

  function resolvedTheme() {
    return override || (system && system.matches ? 'dark' : 'light');
  }

  function applyTheme() {
    var theme = resolvedTheme();
    root.setAttribute('data-theme', theme);
    root.style.colorScheme = theme;
    Array.prototype.forEach.call(buttons, function (button) {
      var action = theme === 'dark' ? 'light' : 'dark';
      var label = messages[action === 'dark' ? 'switchToDark' : 'switchToLight'];
      button.setAttribute('data-theme', theme);
      button.setAttribute('aria-label', label);
      button.setAttribute('title', label);
      button.setAttribute('aria-pressed', theme === 'dark' ? 'true' : 'false');
      button.hidden = false;
    });
  }

  applyTheme();

  function bindButtons() {
    buttons = document.querySelectorAll('[data-theme-toggle]');
    Array.prototype.forEach.call(buttons, function (button) {
      button.addEventListener('click', function () {
        override = resolvedTheme() === 'dark' ? 'light' : 'dark';
        applyTheme();
        try {
          window.localStorage.setItem(key, override);
        } catch (error) {
          warnStorage(error);
        }
      });
    });
    applyTheme();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bindButtons, { once: true });
  } else {
    bindButtons();
  }

  function systemChanged() {
    if (override === null) applyTheme();
  }
  if (system) {
    if (system.addEventListener) system.addEventListener('change', systemChanged);
    else if (system.addListener) system.addListener(systemChanged);
  }

  window.addEventListener('storage', function (event) {
    if (event.key !== key && event.key !== null) return;
    override = validTheme(event.newValue) ? event.newValue : null;
    applyTheme();
  });
});
