$(document).ready(() => {
  const simplemde = new SimpleMDE({
    element: document.getElementById('commentTextarea'),
    autosave: {
      enabled: false,
    },
    spellChecker: false
  })
});