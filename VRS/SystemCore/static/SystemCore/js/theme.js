(function(){
  const KEY = 'theme';
  const DARK = 'dark';
  function applyTheme(theme){
    if(theme === DARK){
      document.documentElement.classList.add(DARK);
    } else {
      document.documentElement.classList.remove(DARK);
    }
  }

  document.addEventListener('DOMContentLoaded', function(){
    const toggle = document.getElementById('theme-toggle');
    if(!toggle) return;

    // Determine initial theme: stored > prefers-color-scheme > light
    const stored = localStorage.getItem(KEY);
    const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    const initial = stored || (prefersDark ? DARK : 'light');
    applyTheme(initial);
    toggle.checked = (initial === DARK);

    toggle.addEventListener('change', function(){
      const t = this.checked ? DARK : 'light';
      applyTheme(t);
      try{ localStorage.setItem(KEY, t); }catch(e){/* ignore */}
    });
  });
})();
