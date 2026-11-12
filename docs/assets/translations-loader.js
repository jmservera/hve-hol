(function () {
  'use strict';

  var englishUrl = new URL('../translations.js', document.currentScript.src).href;
  window.HVE_GUIDE_TRANSLATIONS_READY = new Promise(function (resolve) {
    if (window.HVE_GUIDE_TRANSLATIONS) {
      resolve(window.HVE_GUIDE_TRANSLATIONS);
      return;
    }

    console.error('Missing translations.js for this page. Falling back to English.');
    var script = document.createElement('script');
    script.src = englishUrl;
    function unavailable() {
      console.error('English translations are unavailable. Interactive features cannot start.', englishUrl);
      resolve(null);
    }
    script.onload = function () {
      if (window.HVE_GUIDE_TRANSLATIONS) resolve(window.HVE_GUIDE_TRANSLATIONS);
      else unavailable();
    };
    script.onerror = unavailable;
    document.head.appendChild(script);
  });
})();
