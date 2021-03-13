$(document).ready(() => {
  const formFile = $('#formFile');
  const postTitle = $('#postTitle')[0];
  const postCategory = $('#postCategory')[0];
  const newPostFormContainer = $('#newPostFormContainer')[0];
  const formImageContainer = $('#formImageContainer');
  const imagePreview = $('#formImagePreview');
  let post = null;

  const simplemde = new SimpleMDE({
    element: document.getElementById('postText'),
    autosave: {
      enabled: true,
      delay: 5000,
      uniqueId: Cookies.get('csrftoken')
    },
    spellChecker: false
  });

  formFile.change(() => {
    const reader = new FileReader();

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

    simplemde.clearAutosavedValue();
    return true;
  });

  const getPost = () => {
    const { dataset } = newPostFormContainer;
    if (!dataset.postid) return;

    post = dataset;

    setPostValue();
  }

  const setPostValue = () => {
    postTitle.value = post.title;
    postCategory.value = post.categoryid;
    simplemde.value(post.body);
    if (post.image) {
      imagePreview[0].src = post.image;
      formImageContainer.removeClass('d-none');
    }
  }

  getPost();

  window.onunload = () => {
    console.log('HERE LEAVE');
    simplemde.clearAutosavedValue();
  };
});
