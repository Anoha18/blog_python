$(document).ready(() => {
  const textAreas = {};
  const deletePostLink = $('#deletePostLink');
  const csrftoken = Cookies.get('csrftoken');
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
        if (elem.id !== `replyForm-${commentId}`) {
          $(`#${elem.id}`).css('display', 'none');
        }
      })
      e.target.innerText = 'Скрыть';
    }
  });

  deletePostLink.click(async () => {
    const { dataset: { postId } = {} } = deletePostLink[0];
    if (!postId) return;

    try {
      const response = await fetch(`/posts/${postId}`, {
        method: 'DELETE',
        body: JSON.stringify({
          postId,
        }),
        headers: {
          'X-CSRFToken': csrftoken,
        }
      });

      if (response.status === 403) {
        return alert('Вы не авторизованы');
      }

      if (response.status === 200) {
        window.location.reload();
      }
    } catch (error) {
      console.error(error);
      return alert(`Произошла ошибка при удалении поста. Сообщение ошибки = ${error.message}`);
    }
  });
});