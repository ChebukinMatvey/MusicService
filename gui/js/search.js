function search_click() {
    query = $("#search-input").val()
    $.ajax({
      method: 'POST',
      url: "http://localhost:5000/track",
      contentType: 'application/json',
      dataType: 'json',
      data: JSON.stringify({ username:username, query: query }),
      success: (data) => {
        show_tracks(data.result);
      }
    })
  }