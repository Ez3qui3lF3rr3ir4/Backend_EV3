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

// --- Edit buttons handler: populate forms from data-* attributes ---
(function(){
  function onReady(fn){
    if(document.readyState !== 'loading') fn(); else document.addEventListener('DOMContentLoaded', fn);
  }

  onReady(function(){
    // Vehiculo
    document.querySelectorAll('.edit-vehiculo').forEach(function(btn){
      btn.addEventListener('click', function(){
        document.getElementById('vehiculo_id').value = this.dataset.id || '';
        document.getElementById('patente').value = this.dataset.patente || '';
        document.getElementById('marca').value = this.dataset.marca || '';
        document.getElementById('modelo').value = this.dataset.modelo || '';
        window.scrollTo({ top: 0, behavior: 'smooth' });
      });
    });

    // Registro
    document.querySelectorAll('.edit-registro').forEach(function(btn){
      btn.addEventListener('click', function(){
        document.getElementById('registro_id').value = this.dataset.id || '';
        document.getElementById('tipo_reg').value = this.dataset.tipo || '';
        document.getElementById('desc_reg').value = this.dataset.desc || '';
        window.scrollTo({ top: 0, behavior: 'smooth' });
      });
    });

    // RegistroVehiculo
    document.querySelectorAll('.edit-rv').forEach(function(btn){
      btn.addEventListener('click', function(){
        document.getElementById('rv_id').value = this.dataset.id || '';
        document.getElementById('rv_vehiculo').value = this.dataset.vehiculo || '';
        document.getElementById('rv_registro').value = this.dataset.registro || '';
        document.getElementById('rv_salida').value = this.dataset.fecha || '';
        window.scrollTo({ top: 0, behavior: 'smooth' });
      });
    });
  });
})();
