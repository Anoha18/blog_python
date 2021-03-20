$(document).ready(() => {
  const data = JSON.parse($('#container')[0].getAttribute('data-json'));

  const drawPostsViewsChart = () => {
    const { post_views } = data;
    if (!post_views || !Array.isArray(post_views)) return;

    const context = $('#chartPostViews')[0].getContext('2d');
    const chart = new Chart(context, {
      type: 'line',
      data: {
          labels: post_views.map(postView => postView.month),
          datasets: [{
              label: 'Просмотры постов',
              backgroundColor: 'rgb(255, 99, 132)',
              borderColor: 'rgb(255, 99, 132)',
              data: post_views.map(postView => postView.count)
          }]
      },
      options: {}
    });
  }

  const drawPostCommentsChart = () => {
    const { post_comments } = data;
    if (!post_comments || !Array.isArray(post_comments)) return;

    const context = $('#chartPostComments')[0].getContext('2d');
    const chart = new Chart(context, {
      type: 'line',
      data: {
          labels: post_comments.map(postComment => postComment.month),
          datasets: [{
              label: 'Комментарии постов',
              backgroundColor: 'rgb(0,255,51)',
              borderColor: 'rgb(0,255,0)',
              data: post_comments.map(postComment => postComment.count),
          }]
      },
      options: {}
    });
  }

  drawPostsViewsChart();
  drawPostCommentsChart()
});