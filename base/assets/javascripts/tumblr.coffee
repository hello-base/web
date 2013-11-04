Tumblr = Tumblr or {}
Tumblr.RecentPosts = (el, postsCount) ->
  apiUrl = "http://blog.hello-base.com/api/read/json?callback=?&filter=text&num=" + (postsCount or 10)
  titleTypes =
    regular: "regular-title"
    link: "link-text"
    quote: "quote-source"
    photo: "photo-caption"
    conversation: "conversation-title"
    video: "video-caption"
    audio: "audio-caption"
    answer: "question"

  renderPosts = (posts) ->
    $.map $.map(posts, postInfo), renderPost

  renderPost = (post) ->
    '<span class="ss-icon ss-lightbulbon"></span> The latest from our blog <i>Standing Idol</i>: <a href="' + post.url + '">' + post.title + ' </a>'

  postInfo = (post) ->
    titleType = titleTypes[post.type]
    if titleType of post
      title: post[titleType]
      url: post["url-with-slug"]

  render: ->
    loadingEl = $('<div class="recent-posts container">').text('Loading...').appendTo($(el))
    $.getJSON apiUrl, (data) ->
      loadingEl.remove()
      $('<div class="recent-posts container">').appendTo($(el)).hide().append(renderPosts(data.posts).join('\n')).fadeIn 'slow'

    this

$ ->
  new Tumblr.RecentPosts($('#standing-idol'), 1).render()
