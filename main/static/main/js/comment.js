$(document).ready(() => {
  const simplemde = new SimpleMDE({
    element: document.getElementById('commentTextarea'),
    autosave: {
      enabled: false,
    },
    spellChecker: false
  });

  $('#commentForm').submit(() => {
    if (simplemde.value().trim() === '') {
      alert('Комментарий пуст');
      return false;
    }

    return true;
  });
});