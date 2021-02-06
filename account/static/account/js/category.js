$(document).ready(() => {
  const categoryName = $('#categoryName');
  const categoryDesc= $('#categoryDesc');
  const categoryNameError = $('#categoryNameError');

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
          'X-CSRFToken': Cookies.get('csrftoken'),
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
});

  // addNewCategoryButton.addEventListener('click', () => {
  //   const newCategoryModal = document.getElementById('newCategoryModal');
  // });
