(() => {
  const form = document.getElementById('loginForm');
  const idInput = document.getElementById('identifier');
  const pwInput = document.getElementById('password');
  const remember = document.getElementById('remember');
  const alertBox = document.getElementById('alert');
  const btn = document.getElementById('submitBtn');
  const btnText = btn.querySelector('.btn-text');
  const arrow = btn.querySelector('.arrow');
  const spinner = btn.querySelector('.spinner');
  const csrf = document.querySelector('meta[name="csrf-token"]').content;

  // show / hide password
  const toggle = document.getElementById('togglePw');
  toggle.addEventListener('click', () => {
    const show = pwInput.type === 'password';
    pwInput.type = show ? 'text' : 'password';
    toggle.querySelector('.eye').hidden = show;
    toggle.querySelector('.eye-off').hidden = !show;
    toggle.setAttribute('aria-label', show ? 'Hide password' : 'Show password');
    pwInput.focus();
  });

  const showError = (msg) => { alertBox.textContent = msg; alertBox.hidden = false; };
  const clearError = () => {
    alertBox.hidden = true;
    document.querySelectorAll('.input.invalid').forEach(el => el.classList.remove('invalid'));
  };
  const setLoading = (on) => {
    btn.disabled = on;
    spinner.hidden = !on;
    arrow.hidden = on;
    btnText.textContent = on ? 'Signing in...' : 'Sign In';
  };

  [idInput, pwInput].forEach(el => el.addEventListener('input', clearError));

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    clearError();

    const identifier = idInput.value.trim();
    const password = pwInput.value;
    if (!identifier || !password) {
      if (!identifier) idInput.parentElement.classList.add('invalid');
      if (!password) pwInput.parentElement.classList.add('invalid');
      showError('Please enter your email or username and password.');
      (identifier ? pwInput : idInput).focus();
      return;
    }

    setLoading(true);
    try {
      const res = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRF-Token': csrf },
        body: JSON.stringify({ identifier, password, remember: remember.checked }),
      });
      const data = await res.json().catch(() => ({}));
      if (res.ok && data.ok) {
        window.location.href = data.redirect || '/dashboard';
        return;
      }
      showError(data.message || 'Sign in failed. Please try again.');
      pwInput.value = '';
      pwInput.focus();
    } catch (err) {
      showError('Cannot connect to the server. Please check your connection.');
    }
    setLoading(false);
  });
})();
