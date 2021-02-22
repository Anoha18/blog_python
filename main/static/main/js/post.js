$(document).ready(() => {
  const textAreas = {};
  const simplemde = new SimpleMDE({
    element: document.getElementById('commentTextarea'),
    autosave: {
      enabled: false,
    },
    spellChecker: false
  });

  const checkCommentText = (smde) => {
    if (!smde) return false;
    if (!smde.value) return false;
    if (typeof smde.value !== 'function') return false;

    if (smde.value().trim() === '') {
      alert('Комментарий пуст');
      return false;
    }

    return true;
  }

  $('#commentForm').submit(() => checkCommentText(simplemde));

  $('.reply__link').click((e) => {
    const { target: { dataset = null } } = e || {};
    if (!dataset) return;

    const { commentId } = dataset;
    if (!commentId) return;

    const replyForm = `#replyForm-${commentId}`;
    if ($(replyForm).css("display") === 'block') {
      $(replyForm).css("display", "none");
      e.target.innerText = 'Ответить';
    } else {
      if (!textAreas[commentId]) {
        textAreas[commentId] = new SimpleMDE({
          element: document.getElementById(`commentTextarea${commentId}`),
          autosave: {
            enabled: false,
          },
          spellChecker: false
        });
      }
      $(replyForm).css("display", "block");
      $(`#commentForm${commentId}`).submit(() => checkCommentText(textAreas[commentId]));
      const replyForms = $(`.reply__form`);
      replyForms.map(index => {
        elem = replyForms[index];
      })
      e.target.innerText = 'Скрыть';
    }
  });
});