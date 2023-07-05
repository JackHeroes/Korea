function showPassword(inputId) {
    const input = document.getElementById(inputId);
    
    if (input && input.type === 'password') {
      input.type = 'text';
    } else if (input) {
      input.type = 'password';
    }
}