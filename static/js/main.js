const languageCheckbox = document.getElementById('languageCheckbox');
const languageText = document.getElementById('languageText');

languageCheckbox.addEventListener('change', function () {
if (languageCheckbox.checked) {
    languageText.textContent = 'ID';
} else {
    languageText.textContent = 'EN';
}
});