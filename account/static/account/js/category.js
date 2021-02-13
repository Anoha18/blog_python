$(document).ready(() => {
  const categoryName = $('#categoryName');
  const categoryDesc= $('#categoryDesc');
  const categoryNameError = $('#categoryNameError');
  const deleteCategoryLink = $('#deleteCategoryLink');
  const csrftoken = Cookies.get('csrftoken');

  categoryName.on('change paste keyup', () => {
    if (!categoryName.val().trim()) {
      categoryName.addClass('is-invalid');
      categoryNameError.removeClass('d-none');
      categoryNameError.text('Наименование не должно быть пустым')
    } else {
      categoryName.removeClass('is-invalid');
      categoryNameError.addClass('d-none');
    }
  });

  $('#addNewCategoryButton').click(async () => {
    if (!categoryName.val().trim()) {
      categoryName.addClass('is-invalid');
      categoryNameError.removeClass('d-none');
      categoryNameError.text('Наименование не должно быть пустым')
      return;
    }

    try {
      const response = await fetch('/account/categories/', {
        method: 'POST',
        credentials: 'same-origin',
        body: JSON.stringify({
          categoryName: categoryName.val().trim(),
          categoryDesc: categoryDesc.val().trim(),
        }),
        headers: {
          'X-CSRFToken': csrftoken,
        }
      });

      console.log(response);

      if (!response.ok) {
        return alert('Произошла ошибка при сохранении');
      }

      $('#newCategoryModal').modal('toggle');
      window.location.reload();
    } catch (error) {
      console.error('Error. category.js ', error);
      alert(`Произошла ошибка. Сообщение ошибки: ${error.message}`);
    }
  });

  deleteCategoryLink.click(async () => {
    const { dataset: { catId } = {} } = deleteCategoryLink[0];

    if (!+catId) {
      return alert('Произошла ошибка при удалении категории');
    }

    try {
      await fetch(`/account/categories/${catId}`, {
        method: 'DELETE',
        body: JSON.stringify({
          catId,
        }),
        headers: {
          'X-CSRFToken': csrftoken,
        }
      })

      window.location.reload();
    } catch (error) {
      console.error(error);
      return alert(`Произошла ошибка при удалении категории. Сообщение ошибки = ${error.message}`);
    }
    // console.log(dataset);
  });
});

  // addNewCategoryButton.addEventListener('click', () => {
  //   const newCategoryModal = document.getElementById('newCategoryModal');
  // });
