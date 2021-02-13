$(document).ready(() => {
  const formFile = $('#formFile');
  const postTitle = $('#postTitle')[0];
  const postCategory = $('#postCategory')[0];

  const simplemde = new SimpleMDE({
    element: document.getElementById('postText'),
    autosave: {
      enabled: true,
      delay: 5000,
      uniqueId: Cookies.get('csrftoken')
    },
    spellChecker: false
  });

  console.log('HERE ', simplemde);

  formFile.change(() => {
    const reader = new FileReader();
    const formImageContainer = $('#formImageContainer');
    const imagePreview = $('#formImagePreview');

    reader.onload = () => {
      imagePreview[0].src = reader.result;
      formImageContainer.removeClass('d-none');
    }

    if (!formFile[0].files[0]) {
      return formImageContainer.addClass('d-none');
    }

    reader.readAsDataURL(formFile[0].files[0]);
  });

  $('#newPostForm').submit(() => {
    if (postCategory.value.trim() === '') {
      alert('Для публикации поста необходимо выбрать категорию');
      return false;
    }

    if (postTitle.value.trim() === '') {
      alert('Заголовок поста не должен быть пустым');
      return false;
    }

    if (simplemde.value().trim() === '') {
      alert('Вы не написали пост');
      return false;
    }

    if (!formFile[0].files[0]) {
      alert('Загрузите обложку поста');
      return false;
    }

    simplemde.clearAutosavedValue();
    return true;
  })
});