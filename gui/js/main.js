var unliked = "https://img.icons8.com/ios/50/000000/facebook-like.png"
var liked = "https://img.icons8.com/ios/50/000000/facebook-like-filled.png"
var track_list
var current_track_index
var current_volume = 0.5
var is_ready_to_play
var player
var track_duration
var username
var { ipcMain } = require('electron')

async function show_tracks(tracks) {
    if (tracks.length < 1) {
        alert("Немає треків")
        return
    }
    track_list = tracks
    $("#list li").remove()
    for (i = 0; i < tracks.length; ++i) {
        track = tracks[i]
        duration = track.duration / 1000 / 60
        template = `<li class="row container"><p class="track-index">${i + 1}</p><div class="img-block" onclick="play_click(this)"><button class="play-button">` +
            `<img src="../img/play.png" alt=""></button><img src="${track.img}"` +
            `class="track-img"></div><p class="track-artists col-5">${track.artists.join()}</p><p class="track-name col-5">${track.name}</p>` +
            `<div class="col 2"><img id='recommend' onclick="recommendation_by_track(this)" src='https://cdn2.iconfinder.com/data/icons/apple-inspire-black/100/Apple-40-512.png'>`+
            `<img id="like"  src="${ track.like ? liked:unliked }" onclick="like_click(this)"></div></li>`
        $(template).appendTo($("#list")[0])
    }
}

function like_click(img) {
    index = parseInt(img.parentElement.parentElement.children[0].innerHTML)
    id = track_list[index - 1].id

    if ($(img).attr('src') === liked) {
        $.ajax({
            method: 'DELETE',
            url: "http://localhost:5000/like",
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify({ user: 'nokinobi', song_id: id }),
            success: (data) => {
                if (data.result) {
                    $(img).attr("src", unliked)
                }
            }
        })
    }
    else {
        $.ajax({
            method: 'POST',
            url: "http://localhost:5000/like",
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify({ user: 'nokinobi', song_id: id }),
            success: (data) => {
                if (data.result) {
                    $(img).attr("src", liked)
                }
            }
        })
    }
}

function recommendation_by_track(img){
    index = parseInt(img.parentElement.parentElement.children[0].innerHTML)
    id = track_list[index - 1].id

    $.ajax({
        method: 'POST',
        url: "http://localhost:5000/recommend",
        contentType: 'application/json',
        dataType: 'json',
        data: JSON.stringify({username:username,song_id:id}),
        success: (data) => {
            show_tracks(data.result)
            $($("h3")[0]).html("Схожі пісні")
        }
    })
}