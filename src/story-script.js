(function () {
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Minimal damped-spring integrator (Apple's damping/response model from
  // "Designing Fluid Interfaces", WWDC18). damping 1 = critically damped, no
  // overshoot — correct here since a passage change is a click, not a flick
  // with momentum to carry through.
  function spring(from, to, damping, response, onUpdate, onDone, token) {
    var wn = 2 * Math.PI / response;
    var k = wn * wn;
    var c = 2 * damping * wn;
    var x = from, v = 0, last = performance.now();
    function tick(now) {
      if (token.cancelled) return;
      var dt = Math.min((now - last) / 1000, 0.032);
      last = now;
      v += (-k * (x - to) - c * v) * dt;
      x += v * dt;
      onUpdate(x);
      if (Math.abs(x - to) < 0.002 && Math.abs(v) < 0.002) {
        onUpdate(to);
        if (onDone) onDone();
        return;
      }
      requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }

  // Harlowe's undo/redo path can fire onMutate more than once for what is
  // logically a single navigation. Without cancelling the stale run, two
  // spring loops end up writing the same element's opacity every frame and
  // it never converges — always cancel the previous run before starting one.
  var activeToken = null;
  function animateIn(passage) {
    if (!passage) return;
    if (activeToken) activeToken.cancelled = true;
    var token = { cancelled: false };
    activeToken = token;
    if (reduceMotion) {
      passage.style.opacity = '1';
      passage.style.transform = 'none';
      return;
    }
    spring(0, 1, 1, 0.35, function (p) {
      passage.style.opacity = p;
      passage.style.transform = 'translateY(' + ((1 - p) * 10) + 'px) scale(' + (0.98 + 0.02 * p) + ')';
    }, function () {
      passage.style.transform = '';
    }, token);
  }

  // Harlowe swaps passage content in place rather than firing a documented
  // lifecycle event, so a MutationObserver is the reliable hook — but it also
  // wraps/unwraps content in its own tw-transition-container over several
  // ticks as part of its internal (unused) transition machinery. Those extra
  // mutations carry the same text, so fingerprint the rendered content and
  // only animate on an actual passage change, not Harlowe's own housekeeping.
  var scheduled = false;
  var lastContent = null;
  function onMutate() {
    if (scheduled) return;
    scheduled = true;
    requestAnimationFrame(function () {
      scheduled = false;
      var passage = document.querySelector('tw-story > tw-passage');
      if (!passage) return;
      var fingerprint = passage.textContent;
      if (fingerprint === lastContent) return;
      lastContent = fingerprint;
      animateIn(passage);
    });
  }

  var story = document.querySelector('tw-story');
  if (story) {
    new MutationObserver(onMutate).observe(story, { childList: true, subtree: true });
  }
})();
