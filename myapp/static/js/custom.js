
// ----------------------------------------------------------------
//                  Theme Dark And light toggle 
// ----------------------------------------------------------------

// Apply the stored theme on page load
if (localStorage.getItem('color-theme') === 'dark') {
    document.documentElement.classList.add('dark');
} else {
    document.documentElement.classList.remove('dark');
}

var themeToggleDarkIcon = document.getElementById('theme-toggle-dark-icon');
var themeToggleLightIcon = document.getElementById('theme-toggle-light-icon');
var themeToggleBtn = document.getElementById('theme-toggle');

// Change the icons inside the button based on previous settings
if (localStorage.getItem('color-theme') === 'dark') {
    themeToggleLightIcon.classList.remove('hidden');
} else {
    themeToggleDarkIcon.classList.remove('hidden');
}

themeToggleBtn.addEventListener('click', function() {
    // toggle icons inside button
    themeToggleDarkIcon.classList.toggle('hidden');
    themeToggleLightIcon.classList.toggle('hidden');

    // if set via local storage previously
    if (localStorage.getItem('color-theme')) {
        if (localStorage.getItem('color-theme') === 'light') {
            document.documentElement.classList.add('dark');
            localStorage.setItem('color-theme', 'dark');
        } else {
            document.documentElement.classList.remove('dark');
            localStorage.setItem('color-theme', 'light');
        }
    } else {
        // if NOT set via local storage previously
        if (document.documentElement.classList.contains('dark')) {
            document.documentElement.classList.remove('dark');
            localStorage.setItem('color-theme', 'light');
        } else {
            document.documentElement.classList.add('dark');
            localStorage.setItem('color-theme', 'dark');
        }
    }
});




// ----------------------------------------------------------------
//                  Password Strong And Suggestion 
// ----------------------------------------------------------------


document.addEventListener('DOMContentLoaded', function () {
    const passwordInput = document.getElementById('password');
    const popover = document.getElementById('popover-password');
    const requirements = document.querySelectorAll('.password-requirement');
    const strengthMeter = document.getElementById('strength-meter');
    const strengthBar = document.getElementById('strength-bar');
    const strengthLabel = document.getElementById('strength-label');

    // Show popover on focus
    passwordInput.addEventListener('focus', function () {
        popover.classList.remove('hidden');
        const rect = passwordInput.getBoundingClientRect();
        popover.style.top = rect.bottom + window.scrollY + 'px';
        popover.style.left = rect.left + 'px';
    });

    // Hide popover on blur
    passwordInput.addEventListener('blur', function () {
        setTimeout(() => {
            popover.classList.add('hidden');
        }, 100); // Delay hiding to allow click on popover
    });

    // Check password strength and update requirements
    passwordInput.addEventListener('input', function () {
        const password = passwordInput.value;
        const lengthRequirement = password.length >= 6;
        const uppercaseRequirement = /[A-Z]/.test(password);
        const lowercaseRequirement = /[a-z]/.test(password);
        const symbolRequirement = /[!@#$%^&*(),.?":{}|<>]/.test(password);

        const requirementsMet = [lengthRequirement, uppercaseRequirement, lowercaseRequirement, symbolRequirement];

        requirements.forEach((req, index) => {
            req.classList.toggle('text-gray-300', !requirementsMet[index]);
            req.classList.toggle('text-green-600', requirementsMet[index]);
        });

        // Calculate strength
        const strength = requirementsMet.filter(Boolean).length;
        const strengthPercent = (strength / requirements.length) * 100;

        strengthBar.style.width = strengthPercent + '%';
        if (strengthPercent === 100) {
            strengthLabel.innerText = 'Strong Password';
            strengthBar.classList.add('bg-green-500');
            strengthBar.classList.remove('bg-red-500');
        } else if (strengthPercent >= 50) {
            strengthLabel.innerText = 'Medium Password';
            strengthBar.classList.add('bg-yellow-500');
            strengthBar.classList.remove('bg-red-500', 'bg-green-500');
        } else {
            strengthLabel.innerText = 'Weak Password';
            strengthBar.classList.add('bg-red-500');
            strengthBar.classList.remove('bg-yellow-500', 'bg-green-500');
        }
    });
});


// ----------------------------------------------------