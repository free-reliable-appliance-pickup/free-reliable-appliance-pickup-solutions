/* Partnership Program is future-only. Existing pickup partner fulfillment is unaffected.
   Public applications and paid partner products stay inactive until owner authorizes launch. */
(function () {
  'use strict';
  function pausePartnerEnrollment() {
    var section = document.querySelector('main[data-partnership-program="future-only"]');
    if (section) {
      section.hidden = true;
      section.inert = true;
    }
    var form = document.getElementById('partnerForm');
    if (!form) return;
    // Retain the original future Formspree endpoint but remove it from the active form.
    form.dataset.futureFormAction = form.getAttribute('action') || '';
    form.setAttribute('action', '#');
    form.setAttribute('method', 'GET');
    form.setAttribute('data-public-enrollment', 'paused');
    form.addEventListener('submit', function(event) {
      event.preventDefault();
      event.stopImmediatePropagation();
    }, true);
    var submit = form.querySelector('[type="submit"]');
    if (submit) {
      submit.disabled = true;
      submit.setAttribute('aria-disabled', 'true');
    }
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', pausePartnerEnrollment, {once:true});
  } else {
    pausePartnerEnrollment();
  }
})();
